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

:: 提供选择菜单
echo.
echo 请选择操作:
echo [1] 直接转换 (推荐)
echo [2] 先质量诊断，再转换
echo [3] 仅质量诊断
echo.
set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" goto convert
if "%choice%"=="2" goto check_then_convert  
if "%choice%"=="3" goto check_only
goto convert

:check_only
echo.
echo 🔍 开始质量诊断...
python quality_check.py
goto end

:check_then_convert
echo.
echo 🔍 开始质量诊断...
python quality_check.py
echo.
echo 按任意键继续转换...
pause > nul
echo.
echo 🚀 开始转换...
python convert.py
goto end

:convert
echo 🚀 开始转换...
python convert.py
goto end

:end
echo.
echo 操作完成，按任意键退出...
pause > nul 