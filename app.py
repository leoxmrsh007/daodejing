# -*- coding: utf-8 -*-
"""
道德经多版本对照平台 - Flask 主应用
"""

import os
import json
import re
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 加载数据文件
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'daodejing.json')

# 疑难字标注配置
DIFFICULT_CHARS = {
    "徼": {"pinyin": "jiào", "meaning": "边界，边际"},
    "牝": {"pinyin": "pìn", "meaning": "鸟兽的雌性，喻指柔弱"},
    "玄牝": {"pinyin": "xuán pìn", "meaning": "微妙而神秘的母体"},
    "谷神": {"pinyin": "gǔ shén", "meaning": "形容虚空而神奇的存在"},
    "冲": {"pinyin": "chōng", "meaning": "谦虚，冲和"},
    "渊": {"pinyin": "yuān", "meaning": "深沉，深潭"},
    "湛": {"pinyin": "zhàn", "meaning": "深沉，清澈"},
    "恍": {"pinyin": "huǎng", "meaning": "惚恍，不分明"},
    "惚": {"pinyin": "hū", "meaning": "惚恍，不分明"},
    "窈": {"pinyin": "yǎo", "meaning": "深远，不见踪影"},
    "冥": {"pinyin": "míng", "meaning": "幽暗，深不可测"},
    "橐龠": {"pinyin": "tuó yuè", "meaning": "风箱，比喻虚空而能生风"},
    "刍狗": {"pinyin": "chú gǒu", "meaning": "用草扎的狗，用于祭祀"},
    "歙": {"pinyin": "xī", "meaning": "收缩，收敛"},
    "张": {"pinyin": "zhāng", "meaning": "扩张，张开"},
    "羸": {"pinyin": "léi", "meaning": "瘦弱，衰败"},
    "赘": {"pinyin": "zhuì", "meaning": "多余，累赘"},
    "沌": {"pinyin": "dùn", "meaning": "混沌兮，不分明的样子"},
    "澹": {"pinyin": "dàn", "meaning": "恬静，安定"},
    "飂": {"pinyin": "liù", "meaning": "风声，飘扬"},
    "豫": {"pinyin": "yù", "meaning": "犹豫。容：犹豫，谨慎。"},
    "犹": {"pinyin": "yóu", "meaning": "犹豫，警惕"},
    "俨": {"pinyin": "yǎn", "meaning": "恭敬，庄重"},
    "涣": {"pinyin": "huàn", "meaning": "消散，离散"},
    "敦": {"pinyin": "dūn", "meaning": "淳厚，诚恳"},
    "旷": {"pinyin": "kuàng", "meaning": "空阔，广大"},
    "混": {"pinyin": "hùn", "meaning": "混同，混浊"},
    "浊": {"pinyin": "zhuó", "meaning": "浑浊"},
    "儽": {"pinyin": "lěi", "meaning": "颓丧，疲惫"},
    "孔德": {"pinyin": "kǒng dé", "meaning": "大德，孔指甚、大"},
    "跂": {"pinyin": "qì", "meaning": "踮起脚尖"},
    "跨": {"pinyin": "kuà", "meaning": "迈大步"},
    "瑕谪": {"pinyin": "xiá zhé", "meaning": "过失，缺点"},
    "筹策": {"pinyin": "chóu cè", "meaning": "计数的筹码"},
    "楗": {"pinyin": "jiàn", "meaning": "门栓"},
    "袭明": {"pinyin": "xí míng", "meaning": "承袭光明的智慧"},
    "雄": {"pinyin": "xióng", "meaning": "雄性，刚强"},
    "雌": {"pinyin": "cí", "meaning": "鸟兽的雌性，柔弱"},
    "溪": {"pinyin": "xī", "meaning": "溪涧"},
    "式": {"pinyin": "shì", "meaning": "范式，法式"},
    "忒": {"pinyin": "tè", "meaning": "差错"},
    "谷": {"pinyin": "gǔ", "meaning": "川谷，虚怀"},
    "朴": {"pinyin": "pǔ", "meaning": "朴素，未雕琢的木材"},
    "器": {"pinyin": "qì", "meaning": "器具"},
    "嚣": {"pinyin": "xiāo", "meaning": "喧嚣，吵闹"},
    "垓": {"pinyin": "gāi", "meaning": "极远处，八荒之外"},
}


