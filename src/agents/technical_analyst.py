"""
技术分析师智能体

负责判断入场/出场时机，识别趋势和反转信号
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from .base_agent import BaseAgent


class TechnicalAnalyst(BaseAgent):
    """
    技术分析师

    核心职责：
    - 判断入场/出场时机
    - 识别趋势和反转信号
    - 评估短期动量
    """

    def __init__(self):
        super().__init__(
            name="技术分析师",
            role="Technical Analyst",
            weight=0.20
        )

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        技术分析

        参数:
            data: {
                'price_data': {
                    'current_price': 当前价格,
                    'ma_20': 20日均线,
                    'ma_60': 60日均线,
                    'ma_200': 200日均线,
                    'rsi': RSI指标(0-100),
                    'macd': MACD值,
                    'macd_signal': MACD信号线,
                    'bollinger_upper': 布林带上轨,
                    'bollinger_lower': 布林带下轨,
                    'volume': 成交量,
                    'volume_ma': 成交量均线
                },
                'market_indices': {
                    'index_name': {
                        'price': 指数价格,
                        'trend': 'up'/'down'/'sideways'
                    }
                }
            }

        返回:
            技术分析结果
        """
        try:
            price_data = data.get('price_data', {})
            market_indices = data.get('market_indices', {})

            # 1. 趋势判断
            trend_analysis = self._analyze_trend(price_data)

            # 2. 动量指标
            momentum = self._analyze_momentum(price_data)

            # 3. 支撑压力位
            support_resistance = self._identify_support_resistance(price_data)

            # 4. 成交量分析
            volume_analysis = self._analyze_volume(price_data)

            # 5. 生成信号
            signal = self._generate_signal(trend_analysis, momentum, volume_analysis)

            return {
                'recommendation': signal['action'],
                'confidence': signal['confidence'],
                'reasoning': signal['reasoning'],
                'target_weights': signal['target_weights'],
                'risk_alerts': signal['alerts'],
                'key_metrics': {
                    'trend': trend_analysis['trend'],
                    'momentum': momentum['score'],
                    'rsi': price_data.get('rsi', 50),
                    'macd_signal': momentum['macd_signal'],
                    'volume_signal': volume_analysis['signal'],
                    'key_levels': support_resistance
                }
            }

        except Exception as e:
            return self._error_result(str(e))

    def _analyze_trend(self, price_data: Dict) -> Dict:
        """分析趋势"""
        current_price = price_data.get('current_price', 0)
        ma_20 = price_data.get('ma_20', current_price)
        ma_60 = price_data.get('ma_60', current_price)
        ma_200 = price_data.get('ma_200', current_price)

        # 均线多头排列
        if ma_20 > ma_60 > ma_200 and current_price > ma_20:
            trend = 'strong_up'
            strength = 0.9
        # 均线空头排列
        elif ma_20 < ma_60 < ma_200 and current_price < ma_20:
            trend = 'strong_down'
            strength = 0.9
        # 价格在短期均线上方
        elif current_price > ma_20 > ma_60:
            trend = 'up'
            strength = 0.7
        # 价格在短期均线下方
        elif current_price < ma_20 < ma_60:
            trend = 'down'
            strength = 0.7
        # 震荡
        else:
            trend = 'sideways'
            strength = 0.5

        return {
            'trend': trend,
            'strength': strength,
            'reasoning': f"价格{'高于' if current_price > ma_20 else '低于'}20日均线，均线{'多头排列' if ma_20 > ma_60 else '空头排列' if ma_20 < ma_60 else '交叉'}"
        }

    def _analyze_momentum(self, price_data: Dict) -> Dict:
        """分析动量"""
        rsi = price_data.get('rsi', 50)
        macd = price_data.get('macd', 0)
        macd_signal = price_data.get('macd_signal', 0)

        # RSI评分
        if rsi > 70:
            rsi_signal = 'overbought'
            rsi_score = 0.3
        elif rsi > 60:
            rsi_signal = 'bullish'
            rsi_score = 0.7
        elif rsi > 40:
            rsi_signal = 'neutral'
            rsi_score = 0.5
        elif rsi > 30:
            rsi_signal = 'bearish'
            rsi_score = 0.3
        else:
            rsi_signal = 'oversold'
            rsi_score = 0.7

        # MACD评分
        if macd > macd_signal and macd > 0:
            macd_sig = 'bullish'
            macd_score = 0.8
        elif macd > macd_signal:
            macd_sig = 'bullish_weak'
            macd_score = 0.6
        elif macd < macd_signal and macd < 0:
            macd_sig = 'bearish'
            macd_score = 0.2
        else:
            macd_sig = 'bearish_weak'
            macd_score = 0.4

        # 综合动量
        momentum_score = 0.6 * rsi_score + 0.4 * macd_score

        return {
            'score': momentum_score,
            'rsi': rsi,
            'rsi_signal': rsi_signal,
            'macd': macd,
            'macd_signal': macd_sig,
            'reasoning': f"RSI={rsi:.1f}({rsi_signal})，MACD{macd_sig}"
        }

    def _identify_support_resistance(self, price_data: Dict) -> Dict:
        """识别支撑压力位"""
        current_price = price_data.get('current_price', 0)
        bollinger_upper = price_data.get('bollinger_upper', current_price * 1.1)
        bollinger_lower = price_data.get('bollinger_lower', current_price * 0.9)

        return {
            'current': current_price,
            'resistance': bollinger_upper,
            'support': bollinger_lower,
            'distance_to_resistance': (bollinger_upper - current_price) / current_price,
            'distance_to_support': (current_price - bollinger_lower) / current_price
        }

    def _analyze_volume(self, price_data: Dict) -> Dict:
        """分析成交量"""
        volume = price_data.get('volume', 0)
        volume_ma = price_data.get('volume_ma', volume)

        if volume_ma > 0:
            volume_ratio = volume / volume_ma
        else:
            volume_ratio = 1.0

        if volume_ratio > 2.0:
            signal = 'high'
            strength = 0.8
        elif volume_ratio > 1.5:
            signal = 'above_average'
            strength = 0.6
        elif volume_ratio < 0.5:
            signal = 'low'
            strength = 0.3
        else:
            signal = 'normal'
            strength = 0.5

        return {
            'signal': signal,
            'volume_ratio': volume_ratio,
            'strength': strength,
            'reasoning': f"成交量{'放量' if volume_ratio > 1.5 else '缩量' if volume_ratio < 0.7 else '正常'}（是均量的{volume_ratio:.1f}倍）"
        }

    def _generate_signal(self, trend: Dict, momentum: Dict, volume: Dict) -> Dict:
        """生成交易信号"""
        trend_strength = trend['strength']
        momentum_score = momentum['score']
        volume_strength = volume['strength']

        # 综合评分
        composite_score = (
            0.5 * trend_strength +
            0.35 * momentum_score +
            0.15 * volume_strength
        )

        alerts = []

        # 生成建议
        if composite_score >= 0.75:
            action = 'buy'
            confidence = 0.75
            reasoning = f"技术面强势（{composite_score:.2f}分）: {trend['reasoning']}，{momentum['reasoning']}"
        elif composite_score >= 0.6:
            action = 'buy'
            confidence = 0.65
            reasoning = f"技术面偏强（{composite_score:.2f}分）"
        elif composite_score >= 0.45:
            action = 'hold'
            confidence = 0.55
            reasoning = f"技术面中性（{composite_score:.2f}分）"
        elif composite_score >= 0.35:
            action = 'sell'
            confidence = 0.6
            reasoning = f"技术面偏弱（{composite_score:.2f}分）"
        else:
            action = 'sell'
            confidence = 0.7
            reasoning = f"技术面弱势（{composite_score:.2f}分）: {trend['reasoning']}"

        # 风险预警
        if momentum['rsi'] > 80:
            alerts.append("⚠️ RSI极度超买")
        elif momentum['rsi'] < 20:
            alerts.append("⚠️ RSI极度超卖")

        if trend['trend'] == 'strong_down':
            alerts.append("⚠️ 处于强烈下跌趋势")

        # 目标权重
        if action == 'buy':
            target_weights = {'L3': 0.45, 'L4': 0.15, 'L2': 0.30, 'L1': 0.10}
        elif action == 'sell':
            target_weights = {'L1': 0.30, 'L2': 0.40, 'L3': 0.20, 'L4': 0.05}
        else:
            target_weights = {'L3': 0.35, 'L2': 0.35, 'L1': 0.20, 'L4': 0.10}

        return {
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'target_weights': target_weights,
            'alerts': alerts
        }

    def _error_result(self, error: str) -> Dict:
        """返回错误结果"""
        return {
            'recommendation': 'hold',
            'confidence': 0.0,
            'reasoning': f'技术分析错误: {error}',
            'target_weights': {},
            'risk_alerts': [f'技术分析失败: {error}'],
            'key_metrics': {}
        }
