@echo off
chcp 65001 > nul
echo 🎨 SVG图标转换器
echo.

:: 检查Python是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 安装依赖
echo 📦 安装依赖包...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ✅ 依赖安装完成
echo 🚀 开始转换...
echo.

:: 运行转换器
python convert.py

echo.
echo 转换完成，按任意键退出...
pause > nul 