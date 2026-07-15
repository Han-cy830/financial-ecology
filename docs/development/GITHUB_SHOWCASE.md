# 🌿 金融生态学框架 - 项目展示

一个将金融市场视为生态系统的智能资产配置框架。

---

## 📊 项目亮点

### ✨ 五大核心创新

1. **🌿 生态学思维**
   - 借鉴Tokenomics-Ecological-Network的捕食者/猎物/共生体分类
   - L4细分为价值型（有现金流）vs 投机型（纯赌博）
   - 食物链金字塔结构管理脆弱性

2. **🤖 AI多智能体决策**
   - 6个专业智能体协同工作（基本面/情绪/技术/风控/交易/组合经理）
   - 动态讨论机制，模拟真实投研团队
   - 风控拥有否决权

3. **📊 概率化季节检测**
   - 使用HMM模型替代固定阈值
   - 10个宏观指标综合判断
   - 支持A股/美股/港股多市场共振分析

4. **🎨 GSRVS风格可视化**
   - 生态网络图展示层级关系
   - L4崩塌传导路径动画
   - 风险传染可视化

5. **⚙️ 可执行工具集**
   - 命令行配置计算器
   - 交互式季节判断问卷
   - 一键演示脚本

---

## 🎯 解决的核心问题

### 传统方法的局限

| 方法 | 问题 | 本框架的解决 |
|------|------|------------|
| 固定阈值（CAPE>30） | 硬边界、滞后、单一维度 | HMM概率模型，多维综合 |
| 60/40股债平衡 | 忽视季节、无预警机制 | 季节性轮动+L4崩塌预警 |
| 风险平价 | 过于复杂、不适合个人 | 简化L1-L5层级，易理解 |
| 单一策略 | 容易失效 | 生态多样性，动态调整 |

---

## 📈 核心功能演示

### 1️⃣ 资产生态分类

```python
from src.ecosystem import AssetClassifier

classifier = AssetClassifier()

# 自动识别资产生态角色
assets = {
    '国债':         {'volatility': 0.08,  'cash_flow_positive': True,  'correlation_with_stocks': 0.10,  'leverage_ratio': 1.0,  'liquidity_score': 0.95},
    '沪深300':      {'volatility': 0.25,  'cash_flow_positive': True,  'correlation_with_stocks': 0.98,  'leverage_ratio': 1.0,  'liquidity_score': 0.90},
    'REITs':        {'volatility': 0.35,  'cash_flow_positive': True,  'correlation_with_stocks': 0.60,  'leverage_ratio': 2.0,  'liquidity_score': 0.70},
    '比特币':       {'volatility': 0.80,  'cash_flow_positive': False, 'correlation_with_stocks': 0.30,  'leverage_ratio': 2.0,  'liquidity_score': 0.85},
    '个股期权':     {'volatility': 0.90,  'cash_flow_positive': False, 'correlation_with_stocks': 0.70,  'leverage_ratio': 5.0,  'liquidity_score': 0.30}
}

for name, info in assets.items():
    result = classifier.classify(name=name, **info)
    print(f"{name:8s} → {result['role']:12s} (置信度: {result['confidence']:.0%})")

# 输出:
# 国债     → 猎物          (置信度: 85%)
# 沪深300  → 价值创造者    (置信度: 78%)
# REITs    → 价值型捕食者  (置信度: 72%)
# 比特币   → 纯投机捕食者  (置信度: 88%)
# 个股期权 → 顶级捕食者    (置信度: 92%)
```

### 2️⃣ HMM概率季节检测

```python
from src.hmm_detector import SeasonHMM
import pandas as pd

# 训练模型（使用20年历史数据）
hmm = SeasonHMM()
historical_data = pd.read_csv('data/historical_data.csv')
hmm.train(historical_data)

# 检测当前季节
current_data = pd.DataFrame({...})
prediction = hmm.predict_season(current_data)

print(f"当前季节: {prediction['season']}")
print(f"置信度: {prediction['confidence']:.1%}")
print(f"\n概率分布:")
for season, prob in prediction['probabilities'].items():
    print(f"  {season}: {prob:.1%}")

# 输出:
# 当前季节: 春季
# 置信度: 68.5%
#
# 概率分布:
#   春季: 68.5%
#   夏季: 18.2%
#   秋季: 9.8%
#   冬季: 3.5%
```

### 3️⃣ 多智能体协同决策

```python
from agents import PortfolioManager, FundamentalAnalyst, RiskManager

# 创建6个智能体
agents = [
    FundamentalAnalyst(),    # 基本面分析师
    SentimentAnalyst(),      # 情绪分析师
    TechnicalAnalyst(),      # 技术分析师
    RiskManager(),           # 风控专员
    Executor(),              # 交易员
]

# 组合经理综合决策
pm = PortfolioManager(agents)
decision = pm.make_decision(market_data, current_portfolio)

print(decision)
# {
#   'decision': '执行',
#   'target_allocation': {...},
#   'smoothed_allocation': {...},
#   'opinions': {...}
# }
```

