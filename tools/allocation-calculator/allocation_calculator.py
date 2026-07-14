#!/usr/bin/env python3
"""
资产配置计算器

根据市场季节和风险偏好，自动生成L1-L5资产配置方案
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
import json
import argparse


class AllocationCalculator:
    """
    资产配置计算器

    基于生态季节和风险偏好，智能分配L1-L5层级比例
    """

    # 基础配置方案（不同季节×不同风险偏好）
    BASE_ALLOCATIONS = {
        # 风险偏好: 保守 / 中等 / 积极
        '春季': {
            'conservative': {'L1': 0.25, 'L2': 0.40, 'L3': 0.25, 'L4': 0.07, 'L5': 0.03},
            'moderate':     {'L1': 0.15, 'L2': 0.30, 'L3': 0.40, 'L4': 0.10, 'L5': 0.05},
            'aggressive':   {'L1': 0.10, 'L2': 0.25, 'L3': 0.45, 'L4': 0.15, 'L5': 0.05}
        },
        '夏季': {
            'conservative': {'L1': 0.15, 'L2': 0.30, 'L3': 0.40, 'L4': 0.10, 'L5': 0.05},
            'moderate':     {'L1': 0.10, 'L2': 0.20, 'L3': 0.45, 'L4': 0.20, 'L5': 0.05},
            'aggressive':   {'L1': 0.05, 'L2': 0.15, 'L3': 0.50, 'L4': 0.25, 'L5': 0.05}
        },
        '秋季': {
            'conservative': {'L1': 0.35, 'L2': 0.40, 'L3': 0.18, 'L4': 0.05, 'L5': 0.02},
            'moderate':     {'L1': 0.25, 'L2': 0.35, 'L3': 0.25, 'L4': 0.10, 'L5': 0.05},
            'aggressive':   {'L1': 0.20, 'L2': 0.30, 'L3': 0.35, 'L4': 0.10, 'L5': 0.05}
        },
        '冬季': {
            'conservative': {'L1': 0.50, 'L2': 0.40, 'L3': 0.07, 'L4': 0.02, 'L5': 0.01},
            'moderate':     {'L1': 0.40, 'L2': 0.35, 'L3': 0.15, 'L4': 0.05, 'L5': 0.05},
            'aggressive':   {'L1': 0.35, 'L2': 0.35, 'L3': 0.20, 'L4': 0.07, 'L5': 0.03}
        }
    }

    def __init__(self, risk_free_rate: float = 0.025):
        """
        初始化计算器

        参数:
            risk_free_rate: 无风险利率（默认2.5%）
        """
        self.risk_free_rate = risk_free_rate

    def calculate(self,
                  season: str,
                  risk_preference: str = 'moderate',
                  total_capital: float = 1000000,
                  constraints: Optional[Dict] = None) -> Dict:
        """
        计算资产配置方案

        参数:
            season: 季节 ('春季'/'夏季'/'秋季'/'冬季')
            risk_preference: 风险偏好 ('conservative'/'moderate'/'aggressive')
            total_capital: 总资金（元）
            constraints: 约束条件 {
                'max_l1': L1最大比例,
                'min_l3': L3最小比例,
                'no_l5': 是否禁止L5,
                'custom_weights': 自定义权重 {L1: 0.2, ...}
            }

        返回:
            {
                'allocation': 配置方案,
                'capital_allocation': 资金分配,
                'expected_return': 预期收益率,
                'expected_risk': 预期风险（波动率）,
                'sharpe_ratio': 夏普比率,
                'rebalance_triggers': 再平衡触发条件
            }
        """
        # 1. 获取基础配置
        if season not in self.BASE_ALLOCATIONS:
            raise ValueError(f"无效季节: {season}")

        if risk_preference not in self.BASE_ALLOCATIONS[season]:
            raise ValueError(f"无效风险偏好: {risk_preference}")

        allocation = self.BASE_ALLOCATIONS[season][risk_preference].copy()

        # 2. 应用约束条件
        if constraints:
            allocation = self._apply_constraints(allocation, constraints)

        # 3. 计算资金分配
        capital_allocation = {
            layer: amount
            for layer, amount in allocation.items()
        }

        # 4. 计算预期收益和风险
        expected_return = self._calculate_expected_return(allocation)
        expected_risk = self._calculate_expected_risk(allocation)
        sharpe_ratio = (expected_return - self.risk_free_rate) / expected_risk

        # 5. 生成再平衡触发条件
        rebalance_triggers = self._generate_rebalance_triggers(allocation)

        return {
            'allocation': allocation,
            'capital_allocation': capital_allocation,
            'expected_return': expected_return,
            'expected_risk': expected_risk,
            'sharpe_ratio': sharpe_ratio,
            'rebalance_triggers': rebalance_triggers
        }

    def _apply_constraints(self, allocation: Dict, constraints: Dict) -> Dict:
        """应用约束条件"""
        result = allocation.copy()

        # 自定义权重
        if 'custom_weights' in constraints:
            custom = constraints['custom_weights']
            for layer, weight in custom.items():
                if layer in result:
                    result[layer] = weight

        # L1最大比例
        if 'max_l1' in constraints:
            if result['L1'] > constraints['max_l1']:
                excess = result['L1'] - constraints['max_l1']
                result['L1'] = constraints['max_l1']
                # 按比例分配给其他层级
                other_total = sum(v for k, v in result.items() if k != 'L1')
                for k in result:
                    if k != 'L1':
                        result[k] += excess * (result[k] / other_total)

        # L3最小比例
        if 'min_l3' in constraints:
            if result['L3'] < constraints['min_l3']:
                deficit = constraints['min_l3'] - result['L3']
                result['L3'] = constraints['min_l3']
                # 从其他层级扣除
                other_total = sum(v for k, v in result.items() if k != 'L3')
                for k in result:
                    if k != 'L3':
                        result[k] -= deficit * (result[k] / other_total)
                        if result[k] < 0:
                            result[k] = 0

        # 禁止L5
        if constraints.get('no_l5', False):
            l5_amount = result['L5']
            result['L5'] = 0
            other_total = sum(v for k, v in result.items() if k != 'L5')
            for k in result:
                if k != 'L5':
                    result[k] += l5_amount * (result[k] / other_total)

        # 重新归一化
        total = sum(result.values())
        result = {k: v / total for k, v in result.items()}

        return result

    def _calculate_expected_return(self, allocation: Dict) -> float:
        """计算预期收益率"""
        # 各层预期收益（年化）
        expected_returns = {
            'L1': 0.025,   # 2.5%
            'L2': 0.045,   # 4.5%
            'L3': 0.10,    # 10%
            'L4': 0.15,    # 15%
            'L5': 0.20     # 20%（但可能归零，实际期望更低）
        }

        portfolio_return = sum(
            allocation.get(layer, 0) * expected_returns[layer]
            for layer in expected_returns
        )

        return portfolio_return

    def _calculate_expected_risk(self, allocation: Dict) -> float:
        """计算预期风险（波动率，简化版）"""
        # 各层预期波动率（年化）
        volatilities = {
            'L1': 0.015,
            'L2': 0.05,
            'L3': 0.18,
            'L4': 0.35,
            'L5': 0.80
        }

        # 假设各层之间相关性为0.3
        correlation = 0.3
        variance = 0.0

        for layer1, w1 in allocation.items():
            vol1 = volatilities[layer1]
            for layer2, w2 in allocation.items():
                vol2 = volatilities[layer2]
                if layer1 == layer2:
                    variance += (w1 * vol1) ** 2
                else:
                    variance += 2 * w1 * w2 * vol1 * vol2 * correlation

        return np.sqrt(variance)

    def _generate_rebalance_triggers(self, allocation: Dict) -> Dict:
        """生成再平衡触发条件"""
        return {
            'time_based': {
                'quarterly': '每季度末检查',
                'semi_annually': '每半年末再平衡',
                'annually': '每年末强制再平衡'
            },
            'threshold_based': {
                layer: {
                    'upper_threshold': weight * 1.5,
                    'lower_threshold': weight * 0.5,
                    'trigger': f'{layer}偏离目标±50%时再平衡'
                }
                for layer, weight in allocation.items()
            },
            'event_based': {
                'season_change': '季节转换时调整',
                'l4_collapse': 'L4预警触发时减仓',
                'major_geo_event': '重大地缘政治事件时评估'
            }
        }

    def format_output(self, result: Dict) -> str:
        """格式化输出"""
        output = []
        output.append("\n" + "=" * 60)
        output.append("资产配置方案")
        output.append("=" * 60)

        allocation = result['allocation']
        capital = result['capital_allocation']

        output.append("\n配置比例:")
        output.append("-" * 60)
        for layer in ['L1', 'L2', 'L3', 'L4', 'L5']:
            weight = allocation.get(layer, 0)
            amount = capital.get(layer, 0)
            bar = '█' * int(weight * 50)
            output.append(f"{layer}: {weight:6.1%} {bar} ¥{amount:>12,.0f}")

        output.append("\n组合指标:")
        output.append("-" * 60)
        output.append(f"预期收益率: {result['expected_return']:.2%}")
        output.append(f"预期波动率: {result['expected_risk']:.2%}")
        output.append(f"夏普比率:   {result['sharpe_ratio']:.2f}")

        output.append("\n再平衡触发条件:")
        output.append("-" * 60)
        for key, value in result['rebalance_triggers'].items():
            if isinstance(value, dict):
                output.append(f"\n{key}:")
                for k, v in value.items():
                    if isinstance(v, str):
                        output.append(f"  - {k}: {v}")
                    elif isinstance(v, dict):
                        output.append(f"  {k}:")
                        for kk, vv in v.items():
                            output.append(f"    {kk}: {vv}")

        return "\n".join(output)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='金融生态学 - 资产配置计算器')
    parser.add_argument('--season', required=True,
                       choices=['春季', '夏季', '秋季', '冬季'],
                       help='当前市场季节')
    parser.add_argument('--risk', default='moderate',
                       choices=['conservative', 'moderate', 'aggressive'],
                       help='风险偏好')
    parser.add_argument('--capital', type=float, default=1000000,
                       help='总资金（元）')
    parser.add_argument('--no-l5', action='store_true',
                       help='禁止L5投机仓位')
    parser.add_argument('--max-l1', type=float,
                       help='L1最大比例（0-1）')
    parser.add_argument('--json', action='store_true',
                       help='输出JSON格式')

    args = parser.parse_args()

    calculator = AllocationCalculator()

    constraints = {}
    if args.no_l5:
        constraints['no_l5'] = True
    if args.max_l1:
        constraints['max_l1'] = args.max_l1

    result = calculator.calculate(
        season=args.season,
        risk_preference=args.risk,
        total_capital=args.capital,
        constraints=constraints if constraints else None
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(calculator.format_output(result))


if __name__ == "__main__":
    main()
