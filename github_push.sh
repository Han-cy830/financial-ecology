#!/bin/bash
# GitHub 推送脚本

set -e

echo "========================================"
echo "金融生态学框架 - GitHub推送脚本"
echo "========================================"
echo ""

# 配置Git用户信息
echo "[1/6] 配置Git用户信息..."
git config user.name "Han-cy830"
git config user.email "han-cy830@example.com"
echo "✓ Git配置完成"
echo ""

# 检查Git状态
echo "[2/6] 检查Git状态..."
git status
echo ""

# 添加所有文件
echo "[3/6] 添加文件到暂存区..."
git add .
echo "✓ 文件添加完成"
echo ""

# 提交
echo "[4/6] 提交更改..."
git commit -m "feat: 金融生态学框架v1.0 - 基于生态学原理的智能资产配置系统

- 实现L1-L5五层资产配置体系
- 集成HMM概率季节检测模型
- 多智能体协同决策系统
- GSRVS风格风险可视化
- 完整的文档和工具集"
echo "✓ 提交完成"
echo ""

# 设置主分支
echo "[5/6] 设置主分支..."
git branch -M main
echo "✓ 主分支设置完成"
echo ""

# 检查远程仓库
echo "[6/6] 检查远程仓库配置..."
if git remote get-url origin > /dev/null 2>&1; then
    echo "远程仓库已配置:"
    git remote -v
else
    echo "⚠️  远程仓库未配置"
    echo ""
    echo "请选择推送方式:"
    echo ""
    echo "方式A: HTTPS (推荐)"
    echo "  git remote add origin https://github.com/Han-cy830/financial-ecology.git"
    echo ""
    echo "方式B: SSH (如果配置了SSH密钥)"
    echo "  git remote add origin git@github.com:Han-cy830/financial-ecology.git"
    echo ""
    echo "然后运行:"
    echo "  git push -u origin main"
fi

echo ""
echo "========================================"
echo "Git配置完成！"
echo "========================================"
echo ""
echo "下一步:"
echo "  1. 在GitHub创建仓库: https://github.com/new"
echo "  2. 仓库名: financial-ecology"
echo "  3. 添加远程仓库: git remote add origin <仓库地址>"
echo "  4. 推送: git push -u origin main"
echo ""
