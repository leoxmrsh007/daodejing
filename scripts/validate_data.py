#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证脚本 - 确保所有经典数据格式一致且完整
"""

import json
import os
import sys
from pathlib import Path

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"

# 标准字段定义
STANDARD_FIELDS = {
    "required": ["chapter", "title", "original"],
    "optional": [
        "modern_chinese",
        "gua_ci",
        "yao_ci",
        "wangbi_note",
        "chengyi_note",
        "zhuxi_note",
        "english_lau",
        "english_henricks",
    ],
}

CLASSICS = [
    ("ddj", "daodejing"),
    ("zzj", "zhuangzi"),
    ("zy", "zy"),
    ("hdnj", "hdnj"),
    ("jgj", "jgj"),
    ("liuzutan", "liuzutan"),
    ("ss", "ss"),
    ("cxl", "cxl"),
    ("ws30", "ws30"),
]


def validate_chapter(chapter: dict, classic_id: str) -> list:
    """验证单个章节数据"""
    errors = []

    # 检查必需字段
    for field in STANDARD_FIELDS["required"]:
        if field not in chapter:
            errors.append(f"缺少必需字段: {field}")

    # 检查字段类型
    if "chapter" in chapter and not isinstance(chapter["chapter"], int):
        errors.append(f"chapter 字段类型错误: {type(chapter['chapter'])}")

    # 检查空值
    if chapter.get("original", "") == "":
        errors.append("original 字段为空")

    return errors


def validate_classic(classic_id: str, folder: str) -> dict:
    """验证单个经典数据"""
    path = DATA_DIR / folder / "chapters.json"

    result = {
        "id": classic_id,
        "valid": True,
        "chapters": 0,
        "errors": [],
        "warnings": [],
    }

    if not path.exists():
        result["valid"] = False
        result["errors"].append(f"文件不存在: {path}")
        return result

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        result["valid"] = False
        result["errors"].append(f"JSON解析错误: {e}")
        return result

    chapters = data.get("chapters", [])
    result["chapters"] = len(chapters)

    if not chapters:
        result["warnings"].append("无章节数据")

    # 验证每个章节
    for i, chapter in enumerate(chapters, 1):
        errors = validate_chapter(chapter, classic_id)
        if errors:
            result["errors"].append(f"第{i}章: {', '.join(errors)}")

    if result["errors"]:
        result["valid"] = False

    return result


def main():
    """主函数"""
    print("=" * 60)
    print("经典数据验证报告")
    print("=" * 60)

    all_valid = True

    for classic_id, folder in CLASSICS:
        result = validate_classic(classic_id, folder)

        status = "✓" if result["valid"] else "✗"
        print(f"\n{status} {classic_id}: {result['chapters']}章")

        if result["errors"]:
            print("  错误:")
            for error in result["errors"][:5]:  # 最多显示5个错误
                print(f"    - {error}")

        if result["warnings"]:
            print("  警告:")
            for warning in result["warnings"]:
                print(f"    - {warning}")

        if not result["valid"]:
            all_valid = False

    print("\n" + "=" * 60)
    if all_valid:
        print("✓ 所有经典数据验证通过")
        return 0
    else:
        print("✗ 发现数据问题，请修复后重试")
        return 1


if __name__ == "__main__":
    sys.exit(main())
