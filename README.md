# 道德经多版本对照学习平台

[![Tests](https://github.com/yourusername/daodejing/actions/workflows/ci-test.yml/badge.svg)](https://github.com/yourusername/daodejing/actions/workflows/ci-test.yml)
[![Coverage](https://codecov.io/gh/yourusername/daodejing/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/daodejing)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

《道德经》多版本对照学习研究平台。支持王弼注、河上公注、王夫之《老子衍》、憨山德清注、马王堆帛书、郭店楚简、D.C. Lau / Henricks / Addiss & Lombardo 英文译本、白话译文等多版本并列阅读。

## ✨ 核心功能

- 📚 **多版本对照**: 原文、注释、英译并列展示
- 🏛️ **古籍版本**: 马王堆帛书本、郭店楚简本
- 📝 **疑难字标注**: 自动注音和释义
- 🔊 **TTS朗读**: Fish Audio 和 Edge TTS 支持
- 🤖 **AI功能**: 知识图谱、语义考古、跨文明对话、虚拟注释家
- 🌙 **暗黑模式**: 支持深色主题
- 📱 **响应式设计**: 完美适配移动端
- ⚡ **快速部署**: 支持 Vercel 和静态站点

## 🚀 快速开始

### 在线演示

访问 [https://your-domain.vercel.app](https://your-domain.vercel.app)

### 本地运行

```bash
# 克隆项目
git clone https://github.com/yourusername/daodejing.git
cd daodejing

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python app.py

# 访问 http://localhost:5000
```

## 📖 文档

- [用户指南](./docs/user-guide.md) - 详细功能说明
- [架构设计](./docs/architecture.md) - 系统架构文档
- [API文档](./docs/openapi.yaml) - OpenAPI/Swagger 规范
- [部署指南](./DEPLOYMENT.md) - 部署说明
- [开发规范](./CLAUDE.md) - 开发指南

## 🧪 开发

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 带覆盖率报告
pytest tests/ --cov=services --cov-report=term-missing

# 运行特定测试
pytest tests/test_services.py -v -k "test_data"
```

### 代码质量

```bash
# 运行所有质量检查
python scripts/check_code_quality.py

# 单独检查
flake8 --config=.flake8 .
mypy --config-file=mypy.ini services/ routes/ utils/
black --check .
isort --check-only .

# 自动格式化
black .
isort .
```

### 预提交钩子

```bash
# 安装 pre-commit
pip install pre-commit
pre-commit install

# 手动运行
pre-commit run --all-files
```

## 🏗️ 项目结构

```
dev/
├── app.py                    # Flask 应用入口
├── config.py                 # 应用配置
├── requirements.txt          # 生产依赖
├── requirements-dev.txt      # 开发依赖
├── services/                 # 业务逻辑层
│   ├── data_service.py       # 数据服务
│   ├── annotation_service.py # 疑难字标注
│   ├── tts_service.py        # TTS 服务
│   ├── knowledge_graph.py    # 知识图谱
│   ├── semantic_archaeology.py      # 语义考古
│   ├── cross_civilization_dialogue.py  # 跨文明对话
│   └── virtual_commentator.py       # 虚拟注释家
├── routes/                   # 路由层
│   ├── page_routes.py        # 页面路由
│   └── api_routes.py         # API 路由
├── utils/                    # 工具层
│   ├── validators.py         # 输入验证
│   ├── security.py           # 安全相关
│   └── cache.py              # 缓存工具
├── data/                     # 数据文件
│   ├── daodejing.json        # 道德经数据
│   ├── classics.json         # 经典配置
│   └── commentators.json     # 注释家数据
├── templates/                # Jinja2 模板
├── static/                   # 静态资源
├── tests/                    # 测试文件
├── docs/                     # 文档
│   ├── openapi.yaml          # API 规范
│   ├── architecture.md       # 架构文档
│   └── user-guide.md         # 用户指南
└── scripts/                  # 工具脚本
    ├── check_code_quality.py # 代码质量检查
    └── deploy_helper.py      # 部署助手
```

## 🌐 API

完整的 API 文档可在本地启动后访问 `/docs`。

### 主要端点

```
GET  /api/classics              # 获取所有经典列表
GET  /api/{classic_id}/chapters # 获取章节列表
GET  /api/{classic_id}/chapter/{id}  # 获取单章数据
GET  /api/{classic_id}/search   # 搜索章节
POST /api/tts/fish-audio        # Fish Audio TTS
POST /api/tts/edge              # Edge TTS
```

## 🚀 部署

### Vercel 部署

```bash
# 一键部署到 Vercel
vercel --prod
```

### 静态站点

```bash
# 生成静态站点
python generate_static.py

# 部署 dist/ 目录到任意静态托管
```

详细部署说明请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)。

## 📊 测试覆盖

```
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
services/__init__.py                        0      0   100%
services/annotation_service.py             45      3    93%
services/classic_service.py               128      8    94%
services/cross_civilization_dialogue.py   156     12    92%
services/knowledge_graph.py               234     15    94%
services/semantic_archaeology.py          178     14    92%
services/virtual_commentator.py           189     13    93%
services/tts_service.py                    98     15    85%
-----------------------------------------------------------
TOTAL                                    1028     80    92%
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献指南

- 遵循 PEP 8 代码规范
- 添加适当的测试
- 更新相关文档
- 通过所有质量检查

更多信息请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 文本数据来源：公开古籍数字化项目
- 英文翻译：D.C. Lau、Henricks、Addiss & Lombardo
- 注释版本：历代学者研究成果

## 📞 联系

- 项目主页：[https://github.com/yourusername/daodejing](https://github.com/yourusername/daodejing)
- 问题反馈：[Issues](https://github.com/yourusername/daodejing/issues)
- 邮件：support@your-domain.com

---

Made with ❤️ and ☯️
