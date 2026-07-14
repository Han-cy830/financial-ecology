"""
组合经理智能体

协调所有智能体，综合各方意见，做出最终决策
"""

from typing import Dict, Any, List, Optional
import numpy as np
from .base_agent import BaseAgent, MarketData
from .fundamental_analyst import FundamentalAnalyst
from .sentiment_analyst import SentimentAnalyst
from .technical_analyst import TechnicalAnalyst
from .risk_manager import RiskManager
from .executor import Executor


class PortfolioManager(BaseAgent):
    """
    组合经理

    核心职责：
    - 协调6个专业智能体的分析
    - 综合各方意见
    - 解决分歧
    - 做出最终决策
    - 管理调仓节奏（平滑过渡）
    """

    def __init__(self, agents: List[BaseAgent] = None):
        super().__init__(
            name="组合经理",
            role="Portfolio Manager",
            weight=1.0  # 最终决策者
        )

        # 初始化智能体
        self.agents = {}
        if agents:
            for agent in agents:
                self.agents[agent.name] = agent
        else:
            # 默认配置
            self._init_default_agents()

    def _init_default_agents(self):
        """初始化默认智能体团队"""
        self.agents = {
            '基本面分析师': FundamentalAnalyst(),
            '情绪分析师': SentimentAnalyst(),
            '技术分析师': TechnicalAnalyst(),
            '风控专员': RiskManager(),
            '交易员': Executor()
        }

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        综合决策

        参数:
            data: {
                'market_data': 市场数据,
                'current_portfolio': 当前组合,
                'hmm_prediction': HMM季节预测,
                'total_capital': 总资金
            }

        返回:
            最终决策
        """
        try:
            market_data = data.get('market_data', {})
            current_portfolio = data.get('current_portfolio', {})
            hmm_prediction = data.get('hmm_prediction', {})
            total_capital = data.get('total_capital', 0)

            # Round 1: 各智能体独立分析
            opinions = self._round_1_independent_analysis(market_data)

            # Round 2: 识别并解决分歧
            resolved_opinions = self._round_2_resolve_disagreements(
                opinions, current_portfolio, hmm_prediction
            )

            # Round 3: 综合决策
            final_decision = self._round_3_synthesize(
                resolved_opinions, current_portfolio, hmm_prediction, total_capital
            )

            return final_decision

        except Exception as e:
            return self._error_result(str(e))

    def _round_1_independent_analysis(self, market_data: Dict) -> Dict[str, Dict]:
        """第一轮：各智能体独立分析"""
        opinions = {}

        for name, agent in self.agents.items():
            try:
                opinion = agent.analyze(market_data)
                opinions[name] = opinion
            except Exception as e:
                opinions[name] = {
                    'recommendation': 'hold',
                    'confidence': 0.0,
                    'reasoning': f'分析失败: {str(e)}',
                    'target_weights': {}
                }

        return opinions

    def _round_2_resolve_disagreements(self, opinions: Dict,
                                      current_portfolio: Dict,
                                      hmm_prediction: Dict) -> Dict[str, Dict]:
        """第二轮：识别并解决分歧"""
        resolved = opinions.copy()

        # 1. 检查风控否决
        risk_manager_opinion = opinions.get('风控专员', {})
        if risk_manager_opinion.get('has_veto', False):
            # 风控否决，其他智能体的权重大幅降低
            for name in resolved:
                if name != '风控专员':
                    resolved[name]['confidence'] *= 0.3
            return resolved

        # 2. 识别重大分歧
        recommendations = [
            op.get('recommendation', 'hold')
            for op in opinions.values()
        ]

        # 如果分歧严重（有buy也有sell），降低冲突方的置信度
        if 'buy' in recommendations and 'sell' in recommendations:
            # 降低看空方的置信度（如果HMM季节支持买入）
            hmm_season = hmm_prediction.get('season', '')
            if hmm_season in ['春季', '夏季']:
                for name, op in resolved.items():
                    if op.get('recommendation') == 'sell':
                        op['confidence'] *= 0.7
            # 降低看多方（如果HMM季节支持卖出）
            elif hmm_season in ['秋季', '冬季']:
                for name, op in resolved.items():
                    if op.get('recommendation') == 'buy':
                        op['confidence'] *= 0.7

        return resolved

    def _round_3_synthesize(self, opinions: Dict, current_portfolio: Dict,
                           hmm_prediction: Dict, total_capital: float) -> Dict:
        """第三轮：综合决策"""
        # 1. 检查是否有否决
        risk_manager = opinions.get('风控专员', {})
        if risk_manager.get('has_veto', False):
            return self._veto_decision(risk_manager)

        # 2. 加权计算目标权重
        target_weights = self._weighted_voting(opinions, hmm_prediction)

        # 3. 平滑调整（避免突变）
        smoothed_weights = self._smooth_transition(current_portfolio, target_weights)

        # 4. 计算调仓指令
        rebalance_instructions = self._generate_rebalance_instructions(
            current_portfolio, smoothed_weights, total_capital
        )

        # 5. 生成最终决策
        return self._format_final_decision(
            opinions, smoothed_weights, rebalance_instructions, hmm_prediction
        )

    def _weighted_voting(self, opinions: Dict, hmm_prediction: Dict) -> Dict[str, float]:
        """加权投票决定目标权重"""
        weights = {'L1': 0, 'L2': 0, 'L3': 0, 'L4': 0, 'L5': 0}
        total_weight = 0

        # 智能体权重
        agent_weights = {
            '基本面分析师': 0.30,
            '情绪分析师': 0.20,
            '技术分析师': 0.20,
            '风控专员': 0.30,
            '交易员': 0.10
        }

        # HMM预测权重（如果置信度高）
        hmm_weight = 0.0
        if hmm_prediction.get('confidence', 0) > 0.7:
            hmm_weight = 0.20

        # 智能体投票
        for name, opinion in opinions.items():
            agent_weight = agent_weights.get(name, 0.1)
            confidence = opinion.get('confidence', 0.5)

            # 综合权重
            combined_weight = agent_weight * confidence

            # 累加目标权重
            for layer, w in opinion.get('target_weights', {}).items():
                weights[layer] = weights.get(layer, 0) + w * combined_weight

            total_weight += combined_weight

        # HMM投票
        if hmm_weight > 0:
            suggested = hmm_prediction.get('suggested_allocation', {})
            for layer, w in suggested.items():
                weights[layer] = weights.get(layer, 0) + w * hmm_weight
            total_weight += hmm_weight

        # 归一化
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}

        return weights

    def _smooth_transition(self, current: Dict, target: Dict,
                          max_single_adjustment: float = 0.15) -> Dict[str, float]:
        """
        平滑过渡（避免单次大幅调仓）

        最大单次调整不超过15%
        """
        smoothed = {}

        for layer in set(list(current.keys()) + list(target.keys())):
            current_w = current.get(layer, 0)
            target_w = target.get(layer, 0)

            diff = target_w - current_w

            # 限制单次调整幅度
            if abs(diff) > max_single_adjustment:
                diff = max_single_adjustment if diff > 0 else -max_single_adjustment

            smoothed[layer] = current_w + diff

        # 归一化
        total = sum(smoothed.values())
        if total > 0:
            smoothed = {k: v / total for k, v in smoothed.items()}

        return smoothed

    def _generate_rebalance_instructions(self, current: Dict, target: Dict,
                                        total_capital: float) -> List[Dict]:
        """生成调仓指令"""
        instructions = []

        all_layers = set(list(current.keys()) + list(target.keys()))

        for layer in all_layers:
            current_w = current.get(layer, 0)
            target_w = target.get(layer, 0)
            diff = target_w - current_w

            # 差异小于1%忽略
            if abs(diff) < 0.01:
                continue

            amount = diff * total_capital

            instructions.append({
                'layer': layer,
                'action': 'buy' if diff > 0 else 'sell',
                'current_weight': current_w,
                'target_weight': target_w,
                'weight_diff': diff,
                'amount': abs(amount)
            })

        # 按金额排序
        instructions.sort(key=lambda x: x['amount'], reverse=True)

        return instructions

    def _veto_decision(self, risk_manager_opinion: Dict) -> Dict:
        """风控否决时的决策"""
        target_weights = risk_manager_opinion.get('target_weights', {
            'L1': 0.40, 'L2': 0.40, 'L3': 0.15, 'L4': 0.03, 'L5': 0.02
        })

        return {
            'recommendation': 'veto',
            'confidence': 0.9,
            'reasoning': f"风控否决: {risk_manager_opinion.get('reasoning', '风险过高')}",
            'target_weights': target_weights,
            'risk_alerts': risk_manager_opinion.get('risk_alerts', []),
            'opinions': {'风控专员': risk_manager_opinion},
            'hmm_weight': 0
        }

    def _format_final_decision(self, opinions: Dict, smoothed_weights: Dict,
                              instructions: List[Dict],
                              hmm_prediction: Dict) -> Dict:
        """格式化最终决策"""
        # 计算综合置信度
        confidences = [op.get('confidence', 0.5) for op in opinions.values()]
        avg_confidence = np.mean(confidences) if confidences else 0.5

        # 生成决策摘要
        decision_summary = self._generate_summary(opinions, smoothed_weights, hmm_prediction)

        # HMM权重（如果使用）
        hmm_weight = 0.2 if hmm_prediction.get('confidence', 0) > 0.7 else 0

        return {
            'recommendation': 'approved',
            'confidence': avg_confidence,
            'reasoning': decision_summary,
            'target_allocation': smoothed_weights,
            'rebalance_instructions': instructions,
            'risk_alerts': self._collect_alerts(opinions),
            'opinions': opinions,
            'hmm_weight': hmm_weight,
            'key_metrics': {
                'avg_confidence': avg_confidence,
                'instructions_count': len(instructions),
                'hmm_season': hmm_prediction.get('season', 'unknown'),
                'hmm_confidence': hmm_prediction.get('confidence', 0)
            }
        }

    def _generate_summary(self, opinions: Dict, weights: Dict,
                         hmm_prediction: Dict) -> str:
        """生成决策摘要"""
        parts = []

        # 当前季节
        season = hmm_prediction.get('season', '未知')
        parts.append(f"当前为{season}")

        # 配置变化
        if weights:
            max_layer = max(weights, key=weights.get)
            parts.append(f"重点配置{max_layer}({weights[max_layer]:.0%})")

        # 主要依据
        if opinions:
            # 找出最自信的智能体
            most_confident = max(opinions.items(),
                               key=lambda x: x[1].get('confidence', 0))
            if most_confident[1].get('confidence', 0) > 0.7:
                parts.append(f"{most_confident[0]}高度看好")

        return "；".join(parts)

    def _collect_alerts(self, opinions: Dict) -> List[str]:
        """收集所有预警"""
        alerts = []
        for name, opinion in opinions.items():
            opinion_alerts = opinion.get('risk_alerts', [])
            for alert in opinion_alerts:
                alerts.append(f"[{name}] {alert}")
        return alerts

    def _error_result(self, error: str) -> Dict:
        """返回错误结果"""
        return {
            'recommendation': 'hold',
            'confidence': 0.0,
            'reasoning': f'组合决策失败: {error}',
            'target_weights': {},
            'risk_alerts': [f'组合决策错误: {error}'],
            'key_metrics': {}
        }
