# -*- coding: utf-8 -*-
"""
性能监控模块 - 监控API响应时间和性能指标
"""

import time
from functools import wraps
from typing import Any, Callable, Dict

# 性能指标存储
_performance_metrics: Dict[str, list] = {}


def monitor_performance(endpoint: str) -> Callable[..., Any]:
    """
    API性能监控装饰器
    记录API响应时间
    """

    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()

            try:
                result = f(*args, **kwargs)
                duration_ms = (time.time() - start_time) * 1000

                if endpoint not in _performance_metrics:
                    _performance_metrics[endpoint] = []
                _performance_metrics[endpoint].append(
                    {
                        "timestamp": start_time,
                        "duration_ms": duration_ms,
                        "status": "success",
                    }
                )

                # 警告慢响应（>300ms）
                if duration_ms > 300:
                    print(
                        f"[Performance] 慢API响应: {endpoint} ({duration_ms:.0f}ms > 300ms)"
                    )

                return result

            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000

                if endpoint not in _performance_metrics:
                    _performance_metrics[endpoint] = []
                _performance_metrics[endpoint].append(
                    {
                        "timestamp": start_time,
                        "duration_ms": duration_ms,
                        "status": "error",
                    }
                )

                raise e

        return wrapper

    return decorator


def get_performance_summary() -> Dict[str, Any]:
    """
    获取性能指标摘要

    Returns:
        各端点的性能统计
    """
    summary = {}

    for endpoint, records in _performance_metrics.items():
        if not records:
            continue

        total_requests = len(records)
        successful_requests = len([r for r in records if r["status"] == "success"])
        failed_requests = len([r for r in records if r["status"] == "error"])

        durations = [r["duration_ms"] for r in records]
        avg_duration = sum(durations) / len(durations) if durations else 0
        max_duration = max(durations) if durations else 0
        p95_duration = (
            sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 1 else 0
        )
        p99_duration = (
            sorted(durations)[int(len(durations) * 0.99)] if len(durations) > 1 else 0
        )

        summary[endpoint] = {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (
                f"{(successful_requests / total_requests * 100):.1f}%"
                if total_requests > 0
                else "0%"
            ),
            "avg_duration_ms": f"{avg_duration:.1f}",
            "max_duration_ms": f"{max_duration:.1f}",
            "p95_duration_ms": f"{p95_duration:.1f}",
            "p99_duration_ms": f"{p99_duration:.1f}",
        }

    return summary


def get_all_performance_metrics() -> Dict[str, list]:
    """
    获取所有原始性能数据
    """
    return _performance_metrics.copy()


def clear_performance_metrics() -> None:
    """
    清除性能指标
    """
    _performance_metrics.clear()
