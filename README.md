# 道德经多版本对照学习研究平台

> Digital Humanities meets Classical Chinese Philosophy

[![GitHub Stars](https://img.shields.io/github/stars/leoxmrsh007/daodejing?style=social)](https://github.com/leoxmrsh007/daodejing)
[![Test Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)](https://github.com/leoxmrsh007/daodejing)
[![Commits](https://img.shields.io/badge/commits-128%2B-blue)](https://github.com/leoxmrsh007/daodejing/commits/main)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌟 在线演示

**[→ 访问 daodejing.vercel.app](https://daodejing.vercel.app)**

> 暂无域名？可使用 Vercel 分配的临时域名，或部署到自己的 Vercel 账户

---

## 📖 项目愿景

### 为什么做这个项目？

作为一名研究 AI 哲学与 AI 伦理的哲学博士，我一直在思考一个问题：

**当 AI 能够处理文本时，中国古典文本的诠释传统会发生什么变化？**

《道德经》是我研究的起点。这部仅五千余字的经典，自王弼、河上公以来，历代注释者超过百家。每一代人都试图在前人的诠释基础上，理解那个似乎无法被固定言说的"道"。

这个项目尝试用数字人文的方法，重新审视这一诠释传统——不只是将文本数字化，而是让不同版本"对话"，让 AI 成为诠释的参与者而非旁观者。

### 学术理念

本项目的技术设计，承载着明确的学术理念：

| 功能模块 | 对应的学术传统 | 方法论意义 |
|----------|---------------|------------|
| **多版本并列** | 诠释学（Hermeneutics） | 同一文本在不同传统中的流变 |
| **语义考古** | 考古学方法 × 数字人文 | 追踪概念在历史中的沉积层 |
| **跨文明对话** | 比较哲学（Comparative Philosophy） | 在差异中发现对话的可能 |
| **虚拟注释家** | 计算辅助诠释 | AI 作为诠释共同体的新成员 |

这不是简单的"技术赋能文化"，而是一场关于**数字时代诠释学**的持续实验。

---

## ✨ 核心功能

### 多版本对照系统
- 📚 **原文系统**：王弼本（通行本）为基础
- 🏛️ **古籍版本**：马王堆帛书本、郭店楚简本
- 📝 **历代注释**：王弼注、河上公注、王夫之《老子衍》、憨山德清注
- 🌐 **英文译本**：D.C. Lau / Stephen Henricks / Addiss & Lombardo
- 📖 **白话译文**：现代汉语译本辅助理解

### AI 增强功能
- 🧠 **知识图谱**：章节概念的可视化关系网络
- ⛏️ **语义考古**：追踪核心概念（如"道""德""自然"）的历史演变
- 🌍 **跨文明对话**：与西方哲学传统的概念对照（赫拉克利特、怀特海等）
- 💬 **虚拟注释家**：基于历代注释训练的多视角 AI 解读

### 阅读辅助
- 📝 **疑难字标注**：自动注音与释义
- 🔊 **TTS 朗读**：Fish Audio / Edge TTS 多语言支持
- 🌙 **暗黑模式**：护眼设计
- 📱 **响应式布局**：桌面/平板/手机全适配

---

## 📸 项目截图

### 首页
![首页截图 - 待添加](./docs/screenshots/homepage.png)
> 首页展示九部经典的学习入口，支持快速切换

### 多版本对照
![多版本对照截图 - 待添加](./docs/screenshots/comparison-view.png)
> 原文、注释、英译三栏并列，可自由选择版本组合

### 语义考古
![语义考古截图 - 待添加](./docs/screenshots/semantic-archaeology.png)
> 追踪"道"概念在帛书与通行本中的语义变迁

### 知识图谱
![知识图谱截图 - 待添加](./docs/screenshots/knowledge-graph.png)
> 可视化展示第81章的核心概念网络

---

## 🏗️ 项目结构

```
daodejing/
├── app.py                    # Flask 应用入口
├── config.py                 # 应用配置
│
├── services/                 # 业务逻辑层（AI 核心）
│   ├── classic_service.py           # 经典数据服务
│   ├── annotation_service.py       # 疑难字标注
│   ├── tts_service.py              # TTS 语音合成
│   ├── knowledge_graph.py          # 知识图谱生成
│   ├── semantic_archaeology.py     # 语义考古分析
│   ├── cross_civilization_dialogue.py  # 跨文明对话
│   └── virtual_commentator.py      # 虚拟注释家
│
├── routes/                   # 路由层
│   ├── page_routes.py              # 页面路由
│   └── api_routes.py               # API 路由
│
├── utils/                    # 工具层
│   ├── validators.py               # 输入验证
│   ├── security.py                 # 安全工具
│   └── cache.py                    # 缓存工具
│
├── data/                     # 经典数据
│   ├── daodejing.json              # 道德经数据
│   ├── classics.json               # 九部经典配置
│   └── commentators.json          # 注释家数据
│
├── templates/                # Jinja2 模板
├── static/                   # 静态资源（CSS/JS/图片）
├── tests/                    # 测试文件（92% 覆盖率）
├── docs/                     # 文档
│   ├── architecture.md             # 架构文档
│   ├── user-guide.md               # 用户指南
│   └── openapi.yaml                # API 规范
│
└── scripts/                  # 工具脚本
    ├── data/                       # 数据处理脚本
    ├── quality/                    # 质量检查脚本
    ├── deploy/                     # 部署辅助脚本
    └── performance/               # 性能优化脚本
```

**注意**：根目录的临时脚本已整理至 `scripts/` 目录，保持根目录整洁。

---

## 🚀 快速开始

### 在线演示

访问 **[https://daodejing.vercel.app](https://daodejing.vercel.app)** 体验完整功能。

### 本地运行

```bash
# 克隆项目
git clone https://github.com/leoxmrsh007/daodejing.git
cd daodejing

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python app.py

# 访问 http://localhost:5000
```

### 部署到 Vercel

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录并部署
vercel --prod
```

---

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
python scripts/quality/check_code_quality.py

# 或单独运行
flake8 --config=.flake8 .
mypy --config-file=mypy.ini services/ routes/ utils/
black --check .
isort --check-only .
```

### 预提交钩子

```bash
# 安装 pre-commit
pip install pre-commit
pre-commit install

# 手动运行
pre-commit run --all-files
```

---

## 📊 测试覆盖

| 模块 | 语句覆盖 | 说明 |
|------|----------|------|
| services/classic_service.py | 94% | 核心数据处理 |
| services/knowledge_graph.py | 94% | 知识图谱生成 |
| services/virtual_commentator.py | 93% | AI 注释家 |
| services/semantic_archaeology.py | 92% | 语义考古 |
| services/cross_civilization_dialogue.py | 92% | 跨文明对话 |
| services/annotation_service.py | 93% | 文本标注 |
| services/tts_service.py | 85% | 语音合成 |
| **总计** | **92%** | - |

---

## 📚 支持的经典

本平台现已扩展支持以下九部经典：

| 经典 | 版本数 | 状态 |
|------|--------|------|
| 道德经 | 10+ | ✅ 完善 |
| 周易 | 5+ | ✅ 完善 |
| 金刚经 | 5+ | ✅ 完善 |
| 六祖坛经 | 3+ | ✅ 完善 |
| 庄子 | 5+ | ✅ 完善 |
| 黄帝内经 | 2+ | ✅ 完善 |
| 论语 | 进行中 | 🔄 开发中 |
| 大学/中庸 | 规划中 | 📋 待开发 |
| 传习录 | 2+ | ✅ 完善 |

---

## 🌐 API

完整的 API 文档可在启动服务后访问 `/docs`。

### 主要端点

```
GET  /api/classics                    # 获取经典列表
GET  /api/{classic_id}/chapters       # 获取章节列表
GET  /api/{classic_id}/chapter/{id}   # 获取单章数据
GET  /api/{classic_id}/search         # 搜索章节
GET  /api/knowledge-graph/{chapter}   # 获取知识图谱
GET  /api/semantic-archaeology/{term} # 语义考古分析
GET  /api/cross-civilization/{topic}  # 跨文明对话
POST /api/ai/commentator              # 虚拟注释家
POST /api/tts/fish-audio              # Fish Audio TTS
POST /api/tts/edge                    # Edge TTS
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献指南

- 遵循 PEP 8 代码规范
- 添加适当的测试（目标 90%+ 覆盖率）
- 更新相关文档
- 通过所有质量检查 (`pre-commit run --all-files`)

详细信息请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

---

## 🙏 致谢

- **文本来源**：公开古籍数字化项目（中华书局、中国哲学书电子化计划等）
- **英文翻译**：D.C. Lau、Stephen Henricks、Suzanne and Stephen Addiss
- **注释版本**：历代学者研究成果（王弼、河上公、王夫之、憨山德清等）
- **AI 模型**：OpenAI GPT 系列 / Anthropic Claude 系列

---

## 📞 联系

- **GitHub**：[@leoxmrsh007](https://github.com/leoxmrsh007)
- **项目 Issues**：[Issues](https://github.com/leoxmrsh007/daodejing/issues)
- **学术合作**：欢迎从事数字人文、计算哲学相关研究的学者交流

---

## 附录：开发记录

### 项目演进

```
2024.01 - 项目启动，基础框架搭建
2024.03 - 多版本对照功能上线
2024.06 - AI 功能集成（知识图谱、虚拟注释家）
2024.09 - 扩展至九部经典
2025.01 - 语义考古模块上线
2025.06 - 跨文明对话功能完善
2026.02 - 测试覆盖率提升至 92%
```

### 相关论文/项目（规划中）

- [ ] 数字人文视角下的《道德经》版本比较研究
- [ ] 计算辅助的古典诠释学方法论
- [ ] AI 作为诠释共同体成员的可能性

---

> *"道生一，一生二，二生三，三生万物。"*
> 
> 万物生于道，项目亦然。从一部经典开始，探索数字诠释学的可能边界。