def load_data():
    """加载道德经数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"title": "道德经", "chapters": []}


def annotate_difficult_chars(text):
    """为疑难字添加拼音和释义标注"""
    result = text
    # 按字数降序排序，避免短词覆盖长词
    sorted_chars = sorted(DIFFICULT_CHARS.items(), key=lambda x: -len(x[0]))

    for char, info in sorted_chars:
        pinyin = info['pinyin']
        meaning = info['meaning']
        # 使用 Bootstrap tooltip
        pattern = re.compile(re.escape(char))
        replacement = f'<span class="difficult" data-bs-toggle="tooltip" data-bs-placement="top" title="{pinyin}: {meaning}">{char}</span>'
        result = pattern.sub(replacement, result)

    return result


def get_chapter_content(chapter_id):
    """获取指定章节的内容，并处理疑难字标注"""
    data = load_data()
    chapter = next((c for c in data['chapters'] if c['chapter'] == chapter_id), None)

    if chapter:
        # 为原文添加疑难字标注
        chapter['original_annotated'] = annotate_difficult_chars(chapter.get('original', ''))
        # 获取相邻章节
        idx = data['chapters'].index(chapter)
        chapter['prev_chapter'] = data['chapters'][idx - 1] if idx > 0 else None
        chapter['next_chapter'] = data['chapters'][idx + 1] if idx < len(data['chapters']) - 1 else None
        chapter['total_chapters'] = len(data['chapters'])

    return chapter, data


# ==================== 路由定义 ====================

@app.route('/')
def index():
    """首页重定向"""
    return redirect(url_for('daodejing_index'))


@app.route('/daodejing/')
def daodejing_index():
    """道德经首页 - 章节目录"""
    data = load_data()
    return render_template('ddj/index.html', data=data)


@app.route('/daodejing/chapter/<int:chapter_id>')
def chapter_view(chapter_id):
    """单章阅读页"""
    if chapter_id < 1 or chapter_id > 81:
        return redirect(url_for('daodejing_index'))

    chapter, data = get_chapter_content(chapter_id)
    return render_template('ddj/chapter.html', chapter=chapter, data=data)


@app.route('/daodejing/compare/<int:chapter_id>')
def compare_view(chapter_id):
    """多版本对照页"""
    if chapter_id < 1 or chapter_id > 81:
        return redirect(url_for('daodejing_index'))

    chapter, data = get_chapter_content(chapter_id)
    return render_template('ddj/compare.html', chapter=chapter, data=data)


# ==================== API 路由 ====================

@app.route('/api/daodejing/chapters')
def api_chapters():
    """API: 获取所有章节列表"""
    data = load_data()
    chapters_list = [{'id': c['chapter'], 'title': f'第{c["chapter"]}章'} for c in data['chapters']]
    return jsonify({
        'title': data['title'],
        'subtitle': data.get('subtitle', ''),
        'chapters': chapters_list
    })


@app.route('/api/daodejing/chapter/<int:chapter_id>')
def api_chapter(chapter_id):
    """API: 获取单章数据"""
    chapter, _ = get_chapter_content(chapter_id)
    if chapter:
        return jsonify(chapter)
    return jsonify({'error': 'Chapter not found'}), 404


@app.route('/api/daodejing/search')
def api_search():
    """API: 搜索章节"""
    query = request.args.get('q', '')
    data = load_data()
    results = []

    if query:
        query_lower = query.lower()
        for chapter in data['chapters']:
            # 在原文中搜索
            if query_lower in chapter.get('original', '').lower():
                results.append({
                    'id': chapter['chapter'],
                    'title': f'第{chapter["chapter"]}章',
                    'excerpt': chapter.get('original', '')[:100] + '...'
                })
            # 在现代译文中搜索
            elif query_lower in chapter.get('modern_chinese', '').lower():
                results.append({
                    'id': chapter['chapter'],
                    'title': f'第{chapter["chapter"]}章',
                    'excerpt': chapter.get('modern_chinese', '')[:100] + '...'
                })

    return jsonify({'query': query, 'results': results})


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('ddj/index.html', data=load_data()), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('ddj/index.html', data=load_data()), 500


# ==================== 启动配置 ====================
