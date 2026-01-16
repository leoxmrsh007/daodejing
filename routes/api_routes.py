# -*- coding: utf-8 -*-
"""
API 路由 - JSON API 端点
"""

from flask import Blueprint, jsonify, request
from services.data_service import DataService
from services.tts_service import fish_audio_service, edge_tts_service
from utils.validators import validate_search_query
from utils.security import rate_limit

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/daodejing/chapters')
def api_chapters():
    """API: 获取所有章节列表"""
    data = DataService.load_data()
    chapters_list = [
        {'id': c['chapter'], 'title': f'第{c["chapter"]}章'}
        for c in data['chapters']
    ]
    return jsonify({
        'title': data['title'],
        'subtitle': data.get('subtitle', ''),
        'chapters': chapters_list
    })


@bp.route('/daodejing/chapter/<int:chapter_id>')
def api_chapter(chapter_id):
    """API: 获取单章数据"""
    chapter = DataService.get_chapter_with_annotation(chapter_id)
    if chapter:
        return jsonify(chapter)
    return jsonify({'error': 'Chapter not found'}), 404


@bp.route('/daodejing/search')
@rate_limit(max_requests=30, window=60)
def api_search():
    """API: 搜索章节（带输入验证和速率限制）"""
    query = request.args.get('q', '')

    # 验证输入
    is_valid, error_msg = validate_search_query(query)
    if not is_valid and query:
        return jsonify({'error': error_msg}), 400

    results = DataService.search_chapters(query)
    return jsonify({'query': query, 'results': results})


@bp.route('/tts/fish-audio', methods=['POST'])
@rate_limit(max_requests=10, window=60)
def fish_audio():
    """API: Fish Audio TTS 代理（带速率限制）"""
    return fish_audio_service.synthesize()


@bp.route('/tts/edge', methods=['POST'])
@rate_limit(max_requests=20, window=60)
def edge_tts():
    """API: Edge TTS 代理（带速率限制）"""
    return edge_tts_service.synthesize()
