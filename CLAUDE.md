# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **multi-classic comparative study platform** for classical Chinese literature. It's a Flask web application that can also generate static HTML files for deployment. The platform currently supports 9 classics including 道德经, 庄子, 黄帝内经, 金刚经, 六祖坛经, 唯识三十颂, 周易, 四书, and 传习录.

Each classic supports multiple commentaries, translations, and text versions including ancient manuscripts (Mawangdui silk text, Guodian bamboo slips).

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python app.py

# Generate static site (outputs to dist/)
python generate_static.py
```

## Project Structure

```
app.py                    # Flask application entry point (uses app factory pattern)
config.py                 # Application configuration
services/                 # Business logic layer
  ├── classic_service.py  # Multi-classic data management (main service)
  ├── annotation_service.py # Difficult character annotation
  ├── tts_service.py      # TTS proxy services (Fish Audio, Edge TTS)
  ├── knowledge_graph.py  # Knowledge graph generation
  ├── semantic_archaeology.py # Semantic archaeology analysis
  ├── cross_civilization_dialogue.py # Cross-civilization philosophy dialogue
  ├── virtual_commentator.py # AI-powered virtual commentator
  └── data_service.py     # Legacy data service (deprecated, kept for compatibility)
routes/                   # Route handlers (Flask blueprints)
  ├── page_routes.py      # HTML page routes
  └── api_routes.py       # JSON API routes
utils/                    # Utility functions
  ├── validators.py       # Input validation and sanitization
  ├── security.py         # Security decorators (rate limiting, headers)
  └── cache.py            # Caching utilities
data/                     # Content data
  ├── classics.json       # Classic metadata configuration (9 classics)
  ├── daodejing/chapters.json  # Tao Te Ching chapters
  ├── zhuangzi/chapters.json  # Zhuangzi chapters
  ├── huangdi_neijing/chapters.json  # Yellow Emperor's Inner Canon
  ├── jingangjing/chapters.json  # Diamond Sutra
  ├── liuzutan/chapters.json  # Platform Sutra
  ├── weishi/chapters.json  # Thirty Verses of Consciousness Only
  ├── zhouyi/chapters.json  # I Ching
  ├── sishu/chapters.json  # Four Books
  └── chuanxilu/chapters.json  # Instructions for Practical Living
generate_static.py        # Static site generator
static/                   # Source assets (CSS, JS, images, audio)
templates/                # Jinja2 templates for Flask
dist/                     # Generated static site (output of generate_static.py)
scripts/                  # Utility scripts
  ├── check_code_quality.py # Code quality checker
  └── deploy_helper.py    # Deployment configuration generator
