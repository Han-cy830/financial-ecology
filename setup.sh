#!/bin/bash
# 项目安装脚本

set -e

echo "========================================"
echo "金融生态学框架 - 安装脚本"
echo "========================================"
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "检测到Python版本: $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "错误: 需要Python >= 3.8"
    exit 1
fi

echo "✓ Python版本符合要求"
echo ""

# 创建虚拟环境
echo "[1/5] 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ 虚拟环境创建完成"
else
    echo "✓ 虚拟环境已存在"
fi

# 激活虚拟环境
echo ""
echo "[2/5] 激活虚拟环境..."
source venv/bin/activate
echo "✓ 虚拟环境已激活"

# 升级pip
echo ""
echo "[3/5] 升级pip..."
pip install --upgrade pip -q
echo "✓ pip升级完成"

# 安装依赖
echo ""
echo "[4/5] 安装依赖包..."
pip install -r requirements.txt
echo "✓ 依赖包安装完成"

# 安装项目
echo ""
echo "[5/5] 安装项目..."
pip install -e .
echo "✓ 项目安装完成"

echo ""
echo "========================================"
echo "安装完成！"
echo "========================================"
echo ""
echo "使用方式:"
echo "  1. 激活虚拟环境: source venv/bin/activate"
echo "  2. 运行计算器:   python tools/allocation-calculator/allocation_calculator.py --season 春季"
echo "  3. 退出环境:     deactivate"
echo ""
