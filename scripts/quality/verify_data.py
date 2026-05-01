#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据完整性验证脚本
部署前验证所有经典数据是否完整
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def verify_classic_data(
    classic_id: str, expected_chapters: int, required_fields: list
) -> dict:
    """验证单个经典数据"""
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

    file_path = DATA_DIR / folder_map.get(classic_id) / "chapters.json"

    result = {
        "id": classic_id,
        "file_exists": file_path.exists(),
        "chapters_count": 0,
        "expected_chapters": expected_chapters,
        "fields_complete": {},
        "issues": [],
    }

    if not file_path.exists():
        result["issues"].append("数据文件不存在")
        return result

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("chapters", [])
    result["chapters_count"] = len(chapters)

    if len(chapters) != expected_chapters:
        result["issues"].append(f"章节数不符：{len(chapters)}/{expected_chapters}")

    # 检查字段完整度
    for field in required_fields:
        complete = sum(1 for ch in chapters if ch.get(field))
        percentage = (complete / len(chapters) * 100) if chapters else 0
        result["fields_complete"][field] = {
            "count": complete,
            "total": len(chapters),
            "percentage": round(percentage, 1),
        }
        if percentage < 50:
            result["issues"].append(f"{field} 完整度低：{percentage:.1f}%")

    return result


def verify_all_classics():
    """验证所有经典数据"""
    print("=" * 60)
    print("古典文献平台 - 数据完整性验证")
    print("=" * 60)

    # 经典配置：ID、名称、期望章节数、必需字段
    classics_config = [
        ("ddj", "道德经", 81, ["original", "modern_chinese", "wangbi_note"]),
        ("zzj", "庄子", 33, ["original", "modern_chinese", "chengxuanying_note"]),
        ("zy", "周易", 64, ["original", "gua_ci", "yao_ci"]),
        ("hdnj", "黄帝内经", 81, ["original", "modern_chinese", "wangbing_note"]),
        ("jgj", "金刚经", 32, ["original", "modern_chinese"]),
        ("ss", "四书", 4, ["original", "modern_chinese", "zhuxi_note"]),
        ("cxl", "传习录", 3, ["original", "modern_chinese"]),
        ("liuzutan", "六祖坛经", 10, ["original", "modern_chinese"]),
        ("ws30", "唯识三十颂", 30, ["original", "modern_chinese"]),
    ]

    all_results = []
    total_score = 0

    for classic_id, name, chapters, fields in classics_config:
        print(f"\n验证 {name} ({classic_id})...")
        result = verify_classic_data(classic_id, chapters, fields)
        all_results.append(result)

        # 计算得分
        score = 0
        if result["file_exists"]:
            score += 30
        if result["chapters_count"] == result["expected_chapters"]:
            score += 30
        else:
            score += int(30 * result["chapters_count"] / result["expected_chapters"])

        # 字段完整度得分
        field_scores = [v["percentage"] for v in result["fields_complete"].values()]
        if field_scores:
            score += int(40 * sum(field_scores) / len(field_scores))

        result["score"] = score
        total_score += score

        # 显示状态
        status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
        print(f"  {status} 得分：{score}/100")
        print(f"     章节：{result['chapters_count']}/{result['expected_chapters']}")
        for field, info in result["fields_complete"].items():
            print(f"     {field}: {info['percentage']}%")
        if result["issues"]:
            print(f"     问题：{', '.join(result['issues'])}")

    # 总结
    avg_score = total_score / len(all_results)

    print("\n" + "=" * 60)
    print(f"验证完成！平均得分：{avg_score:.1f}/100")

    if avg_score >= 80:
        print("✅ 数据质量优秀，可以部署")
        deploy_ready = True
    elif avg_score >= 60:
        print("⚠️ 数据质量良好，建议部署")
        deploy_ready = True
    else:
        print("❌ 数据质量不足，需要补充")
        deploy_ready = False

    # 保存验证报告
    report = {
        "timestamp": Path(__file__).stat().st_mtime,
        "average_score": round(avg_score, 1),
        "deploy_ready": deploy_ready,
        "classics": all_results,
    }

    report_file = DATA_DIR / "verification_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n验证报告已保存：{report_file}")
    print("=" * 60)

    return deploy_ready


if __name__ == "__main__":
    deploy_ready = verify_all_classics()
    exit(0 if deploy_ready else 1)
