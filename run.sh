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

# 运行转换器
python3 convert.py

echo ""
echo "转换完成！" 