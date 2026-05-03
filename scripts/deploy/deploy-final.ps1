# 道德经 - 完整部署执行脚本
# 请将此脚本保存为 deploy-manual.ps1 并在 PowerShell 中运行

param(
    [string]$GitHubToken = "",  # 可选：GitHub Personal Access Token
    [switch]$SkipGitPush = $false,
    [switch]$SkipVercelDeploy = $false
)

# 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force -ErrorAction SilentlyContinue

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 道德经部署到 daodejing0.online" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ProjectPath = "D:\项目文件\daodejing"
Set-Location $ProjectPath

# 检查 Git 状态
Write-Host "📋 步骤 1/5: 检查 Git 状态..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "📝 发现未提交的更改，正在提交..." -ForegroundColor Yellow
    git add -A
    $datetime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    git commit -m "deploy: 部署到 daodejing0.online - $datetime"
    Write-Host "✅ 代码已提交" -ForegroundColor Green
} else {
    Write-Host "✅ 没有未提交的更改" -ForegroundColor Green
}

# 推送代码到 GitHub
if (-not $SkipGitPush) {
    Write-Host ""
    Write-Host "📤 步骤 2/5: 推送代码到 GitHub..." -ForegroundColor Yellow
    
    # 尝试直接推送
    git push origin main 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 代码已成功推送到 GitHub" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Git 推送需要认证" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "请选择以下方式之一完成推送：" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "方法 A: 使用 GitHub CLI（推荐）" -ForegroundColor White
        Write-Host "   1. 安装 GitHub CLI: winget install --id GitHub.cli" -ForegroundColor Gray
        Write-Host "   2. 登录: gh auth login" -ForegroundColor Gray
        Write-Host "   3. 重新运行此脚本" -ForegroundColor Gray
        Write-Host ""
        Write-Host "方法 B: 使用 HTTPS + Token" -ForegroundColor White
        Write-Host "   1. 生成 Token: https://github.com/settings/tokens" -ForegroundColor Gray
        Write-Host "   2. 运行: git remote set-url origin https://USERNAME:TOKEN@github.com/leoxmrsh007/daodejing.git" -ForegroundColor Gray
        Write-Host "   3. 重新推送: git push origin main" -ForegroundColor Gray
        Write-Host ""
        Write-Host "方法 C: 使用 SSH" -ForegroundColor White
        Write-Host "   1. 生成 SSH Key: ssh-keygen -t ed25519 -C 'your@email.com'" -ForegroundColor Gray
        Write-Host "   2. 添加公钥到 GitHub: https://github.com/settings/keys" -ForegroundColor Gray
        Write-Host "   3. 切换远程 URL: git remote set-url origin git@github.com:leoxmrsh007/daodejing.git" -ForegroundColor Gray
        Write-Host ""
        
        $continue = Read-Host "是否继续 Vercel 部署？(y/n)"
        if ($continue -ne 'y') {
            exit 1
        }
    }
} else {
    Write-Host "⏭️  跳过 Git 推送" -ForegroundColor Gray
}

# 检查 Vercel CLI
Write-Host ""
Write-Host "🔍 步骤 3/5: 检查 Vercel CLI..." -ForegroundColor Yellow
$vercelPath = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelPath) {
    Write-Host "📦 Vercel CLI 未安装，正在安装..." -ForegroundColor Yellow
    npm install -g vercel
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Vercel CLI 安装失败" -ForegroundColor Red
        Write-Host "请手动运行: npm install -g vercel" -ForegroundColor Yellow
        exit 1
    }
}
Write-Host "✅ Vercel CLI 已就绪" -ForegroundColor Green

# 检查 Vercel 登录
Write-Host ""
Write-Host "🔐 步骤 4/5: 检查 Vercel 登录状态..." -ForegroundColor Yellow
try {
    $vercelUser = vercel whoami 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 已登录 Vercel: $vercelUser" -ForegroundColor Green
    } else {
        throw "Not logged in"
    }
} catch {
    Write-Host "🔑 需要登录 Vercel..." -ForegroundColor Yellow
    Write-Host "   请在浏览器中完成登录授权" -ForegroundColor Gray
    vercel login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Vercel 登录失败" -ForegroundColor Red
        exit 1
    }
}

# 部署到 Vercel
if (-not $SkipVercelDeploy) {
    Write-Host ""
    Write-Host "🚀 步骤 5/5: 部署到 Vercel 生产环境..." -ForegroundColor Yellow
    Write-Host "   项目: leoxmrsh007/daodejing" -ForegroundColor Gray
    Write-Host "   域名: www.daodejing0.online" -ForegroundColor Gray
    Write-Host ""
    
    vercel --prod --confirm
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Vercel 部署成功!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "❌ Vercel 部署失败" -ForegroundColor Red
        Write-Host "请检查错误信息并修复后重试" -ForegroundColor Yellow
        exit 1
    }
    
    # 配置域名
    Write-Host ""
    Write-Host "🌐 配置自定义域名..." -ForegroundColor Yellow
    vercel domains add www.daodejing0.online 2>&1 | Out-Null
    Write-Host "✅ 域名配置完成" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "⏭️  跳过 Vercel 部署" -ForegroundColor Gray
}

# 输出完成信息
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "🎉 部署流程完成!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 部署状态:" -ForegroundColor Cyan
Write-Host "   项目仓库: https://github.com/leoxmrsh007/daodejing" -ForegroundColor White
Write-Host "   网站地址: https://www.daodejing0.online" -ForegroundColor White
Write-Host ""
Write-Host "⚙️  DNS 配置检查:" -ForegroundColor Cyan
Write-Host "   请在阿里云确认以下记录:" -ForegroundColor White
Write-Host "   - CNAME: www -> cname.vercel-dns.com" -ForegroundColor Gray
Write-Host "   - A: @ -> 76.76.21.21" -ForegroundColor Gray
Write-Host ""
Write-Host "🔄 后续更新:" -ForegroundColor Cyan
Write-Host "   修改代码后，运行以下命令部署:" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor Gray
Write-Host "   或重新运行此脚本" -ForegroundColor Gray
Write-Host ""

# 验证部署
try {
    Write-Host "🌐 正在验证网站可访问性..." -ForegroundColor Yellow -NoNewline
    Start-Sleep -Seconds 2
    $response = Invoke-WebRequest -Uri "https://www.daodejing0.online" -TimeoutSec 10 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host " ✅ 网站可正常访问!" -ForegroundColor Green
    } else {
        Write-Host " ⚠️  网站状态: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host " ⚠️  暂时无法访问（DNS 可能需要几分钟生效）" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "按 Enter 键退出"
