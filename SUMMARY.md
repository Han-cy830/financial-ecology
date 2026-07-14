# 🌿 金融生态学框架 - 项目总结

> 一个将金融市场视为生态系统的智能资产配置框架

[English](README.md) | 中文

## ✨ 核心特色

- 🌿 **生态学思维** - 借鉴自然生态系统，L1-L5五层资产结构
- 🤖 **AI增强** - 6个智能体协同决策 + HMM概率季节检测
- 🎨 **可视化** - GSRVS风格风险传导图
- ⚙️ **可执行** - 命令行工具 + Python API + 交互式问卷
- 📊 **实战导向** - 2008年案例回测，可量化验证

## 📦 项目结构

```
financial-ecology/
├── 📚 docs/          # 13个文档（理论+案例）
├── 🐍 src/           # 核心代码（~2500行）
├── 🔧 tools/          # 工具脚本
├── configs/           # 配置文件
└── README.md
```

## 🚀 10分钟快速开始

```bash
# 1. 安装
git clone https://github.com/your-username/financial-ecology.git
cd financial-ecology
./setup.sh

# 2. 判断季节
python tools/season-questionnaire/questionnaire.py

# 3. 生成配置
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 --risk moderate --capital 1000000

# 4. 验证安装
python verify.py
```

## 📊 核心功能

### 1. L1-L5五层资产配置

| 层级 | 类别 | 风险 | 功能 |
|------|------|------|------|
| L1 | 现金 | ⭐ | 流动性 |
| L2 | 债券 | ⭐⭐ | 稳定收益 |
| L3 | 股票 | ⭐⭐⭐ | 长期增长 |
| L4 | 另类 | ⭐⭐⭐⭐ | 高收益机会 |
| L5 | 投机 | ⭐⭐⭐⭐⭐ | 高风险博弈 |

### 2. 四季季节识别

- 🌱 **春季（复苏）**: L3 40%, L2 30%
- ☀️ **夏季（繁荣）**: L3 45%, L4 20%
- 🍂 **秋季（滞胀）**: L2 35%, L1 25%
- ❄️ **冬季（衰退）**: L1 40%, L2 35%

### 3. HMM概率检测

替代固定阈值，基于10个宏观指标综合判断：
- GDP、CPI、M2
- 利率、信用利差
- 股市收益、波动率
- 资金流向等

## 🌟 核心优势

| 维度 | 本框架 | 传统60/40 |
|------|--------|----------|
| 动态调整 | ✅ 季节轮动 | ❌ 固定比例 |
| 风险预警 | ✅ HMM+AI | ❌ 无预警 |
| 可解释性 | ✅ 生态学原理 | ✅ 简单 |
| 适合个人 | ✅ 易上手 | ✅ 简单 |

## 📖 文档导航

- 📘 [快速开始](docs/quick-start.md)
- 📗 [框架原理](docs/framework-principles.md)
- 📙 [生态模型](docs/ecosystem-model.md)
- 📕 [HMM季节检测](docs/hmm-season-detector.md)
- 📔 [FAQ](docs/faq.md)
- 📓 [案例研究](docs/case-studies/)

## 🎯 使用场景

- ✅ **个人投资者** - 系统化配置
- ✅ **量化团队** - 模型基础
- ✅ **学术研究** - 复杂系统建模

## 🤝 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📞 社区

- 💬 Discord: [加入讨论](https://discord.gg/your-invite)
- 📧 Email: your-email@example.com

## 📄 许可证

MIT License

## ⚠️ 免责声明

**本框架仅供教育和研究目的，不构成投资建议。**
投资有风险，入市需谨慎。

---

**Star ⭐ us if you find this helpful!**

**Made with ❤️ and 🌿**
