# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-version comparative study platform for the Tao Te Ching (道德经). It's a Flask web application that can also generate static HTML files for deployment. The platform supports multiple commentaries, translations, and text versions including ancient manuscripts (Mawangdui silk text, Guodian bamboo slips).

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
app.py                    # Single-file Flask application (routes, data loading, templates)
data/daodejing.json       # All content data (81 chapters, commentaries, translations)
generate_static.py        # Static site generator
static/                   # Source assets (CSS, JS, images, audio)
templates/                # Jinja2 templates for Flask
dist/                     # Generated static site (output of generate_static.py)
```

## Architecture

### Backend (Flask)
- **Single-file application**: All routes, data loading, and template rendering in `app.py`
- **No database**: All content stored in `data/daodejing.json`
- **Routes**:
  - `/daodejing/` - Index page with chapter list
  - `/daodejing/chapter/<id>` - Individual chapter view
  - `/api/daodejing/*` - JSON API endpoints

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

Each chapter in `daodejing.json` contains:
- `chapter`: Chapter number (1-81)
- `original`: Original classical Chinese text
- `modern_chinese`: Modern Chinese translation
- `wangbi_note`, `heshanggong_note`, `wangfuzhi_note`, `hanshandeqing_note`: Commentary notes
- `postsilk_text`, `guodian_text`: Ancient manuscript variants
- `english_lau`, `english_henricks`, `english_addiss`: English translations

### Character Annotations

Difficult characters are annotated with pinyin and meanings. The `DIFFICULT_CHARS` dictionary is duplicated in both `app.py` and `generate_static.py` - when adding new annotations, update both files.

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
