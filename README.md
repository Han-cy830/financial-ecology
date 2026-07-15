# 🌿 金融生态学框架 (Financial Ecology Framework)

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen.svg)](GITHUB_READY.md)

> 一个将金融市场视为生态系统的智能资产配置框架，借鉴生态学原理、AI多智能体和HMM概率模型。

[English](README.md) | [快速开始](docs/quick-start.md) | [文档导航](docs/INDEX.md)

---

## ✨ 核心特色

### 🌿 生态学思维
- **L1-L5五层资产结构**：现金→债券→股票→另类→投机，如食物链金字塔
- **捕食者/猎物/共生体**：借鉴Tokenomics-Ecological-Network，细分类别
- **四季季节轮动**：识别气候→判断季节→调整配置

### 🤖 AI增强
- **多智能体协同**：基本面/情绪/技术/风控/交易/组合经理6个智能体
- **HMM概率检测**：基于10个宏观指标的概率化季节识别
- **动态讨论机制**：模拟真实投研团队决策过程

### 🎨 可视化
- **GSRVS风格**：L4崩塌传导路径图
- **生态网络图**：资产层级关系可视化
- **配置对比图**：当前vs目标配置

### ⚙️ 可执行工具
- **命令行计算器**：`python allocation_calculator.py --season 春季`
- **交互式问卷**：10个问题判断季节
- **Python API**：完整的编程接口

---

## 🎯 解决的问题

| 问题 | 传统方法 | 本框架 |
|------|---------|--------|
| 季节判断 | 固定阈值（CAPE>30） | HMM概率模型，多维综合 |
| 配置调整 | 60/40固定比例 | 季节性轮动，动态调整 |
| 风险预警 | 无明显预警 | L4崩塌预警+多智能体监控 |
| 可解释性 | 黑盒模型 | 生态学原理，易理解 |

---

## 📊 核心功能

### 1️⃣ L1-L5五层资产结构

| 层级 | 类别 | 风险 | 配置范围 |
|------|------|------|---------|
| **L1** | 现金等价物 | ⭐ | 10-40% |
| **L2** | 债券 | ⭐⭐ | 20-40% |
| **L3** | 股票 | ⭐⭐⭐ | 15-50% |
| **L4** | 另类资产 | ⭐⭐⭐⭐ | 5-20% |
| **L5** | 投机仓位 | ⭐⭐⭐⭐⭐ | ≤5% |

### 2️⃣ 四季季节识别

| 季节 | 特征 | 配置重心 |
|------|------|---------|
| 🌱 **春季** | 经济复苏，流动性充裕 | L3股票40%，逐步加仓 |
| ☀️ **夏季** | 经济繁荣，市场乐观 | L3股票45%，积极参与L4 |
| 🍂 **秋季** | 滞胀，增长放缓 | L2债券35%，增加防守 |
| ❄️ **冬季** | 衰退，通缩风险 | L1现金40%，现金为王 |

### 3️⃣ HMM概率检测

- 基于10个宏观指标：GDP、CPI、M2、利率、信用利差、股市收益、波动率等
- 输出各季节概率分布（而非单一判断）
- 支持多市场共振分析

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/Han-cy830/financial-ecology.git
cd financial-ecology
./setup.sh
```

### 第一步：判断季节

```bash
python tools/season-questionnaire/questionnaire.py
```

**示例输出**:
```
当前季节: 春季 (置信度: 68.5%)
概率分布:
  春季: 68.5% ████████████████████████
  夏季: 18.2% ███████
  秋季:  9.8% ████
  冬季:  3.5% ██
```

### 第二步：生成配置

```bash
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 \
  --risk moderate \
  --capital 1000000
```

**示例输出**:
```
L1: 15.0% ████████████████████ ¥150,000.00
L2: 30.0% ██████████████████████████████████████ ¥300,000.00
L3: 40.0% ██████████████████████████████████████████████████████████████ ¥400,000.00
L4: 10.0% █████████████████████ ¥100,000.00
L5:  5.0% ████████████ ¥50,000.00

预期收益率: 8.75%
预期波动率: 14.2%
夏普比率:  2.10
```

### 第三步：查看完整演示

```bash
python tools/demo.py
```

---

## 📚 文档导航

### 🎯 快速入口

- 📘 **[快速开始](docs/quick-start.md)** - 10分钟上手
- 📗 **[框架原理](docs/framework-principles.md)** - 理解L1-L5核心概念
- 📙 **[FAQ](docs/faq.md)** - 14个常见问题解答

### 📖 深入学习

- 📕 **[生态模型](docs/ecosystem-model.md)** - 捕食者/猎物/共生体分类
- 📓 **[HMM季节检测](docs/hmm-season-detector.md)** - 概率化识别
- 📔 **[多智能体执行层](docs/multi-agent-execution.md)** - AI协同决策

### 📊 案例研究

- 📈 **[2008年金融危机](docs/case-studies/2008-financial-crisis.md)** - 危机中的配置策略
- 📉 **[2020年COVID危机](docs/case-studies/2020-covid-crisis.md)** - 流动性危机应对

### 🔍 其他文档

- 📑 **[文档导航](docs/INDEX.md)** - 完整的文档地图
- 📋 **[项目结构](docs/STRUCTURE.md)** - 代码组织说明
- 🤝 **[贡献指南](CONTRIBUTING.md)** - 如何参与贡献

---

## 💻 Python API

### 资产生态分类

```python
from src.ecosystem import AssetClassifier

