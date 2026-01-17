# -*- coding: utf-8 -*-
"""
道德经 - Vercel Python 部署
完整版本，使用模板文件
"""

import sys
import os
import json
import re
from pathlib import Path

# 设置路径
project_root = Path('/var/task')
if not project_root.exists():
    project_root = Path(__file__).parent.parent

sys.path.insert(0, str(project_root))
os.chdir(project_root)

from flask import Flask, jsonify, request, render_template

# 设置模板和静态文件路径
template_folder = str(project_root / 'templates')
static_folder = str(project_root / 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# 疑难字标注
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


def annotate_difficult_chars(text):
    """为疑难字添加拼音和释义标注"""
    sorted_chars = sorted(DIFFICULT_CHARS.items(), key=lambda x: -len(x[0]))
    placeholders = {}
    temp_text = text

    for char, info in sorted_chars:
        pinyin = info['pinyin']
        meaning = info['meaning']

        start = 0
        while True:
            pos = temp_text.find(char, start)
            if pos == -1:
                break

            placeholder = f"___PH_{len(placeholders)}___"
            span_html = f'<span class="difficult" data-pinyin="{pinyin}" data-meaning="{meaning}">{char}</span>'
            temp_text = temp_text[:pos] + placeholder + temp_text[pos + len(char):]
            placeholders[placeholder] = span_html
            start = pos + len(placeholder)

    result = temp_text
    for placeholder, html in placeholders.items():
        result = result.replace(placeholder, html)

    return result


def load_data():
    """加载道德经数据"""
    data_file = project_root / 'data' / 'daodejing.json'
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"title": "道德经", "chapters": []}


def get_chapter_with_annotation(chapter_id):
    """获取章节内容（带标注）"""
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


# 路由
@app.route('/')
def index():
    return render_template('ddj/index.html', data=load_data())


@app.route('/daodejing/')
def daodejing_index():
    data = load_data()
    return render_template('ddj/index.html', data=data)


@app.route('/daodejing/chapter/<int:chapter_id>')
def chapter_view(chapter_id):
    if chapter_id < 1 or chapter_id > 81:
        return render_template('ddj/index.html', data=load_data())

    chapter, data = get_chapter_with_annotation(chapter_id)
    return render_template('ddj/chapter.html', chapter=chapter, data=data)


@app.route('/daodejing/compare/<int:chapter_id>')
def compare_view(chapter_id):
    if chapter_id < 1 or chapter_id > 81:
        return render_template('ddj/index.html', data=load_data())

    chapter, data = get_chapter_with_annotation(chapter_id)
    return render_template('ddj/compare.html', chapter=chapter, data=data)


# API 路由
@app.route('/api/daodejing/chapters')
def api_chapters():
    data = load_data()
    chapters_list = [
        {'id': c['chapter'], 'title': f'第{c["chapter"]}章'}
        for c in data['chapters']
    ]
    return jsonify({
        'title': data['title'],
        'subtitle': data.get('subtitle', ''),
        'chapters': chapters_list
    })


@app.route('/api/daodejing/chapter/<int:chapter_id>')
def api_chapter(chapter_id):
    chapter, _ = get_chapter_with_annotation(chapter_id)
    if chapter:
        return jsonify(chapter)
    return jsonify({'error': 'Chapter not found'}), 404


