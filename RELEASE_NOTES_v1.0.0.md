# 🎉 金融生态学框架 v1.0.0

> 一个将金融市场视为生态系统的智能资产配置框架

---

## 🌿 核心特色

### 1. L1-L5 五层资产配置体系
借鉴生态系统食物链金字塔结构，科学管理资产配置：
- **L1 现金** - 流动性储备 (10-40%)
- **L2 债券** - 稳定收益 (20-40%)
- **L3 股票** - 长期增长 (15-50%)
- **L4 另类资产** - 高收益机会 (5-20%)
- **L5 投机仓位** - 高风险博弈 (≤5%)

### 2. 🌸 四季季节识别
根据宏观气候环境识别市场季节：
- 🌱 **春季** - 复苏期：逐步增加股票仓位
- ☀️ **夏季** - 繁荣期：重仓权益，积极参与
- 🍂 **秋季** - 滞胀期：增加防守，降低风险
- ❄️ **冬季** - 衰退期：现金为王，等待机会

### 3. 🤖 AI 增强决策
- **多智能体系统**：基本面/情绪/技术/风控/交易/组合经理协同工作
- **HMM 概率检测**：基于10个宏观指标的概率化季节识别
- **动态讨论机制**：模拟真实投研团队决策过程

### 4. 📊 GSRVS 风格风险可视化
- L4 崩塌传导路径图
- 生态系统网络图
- 资产配置对比分析

---

## 📦 本版本包含

### 核心功能
- ✅ L1-L5 五层资产配置模型
- ✅ 四季季节识别指南
- ✅ HMM 概率化季节检测模型
- ✅ 多智能体协同决策框架（设计文档）
- ✅ 风险可视化工具
- ✅ 生态资产分类器

### 工具脚本
- ✅ 资产配置计算器
- ✅ 交互式季节判断问卷
- ✅ 一键演示脚本

### 文档
- ✅ 完整的框架原理文档
- ✅ 详细的 API 说明
- ✅ 14个常见问题解答
- ✅ 2个历史案例分析（2008金融危机、2020 COVID）
- ✅ 快速开始指南

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/Han-cy830/financial-ecology.git
cd financial-ecology
./setup.sh
```

### 判断季节

```bash
python tools/season-questionnaire/questionnaire.py
```

### 生成配置方案

```bash
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 \
  --risk moderate \
  --capital 1000000
```

### 运行演示

```bash
python tools/demo.py
```

---

## 📚 文档导航

- 📘 **[快速开始](docs/quick-start.md)** - 10分钟上手
- 📗 **[框架原理](docs/framework-principles.md)** - 理解L1-L5核心概念
- 📙 **[生态模型](docs/ecosystem-model.md)** - 捕食者/猎物/共生体分类
- 📕 **[HMM季节检测](docs/hmm-season-detector.md)** - 概率化识别技术
- 📔 **[FAQ](docs/faq.md)** - 常见问题解答

---

## 💻 Python API 示例

```python
from src.ecosystem import AssetClassifier
from src.hmm_detector import SeasonHMM
from tools.allocation_calculator import AllocationCalculator

# 1. 资产生态分类
classifier = AssetClassifier()
btc = classifier.classify(
    name="比特币",
    volatility=0.80,
    cash_flow_positive=False,
    correlation_with_stocks=0.30
)
print(f"生态角色: {btc['role']}")  # 纯投机捕食者

# 2. HMM季节检测
hmm = SeasonHMM()
hmm.train(historical_data)
prediction = hmm.predict_season(current_data)
print(f"当前季节: {prediction['season']}")

# 3. 配置计算
calculator = AllocationCalculator()
result = calculator.calculate(season='春季', risk='moderate')
print(result['allocation'])
```

---

## 🎯 适用场景

- ✅ **个人投资者** - 系统化资产配置
- ✅ **量化团队** - HMM模型基础
- ✅ **学术研究** - 复杂系统建模

---

## 📊 项目统计

- **代码行数**: 2,572 行 Python
- **文档行数**: 5,765 行
- **总文件数**: 29 个
- **核心模块**: 4 个
- **工具脚本**: 3 个

---

## 🤝 贡献

欢迎贡献代码、文档和案例研究！

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## ⚠️ 免责声明

**本框架仅供教育和研究目的，不构成投资建议。**
金融市场具有高度不确定性，历史表现不代表未来结果。

---

## 🙏 致谢

本项目借鉴了以下优秀项目：
- [Evology](https://github.com/oxford-finance/evology) - 牛津大学金融生态学
- [TradingAgents](https://github.com/tradingagents/tradingagents) - AI多智能体交易
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) - AI对冲基金框架
- CFA Institute - 复杂系统研究报告（2025）

---

**🌿 Made with Love by the Financial Ecology Community**

**⭐ 如果这个项目对你有帮助，请给我们一个 Star！**