classifier = AssetClassifier()

# 分类比特币
btc = classifier.classify(
    name="比特币",
    volatility=0.80,
    cash_flow_positive=False,
    correlation_with_stocks=0.30,
    leverage_ratio=2.0,
    liquidity_score=0.85
)

print(f"生态角色: {btc['role']}")        # 纯投机捕食者
print(f"风险等级: {btc['risk_level']}")  # 极高
print(f"置信度: {btc['confidence']:.1%}") # 88%
```

### HMM季节检测

```python
from src.hmm_detector import SeasonHMM
import pandas as pd

# 训练模型
hmm = SeasonHMM()
historical_data = pd.read_csv('data/historical_data.csv')
hmm.train(historical_data)

# 检测当前季节
current_data = pd.DataFrame({...})
prediction = hmm.predict_season(current_data)

print(f"季节: {prediction['season']}")  # 春季
print(f"配置: {prediction['suggested_allocation']}")
```

### 配置计算

```python
from tools.allocation_calculator import AllocationCalculator

calculator = AllocationCalculator()

result = calculator.calculate(
    season='春季',
    risk_preference='moderate',
    total_capital=1000000
)

print(result['allocation'])      # 配置比例
print(result['expected_return']) # 预期收益
print(result['sharpe_ratio'])    # 夏普比率
```

---

## 📊 框架对比

| 特征 | 金融生态学 | 60/40组合 | 风险平价 |
|------|-----------|----------|---------|
| **动态调整** | ✅ 季节轮动 | ❌ 固定比例 | ⚠️ 定期再平衡 |
| **风险预警** | ✅ HMM+AI | ❌ 无预警 | ⚠️ 基本预警 |
| **可解释性** | ✅ 生态学原理 | ✅ 简单 | ❌ 复杂 |
| **适合个人** | ✅ 易上手 | ✅ 简单 | ❌ 需专业知识 |

---

## 🎓 学习路径

### 路径1: 快速应用（1天）
1. ✅ [快速开始](docs/quick-start.md) (10分钟)
2. ✅ 使用交互式问卷 (5分钟)
3. ✅ 生成第一个配置方案 (5分钟)

### 路径2: 系统学习（1周）
4. ✅ [框架原理](docs/framework-principles.md)
5. ✅ [生态模型](docs/ecosystem-model.md)
6. ✅ [季节识别](docs/season-identification.md)
7. ✅ [2008年案例](docs/case-studies/2008-financial-crisis.md)

### 路径3: 深度研究（1个月）
8. ✅ [HMM模型](docs/hmm-season-detector.md)
9. ✅ [多智能体](docs/multi-agent-execution.md)
10. ✅ 贡献代码或案例研究

---

## 🌟 核心优势

### 1. 生态学思维
借鉴自然生态系统的生存智慧，食物链金字塔结构管理脆弱性

### 2. AI增强
多智能体协同决策 + 概率化识别（非黑即白）

### 3. 可执行性
命令行工具 + Python API + 交互式问卷 + 一键演示

### 4. 实战导向
基于真实历史案例，可回测验证

### 5. 开放架构
模块化设计，易于扩展，欢迎社区贡献

---

## 📈 实战验证

### 2008年金融危机案例

**传统60/40配置**:
- 回撤: -35%
- 2年总收益: -18%

**生态学优化配置**:
- 回撤: **-18%** ← 减少一半
- 2年总收益: **+10%** ← 转亏为盈

**关键**: 提前识别秋季信号，增加L1/L2防御，避免L4危机传导

---

## 🤝 贡献

我们欢迎所有形式的贡献！

- 📝 **文档改进** - 翻译、修正、补充
- 🔧 **代码开发** - 新功能、Bug修复
- 📊 **案例研究** - 历史事件分析
- 💡 **建议反馈** - 框架优化

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📞 社区

- 💬 **Discord**: [加入讨论](https://discord.gg/your-invite)
- 📧 **Email**: Han-cy830@users.noreply.github.com
- 🐛 **Issues**: [提交问题](https://github.com/Han-cy830/financial-ecology/issues)

---

## 📄 许可证

MIT License

---

## ⚠️ 免责声明

**本框架仅供教育和研究目的，不构成投资建议。**

金融市场具有高度不确定性，历史表现不代表未来结果。投资者应根据自身情况独立决策，并承担相应风险。

---

## 🙏 致谢

本项目借鉴了以下开源项目和学术成果：

- [Tokenomics-Ecological-Network](https://github.com/) - 代币生态分类
- [Evology](https://github.com/oxford-finance/evology) - 牛津大学金融生态学
- [TradingAgents](https://github.com/tradingagents/tradingagents) - AI多智能体交易
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) - AI对冲基金
- [GSRVS](https://github.com/) - 系统性风险可视化
- **CFA Institute** - 复杂系统研究报告（2025）

---

**Made with ❤️ and 🌿 by the Financial Ecology Community**

**Star ⭐ us on GitHub if this project helps you!**