```

## Architecture

### Backend (Flask)
- **Modular architecture**: Separated into services, routes, and utils
- **App factory pattern**: `create_app()` function for initialization
- **Multi-classic support**: Unified interface for 9+ classics via `ClassicService`
- **Configuration-driven**: Classic metadata in `data/classics.json`
- **Blueprint-based routing**:
  - Pages: `/` (platform home), `/{classic_id}/`, `/{classic_id}/chapter/<id>`
  - API: `/api/classics`, `/api/{classic_id}/*`, `/api/tts/*`
  - Backward compatibility: `/daodejing/*` routes preserved

### Service Layer
- `ClassicService`: Multi-classic data management (main service)
  - Load data with caching per classic
  - Get chapters, search, annotations
  - Support for multiple commentaries and translations
- `annotation_service`: Add pinyin/meaning annotations to difficult characters
- `tts_service`: `FishAudioService`, `EdgeTTSService` for text-to-speech
- `knowledge_graph`: Generate knowledge graph for chapters
- `semantic_archaeology`: Analyze semantic changes over time
- `cross_civilization_dialogue`: Enable East-West philosophy dialogues
- `virtual_commentator`: AI-powered commentary from historical figures
- `data_service`: Legacy service (kept for backward compatibility)

### Security
- Input validation in `utils/validators.py`
- XSS protection for search queries
- Request validation for TTS services

### Frontend
- **No frameworks**: Vanilla JavaScript with modular object-based organization
- **CSS**: Bootstrap 5 + custom CSS with CSS variables for theming
- **Key JS modules** (in `static/js/main.js`):
  - `ThemeManager` - Dark/light mode toggle
  - `SidebarManager` - Mobile sidebar toggle
  - `SearchManager` - Chapter search
  - `KeyboardNavigation` - Arrow key navigation
  - `MusicPlayer` - Background audio
  - `SpeechManager` - Text-to-speech
  - `AIInterpretation` - Client-side AI chat (DeepSeek/OpenAI)

### Data Structure

#### Classic Configuration (`data/classics.json`)
Defines metadata for all supported classics (currently 9):
- Classic ID, name, author, era
- Chapter count and data file path
- Commentators list (e.g., Wang Bi, He Shang Gong)
- Translators list (e.g., D.C. Lau, Robert Henricks)
- Ancient manuscript variants (Mawangdui, Guodian)
- Icon and color for UI

#### Chapter Data Structure
Each chapter in a classic's JSON file contains:
- `chapter`: Chapter number
- `title`: Chapter title (if available)
- `original`: Original classical Chinese text
- `modern_chinese`: Modern Chinese translation
- Commentary notes (varies by classic):
  - 道德经: `wangbi_note`, `heshanggong_note`, `wangfuzhi_note`, etc.
  - 庄子: `chengxuanying_note`, `guoxiang_note`, etc.
- Ancient manuscript variants (where available):
  - `postsilk_text`: Mawangdui silk text
  - `guodian_text`: Guodian bamboo slips
- English translations (varies by classic):
  - 道德经: `english_lau`, `english_henricks`, `english_addiss`
  - 庄子: `english_watson`, `english_ziporyn`

### Character Annotations

Difficult characters are annotated with pinyin and meanings. The `DIFFICULT_CHARS` dictionary is in `services/annotation_service.py` and is also duplicated in `generate_static.py` - when adding new annotations, update both files.

### Static Site Generation

`generate_static.py` creates a complete static site by:
1. Loading data from `data/daodejing.json`
2. Generating HTML pages (index, all-chapters, 81 chapter pages)
3. Copying assets from `static/` to `dist/assets/`
4. Modifying `main.js` to disable search (static version doesn't have API)

The static version removes API-dependent features like search and keeps client-side features (theme toggle, keyboard navigation, music player).

## Deployment

Detailed deployment documentation is available in [DEPLOYMENT.md](./DEPLOYMENT.md), including:

- **Vercel 动态部署**: Flask 应用 + API 功能（搜索、TTS）
- **静态站点部署**: 纯 HTML/CSS/JS，可部署到任何静态托管
- **混合部署**: CDN 静态文件 + Vercel API
- 域名配置、环境变量、故障排查

Quick commands:
```bash
# 方案一：推送到 GitHub，Vercel 自动部署
git push origin main

# 方案二：生成静态文件后部署
python generate_static.py
# 然后上传 dist/ 目录到 Netlify/Vercel/GitHub Pages
```

## Key Conventions

- All text files are UTF-8 encoded
- Flask templates are in `templates/ddj/`
- The difficult character annotation uses placeholder replacement to avoid nested replacements
- Client-side AI keys are stored in localStorage only (never sent to server)

## Code Quality & Testing

The project has comprehensive code quality tools and testing infrastructure:

### Quality Tools
- **Flake8**: Python code style checking (PEP 8 compliance)
- **Mypy**: Static type checking for Python 3.9+ compatibility
- **Black**: Automatic code formatting
- **isort**: Import statement sorting
- **pre-commit**: Git hook automation

### Testing
- **pytest**: Test framework with coverage reporting
- **Coverage Goal**: ≥80% for services/ directory (currently 86% achieved)
- **Test Structure**: 125 tests across unit and integration tests
- **Test Data**: Uses actual `data/classics.json` and classic-specific JSON files for realistic testing

### Quality Commands
```bash
# Run all quality checks
python scripts/check_code_quality.py

# Run tests with coverage
python -m pytest --cov=services --cov-report=term-missing tests/ -v

# Type checking
python -m mypy --config-file=mypy.ini services/ routes/ utils/

# Code style checking
python -m flake8 --config=.flake8 .

# Format code
python -m black .
python -m isort .
```

## API Documentation

The project now includes comprehensive OpenAPI/Swagger documentation:

### Available Documentation
1. **Interactive API Docs**: Access at `/docs` or `/docs/api`
   - Swagger UI interface for exploring and testing endpoints
   - Live documentation with request/response examples
   - Try-it-out functionality for API testing

2. **OpenAPI Specification**: `docs/openapi.yaml`
   - Complete API specification in OpenAPI 3.0 format
   - All endpoints documented with parameters, responses, and examples
   - Rate limiting and security information included

### API Categories
- **Classic Management**: Multi-classic support (DDJ, ZZJ, etc.)
- **Chapter Content**: Chapter retrieval, search, and navigation
- **Backward Compatibility**: Legacy `/daodejing/*` endpoints
- **TTS Services**: Fish Audio and Edge TTS proxies
- **AI Features**: Knowledge graph, semantic archaeology, cross-civilization dialogue

### Access Documentation
```bash
# Start development server
python app.py

# Access API docs at:
# http://localhost:5000/docs
# http://localhost:5000/docs/openapi.yaml
```

## Project Status & Recent Updates

### Completed Milestones
✅ **Code Quality Enhancement**: All 75 mypy errors fixed, 32 flake8 warnings resolved
✅ **Test Coverage Improvement**: Services directory coverage increased to 92% (125+ tests)
✅ **Multi-classic Platform**: Extended from single classic to 9 classics
✅ **Documentation Phase**: Architecture docs (v2.0), user guide (v2.0), and performance docs completed
✅ **Development Standards**: Full quality toolchain established

### Current Development Phase
According to `DEVELOPMENT_GOALS.md`, project is currently in:
- **Short-term Goal 3**: Documentation completion (most docs complete, OpenAPI needs updates for some AI endpoints)
- **Next**: Performance optimization (mid-term goal 4) and feature enhancement phases

### Architecture Updates
- **Multi-classic Support**: Generalized `ClassicService` for 9 classical texts (道德经, 庄子, 黄帝内经, etc.)
- **Modular Structure**: Clean separation of services, routes, and utilities
- **Type Safety**: Full Python type annotations with mypy validation
- **Security**: Input validation, rate limiting, and XSS protection
- **API-First Design**: RESTful APIs supporting all classics with unified interface

### Documentation Status
- ✅ `docs/architecture.md` (v2.0) - System architecture complete
- ✅ `docs/user-guide.md` (v2.0) - User guide complete
- ⏳ `docs/openapi.yaml` (v2.0) - API docs need updates (missing some AI endpoints)
- ✅ `docs/performance-frontend.md` - Frontend performance monitoring
- ✅ `docs/performance-backend.md` - Backend performance monitoring

## Development Workflow

### Getting Started
```bash
# 1. Clone and install
git clone <repository>
cd daodejing
pip install -r requirements.txt

# 2. Run quality checks
python scripts/check_code_quality.py

# 3. Run tests
python -m pytest tests/

# 4. Start development server
python app.py
```

### Common Tasks
```bash
# Add new tests
python -m pytest tests/ -v -k "test_pattern"

# Check coverage for specific module
python -m pytest --cov=services.module_name tests/

# Fix code style issues
python -m black .
python -m isort .

# Pre-commit hooks (if configured)
pre-commit run --all-files
```

### Documentation Updates
When modifying APIs:
1. Update the implementation in `routes/api_routes.py`
2. Update corresponding service methods
3. Update test files in `tests/`
4. Update OpenAPI specification in `docs/openapi.yaml`
5. Verify documentation at `/docs`

## Troubleshooting

### Common Issues
1. **Type Errors**: Run `python -m mypy --config-file=mypy.ini .` to identify issues
2. **Test Failures**: Check `tests/test_services.py` for specific test cases
3. **API Changes**: Ensure backward compatibility for `/daodejing/*` endpoints
4. **Documentation Sync**: Keep `docs/openapi.yaml` updated with API changes

### Performance Tips
- Data is cached in memory after first load
- Use static site generation for production deployment
- Enable gzip compression for API responses
- Consider CDN for static assets in production

---
*Last Updated: 2026-02-15 | Project Phase: Multi-classic Platform Expansion*
