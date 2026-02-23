# 古典文献多版本对照学习平台 - 部署指南

## 📦 部署方式

本项目支持两种部署方式：
1. **Vercel 动态部署** - 支持完整 API 功能（搜索、TTS、AI 功能）
2. **静态站点部署** - 纯 HTML/CSS/JS，可部署到任何静态托管

---

## 🚀 方式一：Vercel 动态部署（推荐）

### 前置准备

1. 安装 Vercel CLI：
```bash
npm install -g vercel
```

2. 登录 Vercel：
```bash
vercel login
```

### 一键部署

```bash
# 1. 生成静态文件
python generate_static.py

# 2. 部署到 Vercel
vercel --prod
```

### 环境变量（可选）

如需启用 TTS 功能，设置以下环境变量：
```bash
# Fish Audio API 密钥
FISH_AUDIO_API_KEY=your_api_key_here

# 密钥（用于 JWT）
SECRET_KEY=your-secret-key-here
```

---

## 🌐 方式二：静态站点部署

### 生成静态文件

```bash
python generate_static.py
```

输出目录：`dist/`

### 部署到 GitHub Pages

```bash
# 1. 初始化 git（如果还没有）
git init
git add .
git commit -m "Deploy static site"

# 2. 推送 dist 目录到 gh-pages 分支
git subtree push --prefix dist origin gh-pages
```

访问：`https://yourusername.github.io/your-repo/`

### 部署到 Netlify

1. 登录 [Netlify](https://netlify.com)
2. 拖拽 `dist/` 文件夹到 Netlify
3. 或连接 GitHub 仓库自动部署

### 部署到阿里云 OSS

```bash
# 使用 ossutil 工具
ossutil cp -r dist oss://your-bucket-name/ --recursive
```

### 部署到腾讯云 COS

```bash
# 使用 coscmd 工具
coscmd upload -r dist/ /
```

---

## 🔧 本地测试

### 测试静态站点

```bash
# 使用 Python 内置服务器
cd dist
python -m http.server 8000

# 访问 http://localhost:8000
```

### 测试 Flask 应用

```bash
# 启动开发服务器
python app.py

# 访问 http://localhost:5000
```

---

## 📊 部署验证清单

部署后请验证以下功能：

- [ ] 首页正常加载
- [ ] 9 部经典列表显示
- [ ] 道德经章节页面正常
- [ ] 庄子章节页面正常
- [ ] 周易卦辞显示正常
- [ ] 黄帝内经章节正常
- [ ] 金刚经译文显示
- [ ] 暗黑模式切换正常
- [ ] 移动端响应式正常
- [ ] 搜索功能（如有 API）

---

## 🎯 性能优化建议

### CDN 配置

对于静态资源（CSS/JS/图片），建议配置 CDN：

```
Cache-Control: public, max-age=31536000, immutable
```

### Gzip 压缩

启用 Gzip 压缩可减少 70% 传输体积：

```nginx
gzip on;
gzip_types text/css application/javascript image/svg+xml;
```

---

## 📝 故障排查

### 页面 404

检查 `vercel.json` 重写规则是否正确。

### 样式丢失

确认 `dist/assets/` 目录已正确复制。

### API 不可用

确保 Flask 应用已正确部署，检查环境变量。

---

## 📞 技术支持

如有问题，请提交 Issue 或联系开发团队。

---

**最后更新**: 2026 年 2 月 23 日
**版本**: 2.0.0
