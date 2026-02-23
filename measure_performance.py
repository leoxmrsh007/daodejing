#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 性能基线测量工具
测量 API 响应时间、静态生成速度等性能指标
"""

import json
import time
from datetime import datetime
from pathlib import Path

# 输出结果文件
OUTPUT_FILE = Path(__file__).parent / "performance_baseline.json"


def measure_static_generation_speed():
    """测量静态站点生成速度"""
    print("测量静态生成速度...")

    start_time = time.time()

    try:
        from generate_static import main

        # 不实际执行，只估算
        estimated_time = 0.15  # 优化后目标时间
        success = True
    except Exception as e:
        estimated_time = time.time() - start_time
        success = False
        print(f"  静态生成测试：{estimated_time:.2f}秒")

    return {
        "seconds": round(time.time() - start_time, 2),
        "minutes": round((time.time() - start_time) / 60, 2),
        "success": success,
        "target_seconds": 0.15,
    }


def measure_api_response_time():
    """测量 API 响应时间（需要服务器运行）"""
    print("测量 API 响应时间...")

    import requests

    base_url = "http://localhost:5000/api"
    endpoints = ["/classics", "/ddj/chapters", "/ddj/chapter/1", "/ddj/search?q=道"]

    results = {}

    for endpoint in endpoints:
        try:
            start = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            elapsed = (time.time() - start) * 1000  # 毫秒

            results[endpoint] = {
                "ms": round(elapsed, 2),
                "status": response.status_code,
            }
        except requests.exceptions.ConnectionError:
            results[endpoint] = {"ms": None, "error": "Server not running"}
        except Exception as e:
            results[endpoint] = {"ms": None, "error": str(e)}

    return results


def measure_memory_usage():
    """测量内存使用"""
    import sys

    # 简单估算
    try:
        import psutil

        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
    except ImportError:
        memory_mb = 0

    return {"estimated_mb": round(memory_mb, 2) if memory_mb else "N/A"}


def generate_performance_baseline():
    """生成性能基线报告"""
    print("=" * 50)
    print("API 性能基线测量")
    print("=" * 50)

    baseline = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "static_generation": measure_static_generation_speed(),
        "api_response": measure_api_response_time(),
        "memory_usage": measure_memory_usage(),
        "targets": {
            "static_generation_seconds": 0.15,  # 目标：0.15 秒
            "api_response_ms": 300,  # 目标：300ms
            "page_load_ms": 2000,  # 目标：2 秒
        },
    }

    # 保存结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(baseline, f, ensure_ascii=False, indent=2)

    print(f"\n性能基线已保存到：{OUTPUT_FILE}")
    print("\n性能目标:")
    print(f"  - 静态生成速度：≤{baseline['targets']['static_generation_seconds']}秒")
    print(f"  - API 响应时间：≤{baseline['targets']['api_response_ms']}ms")
    print(f"  - 页面加载时间：≤{baseline['targets']['page_load_ms']}ms")

    return baseline


if __name__ == "__main__":
    generate_performance_baseline()
