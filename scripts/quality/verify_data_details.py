#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细验证各经典原文和注释的完整性
"""

import json
from pathlib import Path

PROJECT_DATA_ROOT = Path(r"D:\项目文件\daodejing\data")


def check_classic_details(classic_id, classic_name, data_file):
    """详细检查单个经典"""
    print(f"\n{'='*80}")
    print(f"检查: {classic_name} ({classic_id})")
    print(f"{'='*80}")

    if not data_file.exists():
        print(f"❌ 数据文件不存在: {data_file}")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("chapters", [])
    print(f"总章节数: {len(chapters)}")

    # 检查每个章节的原文
    empty_original = []
    short_original = []

    for chapter in chapters:
        chapter_id = chapter.get("id", chapter.get("chapter", 0))
        original = chapter.get("original", "")

        if not original or not original.strip():
            empty_original.append(chapter_id)
        elif len(original.strip()) < 10:
            short_original.append((chapter_id, len(original.strip())))

    if empty_original:
        print(f"\n❌ 原文为空的章节 ({len(empty_original)}): {empty_original[:20]}")
    else:
        print(f"\n✓ 所有章节原文完整")

    if short_original:
        print(f"⚠ 原文过短的章节 ({len(short_original)}): {short_original[:10]}")

    # 检查注释字段
    if chapters:
        sample_chapter = chapters[0]
        note_fields = [
            k
            for k in sample_chapter.keys()
            if "note" in k or "commentary" in k or "comment" in k
        ]

        if note_fields:
            print("\n注释字段: {note_fields}")

            for field in note_fields:
                empty_count = sum(
                    1
                    for ch in chapters
                    if not ch.get(field, "") or not ch.get(field, "").strip()
                )
                filled_count = len(chapters) - empty_count
                coverage = (filled_count / len(chapters) * 100) if chapters else 0

                status = "✓" if coverage >= 80 else "⚠" if coverage >= 50 else "❌"
                print(
                    f"  {status} {field:30s}: {filled_count:3d}/{len(chapters):3d} ({coverage:5.1f}%)"
                )

    # 检查英译字段
    english_fields = [k for k in sample_chapter.keys() if k.startswith("english_")]
    if english_fields:
        print(f"\n英译字段: {english_fields}")

        for field in english_fields:
            empty_count = sum(
                1
                for ch in chapters
                if not ch.get(field, "") or not ch.get(field, "").strip()
            )
            filled_count = len(chapters) - empty_count
            coverage = (filled_count / len(chapters) * 100) if chapters else 0

            status = "✓" if coverage >= 80 else "⚠" if coverage >= 50 else "❌"
            print(
                f"  {status} {field:30s}: {filled_count:3d}/{len(chapters):3d} ({coverage:5.1f}%)"
            )


def main():
    """主函数"""
    print("=" * 80)
    print("详细数据完整性验证")
    print("=" * 80)

    # 加载classics配置
    with open(PROJECT_DATA_ROOT / "classics.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    for classic in config["classics"]:
        data_file = PROJECT_DATA_ROOT.parent / classic["data_file"]
        check_classic_details(classic["id"], classic["name"], data_file)

    print(f"\n{'='*80}")
    print("验证完成")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
