#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
解析黄帝内经素问文本文件，提取章节内容并更新chapters.json
"""

import json
import re
import codecs

# 章节标题映射
CHAPTER_TITLES = {
    1: "上古天真论",
    2: "四气调神大论",
    3: "生气通天论",
    4: "金匮真言论",
    5: "阴阳应象大论",
    6: "阴阳离合论",
    7: "阴阳别论",
    8: "灵兰秘典论",
    9: "六节藏象论",
    10: "五藏生成",
    11: "五藏别论",
    12: "异法方宜论",
    13: "移精变气论",
    14: "汤液醪醴论",
    15: "玉版论要",
    16: "诊要经终论",
    17: "脉要精微论",
    18: "平人气象论",
    19: "玉机真藏论",
    20: "三部九候论",
    21: "经脉别论",
    22: "藏气法时论",
    23: "宣明五气",
    24: "血气形志",
    25: "宝命全形论",
    26: "八正神明论",
    27: "离合真邪",
    28: "通评虚实论",
    29: "太阴阳明论",
    30: "阳明脉解",
    31: "热论",
    32: "刺热",
    33: "评热病论",
    34: "逆调论",
    35: "疟论",
    36: "刺疟",
    37: "气厥论",
    38: "咳论",
    39: "举痛论",
    40: "腹中论",
    41: "刺腰痛",
    42: "风论",
    43: "痹论",
    44: "痿论",
    45: "厥论",
    46: "病能论",
    47: "奇病论",
    48: "大奇论",
    49: "脉解",
    50: "刺要论",
    51: "刺齐论",
    52: "刺禁论",
    53: "刺志论",
    54: "针解",
    55: "长刺节论",
    56: "皮部论",
    57: "经络论",
    58: "气穴论",
    59: "气府论",
    60: "骨空论",
    61: "水热穴论",
    62: "调经论",
    63: "缪刺论",
    64: "四时刺逆从论",
    65: "标本病传论",
    66: "天元纪大论",
    67: "五运行大论",
    68: "六微旨大论",
    69: "气交变大论",
    70: "五常政大论",
    71: "六元正纪大论",
    72: "刺法论",
    73: "本病论",
    74: "至真要大论",
    75: "著至教论",
    76: "示从容论",
    77: "疏五过论",
    78: "徵四失论",
    79: "阴阳类论",
    80: "方盛衰论",
    81: "解精微论",
}


def parse_suwen_file(filepath):
    """
    解析黄帝内经素问文件，提取各章节内容

    Args:
        filepath: 文本文件路径（UTF-16编码）

    Returns:
        dict: 章号 -> {title, original} 的映射
    """
    print(f"正在读取文件：{filepath}")

    # 读取文件
    with codecs.open(filepath, "r", encoding="utf-16-le") as f:
        content = f.read()

    # 清理内容
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # 移除序言部分（直到"卷一"之后）
    volume_one_idx = content.find("○上古天真论")
    if volume_one_idx > 0:
        content = content[volume_one_idx:]

    # 按章节分割
    chapters_data = {}

    # 匹配章节标题的模式
    pattern = r"○([^○]+?)篇(?:第([一二三四五六七八九十百]+))?"
    matches = list(re.finditer(pattern, content))

    print(f"找到 {len(matches)} 个章节")

    for i, match in enumerate(matches):
        chapter_title = match.group(1).strip()
        chapter_num = i + 1

        # 确定章号
        if (
            chapter_num in CHAPTER_TITLES
            and CHAPTER_TITLES[chapter_num] in chapter_title
        ):
            chapter_num = chapter_num
        elif chapter_num in CHAPTER_TITLES and chapter_title.startswith(
            CHAPTER_TITLES[chapter_num]
        ):
            chapter_num = chapter_num
        else:
            # 尝试从标题中找到对应的章号
            for num, title in CHAPTER_TITLES.items():
                if title in chapter_title or chapter_title.startswith(title):
                    chapter_num = num
                    break

        # 获取章节内容
        start_pos = match.start()
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)

        chapter_content = content[start_pos:end_pos]

        # 清理章节内容
        chapter_content = re.sub(
            r"^○[^○]+?篇[第\d一二三四五六七八九十百]+?\s*",
            "",
            chapter_content,
            flags=re.MULTILINE,
        )

        # 格式化：移除空行，合并段落
        lines = [line.strip() for line in chapter_content.split("\n") if line.strip()]
        cleaned_content = "\n".join(lines)

        # 进一步格式化：添加段落分隔
        cleaned_content = re.sub(r"([。？！])\s+([^\s])", r"\1\n\2", cleaned_content)
        cleaned_content = "\n".join(
            [line.strip() for line in cleaned_content.split("\n") if line.strip()]
        )

        chapters_data[chapter_num] = {
            "title": chapter_title + ("篇" if "篇" not in chapter_title else ""),
            "original": cleaned_content,
        }

        print(f"  第{chapter_num}章: {chapter_title} ({len(cleaned_content)} 字符)")

    return chapters_data


def update_chapters_json(parsed_data, input_file, output_file):
    """
    更新chapters.json文件

    Args:
        parsed_data: 解析出的章节数据
        input_file: 输入文件路径
        output_file: 输出文件路径
    """
    print(f"\n读取现有数据：{input_file}")

    # 读取现有数据
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 更新章节
    updated_count = 0
    for i, chapter in enumerate(data["chapters"]):
        chapter_num = chapter["chapter"]
        if chapter_num in parsed_data and chapter_num >= 5:  # 只更新第5章及以后
            new_data = parsed_data[chapter_num]
            # 更新标题
            if new_data["title"]:
                chapter["title"] = new_data["title"]
            # 更新原文
            if new_data["original"] and len(new_data["original"]) > 100:
                chapter["original"] = new_data["original"]
                updated_count += 1
                print(f"  ✓ 更新第{chapter_num}章")
            else:
                print(f"  ✗ 第{chapter_num}章内容太短，跳过")

    # 保存更新后的数据
    print(f"\n保存更新后的数据到：{output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 共更新 {updated_count} 章")
    return updated_count


def main():
    """主函数"""
    # 文件路径
    suwen_file = r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\09医藏-0869部\07素问-18本\07素问-18本\重广补注黄帝内经素问-唐-王冰.txt"
    input_file = "D:\\项目文件\\daodejing\\data\\huangdi_neijing\\chapters.json"
    output_file = "D:\\项目文件\\daodejing\\data\\huangdi_neijing\\chapters.json"

    print("=" * 60)
    print("黄帝内经素问数据解析工具")
    print("=" * 60)

    # 解析文件
    parsed_data = parse_suwen_file(suwen_file)

    if not parsed_data:
        print("\n错误：没有解析到任何数据")
        return

    # 更新JSON文件
    updated = update_chapters_json(parsed_data, input_file, output_file)

    if updated > 0:
        print("\n" + "=" * 60)
        print("✓ 数据解析和更新完成！")
        print(f"✓ 共更新 {updated} 章")
        print("=" * 60)
    else:
        print("\n错误：没有更新任何数据")


if __name__ == "__main__":
    main()
