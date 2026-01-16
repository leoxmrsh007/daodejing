# 部署文档

本文档描述道德经多版本对照平台的部署方案，适用于 Flask + 静态站点双模式部署的项目。

## 目录

- [部署架构](#部署架构)
- [方案一：Vercel 动态部署](#方案一vercel-动态部署)
- [方案二：静态站点部署](#方案二静态站点部署)
- [方案三：混合部署](#方案三混合部署)
- [域名配置](#域名配置)
- [环境变量](#环境变量)
- [故障排查](#故障排查)

---

## 部署架构

```
                    ┌─────────────────────────────────────┐
                    │          用户访问请求                │
                    └─────────────────┬───────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                    ┌────▼─────┐             ┌────▼─────┐
                    │  Vercel  │             │  静态托管  │
                    │  (API)   │             │ (HTML/JS) │
                    └────┬─────┘             └────┬─────┘
                         │                         │
                    ┌────▼─────┐             ┌────▼─────┐
                    │  Flask   │             │  静态文件  │
                    │  app.py  │             │  dist/    │
                    └──────────┘             └──────────┘
```

### 双模式对比

| 特性 | Vercel 动态部署 | 静态站点部署 |
|------|----------------|-------------|
| API 支持 | ✓ 搜索、TTS 代理 | ✗ 仅前端功能 |
| 部署复杂度 | 简单 (Git 推送) | 简单 (上传文件) |
| 运行成本 | Vercel 免费额度 | 完全免费 |
| 响应速度 | 服务器渲染 | 极快 (CDN) |
| 适用场景 | 需要后端功能 | 纯阅读展示 |

---

## 方案一：Vercel 动态部署

适用于需要搜索功能、TTS 代理等 API 功能的场景。

### 1.1 前置要求

- [x] GitHub 账号
- [x] Vercel 账号 (可用 GitHub 登录)
- [x] Python 3.9+ 环境

### 1.2 项目结构

```
daodejing/
├── app.py              # Flask 应用入口
├── requirements.txt    # Python 依赖
├── vercel.json         # Vercel 配置
├── data/               # 数据文件
├── static/             # 静态资源
└── templates/          # 模板文件
```

### 1.3 配置文件

**vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/app.py/api/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/app.py"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600"
        }
      ]
    },
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

**requirements.txt**
```
flask>=2.3.0
cors>=1.0.1
requests>=2.31.0
```

### 1.4 部署步骤

#### 方法 A：通过 Vercel CLI

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
vercel prod

# 设置生产环境域名
vercel alias set <deployment-url> daodejing.vercel.app
```

#### 方法 B：通过 GitHub 自动部署

1. 将代码推送到 GitHub 仓库
2. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
3. 点击 "Add New Project"
4. 导入 GitHub 仓库
5. 配置项目：
   - **Framework Preset**: Other
   - **Build Command**: 留空
   - **Output Directory**: `./`
6. 点击 "Deploy"

### 1.5 环境变量（可选）

在 Vercel Dashboard 设置以下环境变量：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_ENV` | 运行环境 | `production` |
| `PYTHON_VERSION` | Python 版本 | `3.9` |

---

## 方案二：静态站点部署

适用于纯阅读展示场景，无需后端 API。

### 2.1 生成静态文件

```bash
# 进入项目目录
cd daodejing

# 生成静态站点
python generate_static.py
```

生成的文件结构：
```
dist/
├── index.html              # 首页
├── all-chapters.html       # 全章节列表
├── chapter1.html          # 第1章
├── chapter2.html          # 第2章
├── ...
├── chapter81.html         # 第81章
└── assets/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── audio/
        └── gaoshanliushui.mp3
```

### 2.2 部署选项

#### 选项 A：Vercel 静态部署

**vercel.json** (静态版本)
```json
{
  "version": 2,
  "public": true,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/dist/$1"
    }
  ]
}
```

部署步骤同方案一，只需确保 `dist/` 目录已提交到仓库。

#### 选项 B：GitHub Pages

```bash
# 切换到 gh-pages 分支
git checkout -b gh-pages

# 复制 dist/ 内容到根目录
cp -r dist/* .

# 提交并推送
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
```

然后在 GitHub 仓库设置中：
1. Settings > Pages
2. Source 选择 `gh-pages` 分支
3. 保存后访问 `https://username.github.io/daodejing/`

#### 选项 C：Netlify

1. 登录 [Netlify Drop](https://app.netlify.com/drop)
2. 拖拽 `dist/` 目录到页面
3. 部署完成，获得 `https://random-name.netlify.app`

#### 选项 D：传统服务器

```bash
# 上传到服务器
scp -r dist/* user@server:/var/www/daodejing/

# Nginx 配置示例
server {
    listen 80;
    server_name daodejing.example.com;
    root /var/www/daodejing;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(css|js|mp3)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 方案三：混合部署

结合两种方案的优势：静态文件托管到 CDN，API 部署到 Vercel。

### 3.1 架构

```
┌─────────────────────────────────────────────────────┐
│                    用户访问                          │
└─────────────────────┬───────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
    ┌────▼─────┐             ┌────▼─────┐
    │  静态CDN  │             │ Vercel   │
    │  (HTML)  │             │  (API)   │
    └──────────┘             └────┬─────┘
                                   │
                              ┌────▼─────┐
                              │  Flask   │
                              │  app.py  │
                              └──────────┘
```

### 3.2 配置

**前端配置** (static/js/main.js)
```javascript
const API_BASE_URL = 'https://daodejing-api.vercel.app/api';

const SearchManager = {
    API_ENDPOINT: `${API_BASE_URL}/daodejing/search`,
    // ...
};
```

**CORS 配置** (app.py)
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://daodejing.netlify.app"],
        "methods": ["GET", "POST"]
    }
})
```

---

## 域名配置

### Vercel 自定义域名

1. 在 Vercel Dashboard 进入项目设置
2. Domains > Add Domain
3. 输入域名（如 `daodejing.example.com`）
4. 配置 DNS 记录：

| 类型 | 名称 | 值 |
|------|------|-----|
| CNAME | www | cname.vercel-dns.com |
| A | @ | 76.76.21.21 |

### DNS 配置示例

```
# 云解析 DNS
daodejing.example.com    CNAME  cname.vercel-dns.com
www.daodejing.example.com CNAME  cname.vercel-dns.com
```

---

## 环境变量

### 开发环境

```bash
# .env (本地开发)
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
```

### 生产环境

在 Vercel Dashboard 设置：

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `FLASK_ENV` | 运行环境 | `production` |
| `SECRET_KEY` | Flask 密钥 | 随机字符串 |

生成密钥：
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 故障排查

### 常见问题

#### 1. Vercel 部署后 404

**原因**: 路由配置错误

**解决**: 检查 `vercel.json` 中的 `rewrites` 配置

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/app.py"
    }
  ]
}
```

#### 2. 静态文件无法加载

**原因**: 路径错误或文件未复制

**解决**: 检查 `generate_static.py` 中的资源复制逻辑

```python
def copy_assets():
    dist_static = output_dir / "assets"
    dist_static.mkdir(exist_ok=True)

    # 复制 CSS
    shutil.copytree("static/css", dist_static / "css", dirs_exist_ok=True)
    # 复制 JS
    shutil.copytree("static/js", dist_static / "js", dirs_exist_ok=True)
```

#### 3. API 跨域错误

**原因**: CORS 未正确配置

**解决**:
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

#### 4. Vercel 构建超时

**原因**: 数据文件过大或构建时间过长

**解决**: 将大文件移至外部存储，或使用静态部署

---

## 更新部署

### 自动部署 (Git Push)

```bash
# 修改代码后直接推送
git add .
git commit -m "Update content"
git push origin main

# Vercel 自动触发部署
```

### 手动部署

```bash
# Vercel CLI
vercel --prod

# Netlify (静态)
netlify deploy --prod --dir=dist
```

---

## 监控和日志

### Vercel Dashboard

- 访问 [Vercel Dashboard](https://vercel.com/dashboard)
- 查看部署日志、访问统计、错误追踪

### 日志查看

```bash
# Vercel CLI 查看日志
vercel logs <deployment-url>

# 实时日志
vercel logs <deployment-url> --follow
```

---

## 成本估算

| 方案 | 月成本 | 流量限制 |
|------|--------|----------|
| Vercel 免费版 | $0 | 100GB 带宽 |
| Vercel Pro | $20/月 | 1TB 带程 |
| 静态托管 | $0 | 无限制 |

对于中小型阅读网站，免费版完全足够。

---

## 参考资料

- [Vercel Python 部署文档](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Flask 部署最佳实践](https://flask.palletsprojects.com/en/latest/deploying/)
- [静态站点生成器指南](https://www.staticgen.com/)
