# 📚 文档导航

本框架的所有文档，按学习路径组织。

## 🎯 快速入口

### 新手起点

1. **[快速开始](quick-start.md)** ⭐ 从安装到第一个配置方案，10分钟上手
2. **[框架原理](framework-principles.md)** 📖 理解核心理念和L1-L5层级设计
3. **[常见问题](faq.md)** ❓ 遇到问题先查这里

### 进阶学习

4. **[生态模型](ecosystem-model.md)** 🌿 优化后的捕食者-猎物分类体系
5. **[季节识别指南](season-identification.md)** 🔍 手动判断市场季节
6. **[多智能体执行层](multi-agent-execution.md)** 🤖 AI协同决策系统

### 高级功能

7. **[HMM季节检测模型](hmm-season-detector.md)** 📊 概率化季节识别
8. **[风险可视化工具](visualization.md)** 📈 GSRVS风格风险传导图

### 实践案例

9. **[2008年金融危机](case-studies/2008-financial-crisis.md)** 📉 危机中的配置策略
10. **[2020年COVID危机](case-studies/2020-covid-crisis.md)** 🦠 流动性危机的应对

---

## 📖 按主题分类

### 理论原理

| 文档 | 难度 | 时间 |
|------|------|------|
| [框架原理](framework-principles.md) | ⭐⭐ | 30分钟 |
| [生态模型](ecosystem-model.md) | ⭐⭐⭐ | 45分钟 |
| [季节识别指南](season-identification.md) | ⭐⭐⭐ | 30分钟 |

### 工具与实践

| 文档 | 难度 | 时间 |
|------|------|------|
| [快速开始](quick-start.md) | ⭐ | 10分钟 |
| [FAQ](faq.md) | ⭐⭐ | 按需查阅 |
| [多智能体执行层](multi-agent-execution.md) | ⭐⭐⭐⭐ | 60分钟 |
| [HMM季节检测模型](hmm-season-detector.md) | ⭐⭐⭐⭐ | 45分钟 |
| [风险可视化工具](visualization.md) | ⭐⭐⭐ | 30分钟 |

### 案例研究

| 文档 | 时间 | 核心要点 |
|------|------|---------|
| [2008年金融危机](case-studies/2008-financial-crisis.md) | 20分钟 | 流动性危机中的防守 |
| [2020年COVID危机](case-studies/2020-covid-crisis.md) | 20分钟 | V型反弹的机会 |

---

## 🔄 推荐学习路径

### 路径1: 快速应用（1天）

适合：想快速上手的实用主义者

1. [快速开始](quick-start.md) (10分钟)
2. [FAQ](faq.md) - 只看前5个问题 (15分钟)
3. 使用交互式问卷判断当前季节 (5分钟)
4. 使用配置计算器生成方案 (5分钟)

**目标**: 生成第一个配置方案

---

### 路径2: 系统学习（1周）

适合：希望深入理解的投资者

**Day 1**: [框架原理](framework-principles.md)
**Day 2**: [生态模型](ecosystem-model.md) + [FAQ](faq.md)
**Day 3**: [季节识别指南](season-identification.md) + 交互式问卷
**Day 4**: [多智能体执行层](multi-agent-execution.md)（选读）
**Day 5**: [HMM季节检测模型](hmm-season-detector.md)（选读）
**Day 6**: [2008年金融危机案例](case-studies/2008-financial-crisis.md)
**Day 7**: 实践应用 + 复盘

**目标**: 完整理解框架原理和工具

---

### 路径3: 深度研究（1个月）

适合：希望贡献代码或学术研究者

**Week 1**: 基础学习（路径2）
**Week 2**: 深入学习HMM和多智能体系统
**Week 3**: 研究所有案例，建立自己的数据集
**Week 4**: 尝试改进框架，提交贡献

**目标**: 成为框架贡献者

---

## 🗂️ 文档结构

```
docs/
├── framework-principles.md     # 框架原理（核心）
├── ecosystem-model.md          # 生态模型（优化）
├── season-identification.md    # 季节识别指南
├── multi-agent-execution.md    # 多智能体执行层
├── hmm-season-detector.md      # HMM季节检测
├── visualization.md            # 风险可视化
├── allocation-decision.md      # 配置决策手册
├── quick-start.md              # 快速开始
├── faq.md                      # 常见问题
└── case-studies/               # 案例研究
    ├── 2008-financial-crisis.md
    └── 2020-covid-crisis.md

tools/                          # 工具
├── allocation-calculator/      # 配置计算器
└── season-questionnaire/       # 季节问卷

src/                           # 核心代码
├── ecosystem/                 # 生态模型
├── hmm_detector/              # HMM检测器
├── agents/                    # 多智能体
└── visualization/             # 可视化工具
```

---

## 🔍 搜索文档

### 我想了解...

**基础概念**:
- L1-L5是什么？→ [框架原理](framework-principles.md)
- 什么是生态季节？→ [框架原理](framework-principles.md)
- 生态学有什么借鉴价值？→ [生态模型](ecosystem-model.md)

**实际操作**:
- 如何判断当前季节？→ [季节识别指南](season-identification.md)
- 如何生成配置方案？→ [快速开始](quick-start.md)
- 应该配置哪些具体资产？→ [FAQ](faq.md) Q8

**高级功能**:
- 如何使用HMM模型？→ [HMM季节检测](hmm-season-detector.md)
- 如何使用多智能体？→ [多智能体执行层](multi-agent-execution.md)
- 如何可视化风险？→ [风险可视化](visualization.md)

**历史经验**:
- 2008年危机该怎么应对？→ [2008年案例](case-studies/2008-financial-crisis.md)
- 2020年COVID怎么办？→ [2020年案例](case-studies/2020-covid-crisis.md)

---

## 📞 需要帮助？

- 💬 [Discord社区](https://discord.gg/your-invite)
- 📧 your-email@example.com
- 🐛 [提交Issue](https://github.com/your-username/financial-ecology/issues)

---

**提示**: 按 `Cmd/Ctrl + K` (GitHub) 或使用页面搜索功能，可以快速查找关键词。
