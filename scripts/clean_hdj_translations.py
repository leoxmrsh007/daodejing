#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理白话译文字段，仅保留原文
"""

import json


def clean_translations(input_file, output_file):
    """清理译文字段，仅保留前两章的译文"""
    print(f"读取文件：{input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"总章节数：{len(data['chapters'])}")

    updated = 0
    for chapter in data["chapters"]:
        chapter_num = chapter["chapter"]

        # 第1-2章保留译文，其他章节清理
        if chapter_num > 2:
            if "modern_chinese" in chapter and chapter["modern_chinese"]:
                # 如果是占位符文字（少于100字符），则设为空
                if len(chapter["modern_chinese"]) < 100:
                    chapter["modern_chinese"] = ""
                    updated += 1

    # 保存
    print(f"保存文件：{output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ 清理了 {updated} 章的译文字段")
    return updated


def verify_data(filepath):
    """验证数据完整性"""
    print(f"\n验证文件：{filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"总章节数：{len(data['chapters'])}")

    # 统计原文长度
    orig_short = []
    orig_ok = []
    for c in data["chapters"]:
        orig_len = len(c.get("original", ""))
        if orig_len < 100:
            orig_short.append(c["chapter"])
        else:
            orig_ok.append(c["chapter"])

    print(f"原文完整：{len(orig_ok)}/81 章")
    print(
        f"原文不足100字符：{len(orig_short)} 章 {orig_short if len(orig_short) <= 10 else '(前10个)' + str(orig_short[:10])}"
    )

    # 统计译文长度
    trans_full = []
    trans_partial = []
    trans_empty = []
    for c in data["chapters"]:
        trans_len = len(c.get("modern_chinese", ""))
        if trans_len == 0:
            trans_empty.append(c["chapter"])
        elif trans_len > 200:
            trans_full.append(c["chapter"])
        else:
            trans_partial.append(c["chapter"])

    print(f"译文完整：{len(trans_full)} 章 {trans_full}")
    print(f"译文部分：{len(trans_partial)} 章")
    print(f"译文为空：{len(trans_empty)} 章")


def main():
    input_file = "D:\\项目文件\\daodejing\\data\\huangdi_neijing\\chapters.json"
    output_file = "D:\\项目文件\\daodejing\\data\\huangdi_neijing\\chapters.json"

    print("=" * 60)
    print("清理黄帝内经白话译文")
    print("=" * 60)

    # 清理译文
    clean_translations(input_file, output_file)

    # 验证数据
    verify_data(output_file)

    print("\n" + "=" * 60)
    print("✓ 完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
