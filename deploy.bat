@echo off
chcp 65001 >nul
:: 道德经自动部署脚本 (Windows)
:: 自动完成Git推送和Vercel部署

echo 🚀 开始自动部署流程...

:: 检查 Git 状态
echo 📋 检查 Git 状态...
for /f "tokens=*" %%a in ('git status --porcelain') do set GIT_STATUS=%%a
if defined GIT_STATUS (
    echo 📝 发现未提交的更改，正在提交...
    git add -A
    for /f "tokens=*" %%a in ('powershell -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'"') do set DATETIME=%%a
    git commit -m "deploy: 自动部署到 daodejing0.online - %DATETIME%"
    echo ✅ 代码已提交
) else (
    echo ✅ 没有未提交的更改
)

:: 推送到 GitHub
echo 📤 推送到 GitHub...
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 推送失败，请检查网络连接或Git配置
    echo 💡 提示: 如果是认证问题，请确保已配置Git凭证
    pause
    exit /b 1
)
echo ✅ 代码已推送到 GitHub

:: 检查 Vercel CLI
echo 🔍 检查 Vercel CLI...
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 📦 安装 Vercel CLI...
    npm install -g vercel
)
echo ✅ Vercel CLI 已就绪

:: 检查 Vercel 登录状态
echo 🔐 检查 Vercel 登录状态...
vercel whoami >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🔑 需要登录 Vercel...
    echo    请在浏览器中完成登录
    vercel login
)
echo ✅ Vercel 已登录

:: 部署到 Vercel
echo 🚀 部署到 Vercel...
vercel --prod
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 部署失败
    pause
    exit /b 1
)
echo ✅ 部署成功!

:: 配置自定义域名
echo 🌐 配置自定义域名: www.daodejing0.online
vercel domains add www.daodejing0.online 2>nul || echo ⚠️ 域名可能已配置或需要手动设置

echo.
echo ========================================
echo 🎉 部署流程完成!
echo ========================================
echo.
echo 下一步操作:
echo 1. 访问 Vercel Dashboard: https://vercel.com/dashboard
echo 2. 在项目设置中添加域名: www.daodejing0.online
echo 3. 在域名提供商处添加 DNS 记录:
echo    - CNAME: www -^> cname.vercel-dns.com
echo    - A: @ -^> 76.76.21.21
echo.
echo 网站地址:
echo    https://www.daodejing0.online
echo.

pause
