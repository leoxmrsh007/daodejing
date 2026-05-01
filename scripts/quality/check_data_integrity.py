#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查项目数据完整性 - 修正版
"""

import json
from collections import defaultdict
from pathlib import Path

PROJECT_DATA_ROOT = Path(r"D:\项目文件\daodejing\data")


def load_classics_config():
    """加载经典配置"""
    with open(PROJECT_DATA_ROOT / "classics.json", "r", encoding="utf-8") as f:
        return json.load(f)


def check_classic_data(classic_info):
    """检查单个经典的数据完整性"""
    classic_id = classic_info["id"]
    classic_name = classic_info["name"]
    expected_chapters = classic_info["chapters"]

    # 加载章节数据
    data_file = PROJECT_DATA_ROOT.parent / classic_info["data_file"]
    if not data_file.exists():
        return {
            "id": classic_id,
            "name": classic_name,
            "error": f"数据文件不存在: {data_file}",
        }

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("chapters", [])

    # 检查章节数量
    actual_chapters = len(chapters)
    chapter_complete = actual_chapters == expected_chapters

    # 检查每个章节的字段
    field_stats = defaultdict(lambda: {"count": 0, "empty": 0, "missing_chapters": []})

    for chapter in chapters:
        chapter_id = chapter.get("id", chapter.get("chapter", 0))

        # 检查所有字段
        for key, value in chapter.items():
            if key in ["id", "chapter", "title"]:
                continue

            field_stats[key]["count"] += 1

            if not value or (isinstance(value, str) and not value.strip()):
                field_stats[key]["empty"] += 1
                field_stats[key]["missing_chapters"].append(chapter_id)

    # 计算覆盖率
    field_coverage = {}
    for field, stats in field_stats.items():
        coverage_pct = (
            ((stats["count"] - stats["empty"]) / stats["count"] * 100)
            if stats["count"] > 0
            else 0
        )
        field_coverage[field] = {
            "total": stats["count"],
            "filled": stats["count"] - stats["empty"],
            "empty": stats["empty"],
            "coverage": coverage_pct,
            "missing_chapters": stats["missing_chapters"][:10],  # 只显示前10个
        }

    return {
        "id": classic_id,
        "name": classic_name,
        "expected_chapters": expected_chapters,
        "actual_chapters": actual_chapters,
        "chapter_complete": chapter_complete,
        "field_coverage": field_coverage,
    }


def generate_report():
    """生成完整性报告"""
    config = load_classics_config()

    print("=" * 80)
    print("项目数据完整性检查报告")
    print("=" * 80)

    all_reports = []

    for classic in config["classics"]:
        print(f"\n{'='*80}")
        print(f"经典: {classic['name']} ({classic['id']})")
        print(f"{'='*80}")

        report = check_classic_data(classic)

        if "error" in report:
            print(f"❌ 错误: {report['error']}")
            continue

        # 章节完整性
        status = "✓" if report["chapter_complete"] else "❌"
        print(
            f"\n[章节] {status} {report['actual_chapters']}/{report['expected_chapters']}"
        )

        # 字段覆盖率
        print("\n[字段覆盖率]")

        # 按覆盖率排序
        sorted_fields = sorted(
            report["field_coverage"].items(),
            key=lambda x: x[1]["coverage"],
            reverse=True,
        )

        for field, stats in sorted_fields:
            coverage = stats["coverage"]
            status_icon = "✓" if coverage >= 80 else "⚠" if coverage >= 50 else "❌"

            print(
                f"  {status_icon} {field:30s}: {stats['filled']:3d}/{stats['total']:3d} ({coverage:5.1f}%)"
            )

            # 显示缺失章节
            if stats["empty"] > 0 and stats["empty"] <= 10:
                print(f"     缺失章节: {stats['missing_chapters']}")
            elif stats["empty"] > 10:
                print(
                    f"     缺失章节: {stats['missing_chapters']} ... (共{stats['empty']}章)"
                )

        all_reports.append(report)

    # 总结
    print(f"\n{'='*80}")
    print("总结")
    print(f"{'='*80}")

    for report in all_reports:
        if "error" in report:
            continue

        chapter_status = "✓" if report["chapter_complete"] else "❌"

        # 计算平均覆盖率
        if report["field_coverage"]:
            avg_coverage = sum(
                f["coverage"] for f in report["field_coverage"].values()
            ) / len(report["field_coverage"])
        else:
            avg_coverage = 0

        print(
            f"{chapter_status} {report['name']:12s}: {report['actual_chapters']:3d}/{report['expected_chapters']:3d} 章节, "
            f"平均字段覆盖率: {avg_coverage:.1f}%"
        )

    # 保存详细报告
    report_file = PROJECT_DATA_ROOT / "data_integrity_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(all_reports, f, ensure_ascii=False, indent=2)

    print(f"\n详细报告已保存到: {report_file}")

    return all_reports


if __name__ == "__main__":
    generate_report()
