#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据金刚经原文文本补充完善数据
"""

import json
from pathlib import Path

# 读取原文文本
source_file = Path(
    r"E:\软件工具\安装程序\AI工具集\FileNeatAI3.0.18\logs\技术文档\软件安装\软件安装包\常用软件\Compressed\FileNeatAI3.0.18\logs\办公文件\个人资料\个人文档\xwechat_files\huyong8532_53fc\msg\file\2024-11\金刚经原文.txt"
)
target_file = Path(r"D:\项目文件\daodejing\data\jgj\chapters.json")

with open(source_file, "r", encoding="utf-8") as f:
    source_text = f.read()

# 解析原文文本，按分号分割章节
chapters_raw = []
current_chapter = {"title": "", "content": ""}

lines = source_text.strip().split("\n")
chapter_num = 0

for line in lines:
    line = line.strip()
    if not line:
        continue

    # 检测章节标题（包含"分第"）
    if "分第" in line:
        if current_chapter["content"]:
            chapters_raw.append(current_chapter)
        chapter_num += 1
        current_chapter = {"num": chapter_num, "title": line, "content": ""}
    else:
        current_chapter["content"] += line

# 添加最后一章
if current_chapter["content"]:
    chapters_raw.append(current_chapter)

print(f"从原文解析出 {len(chapters_raw)} 章")

# 读取现有数据
with open(target_file, "r", encoding="utf-8") as f:
    existing_data = json.load(f)

print(f"现有数据: {len(existing_data['chapters'])} 章")

# 对比并更新
for i, chapter in enumerate(existing_data["chapters"]):
    chapter_num = chapter.get("chapter", i + 1)

    if chapter_num <= len(chapters_raw):
        raw_chapter = chapters_raw[chapter_num - 1]

        # 更新原文（如果原文更完整）
        if len(raw_chapter["content"]) > len(chapter.get("original", "")):
            print(
                f"第{chapter_num}章: 更新原文 ({len(chapter.get('original', ''))} -> {len(raw_chapter['content'])} 字)"
            )
            chapter["original"] = raw_chapter["content"]

        # 确保标题一致
        if raw_chapter["title"] != chapter.get("title", ""):
            print(f"第{chapter_num}章: 更新标题")
            chapter["title"] = raw_chapter["title"]

# 保存更新后的数据
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)

print(f"\n✓ 已更新金刚经数据: {target_file}")
