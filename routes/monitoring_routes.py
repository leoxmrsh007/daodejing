# -*- coding: utf-8 -*-
"""
性能监控 API 端点
提供缓存统计、API响应时间、系统性能指标
"""

from datetime import datetime
from typing import Literal, Tuple

from flask import Blueprint, Response, jsonify, request

from utils.cache import get_all_cache_stats, reset_all_cache_stats

bp = Blueprint("monitoring", __name__, url_prefix="/monitoring")


# ============ 性能统计端点 ============


@bp.route("/stats")
def get_stats() -> Response:
    """
    获取性能统计信息
    """
    stats = {
        "timestamp": datetime.now().isoformat(),
        "cache": get_all_cache_stats(),
    }
    return jsonify(stats)


@bp.route("/cache")
def get_cache_stats() -> Response:
    """
    获取缓存统计信息
    """
    stats = get_all_cache_stats()
    return jsonify(stats)


@bp.route("/cache/reset", methods=["POST"])
def reset_cache_stats() -> Response:
    """
    重置缓存统计
    """
    reset_all_cache_stats()
    return jsonify({"status": "success", "message": "缓存统计已重置"})


@bp.route("/health")
def health_check() -> Response:
    """
    健康检查端点
    """
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "services": {
                "api": "up",
                "cache": "up",
            },
        }
    )


@bp.route("/metrics", methods=["POST"])
def record_metrics() -> Response | Tuple[Response, Literal[500]]:
    """
    记录前端性能指标
    """
    try:
        data = request.get_json() or {}

        metrics = {
            "timestamp": datetime.now().isoformat(),
            "url": data.get("url", request.headers.get("Referer", "")),
            "user_agent": data.get("userAgent", request.headers.get("User-Agent", "")),
            "metrics": data.get("metrics", {}),
        }

        # 这里可以记录到日志或分析系统
        # 目前只返回成功状态
        print(f"[Metrics] Performance data received from {metrics['url']}")

        return jsonify({"status": "success", "message": "指标已记录"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route("/slow-requests")
def get_slow_requests() -> Response:
    """
    获取慢请求列表
    """
    # 这里可以从日志系统或数据库查询慢请求
    # 目前返回示例数据
    return jsonify(
        {"slow_requests": [], "threshold_ms": 3000, "message": "慢请求记录功能待实现"}
    )
