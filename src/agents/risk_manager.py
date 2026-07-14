"""
风控专员智能体

负责监控L4崩塌信号、生态健康度，管理组合风险
"""

from typing import Dict, Any, List
import numpy as np
from .base_agent import BaseAgent


class RiskManager(BaseAgent):
    """
    风控专员

    核心职责：
    - 监控L4崩塌信号和地缘冲击矩阵
    - 触发减仓预警
    - 评估组合风险暴露
    - **拥有一票否决权**
    """

    def __init__(self):
        super().__init__(
            name="风控专员",
            role="Risk Manager",
            weight=0.30  # 权重最高，且拥有否决权
        )
        self.veto_power = True  # 一票否决权

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        风险评估

        参数:
            data: {
                'portfolio': {
                    'L1': 0.15, 'L2': 0.30, 'L3': 0.38,
                    'L4': 0.12, 'L5': 0.05
                },
                'l4_indicators': {
                    'liquidity_ratio': 流动性比率,
                    'leverage': 杠杆率,
                    'daily_return': 日收益率,
                    'correlation_matrix': 相关性矩阵
                },
                'market_conditions': {
                    'vix': VIX指数,
                    'credit_spread': 信用利差,
                    'market_sentiment': 市场情绪
                }
            }

        返回:
            风险评估结果
        """
        try:
            portfolio = data.get('portfolio', {})
            l4_indicators = data.get('l4_indicators', {})
            market_conditions = data.get('market_conditions', {})

            # 1. 计算组合风险指标
            risk_metrics = self._calculate_risk_metrics(portfolio, market_conditions)

            # 2. 检查L4崩塌风险
            l4_risk = self._check_l4_collapse(l4_indicators)

            # 3. 检查生态健康度
            ecosystem_health = self._check_ecosystem_health(portfolio)

            # 4. 检查最大回撤风险
            drawdown_risk = self._estimate_drawdown_risk(portfolio, market_conditions)

            # 5. 检查VaR
            var = self._calculate_var(portfolio)

            # 6. 判断是否触发否决
            veto = self._check_veto(risk_metrics, l4_risk, ecosystem_health, var)

            # 7. 生成预警
            alerts = self._generate_alerts(l4_risk, ecosystem_health, risk_metrics)

            # 8. 给出建议
            recommendation = self._generate_recommendation(
                veto, risk_metrics, l4_risk, ecosystem_health, var
            )

            return {
                'recommendation': recommendation['action'],
                'confidence': recommendation['confidence'],
                'reasoning': recommendation['reasoning'],
                'target_weights': recommendation['target_weights'],
                'risk_alerts': alerts,
                'has_veto': veto,
                'key_metrics': {
                    **risk_metrics,
                    'l4_risk': l4_risk,
                    'ecosystem_health': ecosystem_health,
                    'drawdown_risk': drawdown_risk,
                    'var_95': var
                }
            }

        except Exception as e:
            return self._error_result(str(e))

    def _calculate_risk_metrics(self, portfolio: Dict, market_conditions: Dict) -> Dict:
        """计算组合风险指标"""
        # 计算各层占比
        total = sum(portfolio.values()) if sum(portfolio.values()) > 0 else 1.0
        ratios = {k: v / total for k, v in portfolio.items()}

        # 捕食者占比
        predator_ratio = ratios.get('L4', 0) + ratios.get('L5', 0)

        # 猎物-捕食者比
        prey_ratio = (ratios.get('L1', 0) + ratios.get('L2', 0)) / max(predator_ratio, 0.01)

        # 流动性比率
        liquidity_ratio = ratios.get('L1', 0)

        # 集中度（HHI指数）
        hhi = sum(r ** 2 for r in ratios.values())
        concentration = "高度集中" if hhi > 0.25 else "中度集中" if hhi > 0.15 else "分散"

        return {
            'predator_ratio': predator_ratio,
            'prey_predator_ratio': prey_ratio,
            'liquidity_ratio': liquidity_ratio,
            'concentration_hhi': hhi,
            'concentration': concentration
        }

    def _check_l4_collapse(self, l4_indicators: Dict) -> Dict:
        """
        检查L4崩塌风险

        触发条件：
        - 流动性比率 < 0.3 → 极高风险
        - 杠杆率 > 5.0 → 高
        - 单日回撤 > 10% → 极高
        """
        liquidity = l4_indicators.get('liquidity_ratio', 1.0)
        leverage = l4_indicators.get('leverage', 2.0)
        daily_return = l4_indicators.get('daily_return', 0.0)
        correlations = l4_indicators.get('correlation_matrix', None)

        # 风险评分 (0-100)
        risk_score = 0

        # 流动性风险
        if liquidity < 0.2:
            risk_score += 40
        elif liquidity < 0.3:
            risk_score += 30
        elif liquidity < 0.5:
            risk_score += 15

        # 杠杆风险
        if leverage > 8.0:
            risk_score += 30
        elif leverage > 5.0:
            risk_score += 20
        elif leverage > 3.0:
            risk_score += 10

        # 价格风险
        if daily_return < -0.15:
            risk_score += 30
        elif daily_return < -0.10:
            risk_score += 20
        elif daily_return < -0.05:
            risk_score += 10

        # 相关性风险（所有资产相关趋近1）
        if correlations is not None:
            avg_correlation = np.mean(correlations)
            if avg_correlation > 0.95:
                risk_score += 20
            elif avg_correlation > 0.85:
                risk_score += 10

        # 风险等级
        if risk_score >= 80:
            level = '极高'
            action = '立即清仓L4b'
        elif risk_score >= 60:
            level = '高'
            action = '减仓50%L4'
        elif risk_score >= 40:
            level = '中'
            action = '减仓25%L4'
        elif risk_score >= 20:
            level = '低'
            action = '监控'
        else:
            level = '极低'
            action = '正常'

        return {
            'level': level,
            'score': risk_score,
            'action': action,
            'liquidity': liquidity,
            'leverage': leverage,
            'daily_return': daily_return
        }

    def _check_ecosystem_health(self, portfolio: Dict) -> Dict:
        """检查生态健康度"""
        total = sum(portfolio.values()) if sum(portfolio.values()) > 0 else 1.0
        ratios = {k: v / total for k, v in portfolio.items()}

        l1 = ratios.get('L1', 0)
        l2 = ratios.get('L2', 0)
        l3 = ratios.get('L3', 0)
        l4 = ratios.get('L4', 0)
        l5 = ratios.get('L5', 0)

        predator_ratio = l4 + l5
        prey_predator_ratio = (l1 + l2) / max(predator_ratio, 0.01)

        # 健康度评分
        score = 100

        # 惩罚过度集中于捕食者
        if predator_ratio > 0.40:
            score -= 30
        elif predator_ratio > 0.30:
            score -= 15

        # 惩罚流动性不足
        if l1 < 0.05:
            score -= 40
        elif l1 < 0.10:
            score -= 20

        # 惩罚猎物-捕食者比失衡
        if prey_predator_ratio < 1.0:
            score -= 30
        elif prey_predator_ratio < 1.5:
            score -= 15

        status = "健康" if score >= 70 else "警示" if score >= 50 else "危险"

        return {
            'score': score,
            'status': status,
            'l1_ratio': l1,
            'l2_ratio': l2,
            'l3_ratio': l3,
            'l4_ratio': l4,
            'l5_ratio': l5,
            'predator_ratio': predator_ratio,
            'prey_predator_ratio': prey_predator_ratio
        }

    def _estimate_drawdown_risk(self, portfolio: Dict, market_conditions: Dict) -> Dict:
        """估算最大回撤风险"""
        vix = market_conditions.get('vix', 20)
        sentiment = market_conditions.get('market_sentiment', 50)

        # 根据市场条件估算
        base_drawdown = 0.10  # 基础回撤10%

        # VIX加成
        if vix > 40:
            vix_add = 0.25
        elif vix > 30:
            vix_add = 0.15
        elif vix > 20:
            vix_add = 0.05
        else:
            vix_add = 0.0

        # 情绪加成
        if sentiment < 20:
            sentiment_add = 0.15
        elif sentiment < 40:
            sentiment_add = 0.10
        elif sentiment < 60:
            sentiment_add = 0.05
        else:
            sentiment_add = 0.0

        estimated_drawdown = base_drawdown + vix_add + sentiment_add

        return {
            'estimated_max_drawdown': estimated_drawdown,
            'confidence_interval': (estimated_drawdown * 0.7, estimated_drawdown * 1.3)
        }

    def _calculate_var(self, portfolio: Dict) -> float:
        """计算VaR (Value at Risk)"""
        # 简化版VaR计算
        volatilities = {'L1': 0.015, 'L2': 0.05, 'L3': 0.18, 'L4': 0.35, 'L5': 0.80}

        portfolio_variance = 0
        for layer, weight in portfolio.items():
            vol = volatilities.get(layer, 0.2)
            portfolio_variance += (weight * vol) ** 2

        portfolio_vol = np.sqrt(portfolio_variance)

        # 95% VaR = 1.645 * σ
        var_95 = -1.645 * portfolio_vol

        return var_95

    def _check_veto(self, risk_metrics: Dict, l4_risk: Dict,
                   ecosystem_health: Dict, var: float) -> bool:
        """
        检查是否触发否决权

        否决条件：
        1. VaR < -20%
        2. L4风险极高
        3. 生态健康度 < 40
        """
        # 条件1: VaR > 20%
        if var < -0.20:
            return True

        # 条件2: L4风险极高
        if l4_risk['level'] == '极高':
            return True

        # 条件3: 生态健康度低于40分
        if ecosystem_health['score'] < 40:
            return True

        return False

    def _generate_alerts(self, l4_risk: Dict, ecosystem_health: Dict,
                        risk_metrics: Dict) -> List[str]:
        """生成预警信息"""
        alerts = []

        # L4风险预警
        if l4_risk['level'] in ['高', '极高']:
            alerts.append(f"🚨 L4风险{l4_risk['level']}: {l4_risk['action']}")

        # 生态健康度预警
        if ecosystem_health['status'] in ['警示', '危险']:
            alerts.append(f"⚠️ 生态健康度{alerts['status']}: 得分{alerts['score']}")

        # 流动性预警
        if risk_metrics['liquidity_ratio'] < 0.10:
            alerts.append(f"💧 流动性严重不足: {risk_metrics['liquidity_ratio']:.1%}")

        # 捕食者占比预警
        if risk_metrics['predator_ratio'] > 0.40:
            alerts.append(f"🐺 捕食者占比过高: {risk_metrics['predator_ratio']:.1%}")

        return alerts

    def _generate_recommendation(self, veto: bool, risk_metrics: Dict,
                                l4_risk: Dict, ecosystem_health: Dict,
                                var: float) -> Dict:
        """生成建议"""
        if veto:
            return {
                'action': 'veto',
                'confidence': 0.9,
                'reasoning': f"触发风控否决：{l4_risk['action']}，生态健康度{alerts['status']}",
                'target_weights': self._calculate_safe_allocation(ecosystem_health)
            }

        # 未触发否决，但根据风险调整
        if l4_risk['level'] in ['高', '极高']:
            action = 'reduce_risk'
            confidence = 0.85
            reasoning = f"L4风险{l4_risk['level']}，建议减仓"
        elif ecosystem_health['status'] == '警示':
            action = 'reduce_risk'
            confidence = 0.75
            reasoning = f"生态健康度警示({alerts['score']}分)，适度防守"
        else:
            action = 'approve'
            confidence = 0.8
            reasoning = f"风险可控，VaR={var:.1%}，生态健康度{alerts['status']}"

        # 目标权重（如果被否决，调整为保守配置）
        if action == 'veto':
            target_weights = {'L1': 0.40, 'L2': 0.40, 'L3': 0.15, 'L4': 0.03, 'L5': 0.02}
        elif action == 'reduce_risk':
            target_weights = {'L1': 0.30, 'L2': 0.35, 'L3': 0.25, 'L4': 0.07, 'L5': 0.03}
        else:
            target_weights = None  # 不强制修改

        return {
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'target_weights': target_weights
        }

    def _calculate_safe_allocation(self, ecosystem_health: Dict) -> Dict:
        """计算安全配置（被否决时）"""
        return {
            'L1': 0.40,
            'L2': 0.40,
            'L3': 0.15,
            'L4': 0.03,
            'L5': 0.02
        }

    def _error_result(self, error: str) -> Dict:
        """返回错误结果"""
        return {
            'recommendation': 'veto',
            'confidence': 0.5,
            'reasoning': f'风控分析失败: {error}，保守起见建议减仓',
            'target_weights': {'L1': 0.30, 'L2': 0.40, 'L3': 0.20, 'L4': 0.07, 'L5': 0.03},
            'has_veto': False,
            'risk_alerts': [f'风控分析失败: {error}'],
            'key_metrics': {}
        }
