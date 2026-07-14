"""
多智能体系统测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents import (
    FundamentalAnalyst,
    SentimentAnalyst,
    TechnicalAnalyst,
    RiskManager,
    Executor,
    PortfolioManager
)


def test_multi_agent_system():
    """测试多智能体系统"""

    print("=" * 70)
    print("金融生态学框架 - 多智能体系统测试")
    print("=" * 70)

    # 1. 创建智能体团队
    print("\n[1/3] 创建智能体团队...")
    agents = [
        FundamentalAnalyst(),
        SentimentAnalyst(),
        TechnicalAnalyst(),
        RiskManager(),
        Executor()
    ]

    for agent in agents:
        print(f"  ✓ {agent.name} ({agent.role})")

    # 2. 创建组合经理
    print("\n[2/3] 初始化组合经理...")
    pm = PortfolioManager(agents)
    print(f"  ✓ 组合经理: {pm.name}")

    # 3. 模拟市场数据
    print("\n[3/3] 测试决策流程...")
    market_data = {
        'assets': {
            '沪深300': {
                'pe': 12.5,
                'pb': 1.5,
                'roe': 0.13,
                'eps_growth': 0.15,
                'free_cash_flow': 1000000000,
                'revenue_growth': 0.12,
                'debt_ratio': 0.45,
                'pe_percentile': 0.35,
                'pb_percentile': 0.30
            },
            '创业板指': {
                'pe': 28.0,
                'pb': 3.2,
                'roe': 0.11,
                'eps_growth': 0.25,
                'free_cash_flow': 500000000,
                'revenue_growth': 0.22,
                'debt_ratio': 0.35,
                'pe_percentile': 0.55,
                'pb_percentile': 0.60
            }
        },
        'market_sentiment': 65,
        'vix': 18.5,
        'fund_flow': 850000000,
        'price_data': {
            'current_price': 3950,
            'ma_20': 3900,
            'ma_60': 3800,
            'ma_200': 3600,
            'rsi': 58,
            'macd': 15.5,
            'macd_signal': 12.3,
            'bollinger_upper': 4100,
            'bollinger_lower': 3700,
            'volume': 2500000000,
            'volume_ma': 2000000000
        },
        'news': {
            'sentiment': 'positive',
            'key_events': [
                {
                    'type': '政策',
                    'description': '央行降准0.5%',
                    'impact': 'positive',
                    'magnitude': 0.7
                }
            ]
        },
        'social_sentiment': {
            'twitter': 0.3,
            'reddit': 0.2,
            'weibo': 0.25
        },
        'put_call_ratio': 0.85,
        'credit_spread': 0.012,
        'l4_indicators': {
            'liquidity_ratio': 0.65,
            'leverage': 3.2,
            'daily_return': -0.015,
            'correlation_matrix': [[1.0, 0.7], [0.7, 1.0]]
        },
        'market_conditions': {
            'vix': 18.5,
            'credit_spread': 0.012,
            'market_sentiment': 65
        }
    }

    current_portfolio = {
        'L1': 0.15,
        'L2': 0.30,
        'L3': 0.40,
        'L4': 0.10,
        'L5': 0.05
    }

    hmm_prediction = {
        'season': '春季',
        'confidence': 0.72,
        'probabilities': {
            '春季': 0.72,
            '夏季': 0.18,
            '秋季': 0.07,
            '冬季': 0.03
        },
        'suggested_allocation': {
            'L1': 0.15,
            'L2': 0.30,
            'L3': 0.40,
            'L4': 0.10,
            'L5': 0.05
        }
    }

    # 4. 获取决策
    print("\n执行决策...")
    decision = pm.analyze({
        'market_data': market_data,
        'current_portfolio': current_portfolio,
        'hmm_prediction': hmm_prediction,
        'total_capital': 1000000
    })

    print("\n" + "=" * 70)
    print("决策结果")
    print("=" * 70)

    print(f"\n✓ 决策建议: {decision['recommendation']}")
    print(f"✓ 置信度: {decision['confidence']:.1%}")
    print(f"✓ 决策依据: {decision['reasoning']}")

    print("\n目标配置:")
    for layer, weight in decision['target_allocation'].items():
        print(f"  {layer}: {weight:.1%}")

    if 'rebalance_instructions' in decision and decision['rebalance_instructions']:
        print(f"\n调仓指令 ({len(decision['rebalance_instructions'])}条):")
        for inst in decision['rebalance_instructions'][:5]:  # 显示前5条
            print(f"  - {inst['layer']}: {inst['action']} ¥{inst['amount']:,.0f}")

    if decision.get('risk_alerts'):
        print(f"\n风险预警 ({len(decision['risk_alerts'])}条):")
        for alert in decision['risk_alerts'][:5]:
            print(f"  {alert}")

    print("\n" + "=" * 70)
    print("✓ 多智能体系统测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    test_multi_agent_system()
