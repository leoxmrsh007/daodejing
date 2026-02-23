#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点生成器 - 主入口模块
整合数据加载和模板生成，负责完整的静态站点构建
"""

import shutil
from pathlib import Path
from typing import Any, Dict

from .data_loader import load_all_classics, load_classics_metadata
from .templates import (
    generate_chapter_list_html,
    generate_chapter_page_html,
    generate_index_page_html,
    generate_main_index_page,
)

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "dist"


class StaticSiteGenerator:
    """静态站点生成器"""

    def __init__(self, output_dir: Path = OUTPUT_DIR):
        self.output_dir = output_dir
        self.classics = {}
        self.metadata = {}
        self.idioms = {}  # 成语功能已禁用
        self.stats = {"total_files": 0, "classics": []}

    def load_data(self) -> bool:
        """加载所有数据"""
        print("[1/5] 加载经典元数据...")
        self.metadata = load_classics_metadata()

        print("[2/5] 加载经典数据...")
        self.classics = load_all_classics()
        print(f"      发现 {len(self.classics)} 部经典")

        # 成语功能已暂时禁用
        # print("[3/5] 加载成语数据...")
        # self.idioms = load_idioms()

        return len(self.classics) > 0

    def copy_assets(self) -> None:
        """复制静态资源"""
        print("[4/6] 复制静态资源...")

        assets_src = Path(__file__).parent.parent / "static"
        assets_dst = self.output_dir / "assets"

        if assets_src.exists():
            if assets_dst.exists():
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)
            print("      静态资源已复制")

    def generate_classic_pages(
        self, classic_id: str, classic_data: Dict[str, Any]
    ) -> int:
        """生成单个经典的所有页面"""
        chapters = classic_data.get("chapters", [])
        if not chapters:
            return 0

        # 创建输出目录
        classic_dir = self.output_dir / classic_id
        classic_dir.mkdir(parents=True, exist_ok=True)

        files_generated = 0

        # 生成首页
        index_html = generate_index_page_html(classic_data, self.metadata)
        (classic_dir / "index.html").write_text(index_html, encoding="utf-8")
        files_generated += 1

        # 生成章节列表页
        list_html = generate_chapter_list_html(classic_id, classic_data, self.metadata)
        (classic_dir / "all-chapters.html").write_text(list_html, encoding="utf-8")
        files_generated += 1

        # 生成每个章节页面
        for chapter in chapters:
            chapter_html = generate_chapter_page_html(
                classic_id, chapter, classic_data, self.metadata
            )
            ch_num = chapter.get("chapter", 0)
            (classic_dir / f"chapter{ch_num}.html").write_text(
                chapter_html, encoding="utf-8"
            )
            files_generated += 1

        return files_generated

    def generate_all_classics(self) -> None:
        """生成所有经典的页面"""
        print("[5/6] 生成经典页面...")
        print()

        for classic_id, classic_data in self.classics.items():
            print(f"      正在处理 {classic_data.get('title', classic_id)}...")

            count = self.generate_classic_pages(classic_id, classic_data)

            print(
                f"        生成完成：{len(classic_data.get('chapters', []))} 个章节 + 2 个导航页"
            )

            self.stats["classics"].append(classic_data.get("title", classic_id))
            self.stats["total_files"] += count

        print()

    def generate_main_index(self) -> None:
        """生成网站总首页"""
        print("[6/6] 生成总首页...")

        index_html = generate_main_index_page(self.classics, self.metadata)
        (self.output_dir / "index.html").write_text(index_html, encoding="utf-8")

        self.stats["total_files"] += 1

    def generate(self) -> bool:
        """执行完整的站点生成流程"""
        print("=" * 60)
        print("古籍经典静态网站生成器")
        print("=" * 60)
        print()

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 加载数据
        if not self.load_data():
            print("✗ 数据加载失败")
            return False

        # 复制资源
        self.copy_assets()

        # 生成所有页面
        self.generate_all_classics()

        # 生成首页
        self.generate_main_index()

        # 打印统计
        print()
        print("=" * 60)
        print("✓ 静态网站生成完成！")
        print("=" * 60)
        print(f"  输出目录: {self.output_dir}")
        print(f"  总文件数: {self.stats['total_files']} 个HTML文件")
        print(f"  包含经典: {', '.join(self.stats['classics'])}")
        print()

        return True


def main():
    """主函数"""
    generator = StaticSiteGenerator()
    success = generator.generate()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
