"""
情绪/新闻分析师智能体

负责解析市场气候系统，监测情绪和地缘政治风险
"""

from typing import Dict, Any
import numpy as np
from .base_agent import BaseAgent, MarketData


class SentimentAnalyst(BaseAgent):
    """
    情绪/新闻分析师

    核心职责：
    - 解析"气候系统"（地缘政治、政策变化）
    - 监测市场情绪（VIX、社交媒体情绪、资金流向）
    - 识别潜在的"黑天鹅"风险
    """

    def __init__(self):
        super().__init__(
            name="情绪分析师",
            role="Sentiment Analyst",
            weight=0.20
        )

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析市场情绪和新闻

        参数:
            data: {
                'market_sentiment': 0-100,
                'vix': VIX指数,
                'fund_flow': 资金流向,
                'news': {
                    'sentiment': 'positive'/'neutral'/'negative',
                    'key_events': [
                        {
                            'type': '政策'/'地缘政治'/'公司'/'行业',
                            'description': '事件描述',
                            'impact': 'positive'/'neutral'/'negative',
                            'magnitude': 0.0-1.0
                        }
                    ]
                },
                'social_sentiment': {
                    'twitter': -1到1,
                    'reddit': -1到1,
                    'weibo': -1到1
                },
                'put_call_ratio': 看跌/看涨期权比率,
                'credit_spread': 信用利差
            }

        返回:
            情绪分析结果
        """
        try:
            # 1. 计算情绪指数
            sentiment_index = self._calculate_sentiment_index(data)

            # 2. 评估新闻影响
            news_impact = self._assess_news_impact(data.get('news', {}))

            # 3. 识别风险事件
            risk_events = self._identify_risk_events(data)

            # 4. 生成情绪评分
            sentiment_score = self._score_sentiment(data)

            # 5. 给出建议
            recommendation = self._generate_recommendation(
                sentiment_index, sentiment_score, risk_events
            )

            return {
                'recommendation': recommendation['action'],
                'confidence': recommendation['confidence'],
                'reasoning': recommendation['reasoning'],
                'target_weights': recommendation['target_weights'],
                'risk_alerts': risk_events,
                'key_metrics': {
                    'sentiment_index': sentiment_index,
                    'sentiment_score': sentiment_score,
                    'vix': data.get('vix', 0),
                    'fund_flow': data.get('fund_flow', 0),
                    'news_impact': news_impact
                }
            }

        except Exception as e:
            return self._error_result(str(e))

    def _calculate_sentiment_index(self, data: Dict) -> float:
        """
        计算综合情绪指数 (0-100)

        权重分配：
        - VIX: 30%
        - 资金流向: 25%
        - 社交媒体情绪: 25%
        - 期权情绪: 20%
        """
        index = 50.0  # 中性起点

        # 1. VIX贡献 (30%)
        vix = data.get('vix', 20)
        if vix < 15:
            index += 15  # 极度乐观
        elif vix < 20:
            index += 10
        elif vix < 25:
            index += 0
        elif vix < 35:
            index -= 10
        else:
            index -= 15  # 极度恐慌

        # 2. 资金流向贡献 (25%)
        fund_flow = data.get('fund_flow', 0)
        if fund_flow > 1e9:  # 10亿以上净流入
            index += 12
        elif fund_flow > 5e8:
            index += 8
        elif fund_flow < -1e9:
            index -= 12
        elif fund_flow < -5e8:
            index -= 8

        # 3. 社交媒体情绪 (25%)
        social = data.get('social_sentiment', {})
        social_avg = np.mean([
            social.get('twitter', 0),
            social.get('reddit', 0),
            social.get('weibo', 0)
        ])
        index += social_avg * 12.5

        # 4. 看跌/看涨期权比率 (20%)
        pcr = data.get('put_call_ratio', 1.0)
        if pcr < 0.7:
            index += 10  # 乐观
        elif pcr > 1.3:
            index -= 10  # 悲观

        return max(0, min(100, index))

    def _assess_news_impact(self, news: Dict) -> Dict:
        """评估新闻影响"""
        if not news:
            return {'impact': 'neutral', 'magnitude': 0.0}

        key_events = news.get('key_events', [])
        if not key_events:
            sentiment = news.get('sentiment', 'neutral')
            return {'impact': sentiment, 'magnitude': 0.0}

        # 计算综合影响
        impacts = []
        for event in key_events:
            impact_score = {
                'positive': 1.0,
                'neutral': 0.0,
                'negative': -1.0
            }.get(event.get('impact', 'neutral'), 0.0)

            impacts.append(impact_score * event.get('magnitude', 0.5))

        avg_impact = np.mean(impacts) if impacts else 0.0

        if avg_impact > 0.3:
            impact_level = 'positive'
        elif avg_impact < -0.3:
            impact_level = 'negative'
        else:
            impact_level = 'neutral'

        return {
            'impact': impact_level,
            'magnitude': abs(avg_impact),
            'events_count': len(key_events)
        }

    def _identify_risk_events(self, data: Dict) -> List[str]:
        """识别风险事件"""
        risks = []

        # VIX异常
        vix = data.get('vix', 20)
        if vix > 40:
            risks.append(f"⚠️ 极度恐慌: VIX={vix:.1f}")
        elif vix > 30:
            risks.append(f"⚠️ 高波动预警: VIX={vix:.1f}")

        # 信用利差异常
        credit_spread = data.get('credit_spread', 0.02)
        if credit_spread > 0.05:
            risks.append(f"⚠️ 信用利差飙升: {credit_spread:.2%}")

        # 资金大幅流出
        fund_flow = data.get('fund_flow', 0)
        if fund_flow < -2e9:
            risks.append(f"⚠️ 资金大幅流出: {fund_flow/1e9:.1f}亿")

        # 新闻事件
        news = data.get('news', {})
        for event in news.get('key_events', []):
            if event.get('impact') == 'negative' and event.get('magnitude', 0) > 0.7:
                risks.append(f"📰 重大负面事件: {event.get('description', '')}")

        return risks

    def _score_sentiment(self, data: Dict) -> float:
        """情绪评分 (0-1)"""
        score = 0.5

        # VIX
        vix = data.get('vix', 20)
        if vix < 15:
            score += 0.2
        elif vix > 30:
            score -= 0.2

        # 资金流向
        fund_flow = data.get('fund_flow', 0)
        if fund_flow > 1e9:
            score += 0.15
        elif fund_flow < -1e9:
            score -= 0.15

        # 社交媒体情绪
        social = data.get('social_sentiment', {})
        social_avg = np.mean([
            social.get('twitter', 0),
            social.get('reddit', 0),
            social.get('weibo', 0)
        ])
        score += social_avg * 0.15

        return max(0, min(1, score))

    def _generate_recommendation(self, sentiment_index: float,
                                 sentiment_score: float,
                                 risk_events: List[str]) -> Dict:
        """生成建议"""
        # 基于情绪指数
        if sentiment_index >= 70:
            action = 'buy'
            confidence = 0.7
            reasoning = f"市场情绪极度乐观({sentiment_index:.0f}分)，但需警惕过热"
        elif sentiment_index >= 55:
            action = 'buy'
            confidence = 0.65
            reasoning = f"市场情绪偏乐观({sentiment_index:.0f}分)"
        elif sentiment_index >= 45:
            action = 'hold'
            confidence = 0.6
            reasoning = f"市场情绪中性({sentiment_index:.0f}分)"
        elif sentiment_index >= 30:
            action = 'sell'
            confidence = 0.65
            reasoning = f"市场情绪偏悲观({sentiment_index:.0f}分)"
        else:
            action = 'sell'
            confidence = 0.7
            reasoning = f"市场情绪极度悲观({sentiment_index:.0f}分)，恐慌中需谨慎"

        # 如果有重大风险事件，降低风险资产权重
        if risk_events:
            action = 'reduce_risk'
            reasoning += f"。检测到{len(risk_events)}个风险事件"

        # 目标权重调整
        target_weights = {}
        if action in ['sell', 'reduce_risk']:
            target_weights = {'L1': 0.3, 'L2': 0.4, 'L3': 0.2, 'L4': 0.05, 'L5': 0.05}
        elif action == 'buy':
            target_weights = {'L1': 0.15, 'L2': 0.25, 'L3': 0.40, 'L4': 0.15, 'L5': 0.05}
        else:
            target_weights = {'L1': 0.20, 'L2': 0.30, 'L3': 0.35, 'L4': 0.10, 'L5': 0.05}

        return {
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'target_weights': target_weights
        }

    def _error_result(self, error: str) -> Dict:
        """返回错误结果"""
        return {
            'recommendation': 'hold',
            'confidence': 0.0,
            'reasoning': f'情绪分析错误: {error}',
            'target_weights': {},
            'risk_alerts': [f'情绪分析失败: {error}'],
            'key_metrics': {}
        }
