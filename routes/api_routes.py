# -*- coding: utf-8 -*-
"""
API 路由 - JSON API 端点
支持多经典：道德经、庄子等
"""

from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

from flask import Blueprint, Response, jsonify, request

from services.classic_service import (
    ClassicService,
    get_all_classics,
    get_default_classic_id,
)
from services.cross_civilization_dialogue import (
    get_available_philosophers,
    get_comparative_analysis,
    get_concept_correspondences,
    start_philosophy_dialogue,
)
from services.knowledge_graph import get_all_concepts, get_chapter_knowledge_graph
from services.semantic_archaeology import (
    get_chapter_archaeology,
    get_concept_interpretation_history,
)
from services.tts_service import edge_tts_service, fish_audio_service
from services.virtual_commentator import (
    generate_commentary_response,
    get_available_commentators,
    get_commentator_persona,
)
from utils.security import rate_limit
from utils.validators import validate_search_query

bp = Blueprint("api", __name__, url_prefix="/api")


# ============ 健康检查 API ============


@bp.route("/health")
def api_health() -> Response:
    """健康检查端点"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "services": {
                "api": "up",
                "data": "up",
            },
        }
    )


# ============ 经典管理 API ============


@bp.route("/classics")
def api_classics() -> Response:
    """API: 获取所有经典列表"""
    classics = get_all_classics()
    return jsonify({"classics": classics, "default": get_default_classic_id()})


@bp.route("/<classic_id>/meta")
def api_classic_meta(classic_id: str) -> Response:
    """API: 获取指定经典的元数据"""
    service = ClassicService(classic_id)
    return jsonify(service.to_dict())


# ============ 章节内容 API ============


@bp.route("/<classic_id>/chapters")
def api_chapters(classic_id: str) -> Response:
    """API: 获取经典所有章节列表"""
    service = ClassicService(classic_id)
    data = service.load_data()
    chapters_list = [
        {"id": c["chapter"], "title": c.get("title", f"第{c['chapter']}章")}
        for c in data["chapters"]
    ]
    return jsonify(
        {
            "classic_id": classic_id,
            "title": data["title"],
            "subtitle": data.get("subtitle", ""),
            "chapters": chapters_list,
        }
    )


@bp.route("/<classic_id>/chapter/<int:chapter_id>")
def api_chapter(
    classic_id: str, chapter_id: int
) -> Union[Response, Tuple[Response, int]]:
    """API: 获取单章数据"""
    service = ClassicService(classic_id)
    chapter = service.get_chapter_with_annotation(chapter_id)
    if chapter:
        return jsonify(chapter)
    return jsonify({"error": "Chapter not found"}), 404


@bp.route("/<classic_id>/search")
@rate_limit(max_requests=30, window=60)
def api_search(classic_id: str) -> Union[Response, Tuple[Response, int]]:
    """API: 搜索章节（带输入验证、速率限制和高级过滤）"""
    query = request.args.get("q", "")

    # 验证输入
    is_valid, error_msg = validate_search_query(query)
    if not is_valid and query:
        return jsonify({"error": error_msg}), 400

    # 获取过滤参数
    commentator = request.args.get("commentator")
    content_type = request.args.get("content_type")  # original/modern/notes/english
    fuzzy_threshold = int(request.args.get("fuzzy_threshold", "70"))
    limit = int(request.args.get("limit", "20"))

    # 验证过滤参数
    valid_content_types = ["original", "modern", "notes", "english"]
    if content_type and content_type not in valid_content_types:
        return (
            jsonify(
                {
                    "error": f"Invalid content_type. Must be one of: {', '.join(valid_content_types)}"
                }
            ),
            400,
        )

    service = ClassicService(classic_id)
    results = service.search_chapters(
        query,
        classic_id=classic_id,
        commentator=commentator,
        content_type=content_type,
        fuzzy_threshold=fuzzy_threshold,
        limit=limit,
    )

    return jsonify(
        {
            "query": query,
            "classic_id": classic_id,
            "filters": {
                "commentator": commentator,
                "content_type": content_type,
                "fuzzy_threshold": fuzzy_threshold,
            },
            "results": results,
        }
    )


# ============ 搜索历史 API ============


@bp.route("/search/history", methods=["POST"])
def api_search_history_add() -> Union[Response, Tuple[Response, int]]:
    """API: 添加搜索历史"""
    data = request.get_json() or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    # 搜索历史主要存储在客户端
    # 这里返回成功状态，实际由客户端管理
    return jsonify(
        {
            "status": "success",
            "message": "Search history is managed on client-side using localStorage",
        }
    )


@bp.route("/search/history", methods=["GET"])
def api_search_history_get() -> Response:
    """API: 获取搜索历史（客户端存储为主）"""
    return jsonify(
        {
            "message": "Search history is managed on client-side using localStorage",
            "hint": "Use localStorage.getItem('daodejing_search_history') on client-side",
        }
    )


@bp.route("/search/history", methods=["DELETE"])
def api_search_history_clear() -> Response:
    """API: 清空搜索历史"""
    return jsonify(
        {
            "status": "success",
            "message": "Search history is managed on client-side using localStorage",
        }
    )


# ============ 个性化推荐 API ============


@bp.route("/recommendations", methods=["GET", "POST"])
def api_recommendations() -> Union[Response, Tuple[Response, int]]:
    """API: 获取个性化推荐章节"""
    from services.classic_service import get_all_classics
    from services.fulltext_search import PersonalizedRecommender

    # 构建经典服务字典
    classic_services: Dict[str, Any] = {}
    for classic in get_all_classics():
        classic_id = classic.get("id")
        if classic_id:
            classic_services[str(classic_id)] = ClassicService(str(classic_id))

    # 初始化推荐系统
    recommender = PersonalizedRecommender(classic_services)

    # 获取用户历史（从客户端请求参数）
    data = request.get_json(silent=True) or {}
    user_history = data.get("history", [])
    limit = int(request.args.get("limit", "5"))

    # 转换用户历史格式：{classic_id, chapter_id}
    history_tuples: List[Tuple[str, int]] = []
    for item in user_history:
        classic_id = item.get("classic_id")
        chapter_id = item.get("chapter_id")
        if classic_id and chapter_id:
            history_tuples.append((str(classic_id), int(chapter_id)))

    # 获取推荐
    recommendations = recommender.recommend_chapters(history_tuples, limit=limit)

    return jsonify(
        {
            "recommendations": recommendations,
            "count": len(recommendations),
            "hint": "Send user history via POST body for personalized recommendations",
        }
    )


# ============ 向后兼容 API ============


@bp.route("/daodejing/chapters")
def api_daodejing_chapters() -> Response:
    """API: 获取道德经所有章节列表（向后兼容）"""
    return api_chapters("ddj")


@bp.route("/daodejing/chapter/<int:chapter_id>")
def api_daodejing_chapter(chapter_id: int) -> Union[Response, Tuple[Response, int]]:
    """API: 获取道德经单章数据（向后兼容）"""
    return api_chapter("ddj", chapter_id)


@bp.route("/daodejing/search")
@rate_limit(max_requests=30, window=60)
def api_daodejing_search() -> Any:
    """API: 搜索道德经章节（向后兼容）"""
    return api_search("ddj")


@bp.route("/tts/fish-audio", methods=["POST"])
@rate_limit(max_requests=10, window=60)
def fish_audio() -> Any:
    """API: Fish Audio TTS 代理（带速率限制）"""
    return fish_audio_service.synthesize()


@bp.route("/tts/edge", methods=["POST"])
@rate_limit(max_requests=20, window=60)
def edge_tts() -> Any:
    """API: Edge TTS 代理（带速率限制）"""
    return edge_tts_service.synthesize()


# ============ AI创新功能 API ============


# 知识图谱 API
@bp.route("/knowledge/concepts")
def api_concepts() -> Response:
    """API: 获取所有概念列表"""
    concepts = get_all_concepts()
    return jsonify({"concepts": concepts})


@bp.route("/knowledge/graph/<int:chapter_id>")
def api_knowledge_graph(chapter_id: int) -> Response:
    """API: 获取章节知识图谱"""
    graph = get_chapter_knowledge_graph(chapter_id)
    return jsonify(graph)


# 语义考古学 API
@bp.route("/archaeology/<int:chapter_id>")
def api_archaeology(chapter_id: int) -> Response:
    """API: 获取章节语义考古分析"""
    result = get_chapter_archaeology(chapter_id)
    return jsonify(result)


@bp.route("/archaeology/<int:chapter_id>/concept/<concept>")
def api_concept_history(chapter_id: int, concept: str) -> Response:
    """API: 获取概念阐释历史"""
    result = get_concept_interpretation_history(chapter_id, concept)
    return jsonify(result)


# 跨文明对话 API
@bp.route("/dialogue/philosophers")
def api_philosophers() -> Response:
    """API: 获取可用哲学家列表"""
    philosophers = get_available_philosophers()
    return jsonify({"philosophers": philosophers})


@bp.route("/dialogue/start", methods=["POST"])
def api_start_dialogue() -> Response:
    """API: 发起哲学对话"""
    data = request.get_json() or {}
    chapter_id = data.get("chapter_id", 1)
    concept = data.get("concept", "道")
    philosopher1 = data.get("philosopher1", "zhuangzi")
    philosopher2 = data.get("philosopher2", "plato")

    result = start_philosophy_dialogue(chapter_id, concept, philosopher1, philosopher2)
    return jsonify(result)


@bp.route("/dialogue/compare", methods=["POST"])
def api_compare_philosophers() -> Response:
    """API: 跨文明比较分析"""
    data = request.get_json() or {}
    chapter_id = data.get("chapter_id", 1)
    concept = data.get("concept", "道")
    philosophers = data.get("philosophers", ["heidegger", "zhuangzi"])

    result = get_comparative_analysis(chapter_id, concept, philosophers)
    return jsonify(result)


@bp.route("/dialogue/correspondence/<concept>/<philosopher_id>")
def api_correspondences(concept: str, philosopher_id: str) -> Response:
    """API: 获取概念对应关系"""
    correspondences = get_concept_correspondences(concept, philosopher_id)
    return jsonify(
        {
            "concept": concept,
            "philosopher": philosopher_id,
            "correspondences": correspondences,
        }
    )


# 虚拟注释家对话 API
@bp.route("/commentary/commentators")
def api_commentators() -> Response:
    """API: 获取可用注释家列表"""
    commentators = get_available_commentators()
    return jsonify({"commentators": commentators})


@bp.route("/commentary/persona/<commentator_id>")
def api_commentator_persona(
    commentator_id: str,
) -> Union[Response, Tuple[Response, int]]:
    """API: 获取注释家人设"""
    persona = get_commentator_persona(commentator_id)
    if persona:
        return jsonify(persona)
    return jsonify({"error": "Commentator not found"}), 404


@bp.route("/commentary/chat", methods=["POST"])
def api_commentary_chat() -> Response:
    """API: 虚拟注释家对话"""
    data = request.get_json() or {}
    commentator_id = data.get("commentator_id", "wangbi")
    chapter_id = data.get("chapter_id", 1)
    question = data.get("question", "")

    result = generate_commentary_response(commentator_id, chapter_id, question)
    return jsonify(result)
