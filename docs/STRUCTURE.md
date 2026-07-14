# 项目结构

```
financial-ecology/
├── README.md                    # 项目首页
├── LICENSE                      # MIT许可证
├── CONTRIBUTING.md              # 贡献指南
├── requirements.txt             # Python依赖
├── setup.sh                     # 安装脚本
├── docs/                        # 文档目录
│   ├── INDEX.md                 # 📚 文档导航
│   ├── framework-principles.md  # 框架原理
│   ├── ecosystem-model.md       # 优化的生态模型
│   ├── season-identification.md # 季节识别指南
│   ├── multi-agent-execution.md # 多智能体执行层
│   ├── hmm-season-detector.md   # HMM季节检测模型
│   ├── visualization.md         # 风险可视化工具
│   ├── allocation-decision.md   # 配置决策手册
│   ├── quick-start.md           # 快速开始
│   ├── faq.md                   # 常见问题
│   └── case-studies/            # 案例研究
│       ├── 2008-financial-crisis.md
│       └── 2020-covid-crisis.md
├── src/                         # 核心代码
│   ├── __init__.py
│   ├── ecosystem/               # 生态模型模块
│   │   ├── __init__.py
│   │   └── asset_classifier.py  # 资产生态分类器
│   ├── hmm_detector/            # HMM季节检测
│   │   ├── __init__.py
│   │   └── season_hmm.py        # HMM模型实现
│   ├── agents/                  # 多智能体系统
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── fundamental_analyst.py
│   │   ├── sentiment_analyst.py
│   │   ├── technical_analyst.py
│   │   ├── risk_manager.py
│   │   ├── executor.py
│   │   └── portfolio_manager.py
│   └── visualization/            # 可视化工具
│       ├── __init__.py
│       └── risk_visualizer.py   # 风险可视化器
├── tools/                       # 工具脚本
│   ├── allocation-calculator/   # 配置计算器
│   │   └── allocation_calculator.py
│   └── season-questionnaire/    # 季节问卷
│       └── questionnaire.py
├── configs/                     # 配置文件
│   └── hmm_config.yaml          # HMM模型配置
├── data/                        # 数据目录
│   ├── sample_configs/          # 示例配置
│   └── historical_data/         # 历史数据
├── notebooks/                   # Jupyter notebook
│   └── tutorials/               # 教程
└── tests/                       # 测试代码
    └── test_*.py
```

## 📁 目录说明

### docs/ - 文档

- **INDEX.md** - 文档导航中心，从这里开始
- **framework-principles.md** - 框架核心理论
- **ecosystem-model.md** - 优化后的生态模型（借鉴Tokenomics-Ecological-Network）
- **multi-agent-execution.md** - 多智能体执行层（借鉴TradingAgents）
- **hmm-season-detector.md** - HMM概率季节检测（借鉴HMM项目）
- **visualization.md** - 风险可视化（借鉴GSRVS）
- **quick-start.md** - 10分钟快速上手
- **faq.md** - 常见问题解答
- **case-studies/** - 历史案例研究

### src/ - 核心代码

#### ecosystem/ - 生态模型

将资产分为5类生态角色：
- 猎物 (Prey)
- 共生体 (Symbiont)
- 价值创造者 (Value Creator)
- 价值型捕食者 (Predator-Value)
- 纯投机捕食者 (Predator-Speculative)

#### hmm_detector/ - HMM季节检测

使用隐马尔可夫模型概率化识别市场季节：
- 支持4个隐藏状态（春夏秋冬）
- 10个可观测宏观指标
- 多市场检测（A股、美股、港股）
- 季节共振分析

#### agents/ - 多智能体系统

6个专业智能体协同决策：
1. **基本面分析师** - 计算ROE、估值分位
2. **情绪/新闻分析师** - 解析气候系统
3. **技术分析师** - 判断入场时机
4. **风控专员** - 监控L4崩塌信号
5. **交易员** - 生成交易指令
6. **组合经理** - 综合决策

#### visualization/ - 可视化工具

GSRVS风格的风险可视化：
- 生态系统网络图
- L4崩塌传导路径
- 资产配置饼图
- 季节概率分布
- 相关性热力图

### tools/ - 实用工具

#### allocation-calculator/ - 配置计算器

命令行工具，快速生成配置方案：
```bash
python tools/allocation-calculator/allocation_calculator.py \
  --season 春季 \
  --risk moderate \
  --capital 1000000
```

#### season-questionnaire/ - 季节问卷

交互式问卷，10个问题判断当前季节：
```bash
python tools/season-questionnaire/questionnaire.py
```

### configs/ - 配置文件

- **hmm_config.yaml** - HMM模型参数配置

### notebooks/ - 教程

Jupyter notebook格式的交互式教程：
- HMM模型训练教程
- 多智能体决策演示
- 风险可视化示例

## 🚀 快速导航

### 我想...

**开始使用**
→ [快速开始](docs/quick-start.md)

**理解框架**
→ [框架原理](docs/framework-principles.md)

**判断季节**
→ [季节识别指南](docs/season-identification.md)

**使用工具**
→ [README](../README.md#🛠️-工具)

**查看案例**
→ [案例研究](docs/case-studies/)

**贡献代码**
→ [贡献指南](CONTRIBUTING.md)

---

**最后更新**: 2026-07-14
**文档版本**: v1.0.0
