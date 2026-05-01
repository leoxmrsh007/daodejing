#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核对外部数据源与项目数据的完整性和对应性
"""

import json
from pathlib import Path
from typing import Dict, List

# 外部数据源路径
EXTERNAL_DATA_ROOT = r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书"

# 项目数据路径
PROJECT_DATA_ROOT = r"D:\项目文件\daodejing\data"

# 经典映射配置
CLASSICS_MAPPING = {
    "ddj": {
        "name": "道德经",
        "external_paths": [
            "03道藏-1689部/09藏外-186种/09藏外-186种",
        ],
        "keywords": ["老子", "道德经"],
        "chapters": 81,
        "commentators": {
            "wangbi": ["王弼"],
            "heshanggong": ["河上公"],
            "wangfuzhi": ["王夫之"],
            "hanshandeqing": ["憨山", "德清"],
            "suzhe": ["苏辙"],
            "yanzun": ["严遵"],
            "weiyuan": ["魏源"],
        },
    },
    "zzj": {
        "name": "庄子",
        "external_paths": [
            "03道藏-1689部",
            "05子藏-1155部",
        ],
        "keywords": ["庄子", "南华经"],
        "chapters": 33,
        "commentators": {
            "chengxuanying": ["成玄英"],
            "guoxiang": ["郭象"],
            "wangfuzhi": ["王夫之"],
        },
    },
    "zy": {
        "name": "周易",
        "external_paths": [
            "01易藏-0195部",
        ],
        "keywords": ["周易", "易经"],
        "chapters": 64,
        "commentators": {
            "wangbi": ["王弼"],
            "chengyi": ["程颐"],
            "zhuxi": ["朱熹"],
        },
    },
    "hdnj": {
        "name": "黄帝内经",
        "external_paths": [
            "09医藏-0869部",
        ],
        "keywords": ["黄帝内经", "素问", "灵枢"],
        "chapters": 81,
        "commentators": {
            "wangbing": ["王冰"],
        },
    },
    "jgj": {
        "name": "金刚经",
        "external_paths": [
            "04佛藏-5678部",
        ],
        "keywords": ["金刚经", "金刚般若"],
        "chapters": 32,
        "commentators": {
            "kumrajiva": ["鸠摩罗什"],
            "xuanzang": ["玄奘"],
        },
    },
    "ss": {
        "name": "四书",
        "external_paths": [
            "02儒藏-0370部",
        ],
        "keywords": ["大学", "中庸", "论语", "孟子", "四书"],
        "chapters": 4,
        "commentators": {
            "zhuxi": ["朱熹"],
        },
    },
    "cxl": {
        "name": "传习录",
        "external_paths": [
            "02儒藏-0370部",
        ],
        "keywords": ["传习录", "王阳明"],
        "chapters": 3,
        "commentators": {
            "wangyangming": ["王阳明"],
        },
    },
    "liuzutan": {
        "name": "六祖坛经",
        "external_paths": [
            "04佛藏-5678部",
        ],
        "keywords": ["六祖坛经", "坛经", "慧能"],
        "chapters": 10,
        "commentators": {
            "zongbao": ["宗宝"],
        },
    },
    "ws30": {
        "name": "唯识三十颂",
        "external_paths": [
            "04佛藏-5678部",
        ],
        "keywords": ["唯识三十颂", "唯识", "世亲"],
        "chapters": 30,
        "commentators": {
            "xuanzang": ["玄奘"],
            "kuiji": ["窥基"],
        },
    },
}


def find_external_files(classic_id: str) -> List[Path]:
    """查找外部数据源中的相关文件"""
    config = CLASSICS_MAPPING[classic_id]
    found_files = []

    for rel_path in config["external_paths"]:
        search_dir = Path(EXTERNAL_DATA_ROOT) / rel_path
        if not search_dir.exists():
            continue

        # 递归查找txt文件
        for txt_file in search_dir.rglob("*.txt"):
            # 跳过临时文件
            if txt_file.name.startswith("~$"):
                continue

            # 检查文件名是否包含关键词
            filename = txt_file.name
            for keyword in config["keywords"]:
                if keyword in filename:
                    found_files.append(txt_file)
                    break

    return found_files


def load_project_data(classic_id: str) -> Dict:
    """加载项目中的经典数据"""
    # 从classics.json获取数据文件路径
    classics_file = Path(PROJECT_DATA_ROOT) / "classics.json"
    with open(classics_file, "r", encoding="utf-8") as f:
        classics_data = json.load(f)

    # 找到对应的经典
    classic_info = None
    for classic in classics_data["classics"]:
        if classic["id"] == classic_id:
            classic_info = classic
            break

    if not classic_info:
        return None

    # 加载章节数据
    data_file = Path(PROJECT_DATA_ROOT).parent / classic_info["data_file"]
    if not data_file.exists():
        return None

    with open(data_file, "r", encoding="utf-8") as f:
        chapters_data = json.load(f)

    return {"info": classic_info, "chapters": chapters_data.get("chapters", [])}


def check_chapter_completeness(classic_id: str, project_data: Dict) -> Dict:
    """检查章节完整性"""
    config = CLASSICS_MAPPING[classic_id]
    expected_chapters = config["chapters"]
    actual_chapters = len(project_data["chapters"])

    result = {
        "expected": expected_chapters,
        "actual": actual_chapters,
        "complete": actual_chapters == expected_chapters,
        "missing": [],
    }

    # 检查是否有缺失的章节
    chapter_ids = set()
    for chapter in project_data["chapters"]:
        chapter_ids.add(chapter.get("id", 0))

    for i in range(1, expected_chapters + 1):
        if i not in chapter_ids:
            result["missing"].append(i)

    return result


def check_commentator_completeness(classic_id: str, project_data: Dict) -> Dict:
    """检查注释本完整性"""
    config = CLASSICS_MAPPING[classic_id]
    expected_commentators = set(config["commentators"].keys())

    # 统计每个注释本的覆盖情况
    commentator_coverage = {}
    for commentator_id in expected_commentators:
        commentator_coverage[commentator_id] = {
            "total_chapters": 0,
            "has_content": 0,
            "empty_chapters": [],
        }

    for chapter in project_data["chapters"]:
        chapter_id = chapter.get("id", 0)
        for commentator_id in expected_commentators:
            commentator_coverage[commentator_id]["total_chapters"] += 1

            # 检查是否有内容
            content = chapter.get(commentator_id, "")
            if content and content.strip():
                commentator_coverage[commentator_id]["has_content"] += 1
            else:
                commentator_coverage[commentator_id]["empty_chapters"].append(
                    chapter_id
                )

    return commentator_coverage


def generate_report(classic_id: str) -> Dict:
    """生成单个经典的核对报告"""
    config = CLASSICS_MAPPING[classic_id]
    print(f"\n{'='*60}")
    print(f"核对经典: {config['name']} ({classic_id})")
    print(f"{'='*60}")

    # 1. 查找外部文件
    print("\n[1] 查找外部数据源文件...")
    external_files = find_external_files(classic_id)
    print(f"    找到 {len(external_files)} 个相关文件:")
    for f in external_files[:10]:  # 只显示前10个
        print(f"    - {f.name}")
    if len(external_files) > 10:
        print(f"    ... 还有 {len(external_files) - 10} 个文件")

    # 2. 加载项目数据
    print("\n[2] 加载项目数据...")
    project_data = load_project_data(classic_id)
    if not project_data:
        print("    ❌ 未找到项目数据")
        return None
    print(f"    ✓ 已加载 {len(project_data['chapters'])} 个章节")

    # 3. 检查章节完整性
    print("\n[3] 检查章节完整性...")
    chapter_check = check_chapter_completeness(classic_id, project_data)
    if chapter_check["complete"]:
        print(f"    ✓ 章节完整: {chapter_check['actual']}/{chapter_check['expected']}")
    else:
        print(
            f"    ❌ 章节不完整: {chapter_check['actual']}/{chapter_check['expected']}"
        )
        if chapter_check["missing"]:
            print(f"    缺失章节: {chapter_check['missing']}")

    # 4. 检查注释本完整性
    print("\n[4] 检查注释本完整性...")
    commentator_check = check_commentator_completeness(classic_id, project_data)
    for commentator_id, coverage in commentator_check.items():
        commentator_names = config["commentators"].get(commentator_id, [commentator_id])
        name = commentator_names[0] if commentator_names else commentator_id

        coverage_pct = (
            (coverage["has_content"] / coverage["total_chapters"] * 100)
            if coverage["total_chapters"] > 0
            else 0
        )
        status = "✓" if coverage_pct >= 80 else "⚠" if coverage_pct >= 50 else "❌"

        print(
            f"    {status} {name}: {coverage['has_content']}/{coverage['total_chapters']} ({coverage_pct:.1f}%)"
        )
        if coverage["empty_chapters"] and len(coverage["empty_chapters"]) <= 10:
            print(f"       空章节: {coverage['empty_chapters']}")

    return {
        "classic_id": classic_id,
        "name": config["name"],
        "external_files": len(external_files),
        "chapter_check": chapter_check,
        "commentator_check": commentator_check,
    }


def main():
    """主函数"""
    print("=" * 60)
    print("古籍经典数据完整性核对")
    print("=" * 60)
    print(f"外部数据源: {EXTERNAL_DATA_ROOT}")
    print(f"项目数据: {PROJECT_DATA_ROOT}")

    all_reports = []

    # 核对每部经典
    for classic_id in CLASSICS_MAPPING.keys():
        report = generate_report(classic_id)
        if report:
            all_reports.append(report)

    # 生成总结
    print(f"\n{'='*60}")
    print("总结")
    print(f"{'='*60}")

    for report in all_reports:
        chapter_status = "✓" if report["chapter_check"]["complete"] else "❌"
        print(
            f"{chapter_status} {report['name']}: {report['chapter_check']['actual']}/{report['chapter_check']['expected']} 章节, {report['external_files']} 个外部文件"
        )

    # 保存报告
    report_file = Path(PROJECT_DATA_ROOT) / "external_data_verification.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(all_reports, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存到: {report_file}")


if __name__ == "__main__":
    main()
