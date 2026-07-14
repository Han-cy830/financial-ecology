#!/usr/bin/env python3
"""
预训练HMM模型生成器

使用示例数据训练HMM模型并保存
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from src.hmm_detector.season_hmm import SeasonHMM
import joblib


def train_and_save_model(data_path: str, output_dir: str = 'models'):
    """
    训练并保存HMM模型

    参数:
        data_path: 数据文件路径（CSV）
        output_dir: 模型输出目录
    """
    print("=" * 70)
    print("HMM模型训练与保存")
    print("=" * 70)

    # 加载数据
    print(f"\n[1/4] 加载数据: {data_path}")
    try:
        df = pd.read_csv(data_path)
        print(f"✓ 加载成功: {len(df)} 条记录")
    except Exception as e:
        print(f"✗ 加载失败: {e}")
        return None

    # 创建模型
    print("\n[2/4] 创建HMM模型...")
    hmm = SeasonHMM(n_seasons=4, random_state=42)
    print("✓ 模型创建完成")

    # 训练模型
    print("\n[3/4] 训练模型...")
    result = hmm.train(df, verbose=True)

    if not result['converged']:
        print("\n⚠️  警告: 模型未完全收敛，但继续保存")

    # 保存模型
    print("\n[4/4] 保存模型...")
    os.makedirs(output_dir, exist_ok=True)

    # 保存模型对象
    model_path = os.path.join(output_dir, 'hmm_season_model.pkl')
    joblib.dump(hmm, model_path)
    print(f"✓ 模型已保存: {model_path}")

    # 保存训练信息
    info = {
        'training_samples': len(df),
        'date_range': f"{df['date'].iloc[0]} 至 {df['date'].iloc[-1]}",
        'log_likelihood': result['log_likelihood'],
        'converged': result['converged'],
        'n_iterations': result['n_iter']
    }

    import json
    info_path = os.path.join(output_dir, 'model_info.json')
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=2)
    print(f"✓ 训练信息已保存: {info_path}")

    # 显示转移矩阵
    print("\n状态转移矩阵:")
    print(hmm.get_transition_matrix().to_string())

    return hmm


def test_model(model_path: str = 'models/hmm_season_model.pkl'):
    """测试已保存的模型"""
    print("\n" + "=" * 70)
    print("测试预训练模型")
    print("=" * 70)

    try:
        # 加载模型
        print(f"\n加载模型: {model_path}")
        hmm = joblib.load(model_path)
        print("✓ 模型加载成功")

        # 创建测试数据
        print("\n创建测试数据...")
        test_data = pd.DataFrame([[
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
        ]], columns=[
            'gdp_growth', 'cpi', 'ppi', 'm2_growth',
            'interest_rate', 'credit_spread', 'real_rate',
            'stock_return_3m', 'volatility', 'fund_flow'
        ])

        # 预测
        print("\n预测当前季节...")
        prediction = hmm.predict_season(test_data)

        print(f"\n✓ 预测结果:")
        print(f"  季节: {prediction['season']}")
        print(f"  置信度: {prediction['confidence']:.1%}")
        print(f"  季节切换概率: {prediction['regime_change_probability']:.1%}")

        print(f"\n概率分布:")
        for season, prob in sorted(prediction['probabilities'].items(),
                                   key=lambda x: -x[1]):
            print(f"  {season}: {prob:6.1%}")

        print(f"\n配置建议:")
        for layer, weight in prediction['suggested_allocation'].items():
            print(f"  {layer}: {weight:.1%}")

        print("\n✓ 模型测试通过！")
        return True

    except Exception as e:
        print(f"\n✗ 模型测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys

    # 检查参数
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # 测试模式
        success = test_model()
        sys.exit(0 if success else 1)
    else:
        # 训练模式
        try:
            # 生成示例数据
            print("\n步骤0: 生成示例数据")
            import subprocess
            result = subprocess.run(
                [sys.executable, 'tools/data/prepare_sample_data.py'],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"数据生成失败: {result.stderr}")
                sys.exit(1)

            # 训练模型
            data_path = 'data/historical_data/macro_data_sample.csv'
            model = train_and_save_model(data_path)

            if model:
                print("\n✓" + "=" * 68)
                print("✓ 模型训练和保存完成！")
                print("✓" + "=" * 68)
                print("\n使用模型:")
                print("  python tools/data/train_hmm_model.py test")
                print("\n或从Python代码:")
                print("  import joblib")
                print("  model = joblib.load('models/hmm_season_model.pkl')")
                print("  prediction = model.predict_season(current_data)")
            else:
                print("\n✗ 模型训练失败")
                sys.exit(1)

        except Exception as e:
            print(f"\n✗ 错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
