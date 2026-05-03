# 一键部署命令
# 复制以下命令到 PowerShell 执行

# 设置变量
$RepoPath = "D:\项目文件\daodejing"
$GitHubUsername = "leoxmrsh007"
$GitHubRepo = "daodejing"

Write-Host "🚀 道德经自动部署工具" -ForegroundColor Green
Write-Host "========================================"

# 进入项目目录
Set-Location $RepoPath

# 检查 GitHub CLI
Write-Host "🔍 检查 GitHub CLI..." -ForegroundColor Yellow
$ghPath = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghPath) {
    Write-Host "📦 正在安装 GitHub CLI..." -ForegroundColor Yellow
    winget install --id GitHub.cli --accept-package-agreements --accept-source-agreements
    Write-Host "✅ GitHub CLI 安装完成" -ForegroundColor Green
} else {
    Write-Host "✅ GitHub CLI 已安装" -ForegroundColor Green
}

# 检查 Vercel CLI
Write-Host "🔍 检查 Vercel CLI..." -ForegroundColor Yellow
$vercelPath = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelPath) {
    Write-Host "📦 正在安装 Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
    Write-Host "✅ Vercel CLI 安装完成" -ForegroundColor Green
} else {
    Write-Host "✅ Vercel CLI 已安装" -ForegroundColor Green
}

# 检查 Git 状态并提交
Write-Host "📋 检查 Git 状态..." -ForegroundColor Yellow
$status = git status --porcelain
if ($status) {
    Write-Host "📝 发现未提交的更改，正在提交..." -ForegroundColor Yellow
    git add -A
    $datetime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "deploy: 自动部署到 daodejing0.online - $datetime"
    Write-Host "✅ 代码已提交" -ForegroundColor Green
} else {
    Write-Host "✅ 没有未提交的更改" -ForegroundColor Green
}

# 登录 GitHub
Write-Host "🔐 检查 GitHub 登录状态..." -ForegroundColor Yellow
$ghAuth = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔑 需要登录 GitHub..." -ForegroundColor Yellow
    gh auth login --web
} else {
    Write-Host "✅ GitHub 已登录" -ForegroundColor Green
}

# 推送到 GitHub
Write-Host "📤 推送到 GitHub..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 代码已推送到 GitHub" -ForegroundColor Green
} else {
    Write-Host "❌ 推送失败" -ForegroundColor Red
    Write-Host "请手动运行: git push origin main" -ForegroundColor Yellow
}

# 登录 Vercel
Write-Host "🔐 检查 Vercel 登录状态..." -ForegroundColor Yellow
$vercelAuth = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔑 需要登录 Vercel..." -ForegroundColor Yellow
    vercel login
} else {
    Write-Host "✅ Vercel 已登录" -ForegroundColor Green
}

# 部署到 Vercel
Write-Host "🚀 部署到 Vercel..." -ForegroundColor Yellow
vercel --prod

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 部署成功!" -ForegroundColor Green
} else {
    Write-Host "❌ 部署失败" -ForegroundColor Red
}

# 配置域名
Write-Host "🌐 配置域名 www.daodejing0.online..." -ForegroundColor Yellow
vercel domains add www.daodejing0.online 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 域名配置完成" -ForegroundColor Green
} else {
    Write-Host "⚠️  域名配置可能需要手动完成" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 部署流程完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步:" -ForegroundColor Yellow
Write-Host "1. 在域名提供商添加 DNS 记录:" -ForegroundColor White
Write-Host "   CNAME: www -> cname.vercel-dns.com" -ForegroundColor Cyan
Write-Host "   A: @ -> 76.76.21.21" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. 访问网站:" -ForegroundColor White
Write-Host "   https://www.daodejing0.online" -ForegroundColor Cyan
Write-Host ""
Read-Host "按 Enter 键退出"
