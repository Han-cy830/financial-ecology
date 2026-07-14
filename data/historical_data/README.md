# 📦 数据包说明

本目录包含用于HMM模型训练和测试的数据文件。

## 📁 文件清单

### 1. macro_data_sample.csv（完整数据）

**说明**: 包含季节标签的示例宏观数据

**时间范围**: 2000-01 至 2024-12（300个月度）

**特征**:
- `date`: 日期
- `season`: 季节标签（春季/夏季/秋季/冬季）
- `gdp_growth`: GDP同比增速
- `cpi`: CPI同比
- `ppi`: PPI同比
- `m2_growth`: M2同比增速
- `interest_rate`: 10年期国债收益率
- `credit_spread`: 信用利差
- `real_rate`: 实际利率
- `stock_return_3m`: 股市3个月收益率
- `volatility`: 波动率（VIX）
- `fund_flow`: 资金流向

**用途**:
- 研究和分析不同季节的特征
- 理解HMM模型的学习目标

### 2. hmm_training_data.csv（训练数据）

**说明**: 用于训练HMM模型的数据集（无标签）

**特征**: 10个宏观指标

**用途**:
```python
from src.hmm_detector.season_hmm import SeasonHMM
import pandas as pd

# 加载训练数据
data = pd.read_csv('data/historical_data/hmm_training_data.csv')

# 训练模型
hmm = SeasonHMM()
hmm.train(data)
```

---

## ⚠️ 数据说明

### 这是示例数据

**重要**：此数据集为**模拟生成**，用于：
1. ✅ 测试HMM模型代码
2. ✅ 演示框架功能
3. ✅ 教学和学习

**不代表真实历史数据**。

### 特征说明

- **季节性明显**: 4个季节各占20-40%
- **符合经济逻辑**:
  - 春季: 温和增长，流动性充裕
  - 夏季: 强劲增长，低波动
  - 秋季: 滞胀，高利率
  - 冬季: 衰退，通缩
- **带有随机噪声**: 模拟真实市场的不确定性

---

## 🚀 使用真实数据

### 方案A：使用真实宏观数据

推荐数据源：

1. **FRED（美联储经济数据库）**
   ```python
   import pandas_datareader.data as web
   import datetime

   start = datetime.datetime(2000, 1, 1)
   end = datetime.datetime(2024, 12, 31)

   gdp = web.DataReader('GDP', 'fred', start, end)
   cpi = web.DataReader('CPIAUCSL', 'fred', start, end)
   vix = web.DataReader('VIXCLS', 'fred', start, end)
   ```

2. **Tushare（中国数据）**
   ```python
   import tushare as ts

   pro = ts.pro_api('YOUR_TOKEN')
   df = pro.cn_gdp(start_date='20000101', end_date='20241231')
   ```

3. **Yahoo Finance**
   ```python
   import yfinance as yf

   sp500 = yf.download('^GSPC', start='2000-01-01', end='2024-12-31')
   vix = yf.download('^VIX', start='2000-01-01', end='2024-12-31')
   ```

### 方案B：使用真实数据后的HMM模型

```python
# 1. 准备真实数据（使用上述方法）
real_data = pd.DataFrame({...})

# 2. 训练HMM模型
from src.hmm_detector.season_hmm import SeasonHMM

hmm = SeasonHMM()
hmm.train(real_data)

# 3. 保存模型
import joblib
joblib.dump(hmm, 'models/hmm_real_data_model.pkl')

# 4. 使用模型预测
prediction = hmm.predict_season(current_data)
print(f"当前季节: {prediction['season']}")
```

---

## 📝 数据准备脚本

### 生成示例数据

```bash
python tools/data/generate_sample_data.py
```

### 下载真实数据（待完善）

```bash
python tools/data/download_data.py
```

### 训练HMM模型

```bash
python tools/data/train_hmm_model.py
```

---

## 📊 数据质量要求

### 最少数据量

- **时间跨度**: ≥10年
- **数据频率**: 月度
- **样本数量**: ≥120个

### 推荐配置

- **时间跨度**: 20年以上
- **数据频率**: 日度或月度
- **样本数量**: 500+

### 特征完整性

- ✅ 无缺失值
- ✅ 无异常值
- ✅ 时间连续
- ✅ 经过标准化/归一化

---

## 🔗 相关文档

- [HMM季节检测模型](../docs/hmm-season-detector.md)
- [数据下载脚本](../../tools/data/download_data.py)
- [模型训练脚本](../../tools/data/train_hmm_model.py)

---

**最后更新**: 2026-07-14
