#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML模板模块 - 负责生成所有HTML页面
"""

from pathlib import Path
from typing import Dict, List, Any, Optional

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "dist"


def get_base_template() -> str:
    """获取基础HTML模板"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body>
    {content}
    <script src="/assets/js/main.js"></script>
</body>
</html>"""


def generate_chapter_list_html(
    classic_id: str, classic_data: Dict[str, Any], metadata: Dict[str, Any]
) -> str:
    """生成章节列表页面"""
    chapters = classic_data.get("chapters", [])
    title = classic_data.get("title", "")

    chapter_links = []
    for ch in chapters:
        ch_num = ch.get("chapter", 0)
        ch_title = ch.get("title", f"第{ch_num}章")
        chapter_links.append(f'<li><a href="chapter{ch_num}.html">{ch_title}</a></li>')

    content = f"""
    <div class="container">
        <h1>{title}</h1>
        <ul class="chapter-list">
            {"".join(chapter_links)}
        </ul>
    </div>
    """

    return get_base_template().format(title=title, content=content)


def generate_chapter_page_html(
    classic_id: str,
    chapter: Dict[str, Any],
    classic_data: Dict[str, Any],
    metadata: Dict[str, Any],
) -> str:
    """生成单个章节页面"""
    ch_num = chapter.get("chapter", 0)
    ch_title = chapter.get("title", f"第{ch_num}章")
    original = chapter.get("original", "")

    # 构建注释部分
    notes_html = []
    for key in chapter.keys():
        if "note" in key.lower():
            note_content = chapter[key]
            note_name = key.replace("_note", "").replace("_", " ").title()
            notes_html.append(
                f'<div class="note"><h3>{note_name}</h3><p>{note_content}</p></div>'
            )

    content = f"""
    <div class="container">
        <nav class="breadcrumb">
            <a href="/">首页</a> / <a href="index.html">{classic_data.get("title", "")}</a>
        </nav>
        <article class="chapter">
            <h1>{ch_title}</h1>
            <div class="original-text">{original}</div>
            <div class="notes">{"".join(notes_html)}</div>
        </article>
        <nav class="chapter-nav">
            {f'<a href="chapter{ch_num - 1}.html">上一章</a>' if ch_num > 1 else ""}
            {f'<a href="chapter{ch_num + 1}.html">下一章</a>' if ch_num < len(classic_data.get("chapters", [])) else ""}
        </nav>
    </div>
    """

    return get_base_template().format(
        title=f"{ch_title} - {classic_data.get('title', '')}", content=content
    )


def generate_index_page_html(
    classic_data: Dict[str, Any], metadata: Dict[str, Any]
) -> str:
    """生成经典首页"""
    title = classic_data.get("title", "")
    subtitle = classic_data.get("subtitle", "")
    chapters = classic_data.get("chapters", [])

    content = f"""
    <div class="container">
        <header class="classic-header">
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
            <p class="chapter-count">共 {len(chapters)} 章</p>
        </header>
        <div class="actions">
            <a href="all-chapters.html" class="btn">查看全部章节</a>
            <a href="chapter1.html" class="btn btn-primary">开始阅读</a>
        </div>
    </div>
    """

    return get_base_template().format(title=title, content=content)


def generate_main_index_page(
    classics: Dict[str, Dict[str, Any]], metadata: Dict[str, Any]
) -> str:
    """生成网站总首页"""
    classic_list = metadata.get("classics", [])

    cards = []
    for classic_meta in classic_list:
        cid = classic_meta.get("id", "")
        name = classic_meta.get("name", "")
        desc = classic_meta.get("description", "")
        icon = classic_meta.get("icon", "📚")

        cards.append(f"""
        <div class="classic-card">
            <div class="icon">{icon}</div>
            <h3>{name}</h3>
            <p>{desc}</p>
            <a href="/{cid}/index.html" class="btn">阅读</a>
        </div>
        """)

    content = f"""
    <div class="container">
        <header class="site-header">
            <h1>古籍经典学习平台</h1>
            <p class="tagline">九部经典，一站式学习</p>
        </header>
        <div class="classics-grid">
            {"".join(cards)}
        </div>
    </div>
    """

    return get_base_template().format(title="古籍经典学习平台", content=content)
