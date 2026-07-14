#!/bin/bash
# 创建 GitHub Release 脚本

set -e

echo "========================================"
echo "金融生态学框架 - 创建 Release v1.0.0"
echo "========================================"
echo ""

# 检查是否已安装 gh
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI 未安装"
    exit 1
fi

# 检查是否已登录
if ! gh auth status &> /dev/null; then
    echo "❌ 请先登录 GitHub CLI: gh auth login"
    exit 1
fi

# 检查 Release Notes 文件是否存在
if [ ! -f "RELEASE_NOTES_v1.0.0.md" ]; then
    echo "❌ Release Notes 文件不存在"
    exit 1
fi

echo "[1/3] 创建 Git tag..."
git tag -a v1.0.0 -m "Release version 1.0.0 - 金融生态学框架正式发布"
echo "✓ Tag 创建完成"
echo ""

echo "[2/3] 推送 tag 到 GitHub..."
git push origin v1.0.0
echo "✓ Tag 推送完成"
echo ""

echo "[3/3] 创建 GitHub Release..."
gh release create v1.0.0 \
  --title "v1.0.0 - 🌿 金融生态学框架正式发布" \
  --notes-file RELEASE_NOTES_v1.0.0.md \
  --latest

echo ""
echo "========================================"
echo "✓ Release 创建完成！"
echo "========================================"
echo ""
echo "访问地址:"
echo "  https://github.com/Han-cy830/financial-ecology/releases/tag/v1.0.0"
echo ""
