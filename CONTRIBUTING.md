# 贡献指南

欢迎贡献！我们欢迎各种形式的贡献，包括但不限于：

- 📝 文档改进和翻译
- 🔧 工具开发（Python计算器、可视化工具等）
- 📊 历史案例研究
- 💡 框架优化建议
- 🐛 Bug报告和修复

## 🚀 快速开始

### 1. Fork & Clone

```bash
# Fork本仓库，然后克隆到本地
git clone https://github.com/your-username/financial-ecology.git
cd financial-ecology

# 安装开发环境
./setup.sh
```

### 2. 创建分支

```bash
# 创建功能分支
git checkout -b feature/amazing-feature

# 或者创建bug修复分支
git checkout -b fix/issue-123
```

**分支命名规范**:
- `feature/xxx`: 新功能
- `fix/xxx`: Bug修复
- `docs/xxx`: 文档更新
- `refactor/xxx`: 代码重构

### 3. 开发与测试

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行测试
pytest tests/

# 代码格式化
black src/

# 代码检查
flake8 src/
```

### 4. 提交代码

```bash
# 添加更改
git add .

# 提交（遵循提交信息规范）
git commit -m "feat: 添加新的季节检测算法"

# 推送到你的分支
git push origin feature/amazing-feature
```

**提交信息规范**:
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 5. 创建Pull Request

在GitHub上创建Pull Request，并填写PR模板。

---

## 📝 贡献指南

### 文档贡献

#### 翻译文档

1. 创建翻译分支: `i18n/zh-CN`
2. 翻译对应的Markdown文件
3. 确保格式正确
4. 提交PR时注明: `[i18n] 翻译文档: framework-principles.md`

#### 改进文档

- 修正语法错误
- 补充图表和示例
- 优化排版和可读性
- 添加更多案例研究

### 代码贡献

#### 添加新功能

1. 在`src/`下创建对应模块
2. 编写完整的文档字符串（docstring）
3. 添加单元测试（`tests/`）
4. 更新README和相关文档

#### 修复Bug

1. 在GitHub上创建Issue，描述问题
2. 创建`fix/issue-xxx`分支
3. 修复并提交
4. PR时关联Issue: `Fixes #xxx`

### 案例研究

#### 提交历史案例

1. 格式参考: `docs/case-studies/YYYY-event-name.md`
2. 包含:
   - 事件背景
   - 生态学分析
   - 配置策略
   - 结果对比
   - 关键教训

#### 提交自己使用框架的记录

- 匿名化处理个人信息
- 记录配置决策过程
- 总结效果和经验

---

## 🎯 贡献范围

### 优先级高

- [ ] 多市场HMM模型训练脚本
- [ ] 历史数据下载工具
- [ ] 实时季节检测Web服务
- [ ] 更多历史案例研究

### 优先级中

- [ ] 多智能体决策的可视化
- [ ] 风险评估仪表板
- [ ] 回测框架
- [ ] 移动端适配

### 优先级低

- [ ] 更多AI智能体（宏观分析师、行业分析师等）
- [ ] 智能合约集成（DeFi资产配置）
- [ ] 社交化功能（分享配置方案）

---

## 📋 Pull Request检查清单

在提交PR前，请确保：

- [ ] 代码通过所有测试 (`pytest tests/`)
- [ ] 代码格式化 (`black src/`)
- [ ] 代码无警告 (`flake8 src/`)
- [ ] 添加了新的测试（如适用）
- [ ] 更新了相关文档
- [ ] Commit信息符合规范
- [ ] PR描述清晰说明改动内容

---

## 🤝 行为准则

- 尊重所有参与者
- 接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

---

## 📞 联系方式

- 📧 Email: your-email@example.com
- 💬 Discord: [加入讨论](https://discord.gg/your-invite)
- 🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)

---

**感谢你的贡献！🌿**
