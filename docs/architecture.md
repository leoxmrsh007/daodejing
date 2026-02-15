# 系统架构设计文档

## 1. 项目概述

### 1.1 项目简介

《道德经》多版本对照学习平台是一个基于 Flask 的 Web 应用程序，现已扩展为**多经典对照学习平台**。平台支持多版本古籍对照阅读、疑难字标注、TTS语音朗读、AI辅助学习等功能。

当前支持的9部经典：
- **道家**: 道德经、庄子
- **中医**: 黄帝内经
- **佛学**: 金刚经、六祖坛经、唯识三十颂
- **儒家**: 周易、四书、传习录

### 1.2 核心功能

- **多版本对照**：支持原文、多种注释、英文翻译并列展示
- **古籍版本**：马王堆帛书本、郭店楚简本
- **注释版本**：
  - 道德经：王弼注、河上公注、王夫之、憨山德清注、苏辙注、李涵虚注等
  - 庄子：成玄英疏、郭象注、王夫之
  - 黄帝内经：王冰注、张介宾注、马莳注
- **英文翻译**：
  - 道德经：D.C. Lau、Henricks、Addiss & Lombardo、Arthur Waley、林语堂
  - 庄子：Burton Watson、Brook Ziporyn
  - 黄帝内经：Nelson Wu、Paul Unschuld
- **TTS朗读**：Fish Audio 和 Microsoft Edge TTS
- **AI创新功能**：
  - 知识图谱：概念关联可视化
  - 语义考古：文本演变分析
  - 跨文明对话：中西方哲学对话
  - 虚拟注释家：与历史人物对话

### 1.3 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Flask (Python 3.9+) |
| 前端 | Vanilla JavaScript + Bootstrap 5 |
| CSS | Bootstrap 5 + 自定义 CSS |
| 数据存储 | JSON 文件 (data/classics.json + 各经典目录) |
| API文档 | OpenAPI 3.0 / Swagger UI |
| 测试 | pytest + pytest-cov |
| 代码质量 | flake8, mypy, black, isort |
| CI/CD | GitHub Actions |
| 部署 | Vercel (动态) / 静态托管 |

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                      客户端 (Browser)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   HTML页面   │  │  JavaScript  │  │    CSS       │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
┌────────────────────┴────────────────────────────────────┐
│                    Flask 应用服务器                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │                   路由层 (Routes)                 │  │
│  │  ┌──────────────┐  ┌──────────────┐             │  │
│  │  │  page_routes │  │  api_routes  │             │  │
│  │  └──────────────┘  └──────────────┘             │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │                   服务层 (Services)               │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │  │
│  │  │Classic   │ │Annotation│ │  TTS     │         │  │
│  │  │Service   │ │Service   │ │ Service  │         │  │
│  │  └──────────┘ └──────────┘ └──────────┘         │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │  │
│  │  │Knowledge │ │Semantic  │ │ Cross-   │         │  │
│  │  │Graph     │ │Archaeology││Civilization│        │  │
│  │  └──────────┘ └──────────┘ └──────────┘         │  │
│  │  ┌──────────┐                                      │  │
│  │  │ Virtual  │                                      │  │
│  │  │Commentator│                                     │  │
│  │  └──────────┘                                      │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │                   工具层 (Utils)                  │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │  │
│  │  │Validators│ │ Security │ │  Cache   │         │  │
│  │  └──────────┘ └──────────┘ └──────────┘         │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │                   数据层 (Data)                   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │  │
│  │  │classics  │ │ daodejing│ │ zhuangzi │         │  │
│  │  │.json     │ │/chapters │ │/chapters │         │  │
│  │  │          │ │  .json   │ │  .json   │         │  │
│  │  │  +8 more│ └──────────┘ └──────────┘         │  │
│  │  │  classics│        +7 more classics          │  │
│  │  └──────────┘ └───────────────────────────────┘  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 模块化设计

#### 2.2.1 路由层 (routes/)

- **page_routes.py**: HTML页面路由
  - `/` - 平台首页（展示所有经典）
  - `/{classic_id}/` - 经典章节目录页
  - `/{classic_id}/chapter/<id>` - 章节详情页
  - `/{classic_id}/compare/<id>` - 多版本对照页
  - `/daodejing/*` - 向后兼容路由
  - `/docs` - API文档页面

- **api_routes.py**: API端点
  - `/api/classics` - 获取所有经典列表
  - `/api/{classic_id}/*` - 多经典统一API接口
  - `/api/daodejing/*` - 向后兼容API
  - TTS 服务 API
  - AI创新功能 API（知识图谱、语义考古、跨文明对话、虚拟注释家）

#### 2.2.2 服务层 (services/)

| 服务模块 | 职责 | 关键类/函数 |
|----------|------|-------------|
| classic_service.py | 经典数据管理 | ClassicService, get_all_classics |
| annotation_service.py | 疑难字标注 | annotate_difficult_chars |
| tts_service.py | 语音合成 | FishAudioService, EdgeTTSService |
| knowledge_graph.py | 知识图谱 | get_chapter_knowledge_graph |
| semantic_archaeology.py | 语义考古 | get_chapter_archaeology |
| cross_civilization_dialogue.py | 跨文明对话 | start_philosophy_dialogue |
| virtual_commentator.py | 虚拟注释家 | generate_commentary_response |

#### 2.2.3 工具层 (utils/)

- **validators.py**: 输入验证和清理
  - `validate_chapter_id()`
  - `validate_search_query()`
  - `sanitize_text()`

- **security.py**: 安全相关
  - `rate_limit()` 装饰器
  - 安全响应头
  - CORS 配置

- **cache.py**: 缓存管理
  - 内存缓存
  - 缓存失效策略

