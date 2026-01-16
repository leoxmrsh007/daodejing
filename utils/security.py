# -*- coding: utf-8 -*-
"""
安全工具 - 速率限制、CORS、安全头
"""

import time
from functools import wraps
from flask import request, jsonify
from typing import Callable, Dict


class RateLimiter:
    """
    简单的内存速率限制器
    注意：生产环境应使用 Redis 等外部存储
    """

    def __init__(self):
        self._requests: Dict[str, list] = {}

    def is_allowed(self, key: str, max_requests: int = 10, window: int = 60) -> bool:
        """
        检查是否允许请求

        Args:
            key: 请求标识符（如 IP 地址）
            max_requests: 时间窗口内最大请求数
            window: 时间窗口（秒）

        Returns:
            是否允许请求
        """
        now = time.time()

        if key not in self._requests:
            self._requests[key] = []

        # 清理过期记录
        self._requests[key] = [
            timestamp for timestamp in self._requests[key]
            if now - timestamp < window
        ]

        # 检查是否超过限制
        if len(self._requests[key]) >= max_requests:
            return False

        # 记录本次请求
        self._requests[key].append(now)
        return True

    def clear(self, key: str = None):
        """清理记录"""
        if key:
            self._requests.pop(key, None)
        else:
            self._requests.clear()


# 全局限流器实例
_rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 10, window: int = 60):
    """
    速率限制装饰器

    Args:
        max_requests: 时间窗口内最大请求数
        window: 时间窗口（秒）

    Usage:
        @app.route('/api/search')
        @rate_limit(max_requests=20, window=60)
        def search():
            ...
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            # 使用 IP 地址作为标识符
            key = request.remote_addr or 'unknown'

            if not _rate_limiter.is_allowed(key, max_requests, window):
                return jsonify({
                    'error': 'Too many requests',
                    'retry_after': window
                }), 429

            return f(*args, **kwargs)
        return wrapper
    return decorator


def get_client_ip() -> str:
    """
    获取客户端真实 IP 地址

    Returns:
        IP 地址字符串
    """
    # 检查代理头
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr or 'unknown'


def get_security_headers() -> Dict[str, str]:
    """
    获取推荐的安全响应头

    Returns:
        安全头字典
    """
    return {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
    }


def add_security_headers(response):
    """
    为 Flask 响应添加安全头

    Args:
        response: Flask Response 对象

    Returns:
        修改后的 Response 对象
    """
    for key, value in get_security_headers().items():
        response.headers[key] = value
    return response


def get_cors_config() -> Dict:
    """
    获取 CORS 配置

    Returns:
        CORS 配置字典
    """
    return {
        'origins': '*',  # 生产环境应限制为具体域名
        'methods': ['GET', 'POST', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization'],
        'max_age': 3600,
        'vary_header': True
    }


def init_security(app):
    """
    初始化应用安全配置

    Args:
        app: Flask 应用实例
    """
    # 添加安全头到所有响应
    @app.after_request
    def apply_security_headers(response):
        return add_security_headers(response)

    # CORS 处理（简单实现）
    @app.before_request
    def handle_cors():
        if request.method == 'OPTIONS':
            response = jsonify({'status': 'ok'})
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Max-Age'] = '3600'
            return response
