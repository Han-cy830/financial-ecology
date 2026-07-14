#!/usr/bin/env python3
"""
数据生成脚本（纯Python版本，无需pandas）

生成用于HMM模型训练的示例数据
"""

import random
import csv
import os
from datetime import datetime, timedelta


def generate_sample_csv(output_path='data/historical_data/macro_data_sample.csv'):
    """
    生成示例宏观数据（CSV格式）

    参数:
        output_path: 输出文件路径
    """
    print("=" * 70)
    print("生成示例宏观数据（纯Python版本）")
    print("=" * 70)

    # 创建目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 季节配置
    seasonal_patterns = {
        '春季': {
            'gdp': 0.05, 'cpi': 0.02, 'ppi': 0.03, 'm2': 0.11,
            'rate': 0.028, 'credit_spread': 0.012, 'real_rate': 0.006,
            'stock_ret': 0.08, 'vol': 0.18, 'flow': 0.3
        },
        '夏季': {
            'gdp': 0.08, 'cpi': 0.025, 'ppi': 0.04, 'm2': 0.10,
            'rate': 0.032, 'credit_spread': 0.010, 'real_rate': 0.008,
            'stock_ret': 0.12, 'vol': 0.15, 'flow': 0.5
        },
        '秋季': {
            'gdp': 0.02, 'cpi': 0.045, 'ppi': 0.02, 'm2': 0.08,
            'rate': 0.035, 'credit_spread': 0.020, 'real_rate': -0.005,
            'stock_ret': -0.03, 'vol': 0.25, 'flow': -0.2
        },
        '冬季': {
            'gdp': -0.03, 'cpi': 0.01, 'ppi': -0.02, 'm2': 0.06,
            'rate': 0.030, 'credit_spread': 0.025, 'real_rate': -0.015,
            'stock_ret': -0.10, 'vol': 0.35, 'flow': -0.5
        }
    }

    # 生成日期序列（月度，2000-01至2024-12）
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2024, 12, 1)

    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        # 下一个月
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)

    n = len(dates)
    print(f"\n时间范围: {dates[0].strftime('%Y-%m-%d')} 至 {dates[-1].strftime('%Y-%m-%d')}")
    print(f"数据点数: {n} 个月")

    # 生成数据
    print("\n生成数据...")
    rows = []
    seasons = ['春季', '夏季', '秋季', '冬季']

    for i, date in enumerate(dates):
        # 每60个月为一个季节周期
        season_idx = (i // 60) % 4
        season = seasons[season_idx]
        p = seasonal_patterns[season]

        # 趋势
        trend = i / n

        # 生成数据行
        row = {
            'date': date.strftime('%Y-%m-%d'),
            'season': season,
            'gdp_growth': p['gdp'] + random.gauss(0, 0.02) + trend * 0.01,
            'cpi': p['cpi'] + random.gauss(0, 0.005),
            'ppi': p['ppi'] + random.gauss(0, 0.008),
            'm2_growth': p['m2'] + random.gauss(0, 0.02),
            'interest_rate': p['rate'] + random.gauss(0, 0.003),
            'credit_spread': p['credit_spread'] + random.gauss(0, 0.003),
            'real_rate': p['real_rate'] + random.gauss(0, 0.002),
            'stock_return_3m': p['stock_ret'] + random.gauss(0, 0.05),
            'volatility': p['vol'] + random.gauss(0, 0.03),
            'fund_flow': p['flow'] * 1e9 + random.gauss(0, 1e8)
        }
        rows.append(row)

    # 写入CSV
    print(f"\n写入文件: {output_path}")
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['date', 'season'] + [k for k in rows[0].keys() if k not in ['date', 'season']]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    # 统计
    print("\n✓ 数据生成完成！")

    print("\n数据预览 (前10行):")
    print(f"{'日期':12} {'季节':6} {'GDP':8} {'CPI':8} {'M2':8} {'利率':8} {'股市收益':10}")
    print("-" * 70)
    for row in rows[:10]:
        print(f"{row['date']:12} {row['season']:6} "
              f"{row['gdp_growth']:8.4f} {row['cpi']:8.4f} "
              f"{row['m2_growth']:8.4f} {row['interest_rate']:8.4f} "
              f"{row['stock_return_3m']:10.4f}")

    print(f"\n总计: {n} 条记录")
    print(f"保存: {output_path}")

    # 季节统计
    season_counts = {}
    for row in rows:
        s = row['season']
        season_counts[s] = season_counts.get(s, 0) + 1

    print("\n季节分布:")
    for s, c in season_counts.items():
        print(f"  {s}: {c} ({c/n*100:.1f}%)")

    return rows


def create_hmm_training_data(output_path='data/historical_data/hmm_training_data.csv'):
    """
    创建适合HMM训练的数据集（移除season标签）

    参数:
        output_path: 输出路径
    """
    print("\n" + "=" * 70)
    print("创建HMM训练数据集（无标签）")
    print("=" * 70)

    # 先生成完整数据
    full_data = generate_sample_csv()

    # 提取数值特征
    features = [
        'gdp_growth', 'cpi', 'ppi', 'm2_growth',
        'interest_rate', 'credit_spread', 'real_rate',
        'stock_return_3m', 'volatility', 'fund_flow'
    ]

    # 写入训练数据（不含season标签）
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(features)  # 表头

        for row in full_data:
            writer.writerow([row[feat] for feat in features])

    print(f"\n✓ HMM训练数据已保存: {output_path}")
    print(f"  特征: {', '.join(features)}")


if __name__ == "__main__":
    import sys

    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'training':
            # 仅创建训练数据
            create_hmm_training_data()
        else:
            # 生成完整数据
            generate_sample_csv()
            create_hmm_training_data()

        print("\n✅ 数据生成完成！")
        print("\n下一步:")
        print("  1. 安装依赖: pip install numpy pandas scikit-learn hmmlearn")
        print("  2. 训练模型: python tools/data/train_hmm_model.py")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