## 3. 数据流

### 3.1 章节内容获取流程

```
用户请求 -> page_routes -> ClassicService.load_data()
-> annotation_service.annotate_difficult_chars()
-> 模板渲染 -> HTML响应
```

### 3.2 API 请求处理流程

```
HTTP请求 -> api_routes -> 参数验证 -> Service层处理
-> JSON序列化 -> HTTP响应
```

### 3.3 TTS 语音合成流程

```
POST /api/tts/fish-audio -> rate_limit -> fish_audio_service.synthesize()
-> 调用Fish Audio API -> 音频流响应
```

## 4. 多经典架构

### 4.1 设计原则

- **统一接口**: 所有经典使用相同的API接口
- **配置驱动**: 经典信息存储在 `data/classics.json`
- **向后兼容**: 保留 `/daodejing/*` 路径
- **可扩展性**: 轻松添加新经典，无需修改代码

### 4.2 经典配置

```json
{
  "classics": [
    {
      "id": "ddj",
      "name": "道德经",
      "short_name": "道德经",
      "author": "老子",
      "era": "春秋末期",
      "chapters": 81,
      "data_file": "data/daodejing/chapters.json",
      "icon": "☯",
      "color": "#d4a574",
      "description": "道家哲学奠基之作，五千余言阐述宇宙本源与人生智慧",
      "commentators": [...],
      "translators": [...],
      "variants": [...]
    }
    // + 8 more classics
  ],
  "default_classic": "ddj"
}
```

### 4.3 URL 设计

| 端点 | 描述 | 示例 |
|------|------|------|
| `/` | 平台首页（所有经典） | `https://example.com/` |
| `/{classic_id}/` | 经典章节目录 | `/ddj/`, `/zzj/` |
| `/{classic_id}/chapter/{id}` | 章节详情页 | `/ddj/chapter/1` |
| `/{classic_id}/compare/{id}` | 多版本对照页 | `/ddj/compare/1` |
| `/api/classics` | 获取所有经典列表 | GET `/api/classics` |
| `/api/{classic_id}/chapters` | 获取章节列表 | GET `/api/ddj/chapters` |
| `/api/{classic_id}/chapter/{id}` | 获取单章数据 | GET `/api/ddj/chapter/1` |
| `/api/{classic_id}/search` | 搜索章节 | GET `/api/ddj/search?q=道` |
| `/daodejing/*` | 向后兼容 | `/daodejing/chapter/1` |

### 4.4 支持的经典列表

| ID | 名称 | 作者 | 时代 | 章节数 | 主要注释 |
|----|------|------|------|--------|----------|
| ddj | 道德经 | 老子 | 春秋末期 | 81 | 王弼、河上公、王夫之等11家 |
| zzj | 庄子 | 庄周 | 战国中期 | 33 | 成玄英、郭象、王夫之 |
| hdnj | 黄帝内经 | 黄帝 | 战国至西汉 | 81 | 王冰、张介宾、马莳 |
| jgj | 金刚经 | 达摩祖师传译 | 后秦至北魏 | 1 | - |
| lztyj | 六祖坛经 | 慧能 | 唐代 | 10 | - |
| ws30 | 唯识三十颂 | 世亲 | 四至五世纪 | 30 | - |
| zy | 周易 | 文王、周公 | 西周 | 64 | - |
| ss | 四书 | 朱熹 | 南宋 | 4 | - |
| cxl | 传习录 | 王阳明 | 明代 | 3 | - |

## 5. 安全设计

### 5.1 输入验证

- 章节ID范围检查 (1-81)
- 搜索查询长度限制 (≤200字符)
- XSS防护 (HTML标签过滤)
- 特殊字符清理

### 5.2 速率限制

| 端点 | 限制 |
|------|------|
| 搜索 API | 30请求/60秒 |
| Fish Audio TTS | 10请求/60秒 |
| Edge TTS | 20请求/60秒 |

### 5.3 安全头部

```python
{
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}
```

## 6. 部署架构

### 6.1 动态部署 (Vercel)

```
GitHub Push -> Vercel Build -> Flask App Deployed
                    ↓
              Serverless Functions
```

### 6.2 静态部署

```
python generate_static.py -> dist/ -> 静态托管
```

### 6.3 混合部署

```
CDN (静态资源) + Vercel (API) -> 用户
```

## 7. 开发工作流

### 7.1 代码质量保证

```
代码提交 -> pre-commit hooks -> flake8 -> mypy -> black -> isort
                              ↓
                        GitHub Actions
                              ↓
                        pytest -> 覆盖率检查
```

### 7.2 测试策略

- **单元测试**: 服务层函数测试
- **集成测试**: API端点测试
- **覆盖率目标**: ≥85%

## 8. 扩展性设计

### 8.1 添加新经典

1. 准备数据文件 (JSON格式)
2. 更新 classics.json 配置
3. 无需修改代码即可支持

### 8.2 添加新注释版本

1. 在数据文件中添加注释字段
2. 前端模板自动展示

### 8.3 添加新API功能

1. 在 services/ 实现业务逻辑
2. 在 api_routes.py 注册端点
3. 更新 openapi.yaml 文档

## 9. 性能优化策略

### 9.1 当前优化

- 数据内存缓存
- 静态资源CDN
- 响应压缩

### 9.2 未来优化方向

- 数据库迁移
- Redis缓存
- 异步任务队列
- CDN边缘缓存

## 10. 监控与日志

### 10.1 性能监控

- API响应时间
- 错误率统计
- 用户行为分析

### 10.2 日志记录

- 请求日志
- 错误日志
- 安全事件日志

---

*文档版本: 2.0*
*更新日期: 2026-02-15*
*更新内容: 扩展为多经典平台架构*
