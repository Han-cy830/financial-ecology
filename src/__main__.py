"""
金融生态学框架 - CLI 入口

用法:
    python -m src                              # 显示帮助
    python -m src demo                         # 运行完整演示
    python -m src classify --volatility 0.25   # 资产分类
    python -m src hmm                           # HMM季节检测演示
"""

import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1]

    if command == 'demo':
        from tools.demo import main as demo_main
        demo_main()

    elif command == 'classify':
        from src.ecosystem.asset_classifier import AssetClassifier
        import argparse

        parser = argparse.ArgumentParser(description='资产生态分类')
        parser.add_argument('--name', required=True, help='资产名称')
        parser.add_argument('--volatility', type=float, default=0.2, help='波动率')
        parser.add_argument('--leverage', type=float, default=1.0, help='杠杆率')
        parser.add_argument('--liquidity', type=float, default=0.7, help='流动性评分')
        args = parser.parse_args(sys.argv[2:])

        classifier = AssetClassifier()
        result = classifier.classify(
            name=args.name,
            volatility=args.volatility,
            leverage_ratio=args.leverage,
            liquidity_score=args.liquidity,
        )
        print(f"资产: {result['name']}")
        print(f"生态角色: {result['role']}")
        print(f"风险等级: {result['risk_level']}")
        print(f"置信度: {result['confidence']:.1%}")

    elif command == 'hmm':
        from src.hmm_detector.season_hmm import SeasonHMM
        import numpy as np
        import pandas as pd

        np.random.seed(42)
        n_samples = 200
        seasonal_means = {
            '春季': [0.05, 0.02, 0.03, 0.12, 0.028, 0.012, 0.006, 0.08, 0.18, 0.3],
            '夏季': [0.08, 0.025, 0.04, 0.10, 0.032, 0.010, 0.008, 0.12, 0.15, 0.5],
            '秋季': [0.02, 0.045, 0.02, 0.08, 0.035, 0.020, -0.005, -0.03, 0.25, -0.2],
            '冬季': [-0.03, 0.01, -0.02, 0.06, 0.030, 0.025, -0.015, -0.10, 0.35, -0.5]
        }
        features = [
            'gdp_growth', 'cpi', 'ppi', 'm2_growth',
            'interest_rate', 'credit_spread', 'real_rate',
            'stock_return_3m', 'volatility', 'fund_flow'
        ]
        data = []
        for i in range(n_samples):
            season_idx = i // 50
            season = ['春季', '夏季', '秋季', '冬季'][season_idx % 4]
            mean = seasonal_means[season]
            sample = [m + np.random.normal(0, 0.1) for m in mean]
            data.append(sample)
        df = pd.DataFrame(data, columns=features)

        print("训练HMM模型...")
        hmm_model = SeasonHMM(n_seasons=4)
        result = hmm_model.train(df, verbose=True)

        current_data = df.iloc[[-1]]
        prediction = hmm_model.predict_season(current_data)
        print(f"\n预测季节: {prediction['season']} (置信度: {prediction['confidence']:.1%})")

    else:
        print(f"未知命令: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
