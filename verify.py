#!/usr/bin/env python3
"""
项目验证脚本

验证核心功能是否正常工作
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试1: 导入检查"""
    print("\n[1/5] 测试导入...")

    try:
        import numpy as np
        print("  ✓ numpy")
    except ImportError:
        print("  ✗ numpy (请运行: pip install numpy)")
        return False

    try:
        import pandas as pd
        print("  ✓ pandas")
    except ImportError:
        print("  ✗ pandas (请运行: pip install pandas)")
        return False

    try:
        from sklearn.preprocessing import StandardScaler
        print("  ✓ scikit-learn")
    except ImportError:
        print("  ✗ scikit-learn (请运行: pip install scikit-learn)")
        return False

    try:
        from hmmlearn import hmm
        print("  ✓ hmmlearn")
    except ImportError:
        print("  ✗ hmmlearn (请运行: pip install hmmlearn)")
        return False

    try:
        import matplotlib
        matplotlib.use('Agg')  # 无GUI模式
        import matplotlib.pyplot as plt
        print("  ✓ matplotlib")
    except ImportError:
        print("  ✗ matplotlib (请运行: pip install matplotlib)")
        return False

    return True


def test_ecosystem_classifier():
    """测试2: 生态分类器"""
    print("\n[2/5] 测试生态分类器...")

    try:
        from src.ecosystem.asset_classifier import AssetClassifier

        classifier = AssetClassifier()

        # 测试国债
        bond = classifier.classify(
            name="测试国债",
            volatility=0.08,
            cash_flow_positive=True,
            correlation_with_stocks=0.10,
            leverage_ratio=1.0,
            liquidity_score=0.95
        )

        assert bond['role'] == '猎物', f"预期'猎物'，实际'{bond['role']}'"
        assert bond['confidence'] > 0.5, "置信度过低"

        print(f"  ✓ 国债分类: {bond['role']} (置信度: {bond['confidence']:.0%})")

        # 测试比特币
        btc = classifier.classify(
            name="测试比特币",
            volatility=0.80,
            cash_flow_positive=False,
            correlation_with_stocks=0.30,
            leverage_ratio=2.0,
            liquidity_score=0.85,
            regulatory_status='semi_regulated'
        )

        assert btc['role'] == '纯投机捕食者', f"预期'纯投机捕食者'，实际'{btc['role']}'"
        print(f"  ✓ 比特币分类: {btc['role']} (置信度: {btc['confidence']:.0%})")

        return True

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_hmm_model():
    """测试3: HMM模型"""
    print("\n[3/5] 测试HMM模型...")

    try:
        import numpy as np
        import pandas as pd
        from src.hmm_detector.season_hmm import SeasonHMM

        # 生成模拟数据
        np.random.seed(42)
        n_samples = 100

        features = [
            'gdp_growth', 'cpi', 'ppi', 'm2_growth',
            'interest_rate', 'credit_spread', 'real_rate',
            'stock_return_3m', 'volatility', 'fund_flow'
        ]

        data = []
        for i in range(n_samples):
            season_idx = i // 25
            season_means = {
                0: [0.05, 0.02, 0.03, 0.12, 0.028, 0.012, 0.006, 0.08, 0.18, 0.3],
                1: [0.08, 0.025, 0.04, 0.10, 0.032, 0.010, 0.008, 0.12, 0.15, 0.5],
                2: [0.02, 0.045, 0.02, 0.08, 0.035, 0.020, -0.005, -0.03, 0.25, -0.2],
                3: [-0.03, 0.01, -0.02, 0.06, 0.030, 0.025, -0.015, -0.10, 0.35, -0.5]
            }
            mean = season_means[season_idx % 4]
            sample = [m + np.random.normal(0, 0.05) for m in mean]
            data.append(sample)

        df = pd.DataFrame(data, columns=features)

        # 训练模型
        print("  → 训练模型...")
        hmm_model = SeasonHMM()
        result = hmm_model.train(df, verbose=False)

        assert result['converged'], "模型未收敛"
        print(f"  ✓ 模型训练完成 (对数似然: {result['log_likelihood']:.2f})")

        # 预测
        print("  → 预测季节...")
        test_data = pd.DataFrame([df.iloc[-1].values], columns=features)
        prediction = hmm_model.predict_season(test_data)

        assert 'season' in prediction, "预测结果缺少季节字段"
        assert 'probabilities' in prediction, "预测结果缺少概率分布"

        print(f"  ✓ 预测季节: {prediction['season']} (置信度: {prediction['confidence']:.1%})")
        print(f"    概率分布: {prediction['probabilities']}")

        return True

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_allocation_calculator():
    """测试4: 配置计算器"""
    print("\n[4/5] 测试配置计算器...")

    try:
        # 导入
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools/allocation-calculator'))
        from allocation_calculator import AllocationCalculator

        calculator = AllocationCalculator()

        # 测试春季中等风险
        result = calculator.calculate(
            season='春季',
            risk_preference='moderate',
            total_capital=1000000
        )

        # 验证
        assert 'allocation' in result, "结果缺少配置"
        assert 'expected_return' in result, "结果缺少预期收益"

        total = sum(result['allocation'].values())
        assert abs(total - 1.0) < 0.01, f"配置比例总和不为1: {total}"

        print(f"  ✓ 春季配置:")
        for layer, weight in result['allocation'].items():
            print(f"    {layer}: {weight:.1%}")

        print(f"  ✓ 预期收益: {result['expected_return']:.2%}")
        print(f"  ✓ 夏普比率: {result['sharpe_ratio']:.2f}")

        return True

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_questionnaire():
    """测试5: 季节问卷"""
    print("\n[5/5] 测试季节问卷...")

    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools/season-questionnaire'))
        from questionnaire import SeasonQuestionnaire

        questionnaire = SeasonQuestionnaire()

        # 测试评分功能
        test_answers = {
            'gdp_growth': 3,      # 温和增长
            'inflation': 3,        # 温和通胀
            'monetary_policy': 3,  # 降息
            'corporate_earnings': 3,  # 温和增长
            'market_sentiment': 3, # 中性
            'stock_market': 3,     # 温和上涨
            'liquidity': 3,        # 正常
            'credit_condition': 3, # 正常
            'employment': 3,       # 稳定
            'geopolitical': 3      # 相对稳定
        }

        result = questionnaire.calculate_score(test_answers)

        assert 'season' in result, "结果缺少季节"
        assert 'probabilities' in result, "结果缺少概率分布"
        assert 'confidence' in result, "结果缺少置信度"

        print(f"  ✓ 测试答案评分:")
        print(f"    季节: {result['season']}")
        print(f"    置信度: {result['confidence']:.1%}")
        print(f"    概率分布: {result['probabilities']}")

        return True

    except Exception as e:
        print(f"  ✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("  金融生态学框架 - 项目验证")
    print("=" * 60)

    start_time = __import__('time').time()

    results = []
    results.append(("导入检查", test_imports()))
    results.append(("生态分类器", test_ecosystem_classifier()))
    results.append(("HMM模型", test_hmm_model()))
    results.append(("配置计算器", test_allocation_calculator()))
    results.append(("季节问卷", test_questionnaire()))

    elapsed = __import__('time').time() - start_time

    # 总结
    print("\n" + "=" * 60)
    print("  验证结果")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")

    print(f"\n总计: {passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有测试通过！项目可以正常使用。")
        print("\n下一步:")
        print("  1. 阅读文档: docs/INDEX.md")
        print("  2. 运行演示: python tools/demo.py")
        print("  3. 开始使用: python tools/season-questionnaire/questionnaire.py")
    else:
        print(f"\n⚠️  {total - passed} 个测试失败")
        print("请检查依赖安装: pip install -r requirements.txt")

    print(f"\n⏱️  验证耗时: {elapsed:.2f}秒")
    print()

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