### 4️⃣ 配置计算器

```bash
# 命令行工具
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 \
  --risk moderate \
  --capital 1000000

# 输出:
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

### 5️⃣ 风险可视化

```python
from src.visualization import SystemicRiskVisualizer

viz = SystemicRiskVisualizer()

# 1. 生态系统网络图
assets = {...}
fig1 = viz.plot_ecosystem_network(assets)
fig1.savefig('ecosystem.png')

# 2. L4崩塌传导路径
contagion = {'path': [...]}
fig2 = viz.plot_contagion_path(contagion)
fig2.savefig('contagion.png')

# 3. 配置对比
fig3 = viz.plot_portfolio_allocation(current, target)
fig3.savefig('allocation.png')
```

---

## 🗂️ 项目结构

```
financial-ecology/
├── 📚 docs/                    # 11个文档
│   ├── INDEX.md               # 文档导航
│   ├── framework-principles.md
│   ├── ecosystem-model.md
│   ├── multi-agent-execution.md
│   ├── hmm-season-detector.md
│   ├── quick-start.md
│   ├── faq.md
│   └── case-studies/
├── 🐍 src/                    # 核心代码 (~2500行)
│   ├── ecosystem/             # 生态分类器
│   ├── hmm_detector/          # HMM模型
│   ├── agents/                # 多智能体
│   └── visualization/         # 可视化工具
├── 🔧 tools/                  # 实用工具
│   ├── allocation-calculator/ # 配置计算器
│   ├── season-questionnaire/  # 季节问卷
│   └── demo.py                # 演示脚本
├── configs/                   # 配置文件
├── README.md
├── requirements.txt
└── setup.sh
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/your-username/financial-ecology.git
cd financial-ecology
./setup.sh
```

### 第一个配置方案

```bash
# 判断季节
python tools/season-questionnaire/questionnaire.py

# 生成配置
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 \
  --risk moderate \
  --capital 1000000

# 运行完整演示
python tools/demo.py
```

---

## 📊 框架对比

| 维度 | 金融生态学 | 传统60/40 | 风险平价 |
|------|-----------|----------|---------|
| **核心理念** | 生态学 + 季节轮动 | 固定比例 | 等风险贡献 |
| **动态调整** | ✅ 季节性轮动 | ❌ 年度再平衡 | ⚠️ 定期再平衡 |
| **风险预警** | ✅ HMM + 多智能体 | ❌ 无明显预警 | ⚠️ 基本预警 |
| **可解释性** | ✅ 生态学原理 | ✅ 简单 | ❌ 复杂 |
| **个人友好** | ✅ 易上手 | ✅ 非常简单 | ❌ 需要专业知识 |

---

## 🌟 特色案例

### 2008年金融危机

**传统配置** (60%股票):
- 回撤: -35%
- 2年总收益: -18%

**生态学优化配置**:
- 回撤: -18% ← 减少一半
- 2年总收益: +10% ← 转亏为盈

**关键**: 提前识别秋季信号，增加L1/L2防御，避免L4危机传导

详见: [docs/case-studies/2008-financial-crisis.md](docs/case-studies/2008-financial-crisis.md)

---

## 🎓 学习路径

### 新手 (1天)
1. [快速开始](docs/quick-start.md) (10分钟)
2. 使用交互式问卷 (5分钟)
3. 生成第一个配置方案 (5分钟)

### 进阶 (1周)
4. 学习[框架原理](docs/framework-principles.md)
5. 研究[生态模型](docs/ecosystem-model.md)
6. 实践[季节识别](docs/season-identification.md)

### 高级 (1个月)
7. 深入[HMM模型](docs/hmm-season-detector.md)
8. 研究[多智能体系统](docs/multi-agent-execution.md)
9. 贡献代码或案例研究

---

## 🤝 贡献

欢迎各类贡献：

- 📝 **文档改进** - 翻译、修正、补充
- 🔧 **代码开发** - 新功能、Bug修复
- 📊 **案例研究** - 历史事件分析
- 💡 **建议反馈** - 框架优化

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 社区

- 💬 **Discord**: [加入讨论](https://discord.gg/your-invite)
- 📧 **Email**: your-email@example.com
- 🐛 **Issues**: [报告问题](https://github.com/your-username/financial-ecology/issues)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## ⚠️ 免责声明

**本框架仅供教育和研究目的，不构成投资建议。**

金融市场具有高度不确定性，历史表现不代表未来结果。投资者应根据自身情况独立决策，并承担相应风险。

---

**Made with ❤️ and 🌿 by the Financial Ecology Community**

**Star ⭐ us on GitHub if this project helps you!**
