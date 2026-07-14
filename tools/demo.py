#!/usr/bin/env python3
"""
金融生态学框架演示脚本

展示框架核心功能：
1. 资产生态分类
2. 季节概率检测
3. 配置计算
4. 风险可视化
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import numpy as np
import pandas as pd
from datetime import datetime


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_asset_classification():
    """演示1: 资产生态分类"""
    print_section("演示1: 资产生态分类")

    from src.ecosystem.asset_classifier import AssetClassifier

    classifier = AssetClassifier()

    # 测试资产
    test_assets = [
        {
            'name': '10年期国债',
            'volatility': 0.08,
            'cash_flow_positive': True,
            'correlation_with_stocks': 0.10,
            'leverage_ratio': 1.0,
            'liquidity_score': 0.95
        },
        {
            'name': '沪深300ETF',
            'volatility': 0.25,
            'cash_flow_positive': True,
            'correlation_with_stocks': 0.98,
            'leverage_ratio': 1.0,
            'liquidity_score': 0.90
        },
        {
            'name': 'REITs',
            'volatility': 0.35,
            'cash_flow_positive': True,
            'correlation_with_stocks': 0.60,
            'leverage_ratio': 2.0,
            'liquidity_score': 0.70
        },
        {
            'name': '比特币',
            'volatility': 0.80,
            'cash_flow_positive': False,
            'correlation_with_stocks': 0.30,
            'leverage_ratio': 2.0,
            'liquidity_score': 0.85,
            'regulatory_status': 'semi_regulated'
        },
        {
            'name': '个股期权',
            'volatility': 0.90,
            'cash_flow_positive': False,
            'correlation_with_stocks': 0.70,
            'leverage_ratio': 5.0,
            'liquidity_score': 0.30
        }
    ]

    results = []
    for asset in test_assets:
        result = classifier.classify(**asset)
        results.append({
            '资产': result['name'],
            '生态角色': result['role'],
            '风险等级': result['risk_level'],
            '置信度': f"{result['confidence']:.1%}",
            '最大配置': f"{result['allocation_guidance'].get('max_weight', 0):.0%}"
        })

    df = pd.DataFrame(results)
    print("\n资产生态分类结果:")
    print(df.to_string(index=False))

    print("\n💡 关键发现:")
    print("  - L1/L2资产（猎物）: 国债，低波动，稳定现金流")
    print("  - L3资产（价值创造者）: 沪深300，与企业盈利挂钩")
    print("  - L4a资产（价值型捕食者）: REITs，有现金流但波动较高")
    print("  - L4b资产（纯投机捕食者）: 比特币，无现金流，高投机")
    print("  - L5资产（顶级捕食者）: 个股期权，极高风险")


def demo_season_detection():
    """演示2: HMM季节检测"""
    print_section("演示2: HMM季节检测")

    from src.hmm_detector.season_hmm import SeasonHMM

    # 创建模拟数据（2000-2024年）
    np.random.seed(42)
    n_samples = 240  # 20年×12月

    # 定义各季节特征（简化的宏观指标）
    seasonal_means = {
        '春季': [0.04, 0.02, 0.03, 0.11, 0.028, 0.012, 0.006, 0.06, 0.20, 0.2],
        '夏季': [0.07, 0.025, 0.04, 0.10, 0.032, 0.010, 0.008, 0.10, 0.15, 0.4],
        '秋季': [0.02, 0.045, 0.02, 0.08, 0.035, 0.020, -0.005, -0.02, 0.25, -0.2],
        '冬季': [-0.03, 0.01, -0.02, 0.06, 0.030, 0.025, -0.015, -0.08, 0.35, -0.4]
    }

    features = [
        'gdp_growth', 'cpi', 'ppi', 'm2_growth',
        'interest_rate', 'credit_spread', 'real_rate',
        'stock_return_3m', 'volatility', 'fund_flow'
    ]

    # 生成时间序列
    data = []
    for i in range(n_samples):
        season_idx = i // 60  # 每60个月切换季节
        season = ['春季', '夏季', '秋季', '冬季'][season_idx % 4]
        mean = seasonal_means[season]
        sample = [m + np.random.normal(0, 0.1) for m in mean]
        data.append(sample)

    df = pd.DataFrame(data, columns=features)

    print("\n训练HMM模型...")
    print(f"数据量: {len(df)}个月（20年）")

    hmm_model = SeasonHMM(n_seasons=4, random_state=42)

    # 训练模型
    result = hmm_model.train(df, verbose=False)

    print(f"\n✓ 训练完成")
    print(f"  收敛状态: {'是' if result['converged'] else '否'}")
    print(f"  对数似然: {result['log_likelihood']:.2f}")

    # 模拟当前数据（春季特征）
    current_data = pd.DataFrame([[
        0.045,   # GDP 4.5%
        0.022,   # CPI 2.2%
        0.030,   # PPI 3.0%
        0.105,   # M2 10.5%
        0.028,   # 利率 2.8%
        0.012,   # 信用利差 1.2%
        0.006,   # 实际利率 0.6%
        0.075,   # 3月收益 7.5%
        0.18,    # VIX 18
        0.35     # 资金流向
    ]], columns=features)

    print("\n\n预测当前季节...")
    prediction = hmm_model.predict_season(current_data)

    print(f"\n当前季节: {prediction['season']}")
    print(f"置信度: {prediction['confidence']:.1%}")
    print(f"季节切换概率: {prediction['regime_change_probability']:.1%}")

    print(f"\n概率分布:")
    for season, prob in sorted(prediction['probabilities'].items(),
                              key=lambda x: -x[1]):
        bar = '█' * int(prob * 40)
        print(f"  {season}: {prob:6.1%} {bar}")

    print(f"\n配置建议:")
    for layer, weight in prediction['suggested_allocation'].items():
        print(f"  {layer}: {weight:.1%}")

    print(f"\n未来3个月预测:")
    for forecast in prediction['next_3_seasons']:
        probs = forecast['probabilities']
        dominant = max(probs, key=probs.get)
        print(f"  {forecast['step']}个月后: {forecast['season']} "
              f"({probs[dominant]:.0%}置信)")


def demo_allocation_calculator():
    """演示3: 配置计算器"""
    print_section("演示3: 资产配置计算器")

    from tools.allocation_calculator.allocation_calculator import AllocationCalculator

    calculator = AllocationCalculator()

    scenarios = [
        {'season': '春季', 'risk': 'moderate', 'capital': 1000000, 'label': '春季·中等风险'},
        {'season': '夏季', 'risk': 'moderate', 'capital': 1000000, 'label': '夏季·中等风险'},
        {'season': '秋季', 'risk': 'moderate', 'capital': 1000000, 'label': '秋季·中等风险'},
        {'season': '冬季', 'risk': 'moderate', 'capital': 1000000, 'label': '冬季·中等风险'},
    ]

    results = []
    for scenario in scenarios:
        result = calculator.calculate(
            season=scenario['season'],
            risk_preference=scenario['risk'],
            total_capital=scenario['capital']
        )

        results.append({
            '场景': scenario['label'],
            'L1': f"{result['allocation']['L1']:.0%}",
            'L2': f"{result['allocation']['L2']:.0%}",
            'L3': f"{result['allocation']['L3']:.0%}",
            'L4': f"{result['allocation']['L4']:.0%}",
            'L5': f"{result['allocation']['L5']:.0%}",
            '预期收益': f"{result['expected_return']:.1%}",
            '夏普比率': f"{result['sharpe_ratio']:.2f}"
        })

    df = pd.DataFrame(results)
    print("\n不同季节的配置方案:")
    print(df.to_string(index=False))

    print("\n💡 关键洞察:")
    print("  - 春季复苏: 逐步增加L3股票仓位（40%）")
    print("  - 夏季繁荣: 重仓股票（45%），积极参与L4（20%）")
    print("  - 秋季滞胀: 防御为主，增加L1现金（25%）和L2债券（35%）")
    print("  - 冬季衰退: 现金为王（40%），股票降至最低（15%）")


def demo_risk_visualization():
    """演示4: 风险可视化"""
    print_section("演示4: 风险可视化（生成图片）")

    from src.visualization.risk_visualizer import SystemicRiskVisualizer

    viz = SystemicRiskVisualizer()

    # 1. 生态系统网络图
    print("\n1. 生成生态系统网络图...")
    assets = {
        '国债': {'layer': 'L1', 'risk_score': 10},
        '货币基金': {'layer': 'L1', 'risk_score': 5},
        '国债ETF': {'layer': 'L2', 'risk_score': 15},
        '沪深300': {'layer': 'L3', 'risk_score': 50},
        'REITs': {'layer': 'L4', 'risk_score': 65},
        '比特币': {'layer': 'L4', 'risk_score': 85},
        '个股期权': {'layer': 'L5', 'risk_score': 95}
    }

    fig1 = viz.plot_ecosystem_network(assets)
    output_path = '../ecosystem_network.png'
    fig1.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✓ 已保存: {output_path}")

    # 2. L4传导路径
    print("\n2. 生成L4崩塌传导路径...")
    contagion = {
        'path': [
            {'layer': 'L4', 'asset': '比特币', 'shock': -0.70, 'time': 'T+0'},
            {'layer': 'L4', 'asset': '以太坊', 'shock': -0.65, 'time': 'T+0'},
            {'layer': 'L3', 'asset': '纳指100', 'shock': -0.15, 'time': 'T+1'},
            {'layer': 'L3', 'asset': '标普500', 'shock': -0.12, 'time': 'T+1'},
            {'layer': 'L2', 'asset': '投资级债券', 'shock': -0.03, 'time': 'T+2'},
            {'layer': 'L1', 'asset': '国债', 'shock': +0.02, 'time': 'T+3'}
        ],
        'amplification': 2.3
    }

    fig2 = viz.plot_contagion_path(contagion)
    output_path = '../contagion_path.png'
    fig2.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✓ 已保存: {output_path}")

    # 3. 配置对比
    print("\n3. 生成配置对比图...")
    current = {'L1': 0.15, 'L2': 0.30, 'L3': 0.38, 'L4': 0.12, 'L5': 0.05}
    target = {'L1': 0.20, 'L2': 0.30, 'L3': 0.35, 'L4': 0.10, 'L5': 0.05}

    fig3 = viz.plot_portfolio_allocation(current, target)
    output_path = '../allocation_comparison.png'
    fig3.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✓ 已保存: {output_path}")

    print("\n💡 可视化说明:")
    print("  - ecosystem_network.png: 资产层级和风险传导关系")
    print("  - contagion_path.png: L4崩塌如何传导到其他层级")
    print("  - allocation_comparison.png: 当前配置vs目标配置")


def main():
    """运行所有演示"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "金融生态学框架 - 功能演示" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")

    start_time = datetime.now()

    try:
        demo_asset_classification()
        demo_season_detection()
        demo_allocation_calculator()
        demo_risk_visualization()

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # 总结
    elapsed = (datetime.now() - start_time).total_seconds()
    print_section("演示完成")
    print(f"\n⏱️  总耗时: {elapsed:.1f}秒")
    print("\n✨ 框架核心功能:")
    print("  1. 资产生态分类 - 将资产分为5类生态角色")
    print("  2. HMM季节检测 - 概率化识别市场季节")
    print("  3. 配置计算器 - 根据季节生成配置方案")
    print("  4. 风险可视化 - 展示传导路径和配置对比")
    print("\n📚 下一步:")
    print("  - 阅读文档: docs/INDEX.md")
    print("  - 使用工具: python tools/...")
    print("  - 查看案例: docs/case-studies/")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
