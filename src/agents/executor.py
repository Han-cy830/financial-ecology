"""
交易员智能体

负责将决策转化为具体交易指令，优化执行成本
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent


class Executor(BaseAgent):
    """
    交易员

    核心职责：
    - 将决策转化为具体交易指令
    - 优化执行成本
    - 考虑交易时机和流动性
    """

    def __init__(self):
        super().__init__(
            name="交易员",
            role="Executor",
            weight=0.10
        )

        # 交易成本参数
        self.commission_rate = 0.00025  # 佣金万2.5
        self.stamp_tax = 0.001  # 印花税千1（仅卖出）
        self.transfer_fee = 0.00002  # 过户费万0.2

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成交易指令

        参数:
            data: {
                'current_portfolio': 当前组合权重,
                'target_allocation': 目标权重,
                'total_capital': 总资金,
                'prices': {
                    '资产名': 当前价格
                },
                'liquidity': {
                    '资产名': {
                        'bid_ask_spread': 买卖价差,
                        'avg_volume': 平均成交量
                    }
                }
            }

        返回:
            交易指令
        """
        try:
            current_portfolio = data.get('current_portfolio', {})
            target_allocation = data.get('target_allocation', {})
            total_capital = data.get('total_capital', 0)
            prices = data.get('prices', {})
            liquidity = data.get('liquidity', {})

            if not target_allocation or total_capital == 0:
                return self._empty_result("无目标配置或资金")

            # 1. 计算调仓需求
            rebalance_needs = self._calculate_rebalance(
                current_portfolio, target_allocation, total_capital, prices
            )

            # 2. 优化执行策略
            execution_plan = self._optimize_execution(rebalance_needs, liquidity)

            # 3. 估算成本
            cost_estimate = self._estimate_costs(execution_plan)

            # 4. 检查是否可执行
            feasibility = self._check_feasibility(execution_plan, liquidity)

            return {
                'recommendation': 'execute',
                'confidence': feasibility['confidence'],
                'reasoning': f"生成{len(execution_plan['instructions'])}条交易指令，预估成本{cost_estimate['total_cost_ratio']:.2%}",
                'target_weights': target_allocation,
                'risk_alerts': feasibility['alerts'],
                'key_metrics': {
                    'instructions_count': len(execution_plan['instructions']),
                    'estimated_cost': cost_estimate,
                    'feasibility': feasibility
                },
                'execution_plan': execution_plan
            }

        except Exception as e:
            return self._error_result(str(e))

    def _calculate_rebalance(self, current: Dict, target: Dict,
                            total_capital: float, prices: Dict) -> List[Dict]:
        """计算调仓需求"""
        instructions = []

        all_assets = set(list(current.keys()) + list(target.keys()))

        for asset in all_assets:
            current_weight = current.get(asset, 0)
            target_weight = target.get(asset, 0)
            weight_diff = target_weight - current_weight

            # 如果差异小于1%，忽略
            if abs(weight_diff) < 0.01:
                continue

            # 计算交易金额
            trade_amount = weight_diff * total_capital

            # 计算交易股数（如果知道价格）
            if asset in prices and prices[asset] > 0:
                shares = int(trade_amount / prices[asset])
                actual_amount = shares * prices[asset]
            else:
                shares = 0
                actual_amount = trade_amount

            action = 'buy' if trade_amount > 0 else 'sell'

            instructions.append({
                'asset': asset,
                'action': action,
                'target_weight': target_weight,
                'current_weight': current_weight,
                'weight_diff': weight_diff,
                'trade_amount': abs(trade_amount),
                'shares': abs(shares),
                'actual_amount': abs(actual_amount)
            })

        # 按金额排序（大额优先）
        instructions.sort(key=lambda x: x['trade_amount'], reverse=True)

        return instructions

    def _optimize_execution(self, instructions: List[Dict], liquidity: Dict) -> Dict:
        """优化执行策略"""
        optimized = []

        for inst in instructions:
            asset = inst['asset']

            # 获取流动性信息
            asset_liquidity = liquidity.get(asset, {})
            avg_volume = asset_liquidity.get('avg_volume', 1e9)
            bid_ask_spread = asset_liquidity.get('bid_ask_spread', 0.001)

            # 判断是否使用TWAP策略
            amount = inst['actual_amount']
            if amount > avg_volume * 0.1:  # 超过日均量10%
                strategy = 'TWAP'
                duration = '2-4小时'
            elif amount > avg_volume * 0.05:
                strategy = 'VWAP'
                duration = '1小时'
            else:
                strategy = '市价单'
                duration = '即时'

            # 设定价格限制
            if bid_ask_spread > 0.005:
                price_limit = '±0.5%'
            else:
                price_limit = '市价'

            optimized.append({
                **inst,
                'execution': {
                    'strategy': strategy,
                    'duration': duration,
                    'price_limit': price_limit,
                    'liquidity_ok': amount < avg_volume * 0.2  # 不超过20%日均量
                }
            })

        return {
            'instructions': optimized,
            'total_buy': sum(i['trade_amount'] for i in optimized if i['action'] == 'buy'),
            'total_sell': sum(i['trade_amount'] for i in optimized if i['action'] == 'sell')
        }

    def _estimate_costs(self, plan: Dict) -> Dict:
        """估算交易成本"""
        total_turnover = 0
        total_commission = 0
        total_stamp_tax = 0
        total_transfer = 0

        for inst in plan['instructions']:
            amount = inst['actual_amount']
            total_turnover += amount

            # 佣金（买卖双向）
            commission = amount * self.commission_rate
            total_commission += commission

            # 印花税（仅卖出）
            if inst['action'] == 'sell':
                stamp_tax = amount * self.stamp_tax
                total_stamp_tax += stamp_tax

            # 过户费
            transfer = amount * self.transfer_fee
            total_transfer += transfer

        total_cost = total_commission + total_stamp_tax + total_transfer
        cost_ratio = total_cost / total_turnover if total_turnover > 0 else 0

        return {
            'total_turnover': total_turnover,
            'total_cost': total_cost,
            'commission': total_commission,
            'stamp_tax': total_stamp_tax,
            'transfer_fee': total_transfer,
            'total_cost_ratio': cost_ratio
        }

    def _check_feasibility(self, plan: Dict, liquidity: Dict) -> Dict:
        """检查执行可行性"""
        alerts = []
        confidence = 0.9

        for inst in plan['instructions']:
            asset = inst['asset']
            exec_info = inst['execution']

            # 流动性不足
            if not exec_info['liquidity_ok']:
                alerts.append(f"⚠️ {asset}交易量过大，可能影响价格")
                confidence -= 0.1

            # 大额交易
            if inst['trade_amount'] > 1e7:  # 1000万
                alerts.append(f"⚠️ {asset}交易金额过大({inst['trade_amount']/1e6:.0f}M)")
                confidence -= 0.05

        return {
            'feasible': confidence >= 0.7,
            'confidence': max(0, confidence),
            'alerts': alerts
        }

    def _empty_result(self, message: str) -> Dict:
        """返回空结果"""
        return {
            'recommendation': 'hold',
            'confidence': 0.0,
            'reasoning': message,
            'target_weights': {},
            'risk_alerts': [message],
            'key_metrics': {}
        }

    def _error_result(self, error: str) -> Dict:
        """返回错误结果"""
        return {
            'recommendation': 'hold',
            'confidence': 0.0,
            'reasoning': f'交易执行错误: {error}',
            'target_weights': {},
            'risk_alerts': [f'交易执行失败: {error}'],
            'key_metrics': {}
        }
