@echo off
REM 古典文献平台 - 一键部署脚本 (Windows)

echo ============================================================
echo 古典文献多版本对照学习平台 - 一键部署
echo ============================================================
echo.

REM 1. 验证数据
echo [1/4] 验证数据完整性...
python verify_data.py
if errorlevel 1 (
    echo.
    echo ✗ 数据验证失败，请检查数据
    pause
    exit /b 1
)
echo.

REM 2. 生成静态文件
echo [2/4] 生成静态站点...
python generate_static.py
if errorlevel 1 (
    echo.
    echo ✗ 静态站点生成失败
    pause
    exit /b 1
)
echo.

REM 3. 运行测试
echo [3/4] 运行测试...
python -m pytest tests/ -q --tb=no
echo.

REM 4. 部署到 Vercel
echo [4/4] 部署到 Vercel...
echo.
echo 请选择部署方式:
echo   1) 预览部署 (测试环境)
echo   2) 生产部署 (正式环境)
echo   3) 跳过 Vercel 部署 (仅生成本地文件)
echo.
set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 正在部署到预览环境...
    vercel --yes
) else if "%choice%"=="2" (
    echo.
    echo 正在部署到生产环境...
    vercel --prod --yes
) else if "%choice%"=="3" (
    echo.
    echo 已跳过 Vercel 部署
    echo 静态文件已生成到 dist/ 目录
) else (
    echo.
    echo 无效选择，已跳过 Vercel 部署
)

echo.
echo ============================================================
echo 部署完成！
echo ============================================================
echo.
echo 静态文件位置：%CD%\dist
echo.
echo 本地测试：cd dist && python -m http.server 8000
echo.
pause
