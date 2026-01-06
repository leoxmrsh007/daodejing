# -*- coding: utf-8 -*-
"""
道德经多版本对照平台 - Flask 主应用
"""

import os
import json
import re
import requests
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response

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
    # 按字数降序排序，先处理长词（如"玄牝"、"谷神"）
    sorted_chars = sorted(DIFFICULT_CHARS.items(), key=lambda x: -len(x[0]))

    # 使用占位符记录已标注的内容，避免嵌套
    placeholders = {}
    temp_text = text

    for char, info in sorted_chars:
        pinyin = info['pinyin']
        meaning = info['meaning']

        # 在临时文本中查找并替换
        start = 0
        while True:
            pos = temp_text.find(char, start)
            if pos == -1:
                break

            # 执行替换，使用占位符
            placeholder = f"___PH_{len(placeholders)}___"
            span_html = f'<span class="difficult" data-pinyin="{pinyin}" data-meaning="{meaning}">{char}</span>'
            temp_text = temp_text[:pos] + placeholder + temp_text[pos + len(char):]
            placeholders[placeholder] = span_html
            start = pos + len(placeholder)

    # 将所有占位符替换回实际的HTML
    result = temp_text
    for placeholder, html in placeholders.items():
        result = result.replace(placeholder, html)

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


@app.route('/api/tts/fish-audio', methods=['POST'])
def fish_audio_proxy():
    """Fish Audio TTS 代理端点 - 解决CORS问题"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        api_key = data.get('api_key')
        text = data.get('text')
        model_id = data.get('model_id')

        if not api_key or not text:
            return jsonify({'error': 'Missing api_key or text'}), 400

        # 构建Fish Audio API请求
        fish_api_url = 'https://api.fish.audio/v1/tts'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        request_body = {
            'text': text,
            'format': 'mp3'
        }

        # 如果提供了model_id，添加到请求体
        if model_id:
            request_body['model_id'] = model_id

        # 发送请求到Fish Audio API
        response = requests.post(
            fish_api_url,
            headers=headers,
            json=request_body,
            timeout=30
        )

        # 如果请求成功，返回音频数据
        if response.status_code == 200:
            return Response(
                response.content,
                mimetype='audio/mpeg',
                headers={
                    'Content-Disposition': 'attachment; filename=tts.mp3'
                }
            )
        else:
            # 返回错误信息
            return jsonify({
                'error': f'Fish Audio API error: {response.status_code}',
                'detail': response.text
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/tts/edge', methods=['POST'])
def edge_tts_proxy():
    """Edge TTS 代理端点 - 微软免费TTS"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        text = data.get('text')
        voice = data.get('voice', 'zh-CN-XiaoxiaoNeural')

        if not text:
            return jsonify({'error': 'Missing text'}), 400

        # 使用Edge TTS的公共API
        # 构建SSML格式
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN"><voice name="{voice}">{text}</voice></speak>'

        # Edge TTS API端点
        edge_tts_url = 'https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1'

        headers = {
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.post(
            edge_tts_url,
            headers=headers,
            data=ssml.encode('utf-8'),
            timeout=30
        )

        if response.status_code == 200:
            return Response(
                response.content,
                mimetype='audio/mpeg',
                headers={
                    'Content-Disposition': 'attachment; filename=tts.mp3'
                }
            )
        else:
            return jsonify({
                'error': f'Edge TTS error: {response.status_code}',
                'detail': response.text[:500]
            }), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 502
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('ddj/index.html', data=load_data()), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('ddj/index.html', data=load_data()), 500


# ==================== 启动配置 ====================

# Vercel 无服务器函数入口
# 从 Vercel 的 Python 运行时导入 app
app = app

# 本地开发入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
