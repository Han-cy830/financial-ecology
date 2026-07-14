#!/usr/bin/env python3
"""
数据准备工具

生成示例数据集（用于测试和演示）
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def generate_sample_data(start_date='2000-01-01', end_date='2024-12-31', output_dir='data/historical_data'):
    """
    生成模拟的宏观数据（用于测试和演示）

    参数:
        start_date: 开始日期
        end_date: 结束日期
        output_dir: 输出目录
    """
    print("=" * 70)
    print("生成示例宏观数据")
    print("=" * 70)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成日期序列（月度）
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    n = len(dates)

    print(f"\n时间范围: {dates[0].date()} 至 {dates[-1].date()}")
    print(f"数据点数: {n} 个月")

    # 模拟4个季节的特征
    seasonal_patterns = {
        '春季': {'gdp': 0.05, 'cpi': 0.02, 'ppi': 0.03, 'm2': 0.11,
                 'rate': 0.028, 'credit_spread': 0.012, 'real_rate': 0.006,
                 'stock_ret': 0.08, 'vol': 0.18, 'flow': 0.3},
        '夏季': {'gdp': 0.08, 'cpi': 0.025, 'ppi': 0.04, 'm2': 0.10,
                 'rate': 0.032, 'credit_spread': 0.010, 'real_rate': 0.008,
                 'stock_ret': 0.12, 'vol': 0.15, 'flow': 0.5},
        '秋季': {'gdp': 0.02, 'cpi': 0.045, 'ppi': 0.02, 'm2': 0.08,
                 'rate': 0.035, 'credit_spread': 0.020, 'real_rate': -0.005,
                 'stock_ret': -0.03, 'vol': 0.25, 'flow': -0.2},
        '冬季': {'gdp': -0.03, 'cpi': 0.01, 'ppi': -0.02, 'm2': 0.06,
                 'rate': 0.030, 'credit_spread': 0.025, 'real_rate': -0.015,
                 'stock_ret': -0.10, 'vol': 0.35, 'flow': -0.5}
    }

    # 生成数据
    data = []
    for i, date in enumerate(dates):
        # 每60个月为一个季节周期
        season_idx = (i // 60) % 4
        season = ['春季', '夏季', '秋季', '冬季'][season_idx]
        pattern = seasonal_patterns[season]

        # 添加噪声和趋势
        trend = i / n  # 0到1的线性趋势

        row = {
            'date': date.strftime('%Y-%m-%d'),
            'gdp_growth': pattern['gdp'] + np.random.normal(0, 0.02) + trend * 0.01,
            'cpi': pattern['cpi'] + np.random.normal(0, 0.005),
            'ppi': pattern['ppi'] + np.random.normal(0, 0.008),
            'm2_growth': pattern['m2'] + np.random.normal(0, 0.02),
            'interest_rate': pattern['rate'] + np.random.normal(0, 0.003),
            'credit_spread': pattern['credit_spread'] + np.random.normal(0, 0.003),
            'real_rate': pattern['real_rate'] + np.random.normal(0, 0.002),
            'stock_return_3m': pattern['stock_ret'] + np.random.normal(0, 0.05),
            'volatility': pattern['vol'] + np.random.normal(0, 0.03),
            'fund_flow': pattern['flow'] * 1e9 + np.random.normal(0, 1e8),
            'season': season
        }
        data.append(row)

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 保存到CSV
    output_path = os.path.join(output_dir, 'macro_data_sample.csv')
    df.to_csv(output_path, index=False)

    print(f"\n✓ 数据已保存: {output_path}")

    # 显示统计信息
    print("\n数据预览:")
    print(df.head(10).to_string(index=False))

    print("\n数据统计:")
    print(df.describe().round(4).to_string())

    print("\n季节分布:")
    print(df['season'].value_counts())

    return df


if __name__ == "__main__":
    import sys

    try:
        df = generate_sample_data()
        print("\n✅ 数据生成完成！")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
