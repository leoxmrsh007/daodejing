# -*- coding: utf-8 -*-
"""
安全工具 - 速率限制、CORS、安全头
"""

import os
import time
from functools import wraps
from typing import Any, Callable, Dict, Optional

from flask import Flask, Response, jsonify, request


class RateLimiter:
    """
    简单的内存速率限制器
    注意：生产环境应使用 Redis 等外部存储
    """

    def __init__(self) -> None:
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
            timestamp for timestamp in self._requests[key] if now - timestamp < window
        ]

        # 检查是否超过限制
        if len(self._requests[key]) >= max_requests:
            return False

        # 记录本次请求
        self._requests[key].append(now)
        return True

    def clear(self, key: Optional[str] = None) -> None:
        """清理记录"""
        if key:
            self._requests.pop(key, None)
        else:
            self._requests.clear()


# 全局限流器实例
_rate_limiter = RateLimiter()


def rate_limit(
    max_requests: int = 10, window: int = 60
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
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

    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 使用 IP 地址作为标识符
            key = request.remote_addr or "unknown"

            if not _rate_limiter.is_allowed(key, max_requests, window):
                return (
                    jsonify({"error": "Too many requests", "retry_after": window}),
                    429,
                )

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
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for is not None:
        return x_forwarded_for.split(",")[0].strip()
    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip is not None:
        return x_real_ip
    remote_addr = request.remote_addr
    if remote_addr is not None:
        return remote_addr
    return "unknown"


def get_security_headers() -> Dict[str, str]:
    """
    获取推荐的安全响应头

    Returns:
        安全头字典
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }


def add_security_headers(response: Response) -> Response:
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
    # 从环境变量获取允许的来源
    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")

    # 生产环境安全检查
    if os.environ.get("FLASK_ENV") == "production" and allowed_origins == "*":
        import warnings

        warnings.warn(
            "生产环境CORS配置允许所有来源('*')，存在安全风险。"
            "请设置ALLOWED_ORIGINS环境变量限制具体域名。"
        )

    return {
        "origins": (
            allowed_origins.split(",") if "," in allowed_origins else allowed_origins
        ),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "max_age": 3600,
        "vary_header": True,
    }


def init_security(app: Flask) -> None:
    """
    初始化应用安全配置

    Args:
        app: Flask 应用实例
    """

    # 添加安全头到所有响应
    @app.after_request
    def apply_security_headers(response: Response) -> Response:
        return add_security_headers(response)

    # CORS 配置
    cors_config = get_cors_config()

    # CORS 处理
    @app.after_request
    def apply_cors_headers(response: Response) -> Response:
        """为所有响应添加CORS头"""
        origin = request.headers.get("Origin")
        if origin:
            # 检查来源是否在允许列表中
            allowed_origins = cors_config["origins"]
            if allowed_origins == "*" or origin in allowed_origins:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = ", ".join(
                    cors_config["methods"]
                )
                response.headers["Access-Control-Allow-Headers"] = ", ".join(
                    cors_config["allow_headers"]
                )
                response.headers["Access-Control-Max-Age"] = str(cors_config["max_age"])
                response.headers["Vary"] = "Origin"
        return response

    # OPTIONS 预检请求处理
    @app.before_request
    def handle_options_request() -> Optional[Response]:
        if request.method == "OPTIONS":
            response = jsonify({"status": "ok"})
            origin = request.headers.get("Origin")
            if origin:
                allowed_origins = cors_config["origins"]
                if allowed_origins == "*" or origin in allowed_origins:
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Methods"] = ", ".join(
                        cors_config["methods"]
                    )
                    response.headers["Access-Control-Allow-Headers"] = ", ".join(
                        cors_config["allow_headers"]
                    )
                    response.headers["Access-Control-Max-Age"] = str(
                        cors_config["max_age"]
                    )
                    response.headers["Vary"] = "Origin"
            return response
        return None
