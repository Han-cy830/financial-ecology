#!/usr/bin/env python3
"""
真实数据下载脚本

从公开数据源下载宏观数据用于HMM模型训练
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def download_from_tushare():
    """从Tushare下载数据（需要安装tushare并获取token）"""
    try:
        import tushare as ts

        print("从Tushare下载数据...")
        print("⚠️  需要先在 https://tushare.pro 注册并获取token")

        # 设置token
        # ts.set_token('YOUR_TOKEN_HERE')
        # pro = ts.pro_api()

        # 示例：获取GDP数据
        # df = pro.cn_gdp(start_date='20000101', end_date='20241231')

        print("Tushare下载功能待实现")
        return None

    except ImportError:
        print("⚠️  tushare未安装，跳过")
        return None


def download_from_yfinance():
    """从Yahoo Finance下载数据"""
    try:
        import yfinance as yf

        print("从Yahoo Finance下载数据...")

        # 下载标普500（美股代表）
        print("  下载标普500...")
        sp500 = yf.download('^GSPC', start='2000-01-01', end='2024-12-31', progress=False)

        # 下载VIX
        print("  下载VIX...")
        vix = yf.download('^VIX', start='2000-01-01', end='2024-12-31', progress=False)

        # 下载10年期国债收益率
        print("  下载10年期国债收益率...")
        tnx = yf.download('^TNX', start='2000-01-01', end='2024-12-31', progress=False)

        print("✓ Yahoo Finance数据下载完成")

        return {
            'sp500': sp500,
            'vix': vix,
            'tnx': tnx
        }

    except ImportError:
        print("⚠️  yfinance未安装")
        print("   安装: pip install yfinance")
        return None


def download_from_fred():
    """从FRED（美联储经济数据库）下载数据"""
    try:
        import pandas_datareader.data as web
        import datetime

        print("从FRED下载宏观数据...")

        start = datetime.datetime(2000, 1, 1)
        end = datetime.datetime(2024, 12, 31)

        # GDP
        print("  下载GDP...")
        gdp = web.DataReader('GDP', 'fred', start, end)

        # CPI
        print("  下载CPI...")
        cpi = web.DataReader('CPIAUCSL', 'fred', start, end)

        # 失业率
        print("  下载失业率...")
        unemployment = web.DataReader('UNRATE', 'fred', start, end)

        print("✓ FRED数据下载完成")

        return {
            'gdp': gdp,
            'cpi': cpi,
            'unemployment': unemployment
        }

    except ImportError:
        print("⚠️  pandas-datareader未安装")
        print("   安装: pip install pandas-datareader")
        return None


def generate_china_macro_data():
    """
    生成中国宏观数据（基于公开信息的手动整理）

    由于中国宏观数据来源分散，这里提供一个模板
    """
    print("生成中国宏观数据模板...")

    # 创建月度日期
    dates = pd.date_range(start='2000-01-01', end='2024-12-31', freq='M')

    # 这里应该填入实际的中国宏观数据
    # 由于数据量较大，这里只生成模板
    data = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'gdp_growth': np.nan,
        'cpi': np.nan,
        'ppi': np.nan,
        'm2_growth': np.nan,
        'interest_rate': np.nan,
        'credit_spread': np.nan,
        'real_rate': np.nan,
        'stock_return_3m': np.nan,
        'volatility': np.nan,
        'fund_flow': np.nan
    })

    # 保存模板
    os.makedirs('data/historical_data', exist_ok=True)
    output_path = 'data/historical_data/china_macro_template.csv'
    data.to_csv(output_path, index=False)

    print(f"✓ 模板已生成: {output_path}")
    print("  请手动填入实际数据")

    return data


def main():
    """主函数"""
    print("=" * 70)
    print("宏观数据下载工具")
    print("=" * 70)

    print("\n请选择数据源:")
    print("  1. Yahoo Finance（美股数据）")
    print("  2. FRED（美联储数据）")
    print("  3. Tushare（A股数据，需要token）")
    print("  4. 生成示例数据")

    # 自动执行所有可用的
    print("\n自动尝试所有数据源...\n")

    # 尝试Yahoo Finance
    yf_data = download_from_yfinance()

    # 尝试FRED
    fred_data = download_from_fred()

    # 生成示例数据
    print("\n生成示例数据...")
    from tools.data.prepare_sample_data import generate_sample_data
    sample_data = generate_sample_data()

    print("\n✓" + "=" * 68)
    print("✓ 数据准备完成！")
    print("✓" + "=" * 68)
    print("\n下一步:")
    print("  python tools/data/train_hmm_model.py")


if __name__ == "__main__":
    main()
