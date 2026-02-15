#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能基准测试脚本
测量当前性能基线，用于优化前后对比
"""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List


def measure_file_size(file_path: Path) -> Dict[str, int]:
    """测量文件大小"""
    if not file_path.exists():
        return {"bytes": 0, "kb": 0, "mb": 0}
    size_bytes = file_path.stat().st_size
    return {
        "bytes": size_bytes,
        "kb": round(size_bytes / 1024, 2),
        "mb": round(size_bytes / (1024 * 1024), 2),
    }


def measure_directory_size(dir_path: Path) -> Dict[str, int]:
    """测量目录总大小"""
    total_bytes = 0
    file_count = 0
    for file_path in dir_path.rglob("*"):
        if file_path.is_file():
            total_bytes += file_path.stat().st_size
            file_count += 1
    return {
        "bytes": total_bytes,
        "kb": round(total_bytes / 1024, 2),
        "mb": round(total_bytes / (1024 * 1024), 2),
        "file_count": file_count,
    }


def measure_js_bundle_size(static_dir: Path) -> Dict[str, Any]:
    """测量JavaScript包大小"""
    js_dir = static_dir / "js"
    results = {}

    if js_dir.exists():
        for js_file in js_dir.glob("**/*.js"):
            size = measure_file_size(js_file)
            results[str(js_file.relative_to(static_dir))] = size

        # 计算总计
        total_bytes = sum(r["bytes"] for r in results.values())
        results["_total"] = {
            "bytes": total_bytes,
            "kb": round(total_bytes / 1024, 2),
            "mb": round(total_bytes / (1024 * 1024), 2),
            "file_count": len(results),
        }
    return results


def measure_css_size(static_dir: Path) -> Dict[str, Any]:
    """测量CSS文件大小"""
    css_dir = static_dir / "css"
    results = {}

    if css_dir.exists():
        for css_file in css_dir.glob("**/*.css"):
            size = measure_file_size(css_file)
            results[str(css_file.relative_to(static_dir))] = size

        # 计算总计
        total_bytes = sum(r["bytes"] for r in results.values())
        results["_total"] = {
            "bytes": total_bytes,
            "kb": round(total_bytes / 1024, 2),
            "mb": round(total_bytes / (1024 * 1024), 2),
            "file_count": len(results),
        }
    return results


def measure_image_size(static_dir: Path) -> Dict[str, Any]:
    """测量图片大小"""
    image_exts = [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"]
    results = {}

    for ext in image_exts:
        for img_file in static_dir.rglob(f"*{ext}"):
            size = measure_file_size(img_file)
            results[str(img_file.relative_to(static_dir))] = size

    # 计算总计
    total_bytes = sum(r["bytes"] for r in results.values())
    results["_total"] = {
        "bytes": total_bytes,
        "kb": round(total_bytes / 1024, 2),
        "mb": round(total_bytes / (1024 * 1024), 2),
        "file_count": len(results),
    }
    return results


def measure_static_generation_time() -> Dict[str, float]:
    """测量静态站点生成时间"""
    generate_script = Path(__file__).parent.parent / "generate_static.py"
    if not generate_script.exists():
        return {"error": "generate_static.py not found"}

    start_time = time.time()
    try:
        result = subprocess.run(
            ["python", str(generate_script)],
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
        )
        elapsed_time = time.time() - start_time
        return {
            "seconds": round(elapsed_time, 2),
            "minutes": round(elapsed_time / 60, 2),
            "success": result.returncode == 0,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        return {
            "seconds": round(elapsed_time, 2),
            "minutes": round(elapsed_time / 60, 2),
            "error": "timeout",
        }
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            "seconds": round(elapsed_time, 2),
            "minutes": round(elapsed_time / 60, 2),
            "error": str(e),
        }


def measure_api_response_time(
    base_url: str = "http://localhost:5000",
) -> Dict[str, Any]:
    """测量API响应时间（需要服务器运行）"""
    import requests

    endpoints = [
        "/api/classics",
        "/api/ddj/chapters",
        "/api/ddj/chapter/1",
        "/api/ddj/search?q=道",
    ]

    results = {}
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            elapsed_time = time.time() - start_time
            results[endpoint] = {
                "ms": round(elapsed_time * 1000, 2),
                "status_code": response.status_code,
                "success": response.status_code == 200,
            }
        except requests.exceptions.RequestException as e:
            results[endpoint] = {"ms": None, "error": str(e)}

    # 计算平均响应时间
    times = [r.get("ms") for r in results.values() if r.get("ms") is not None]
    if times:
        results["_average"] = {
            "ms": round(sum(times) / len(times), 2),
            "count": len(times),
        }

    return results


def run_performance_benchmark(
    base_url: str = "http://localhost:5000",
) -> Dict[str, Any]:
    """运行完整的性能基准测试"""
    base_dir = Path(__file__).parent.parent
    static_dir = base_dir / "static"
    dist_dir = base_dir / "dist"

    print("=" * 60)
    print("🚀 性能基准测试开始")
    print("=" * 60)

    results = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "baseline": {}}

    # 1. 测量静态资源大小
    print("\n📊 测量静态资源大小...")
    results["baseline"]["static_dir"] = measure_directory_size(static_dir)

    # 2. 测量JavaScript包大小
    print("📦 测量JavaScript包大小...")
    js_sizes = measure_js_bundle_size(static_dir)
    results["baseline"]["js_bundles"] = js_sizes
    if "_total" in js_sizes:
        print(
            f"   JS总计: {js_sizes['_total']['kb']} KB ({js_sizes['_total']['file_count']} 文件)"
        )

    # 3. 测量CSS文件大小
    print("🎨 测量CSS文件大小...")
    css_sizes = measure_css_size(static_dir)
    results["baseline"]["css_files"] = css_sizes
    if "_total" in css_sizes:
        print(
            f"   CSS总计: {css_sizes['_total']['kb']} KB ({css_sizes['_total']['file_count']} 文件)"
        )

    # 4. 测量图片大小
    print("🖼️  测量图片大小...")
    img_sizes = measure_image_size(static_dir)
    results["baseline"]["images"] = img_sizes
    if "_total" in img_sizes:
        print(
            f"   图片总计: {img_sizes['_total']['mb']} MB ({img_sizes['_total']['file_count']} 文件)"
        )

    # 5. 测量静态生成时间
    print("\n⏱️  测量静态站点生成时间...")
    gen_time = measure_static_generation_time()
    results["baseline"]["static_generation"] = gen_time
    if "seconds" in gen_time:
        print(f"   生成时间: {gen_time['seconds']} 秒 ({gen_time['minutes']} 分钟)")

    # 6. 测量API响应时间（可选）
    print("\n🌐 测量API响应时间...")
    print("   提示: 需要服务器运行 (python app.py)")
    try:
        api_results = measure_api_response_time(base_url)
        results["baseline"]["api_responses"] = api_results
        if "_average" in api_results:
            print(f"   平均响应时间: {api_results['_average']['ms']} ms")
    except ImportError:
        print("   跳过API测试 (未安装requests库)")
        results["baseline"]["api_responses"] = {"skipped": "requests not installed"}

    # 7. 测量dist目录大小（如果存在）
    if dist_dir.exists():
        print("\n📁 测量dist目录大小...")
        dist_size = measure_directory_size(dist_dir)
        results["baseline"]["dist_dir"] = dist_size
        print(f"   dist总计: {dist_size['mb']} MB ({dist_size['file_count']} 文件)")

    # 8. 计算优化目标
    print("\n🎯 优化目标...")
    results["targets"] = {
        "static_generation": {
            "current": gen_time.get("seconds", 0),
            "target_reduction": 0.50,  # 减少50%
            "target_seconds": gen_time.get("seconds", 0) * 0.50,
        },
        "api_response": {
            "current_avg": results["baseline"]
            .get("api_responses", {})
            .get("_average", {})
            .get("ms", 0),
            "target_ms": 300,  # < 300ms
        },
        "page_load": {"target_reduction": 0.30},  # 减少30%
    }

    # 保存结果
    output_file = base_dir / "performance_baseline.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("✅ 性能基准测试完成")
    print(f"📄 结果已保存到: {output_file}")
    print("=" * 60)

    return results


def main():
    """主函数"""
    import sys

    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    run_performance_benchmark(base_url)


if __name__ == "__main__":
    main()
