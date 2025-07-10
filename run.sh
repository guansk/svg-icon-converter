#!/bin/bash

echo "🎨 SVG图标转换器"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到Python3，请先安装Python 3.7+"
    exit 1
fi

# 安装依赖
echo "📦 安装依赖包..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，请检查网络连接"
    exit 1
fi

echo ""
echo "✅ 依赖安装完成"
echo "🚀 开始转换..."
echo ""

# 提供选择菜单
echo ""
echo "请选择操作:"
echo "[1] 直接转换 (推荐)"
echo "[2] 先质量诊断，再转换"
echo "[3] 仅质量诊断"
echo ""
read -p "请输入选择 (1-3): " choice

case $choice in
    2)
        echo ""
        echo "🔍 开始质量诊断..."
        python3 quality_check.py
        echo ""
        read -p "按回车键继续转换..."
        echo ""
        echo "🚀 开始转换..."
        python3 convert.py
        ;;
    3)
        echo ""
        echo "🔍 开始质量诊断..."
        python3 quality_check.py
        ;;
    *)
        echo "🚀 开始转换..."
        python3 convert.py
        ;;
esac

echo ""
echo "操作完成！" 