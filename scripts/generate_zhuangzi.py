# -*- coding: utf-8 -*-
"""
生成庄子33章数据
"""

import json
from pathlib import Path

# 庄子33篇目录
ZHUANGZI_CHAPTERS = [
    # 内篇（庄子本人所作）
    (1, "逍遥游"),
    (2, "齐物论"),
    (3, "养生主"),
    (4, "人间世"),
    (5, "德充符"),
    (6, "大宗师"),
    (7, "应帝王"),
    # 外篇
    (8, "骈拇"),
    (9, "马蹄"),
    (10, "胠箧"),
    (11, "在宥"),
    (12, "天地"),
    (13, "天道"),
    (14, "天运"),
    (15, "刻意"),
    (16, "缮性"),
    (17, "秋水"),
    (18, "至乐"),
    (19, "达生"),
    (20, "山木"),
    (21, "田子方"),
    (22, "知北游"),
    # 杂篇
    (23, "庚桑楚"),
    (24, "徐无鬼"),
    (25, "则阳"),
    (26, "外物"),
    (27, "寓言"),
    (28, "让王"),
    (29, "盗跖"),
    (30, "说剑"),
    (31, "渔父"),
    (32, "列御寇"),
    (33, "天下"),
]

# 读取现有的第1章内容
existing_file = Path("data/zhuangzi/chapters.json")
if existing_file.exists():
    with open(existing_file, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
    first_chapter = existing_data["chapters"][0]
else:
    first_chapter = None

# 生成新数据
chapters = []

# 添加现有的第1章
if first_chapter:
    chapters.append(first_chapter)

# 为其余章节创建结构
for num, title in ZHUANGZI_CHAPTERS[1:]:
    chapter = {
        "chapter": num,
        "title": title,
        "original": "此章节内容待补充。",
        "modern_chinese": f"《{title}》是庄子的第{num}篇，内容待补充。",
        "guoxiang_note": "此版本暂未收录",
        "chengxuanying_note": "此版本暂未收录",
        "wangfuzhi_note": "此版本暂未收录",
        "english_watson": "",
        "english_ziporyn": ""
    }
    chapters.append(chapter)

# 保存完整数据
output = {
    "title": "庄子",
    "subtitle": "道家经典读本",
    "chapters": chapters
}

output_file = Path("data/zhuangzi/chapters.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"已生成庄子33章结构，保存至 {output_file}")
print(f"共 {len(chapters)} 章")
