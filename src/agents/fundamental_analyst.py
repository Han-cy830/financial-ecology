"""
基本面分析师智能体

负责分析资产基本面，计算估值、质量、成长性指标
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_agent import BaseAgent, MarketData


class FundamentalAnalyst(BaseAgent):
    """
    基本面分析师

    核心职责：
    - 计算ROE、市赚率、估值分位
    - 评估企业盈利质量和增长潜力
    - 识别被低估/高估的资产
    """

    def __init__(self):
        super().__init__(
            name="基本面分析师",
            role="Fundamental Analyst",
            weight=0.30
        )

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析资产基本面

        参数:
            data: {
                'assets': {
                    '资产名': {
                        'pe': 市盈率,
                        'pb': 市净率,
                        'roe': 净资产收益率,
                        'eps_growth': 盈利增速,
                        'free_cash_flow': 自由现金流,
                        'revenue_growth': 营收增速,
                        'debt_ratio': 负债率
                    }
                },
                'macro': {
                    'gdp_growth': GDP增速,
                    'interest_rate': 利率
                }
            }

        返回:
            分析结果和建议
        """
        try:
            assets_data = data.get('assets', {})
            macro_data = data.get('macro', {})

            if not assets_data:
                return self._empty_result("无资产数据")

            # 分析每个资产
            analysis = {}
            for asset_name, asset_data in assets_data.items():
                analysis[asset_name] = self._analyze_asset(asset_data, macro_data)

            # 生成整体建议
            overall_recommendation = self._generate_overall_recommendation(analysis)

            return {
                'recommendation': overall_recommend['action'],
                'confidence': overall_recommend['confidence'],
                'reasoning': overall_recommend['reasoning'],
                'target_weights': overall_recommend['target_weights'],
                'risk_alerts': overall_recommend['alerts'],
                'key_metrics': {
                    asset: {
                        'composite_score': result['composite_score'],
                        'valuation_score': result['valuation_score'],
                        'quality_score': result['quality_score'],
                        'growth_score': result['growth_score']
                    }
                    for asset, result in analysis.items()
                },
                'detailed_analysis': analysis
            }

        except Exception as e:
            return self._error_result(str(e))

    def _analyze_asset(self, asset_data: Dict, macro_data: Dict) -> Dict:
        """分析单个资产"""
        # 1. 估值评分 (0-1)
        valuation_score = self._score_valuation(asset_data)

        # 2. 质量评分 (0-1)
        quality_score = self._score_quality(asset_data)

        # 3. 成长性评分 (0-1)
        growth_score = self._score_growth(asset_data)

        # 4. 财务健康评分 (0-1)
        health_score = self._score_financial_health(asset_data)

        # 5. 综合评分
        composite_score = (
            0.35 * valuation_score +
            0.30 * quality_score +
            0.25 * growth_score +
            0.10 * health_score
        )

        return {
            'composite_score': composite_score,
            'valuation_score': valuation_score,
            'quality_score': quality_score,
            'growth_score': growth_score,
            'health_score': health_score,
            'recommendation': self._score_to_recommendation(composite_score),
            'reasoning': self._generate_reasoning(asset_data, composite_score)
        }

    def _score_valuation(self, data: Dict) -> float:
        """估值评分 (0-1)"""
        score = 0.5  # 基础分

        # PE估值（历史分位）
        pe_percentile = data.get('pe_percentile', 0.5)
        if pe_percentile < 0.2:
            score += 0.3  # 低估
        elif pe_percentile < 0.4:
            score += 0.15
        elif pe_percentile > 0.8:
            score -= 0.2  # 高估

        # PB估值
        pb_percentile = data.get('pb_percentile', 0.5)
        if pb_percentile < 0.2:
            score += 0.2
        elif pb_percentile > 0.8:
            score -= 0.15

        return max(0, min(1, score))

    def _score_quality(self, data: Dict) -> float:
        """质量评分 (0-1)"""
        score = 0.5

        # ROE
        roe = data.get('roe', 0.10)
        if roe > 0.20:
            score += 0.3
        elif roe > 0.15:
            score += 0.2
        elif roe > 0.10:
            score += 0.1
        elif roe < 0.05:
            score -= 0.2

        # 自由现金流
        fcf = data.get('free_cash_flow', 0)
        if fcf > 0:
            score += 0.2

        return max(0, min(1, score))

    def _score_growth(self, data: Dict) -> float:
        """成长性评分 (0-1)"""
        score = 0.5

        # 盈利增速
        eps_growth = data.get('eps_growth', 0.05)
        if eps_growth > 0.30:
            score += 0.3
        elif eps_growth > 0.20:
            score += 0.2
        elif eps_growth > 0.10:
            score += 0.1
        elif eps_growth < 0:
            score -= 0.3

        # 营收增速
        revenue_growth = data.get('revenue_growth', 0.05)
        if revenue_growth > 0.20:
            score += 0.2
        elif revenue_growth < 0:
            score -= 0.1

        return max(0, min(1, score))

    def _score_financial_health(self, data: Dict) -> float:
        """财务健康评分 (0-1)"""
        score = 0.5

        # 负债率
        debt_ratio = data.get('debt_ratio', 0.5)
        if debt_ratio < 0.4:
            score += 0.3
        elif debt_ratio < 0.6:
            score += 0.1
        elif debt_ratio > 0.8:
            score -= 0.3

        return max(0, min(1, score))

    def _score_to_recommendation(self, score: float) -> str:
        """评分转建议"""
        if score >= 0.7:
            return 'strong_buy'
        elif score >= 0.6:
            return 'buy'
        elif score >= 0.4:
            return 'hold'
        elif score >= 0.3:
            return 'sell'
        else:
            return 'strong_sell'

    def _generate_reasoning(self, data: Dict, score: float) -> str:
        """生成分析理由"""
        reasons = []

        pe_pct = data.get('pe_percentile', 0.5)
        if pe_pct < 0.2:
            reasons.append(f"估值处于历史低位({pe_pct:.0%}分位)")
        elif pe_pct > 0.8:
            reasons.append(f"估值处于历史高位({pe_pct:.0%}分位)")

        roe = data.get('roe', 0)
        if roe > 0.20:
            reasons.append(f"ROE优秀({roe:.1%})")
        elif roe < 0.05:
            reasons.append(f"ROE偏低({roe:.1%})")

        eps_growth = data.get('eps_growth', 0)
        if eps_growth > 0.30:
            reasons.append(f"盈利高增长({eps_growth:.1%})")
        elif eps_growth < 0:
            reasons.append(f"盈利负增长({eps_growth:.1%})")

        return "；".join(reasons) if reasons else "基本面中性"

    def _generate_overall_recommendation(self, analysis: Dict) -> Dict:
        """生成整体建议"""
        if not analysis:
            return {
                'action': 'hold',
                'confidence': 0.5,
                'reasoning': '无数据',
                'target_weights': {},
                'alerts': []
            }

        # 计算平均评分
        scores = [result['composite_score'] for result in analysis.values()]
        avg_score = np.mean(scores)

        # 根据评分给出建议
        if avg_score >= 0.7:
            action = 'buy'
            confidence = 0.75
        elif avg_score >= 0.6:
            action = 'buy'
            confidence = 0.65
        elif avg_score >= 0.4:
            action = 'hold'
            confidence = 0.55
        else:
            action = 'sell'
            confidence = 0.65

        # 生成目标权重（简化版）
        target_weights = self._calculate_target_weights(analysis)

        # 风险预警
        alerts = []
        for asset, result in analysis.items():
            if result['composite_score'] < 0.3:
                alerts.append(f"{asset}基本面较差，建议减仓")

        return {
            'action': action,
            'confidence': confidence,
            'reasoning': f"平均基本面评分{avg_score:.2f}，" + (
                "整体看好" if avg_score >= 0.6 else "中性观望" if avg_score >= 0.4 else "整体偏弱"
            ),
            'target_weights': target_weights,
            'alerts': alerts
        }

    def _calculate_target_weights(self, analysis: Dict) -> Dict[str, float]:
        """计算目标权重"""
        if not analysis:
            return {}

        # 按评分分配权重
        scores = {asset: result['composite_score'] for asset, result in analysis.items()}
        total_score = sum(scores.values())

        if total_score == 0:
            return {asset: 1.0 / len(analysis) for asset in analysis}

        weights = {asset: score / total_score for asset, score in scores.items()}

        # 限制单个资产最大权重为40%
        max_weight = 0.4
        for asset in weights:
            if weights[asset] > max_weight:
                weights[asset] = max_weight

        # 重新归一化
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

        return weights

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
            'reasoning': f'分析错误: {error}',
            'target_weights': {},
            'risk_alerts': [f'基本面分析失败: {error}'],
            'key_metrics': {}
        }