@app.route('/api/daodejing/search')
def api_search():
    """高级搜索 - 支持多范围搜索和正则表达式"""
    query = request.args.get('q', '').strip()
    scope = request.args.get('scope', 'all')  # all, original, translation, commentary, english, ancient, idiom
    use_regex = request.args.get('regex', 'false').lower() == 'true'

    if not query or len(query) > 100:
        return jsonify({'query': query, 'results': [], 'count': 0})

    data = load_data()
    results = []

    # 编译正则表达式（如果启用）
    regex_pattern = None
    if use_regex:
        try:
            regex_pattern = re.compile(query, re.IGNORECASE | re.MULTILINE)
        except re.error:
            # 正则表达式无效，回退到普通搜索
            use_regex = False

    # 搜索范围配置
    search_fields = {
        'original': ['original'],
        'translation': ['modern_chinese'],
        'commentary': ['wangbi_note', 'heshanggong_note', 'wangfuzhi_note', 'hanshandeqing_note'],
        'english': ['english_lau', 'english_henricks', 'english_addiss'],
        'ancient': ['postsilk_text', 'guodian_text'],
        'all': ['original', 'modern_chinese', 'wangbi_note', 'heshanggong_note',
                'wangfuzhi_note', 'hanshandeqing_note', 'english_lau',
                'english_henricks', 'english_addiss', 'postsilk_text', 'guodian_text']
    }

    fields_to_search = search_fields.get(scope, search_fields['all'])

    # 成语数据
    idiom_results = []
    if scope in ['all', 'idiom']:
        idioms_file = project_root / 'data' / 'idioms.json'
        try:
            with open(idioms_file, 'r', encoding='utf-8') as f:
                idioms_data = json.load(f)
                for idiom in idioms_data.get('idioms', []):
                    match_found = False
                    match_reason = []

                    # 在成语词语中搜索
                    if use_regex:
                        if regex_pattern.search(idiom.get('word', '')):
                            match_found = True
                            match_reason.append('词语')
                    else:
                        if query.lower() in idiom.get('word', '').lower():
                            match_found = True
                            match_reason.append('词语')

                    # 在释义中搜索
                    if not match_found:
                        if use_regex:
                            if regex_pattern.search(idiom.get('meaning', '')):
                                match_found = True
                                match_reason.append('释义')
                        else:
                            if query.lower() in idiom.get('meaning', '').lower():
                                match_found = True
                                match_reason.append('释义')

                    # 在原文出处中搜索
                    if not match_found:
                        if use_regex:
                            if regex_pattern.search(idiom.get('source', '')):
                                match_found = True
                                match_reason.append('出处')
                        else:
                            if query.lower() in idiom.get('source', '').lower():
                                match_found = True
                                match_reason.append('出处')

                    if match_found:
                        idiom_results.append({
                            'type': 'idiom',
                            'id': f"idiom_{idiom['word']}",
                            'title': idiom['word'],
                            'meaning': idiom['meaning'],
                            'chapter': idiom.get('chapter'),
                            'source': idiom.get('source', ''),
                            'match_reason': match_reason
                        })
        except FileNotFoundError:
            pass

    # 章节数据搜索
    for chapter in data['chapters']:
        chapter_matches = []

        for field in fields_to_search:
            content = chapter.get(field, '')
            if not content:
                continue

            match_found = False
            matched_text = ''

            if use_regex:
                match = regex_pattern.search(content)
                if match:
                    match_found = True
                    # 获取匹配位置周围的文本
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    prefix = '...' if start > 0 else ''
                    suffix = '...' if end < len(content) else ''
                    matched_text = prefix + content[start:end] + suffix
            else:
                if query.lower() in content.lower():
                    match_found = True
                    # 获取匹配位置周围的文本
                    idx = content.lower().find(query.lower())
                    start = max(0, idx - 30)
                    end = min(len(content), idx + len(query) + 30)
                    prefix = '...' if start > 0 else ''
                    suffix = '...' if end < len(content) else ''
                    matched_text = prefix + content[start:end] + suffix

            if match_found:
                # 确定字段显示名称
                field_names = {
                    'original': '原文',
                    'modern_chinese': '白话译文',
                    'wangbi_note': '王弼注',
                    'heshanggong_note': '河上公注',
                    'wangfuzhi_note': '王夫之注',
                    'hanshandeqing_note': '憨山德清注',
                    'english_lau': '英译(Lau)',
                    'english_henricks': '英译(Henricks)',
                    'english_addiss': '英译(Addiss)',
                    'postsilk_text': '马王堆帛书',
                    'guodian_text': '郭店楚简'
                }

                chapter_matches.append({
                    'field': field_names.get(field, field),
                    'text': matched_text
                })

        if chapter_matches:
            results.append({
                'type': 'chapter',
                'id': chapter['chapter'],
                'title': f'第{chapter["chapter"]}章',
                'matches': chapter_matches,
                'excerpt': chapter_matches[0]['text']  # 主要匹配用于预览
            })

    # 合并成语和章节结果
    all_results = idiom_results + results

    return jsonify({
        'query': query,
        'scope': scope,
        'regex': use_regex,
        'count': len(all_results),
        'results': all_results
    })


@app.route('/api/daodejing/idioms')
def api_idioms():
    """获取成语列表"""
    idioms_file = project_root / 'data' / 'idioms.json'
    try:
        with open(idioms_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'idioms': []})


@app.route('/api/daodejing/user/bookmarks', methods=['GET', 'POST', 'DELETE'])
def api_bookmarks():
    """用户书签管理"""
    from flask import request
    import json

    if request.method == 'GET':
        # 获取所有书签
        bookmarks_json = request.args.get('data', '{}')
        if bookmarks_json:
            try:
                bookmark_ids = json.loads(bookmarks_json)
                data = load_data()
                bookmarks = [c for c in data['chapters'] if c['chapter'] in bookmark_ids]
                return jsonify({'bookmarks': bookmarks})
            except:
                return jsonify({'bookmarks': []})
        return jsonify({'bookmarks': []})

    # 对于POST/DELETE，返回成功，实际存储在客户端localStorage
    return jsonify({'success': True})


@app.route('/api/daodejing/user/notes', methods=['GET', 'POST'])
def api_notes():
    """用户笔记管理"""
    from flask import request, jsonify

    if request.method == 'POST':
        # 保存笔记（实际存储在客户端localStorage）
        data = request.get_json()
        return jsonify({'success': True, 'note': data})

    return jsonify({'notes': []})


# 错误处理器
@app.errorhandler(404)
def not_found(error):
    return render_template('ddj/index.html', data=load_data()), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('ddj/index.html', data=load_data()), 500


# Vercel 入口点
vercel_app = app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
