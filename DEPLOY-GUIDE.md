# 道德经部署到 daodejing0.online 完整指南

## 快速部署步骤

### 第 1 步：推送到 GitHub

由于 GitHub 已停止支持密码认证，请使用以下方法之一推送代码：

#### 方法 A：使用 GitHub CLI（推荐）

```bash
# 1. 安装 GitHub CLI
# Windows: winget install --id GitHub.cli
# macOS: brew install gh
# Linux: 参见 https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# 2. 登录 GitHub
gh auth login
# 选择 HTTPS，然后使用浏览器登录

# 3. 推送代码
gh repo sync
```

#### 方法 B：手动推送

1. 打开项目文件夹 `D:\项目文件\daodejing`
2. 右键 → Git Bash Here（或打开命令行）
3. 运行：
```bash
git push origin main
```
4. 如果提示输入密码，请输入 Personal Access Token

### 第 2 步：Vercel 部署

#### 方法 A：使用自动部署脚本

**Windows:**
```bash
deploy.bat
```

**macOS/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh
```

#### 方法 B：手动部署

1. 访问 https://vercel.com/dashboard
2. 点击 "Add New Project"
3. 导入 `leoxmrsh007/daodejing` 仓库
4. 保持默认设置，点击 "Deploy"
5. 部署完成后，点击 "Continue to Dashboard"

### 第 3 步：配置自定义域名

1. 在 Vercel Dashboard 进入项目
2. 点击 **Settings** → **Domains**
3. 点击 **Add Domain**
4. 输入 `www.daodejing0.online`
5. 点击 **Add**

### 第 4 步：DNS 配置（在域名提供商处）

登录你的域名提供商（如阿里云、腾讯云、Cloudflare），添加以下记录：

| 记录类型 | 主机记录 | 记录值 |
|---------|---------|--------|
| CNAME | www | cname.vercel-dns.com |
| A | @ | 76.76.21.21 |

**常见域名提供商操作：**

- **阿里云**: 登录 → 域名 → 解析 → 添加记录
- **腾讯云**: 登录 → DNS 解析 → 添加记录
- **Cloudflare**: 登录 → 域名 → DNS → 添加记录

### 第 5 步：验证部署

1. 等待 DNS 生效（通常 5-30 分钟）
2. 访问 https://www.daodejing0.online
3. 确认网站正常显示

---

## 配置检查清单

### GitHub 配置 ✅
- [ ] 代码已推送到 main 分支
- [ ] 包含所有必要文件：
  - `app.py`
  - `api/index.py`
  - `vercel.json`
  - `requirements.txt`
  - `data/daodejing.json`
  - `static/` 目录
  - `templates/` 目录

### Vercel 配置 ✅
- [ ] 项目已导入 Vercel
- [ ] 构建成功
- [ ] 域名 `www.daodejing0.online` 已添加

### 域名配置 ✅
- [ ] CNAME 记录: www → cname.vercel-dns.com
- [ ] A 记录: @ → 76.76.21.21
- [ ] DNS 已生效

---

## 故障排查

### 问题 1：Git 推送失败

**症状**: `fatal: Authentication failed`

**解决**:
1. 生成新的 Personal Access Token: https://github.com/settings/tokens
2. 使用 GitHub CLI: `gh auth login`
3. 或更新远程 URL: `git remote set-url origin https://用户名:token@github.com/leoxmrsh007/daodejing.git`

### 问题 2：Vercel 构建失败

**症状**: 部署日志显示错误

**解决**:
1. 检查 `requirements.txt` 是否包含所有依赖
2. 检查 `api/index.py` 路径是否正确
3. 查看 Vercel 部署日志获取详细错误

### 问题 3：域名无法访问

**症状**: 浏览器显示 "无法访问此网站"

**解决**:
1. 检查 DNS 记录是否正确
2. 等待 DNS 传播（最长 48 小时）
3. 使用 `nslookup www.daodejing0.online` 检查解析
4. 在 Vercel Dashboard 检查域名状态

### 问题 4：静态文件加载失败

**症状**: 页面样式丢失，JS 不工作

**解决**:
1. 检查 `vercel.json` 中的静态文件路由
2. 确保 `static/` 目录已提交到 Git
3. 检查浏览器控制台错误

---

## 项目文件结构

```
daodejing/
├── api/
│   └── index.py              # Vercel 入口点 ✅
├── app.py                     # Flask 应用 ✅
├── config.py                  # 配置文件 ✅
├── vercel.json               # Vercel 配置 ✅
├── requirements.txt          # Python 依赖 ✅
├── data/
│   └── daodejing.json        # 道德经数据 ✅
├── static/                   # 静态资源 ✅
│   ├── css/
│   ├── js/
│   └── audio/
├── templates/                # HTML 模板 ✅
│   └── ddj/
├── services/                 # 业务逻辑 ✅
├── routes/                   # 路由 ✅
├── deploy.sh                 # Linux/macOS 部署脚本 ✅
└── deploy.bat                # Windows 部署脚本 ✅
```

---

## 自动部署脚本使用说明

### Windows (deploy.bat)

```bash
# 双击运行，或在命令行执行:
deploy.bat
```

### macOS/Linux (deploy.sh)

```bash
# 赋予执行权限
chmod +x deploy.sh

# 运行
./deploy.sh
```

脚本会自动：
1. 检查并提交未保存的更改
2. 推送到 GitHub
3. 检查并安装 Vercel CLI
4. 登录 Vercel（如未登录）
5. 部署到生产环境
6. 配置自定义域名

---

## 更新部署

后续更新网站时，只需：

```bash
# 修改代码后
git add .
git commit -m "更新内容"
git push origin main

# 如果使用 Vercel Git 集成，会自动部署
# 如果使用 CLI，运行:
vercel --prod
```

---

## 联系支持

如遇到问题：
- Vercel 文档: https://vercel.com/docs
- GitHub 文档: https://docs.github.com
- Flask 文档: https://flask.palletsprojects.com

---

**部署日期**: 2026-02-14  
**目标域名**: https://www.daodejing0.online  
**GitHub 仓库**: https://github.com/leoxmrsh007/daodejing
