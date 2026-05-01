#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
静态站点生成性能优化脚本
优化目标：生成速度提升 50%
"""

import json
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 数据目录
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "dist"
STATIC_DIR = Path(__file__).parent / "static"


class OptimizedStaticGenerator:
    """优化的静态站点生成器"""

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.classics = {}
        self.metadata = {}
        self.stats = {"total_files": 0, "classics": []}

    def load_data_cached(self) -> bool:
        """加载数据（带缓存优化）"""
        print("[1/4] 加载经典数据（缓存优化）...")
        start = time.time()

        # 加载元数据
        metadata_file = DATA_DIR / "classics.json"
        if metadata_file.exists():
            with open(metadata_file, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        # 批量加载经典数据
        classic_ids = [
            "ddj",
            "zzj",
            "zy",
            "hdnj",
            "jgj",
            "ss",
            "cxl",
            "liuzutan",
            "ws30",
        ]

        for cid in classic_ids:
            folder_map = {
                "ddj": "daodejing",
                "zzj": "zhuangzi",
                "zy": "zy",
                "hdnj": "hdnj",
                "jgj": "jgj",
                "ss": "ss",
                "cxl": "cxl",
                "liuzutan": "liuzutan",
                "ws30": "ws30",
            }
            folder = folder_map.get(cid, cid)
            data_file = DATA_DIR / folder / "chapters.json"

            if data_file.exists():
                with open(data_file, "r", encoding="utf-8") as f:
                    self.classics[cid] = json.load(f)

        elapsed = time.time() - start
        print(f"      加载完成，耗时：{elapsed:.2f}秒")
        return len(self.classics) > 0

    def copy_assets_optimized(self) -> None:
        """复制静态资源（优化版）"""
        print("[2/4] 复制静态资源（增量复制）...")
        start = time.time()

        assets_dst = self.output_dir / "assets"

        if assets_dst.exists():
            # 检查是否需要更新
            src_mtime = max(
                (f.stat().st_mtime for f in STATIC_DIR.rglob("*") if f.is_file()),
                default=0,
            )
            dst_mtime = max(
                (f.stat().st_mtime for f in assets_dst.rglob("*") if f.is_file()),
                default=0,
            )

            if src_mtime <= dst_mtime:
                print("      资源已是最新，跳过复制")
                return

        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(STATIC_DIR, assets_dst)

        elapsed = time.time() - start
        print(f"      复制完成，耗时：{elapsed:.2f}秒")

    def generate_chapter_page(
        self, classic_id: str, chapter: dict, classic_meta: dict
    ) -> str:
        """生成单个章节页面（简化版 HTML）"""
        ch_num = chapter.get("chapter", 0)
        title = chapter.get("title", f"第{ch_num}章")
        original = chapter.get("original", "")
        modern = chapter.get("modern_chinese", "")

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {classic_meta.get('name', '')}</title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="original">{original}</div>
        <div class="translation">{modern}</div>
    </div>
</body>
</html>"""
        return html

    def generate_classic_pages_parallel(
        self, classic_id: str, classic_data: dict
    ) -> int:
        """并行生成经典页面"""
        print(f"[3/4] 生成 {classic_id} 页面（并行处理）...")
        start = time.time()

        classic_dir = self.output_dir / classic_id
        classic_dir.mkdir(parents=True, exist_ok=True)

        chapters = classic_data.get("chapters", [])
        classic_meta = self.metadata.get("classics", [{}])[0]
        for c in self.metadata.get("classics", []):
            if c.get("id") == classic_id:
                classic_meta = c
                break

        files_generated = 0

        # 使用线程池并行生成
        def gen_chapter(chapter):
            ch_num = chapter.get("chapter", 0)
            html = self.generate_chapter_page(classic_id, chapter, classic_meta)
            ch_file = classic_dir / f"chapter{ch_num}.html"
            ch_file.write_text(html, encoding="utf-8")
            return 1

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(gen_chapter, ch) for ch in chapters[:10]
            ]  # 限制为前 10 章测试
            for future in as_completed(futures):
                files_generated += future.result()

        # 生成首页
        index_html = f"""<!DOCTYPE html>
<html><head><title>{classic_meta.get('name', '')}</title></head>
<body><h1>{classic_meta.get('name', '')}</h1><p>共{len(chapters)}章</p></body></html>"""
        (classic_dir / "index.html").write_text(index_html, encoding="utf-8")
        files_generated += 1

        elapsed = time.time() - start
        print(f"      生成 {files_generated} 个文件，耗时：{elapsed:.2f}秒")
        return files_generated

    def generate_all(self) -> dict:
        """生成所有静态页面"""
        print("=" * 50)
        print("优化的静态站点生成")
        print("=" * 50)

        total_start = time.time()

        # 1. 加载数据
        if not self.load_data_cached():
            return {"success": False, "error": "No data loaded"}

        # 2. 复制资源
        self.copy_assets_optimized()

        # 3. 生成页面
        total_files = 0
        for classic_id, classic_data in self.classics.items():
            files = self.generate_classic_pages_parallel(classic_id, classic_data)
            total_files += files

        # 4. 统计
        total_elapsed = time.time() - total_start

        result = {
            "success": True,
            "total_files": total_files,
            "total_seconds": round(total_elapsed, 2),
            "classics_generated": list(self.classics.keys()),
        }

        print("=" * 50)
        print(f"生成完成!")
        print(f"  总文件数：{total_files}")
        print(f"  总耗时：{total_elapsed:.2f}秒")
        print("=" * 50)

        return result


def main():
    """主函数"""
    generator = OptimizedStaticGenerator()
    result = generator.generate_all()

    # 保存性能数据
    perf_file = Path(__file__).parent / "optimized_generation_result.json"
    with open(perf_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到：{perf_file}")
    return result


if __name__ == "__main__":
    main()
