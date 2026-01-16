# -*- coding: utf-8 -*-
"""
道德经 - Vercel Python 部署
单文件版本，避免模块导入问题
"""

import sys
import os
import json
from pathlib import Path

# 设置路径
project_root = Path('/var/task')
if not project_root.exists():
    project_root = Path(__file__).parent.parent

sys.path.insert(0, str(project_root))
os.chdir(project_root)

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# 加载数据的函数
def load_data():
    data_file = project_root / 'data' / 'daodejing.json'
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"title": "道德经", "chapters": []}

# HTML 模板
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>道德经 - 多版本对照</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
    <style>
        body { background: #f5f5f0; }
        .chapter-card {
            background: white;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid #ddd;
        }
        .chapter-card:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .chapter-num {
            color: #8B4513;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">☯ 道德经</a>
        </div>
    </nav>

    <div class="container py-4">
        <div class="text-center mb-4">
            <h1>{{ title }}</h1>
            <p class="lead">{{ subtitle }}</p>
        </div>

        <div class="row">
            {% for chapter in chapters %}
            <div class="col-6 col-md-4 col-lg-3 col-xl-2">
                <a href="/chapter/{{ chapter['chapter'] }}" class="text-decoration-none">
                    <div class="chapter-card">
                        <div class="chapter-num">第{{ chapter['chapter'] }}章</div>
                        <small class="text-muted">{{ chapter.get('original', '')[:20] }}...</small>
                    </div>
                </a>
            </div>
            {% endfor %}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

CHAPTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>第{{ chapter }}章 - 道德经</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f5f5f0; }
        .original-text {
            font-family: "KaiTi", "楷体", serif;
            font-size: 1.8rem;
            text-align: center;
            line-height: 2;
            padding: 2rem;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/daodejing/">☯ 道德经</a>
        </div>
    </nav>

    <div class="container py-4">
        <div class="card mb-3">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5>第{{ chapter }}章 · 原文</h5>
                <nav aria-label="chapter navigation">
                    <ul class="pagination pagination-sm mb-0">
                        {% if prev > 0 %}
                        <li class="page-item"><a class="page-link" href="/chapter/{{ prev }}">← 上一章</a></li>
                        {% endif %}
                        <li class="page-item disabled"><span class="page-link">{{ chapter }} / 81</span></li>
                        {% if next < 82 %}
                        <li class="page-item"><a class="page-link" href="/chapter/{{ next }}">下一章 →</a></li>
                        {% endif %}
                    </ul>
                </nav>
            </div>
            <div class="card-body">
                <div class="original-text">{{ original }}</div>
            </div>
        </div>

        <div class="card mb-3">
            <div class="card-header">现代白话译文</div>
            <div class="card-body">
                <p>{{ modern }}</p>
            </div>
        </div>

        <div class="card">
            <div class="card-header">注解</div>
            <div class="card-body">
                <h6>王弼注</h6>
                <p>{{ wangbi }}</p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# 路由
@app.route('/')
def index():
    data = load_data()
    chapters = data.get('chapters', [])[:10]
    return render_template_string(INDEX_TEMPLATE, title=data.get('title', '道德经'),
                                   subtitle=data.get('subtitle', ''), chapters=chapters)

@app.route('/daodejing/')
def daodejing_index():
    data = load_data()
    return render_template_string(INDEX_TEMPLATE, title=data.get('title', '道德经'),
                                   subtitle=data.get('subtitle', ''),
                                   chapters=data.get('chapters', []))

@app.route('/chapter/<int:chapter_id>')
def chapter_view(chapter_id):
    if chapter_id < 1 or chapter_id > 81:
        return '章节不存在', 404

    data = load_data()
    chapter = next((c for c in data.get('chapters', []) if c['chapter'] == chapter_id), None)

    if not chapter:
        return '章节不存在', 404

    # 获取相邻章节
    idx = data['chapters'].index(chapter)
    prev = data['chapters'][idx - 1]['chapter'] if idx > 0 else 0
    next_ch = data['chapters'][idx + 1]['chapter'] if idx < len(data['chapters']) - 1 else 82

    return render_template_string(CHAPTER_TEMPLATE,
                                   chapter=chapter_id,
                                   original=chapter.get('original', ''),
                                   modern=chapter.get('modern_chinese', ''),
                                   wangbi=chapter.get('wangbi_note', ''),
                                   prev=prev,
                                   next=next_ch)

@app.route('/api/daodejing/chapters')
def api_chapters():
    data = load_data()
    return jsonify({
        'title': data.get('title', ''),
        'chapters': [{'id': c['chapter'], 'title': f'第{c["chapter"]}章'} for c in data.get('chapters', [])]
    })

# Vercel 入口点
vercel_app = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
