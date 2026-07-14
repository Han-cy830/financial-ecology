# 快速开始指南

本指南将帮助你在10分钟内开始使用金融生态学框架。

## 📋 目录

1. [安装](#安装)
2. [第一个配置方案](#第一个配置方案)
3. [判断市场季节](#判断市场季节)
4. [进阶使用](#进阶使用)

---

## 安装

### 方式一：使用安装脚本（推荐）

```bash
git clone https://github.com/your-username/financial-ecology.git
cd financial-ecology
./setup.sh
```

### 方式二：手动安装

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/financial-ecology.git
cd financial-ecology

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate.bat  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装项目
pip install -e .
```

---

## 第一个配置方案

### 1. 使用命令行计算器

```bash
# 激活虚拟环境
source venv/bin/activate

# 春季复苏期，中等风险偏好
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 \
  --risk moderate \
  --capital 1000000

# 输出示例:
# L1: 15.0% ████████████████████ ¥150,000.00
# L2: 30.0% ██████████████████████████████████████ ¥300,000.00
# L3: 40.0% ██████████████████████████████████████████████████████████████ ¥400,000.00
# L4: 10.0% █████████████████████ ¥100,000.00
# L5:  5.0% ████████████ ¥50,000.00
#
# 预期收益率: 8.75%
# 预期波动率: 14.2%
# 夏普比率:  2.10
```

### 2. Python代码示例

```python
from src.allocation_calculator import AllocationCalculator

# 创建计算器
calculator = AllocationCalculator()

# 计算配置方案
result = calculator.calculate(
    season='春季',           # 当前季节
    risk_preference='moderate',  # 中等风险偏好
    total_capital=1000000   # 总资金100万
)

# 查看配置比例
print("配置方案:")
for layer, weight in result['allocation'].items():
    print(f"{layer}: {weight:.1%}")

# 查看预期收益
print(f"\n预期收益率: {result['expected_return']:.2%}")
print(f"预期波动率: {result['expected_risk']:.2%}")

# 使用自定义约束
result = calculator.calculate(
    season='春季',
    risk_preference='moderate',
    total_capital=1000000,
    constraints={
        'no_l5': True,        # 禁止投机仓位
        'max_l1': 0.20       # L1不超过20%
    }
)
```

---

## 判断市场季节

### 方法一：交互式问卷（10个问题）

```bash
python tools/season-questionnaire/questionnaire.py
```

**示例会话**:

```
========================================
金融生态学 - 市场季节判断问卷
========================================

问题gdp_growth: GDP增速如何？
  1. 明显负增长（<-2%）
  2. 轻微负增长或接近零（-2%~0%）
  3. 温和正增长（0%~5%）
  4. 强劲正增长（>5%）

请选择 (1-4): 3
✓ 已记录

问题inflation: 通胀水平如何？
  ...

========================================
问卷结果
========================================

各季节概率:
  春季: 55.2% █████████████████████████████████████████
  夏季: 15.3% ██████████
  秋季: 20.1% █████████████
  冬季:  9.4% ██████

诊断结果: 春季
置信度: 55.2%

季节特征: 经济复苏，风险资产开始回暖
参考配置: L3股票40%, L2债券30%, L1现金15%, L4另类10%, L5投机5%
操作建议: 逐步从L2转向L3，保持一定流动性
```

### 方法二：HMM概率模型

```python
from src.hmm_detector import SeasonHMM
import pandas as pd

# 1. 加载历史数据（2000-2024年）
# 包含GDP、CPI、M2、利率、股市收益率等指标
historical_data = pd.read_csv('data/historical_data.csv')

# 2. 训练HMM模型
hmm = SeasonHMM()
hmm.train(historical_data)

# 3. 准备当前数据
current_data = pd.DataFrame({
    'gdp_growth': [0.052],
    'cpi': [0.022],
    'ppi': [0.015],
    'm2_growth': [0.105],
    'interest_rate': [0.028],
    'credit_spread': [0.012],
    'real_rate': [0.006],
    'stock_return_3m': [0.08],
    'volatility': [0.16],
    'fund_flow': [500000000]
})

# 4. 预测季节
result = hmm.predict_season(current_data)

print(f"当前季节: {result['season']}")
print(f"置信度: {result['confidence']:.1%}")
print(f"\n概率分布:")
for season, prob in result['probabilities'].items():
    print(f"  {season}: {prob:.1%}")

print(f"\n季节切换概率: {result['regime_change_probability']:.1%}")
print(f"\n配置建议:")
for layer, weight in result['suggested_allocation'].items():
    print(f"  {layer}: {weight:.1%}")

# 输出示例:
# 当前季节: 春季
# 置信度: 68.5%
#
# 概率分布:
#   春季: 68.5%
#   夏季: 18.2%
#   秋季: 9.8%
#   冬季: 3.5%
#
# 季节切换概率: 31.5%
#
# 配置建议:
#   L1: 17.3%
#   L2: 31.2%
#   L3: 38.5%
#   L4: 9.8%
#   L5: 3.2%
```

---

## 进阶使用

### 多市场季节检测

```python
from src.hmm_detector import MultiMarketHMMDetector

# 创建多市场检测器
detector = MultiMarketHMMDetector()
detector.add_market('A股')
detector.add_market('美股')
detector.add_market('港股')

# 训练所有市场
for market in ['A股', '美股', '港股']:
    data = load_market_data(market)
    detector.train_market(market, data)

# 检测季节
current_data = {
    'A股': load_current_data('A股'),
    '美股': load_current_data('美股'),
    '港股': load_current_data('港股')
}

results = detector.detect(current_data)
alignment = detector.get_season_alignment(current_data)

print(f"主导季节: {alignment['dominant_season']}")
print(f"共振强度: {alignment['strength']:.1%}")
print(f"各市场: {alignment['market_seasons']}")
```

### 可视化风险传导路径

```python
from src.visualization import SystemicRiskVisualizer

# 创建可视化器
viz = SystemicRiskVisualizer()

# 1. 绘制生态系统网络
assets = {
    '国债': {'layer': 'L1', 'risk_score': 10},
    '沪深300': {'layer': 'L3', 'risk_score': 50},
    '比特币': {'layer': 'L4', 'risk_score': 85}
}
fig = viz.plot_ecosystem_network(assets)
fig.savefig('ecosystem.png', dpi=150)

# 2. 绘制L4崩塌传导路径
contagion = {
    'path': [
        {'layer': 'L4', 'asset': '比特币', 'shock': -0.70, 'time': 'T+0'},
        {'layer': 'L3', 'asset': '纳指', 'shock': -0.15, 'time': 'T+1'},
        {'layer': 'L2', 'asset': '债券', 'shock': +0.03, 'time': 'T+2'}
    ],
    'amplification': 2.3
}
fig = viz.plot_contagion_path(contagion)
fig.savefig('contagion.png', dpi=150)

# 3. 绘制配置方案
current = {'L1': 0.15, 'L2': 0.30, 'L3': 0.38, 'L4': 0.12, 'L5': 0.05}
target = {'L1': 0.20, 'L2': 0.30, 'L3': 0.35, 'L4': 0.10, 'L5': 0.05}
fig = viz.plot_portfolio_allocation(current, target)
fig.savefig('allocation.png', dpi=150)
```

### 资产分类

```python
from src.ecosystem import AssetClassifier

classifier = AssetClassifier()

# 分类国债
bond = classifier.classify(
    name="10年期国债",
    volatility=0.08,
    cash_flow_positive=True,
    correlation_with_stocks=0.10,
    leverage_ratio=1.0,
    liquidity_score=0.95
)
print(f"国债: {bond['role']} (置信度: {bond['confidence']:.1%})")

# 分类比特币
btc = classifier.classify(
    name="比特币",
    volatility=0.80,
    cash_flow_positive=False,
    correlation_with_stocks=0.30,
    leverage_ratio=2.0,
    liquidity_score=0.85,
    regulatory_status='semi_regulated'
)
print(f"比特币: {btc['role']} (置信度: {btc['confidence']:.1%})")

# 批量分类
assets = [
    {'name': '沪深300', 'volatility': 0.25, 'cash_flow_positive': True, ...},
    {'name': 'REITs', 'volatility': 0.35, 'cash_flow_positive': True, ...},
    {'name': '个股期权', 'volatility': 0.90, 'cash_flow_positive': False, ...},
]
df = classifier.batch_classify(assets)
print(df)
```

---

## 📚 下一步

- 📖 阅读[框架原理](docs/framework-principles.md)理解核心理念
- 🌿 了解[生态模型](docs/ecosystem-model.md)的优化分类
- 🤖 学习[多智能体执行层](docs/multi-agent-execution.md)
- 📊 探索[HMM季节检测](docs/hmm-season-detector.md)
- 🔍 查看[案例研究](docs/case-studies/)学习历史经验

---

## ❓ 获取帮助

- 📖 查看[常见问题](docs/faq.md)
- 💬 加入[Discord社区](https://discord.gg/your-invite)
- 🐛 提交[Issue](https://github.com/your-username/financial-ecology/issues)

---

**祝投资顺利！🌿📈**
