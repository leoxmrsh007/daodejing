#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从 ctext.org 抓取黄帝内经素问第5-81章数据
自动获取原文和白话译文
"""

import json
import re
import time
import requests
from urllib.parse import urljoin

# 章节名称到URL的映射（基于ctext.org的URL模式）
CHAPTER_SLUGS = {
    1: "shang-gu-tian-zhen-lun",
    2: "si-qi-diao-shen-da-lun",
    3: "sheng-qi-tong-tian-lun",
    4: "jin-gui-zhen-yan-lun",
    5: "yin-yang-ying-xiang-da-lun",
    6: "yin-yang-li-he-lun",
    7: "yin-yang-bie-lun",
    8: "ling-lan-mi-dian-lun",
    9: "liu-jie-zang-xiang-lun",
    10: "wu-cang-sheng-cheng",
    11: "wu-cang-bie-lun",
    12: "yi-fa-fang-yi-lun",
    13: "yi-jing-bian-qi-lun",
    14: "tang-ye-lao-li-lun",
    15: "yu-ban-lun-yao",
    16: "zhen-yao-jing-zhong-lun",
    17: "mai-yao-jing-wei-lun",
    18: "ping-ren-qi-xiang-lun",
    19: "yu-ji-zhen-cang-lun",
    20: "san-bu-jiu-hou-lun",
    21: "jing-mai-bie-lun",
    22: "zang-qi-fa-shi-lun",
    23: "xuan-ming-wu-qi",
    24: "xue-qi-xing-zhi",
    25: "bao-ming-quan-xing-lun",
    26: "ba-zheng-shen-ming-lun",
    27: "li-he-zhen-xie",
    28: "tong-ping-xu-shi-lun",
    29: "tai-yin-yang-ming-lun",
    30: "yang-ming-mai-jie",
    31: "re-lun",
    32: "ci-re",
    33: "ping-re-bing-lun",
    34: "ni-tiao-lun",
    35: "nue-lun",
    36: "ci-nue",
    37: "qi-jue-lun",
    38: "ke-lun",
    39: "ju-tong-lun",
    40: "fu-zhong-lun",
    41: "ci-yao-tong",
    42: "feng-lun",
    43: "bi-lun",
    44: "wei-lun",
    45: "jue-lun",
    46: "bing-neng-lun",
    47: "qi-bing-lun",
    48: "da-qi-lun",
    49: "mai-jie",
    50: "ci-yao-lun",
    51: "ci-qi-lun",
    52: "ci-jin-lun",
    53: "ci-zhi-lun",
    54: "zhen-jie",
    55: "chang-ci-jie-lun",
    56: "pi-bu-lun",
    57: "jing-luo-lun",
    58: "qi-xue-lun",
    59: "qi-fu-lun",
    60: "gu-kong-lun",
    61: "shui-re-xue-lun",
    62: "tiao-jing-lun",
    63: "miao-ci-lun",
    64: "si-shi-ci-ni-cong-lun",
    65: "biao-ben-bing-chuan-lun",
    66: "tian-yuan-ji-da-lun",
    67: "wu-yun-xing-da-lun",
    68: "liu-wei-zhi-da-lun",
    69: "qi-jiao-bian-da-lun",
    70: "wu-chang-zheng-da-lun",
    71: "liu-yuan-zheng-ji-da-lun",
    72: "ci-fa-lun",
    73: "ben-bing-lun",
    74: "zhi-zhen-yao-da-lun",
    75: "zhu-zhi-jiao-lun",
    76: "shi-cong-rong-lun",
    77: "shu-wu-guo-lun",
    78: "zheng-si-shi-lun",
    79: "yin-yang-lei-lun",
    80: "fang-sheng-shuai-lun",
    81: "jie-jing-wei-lun",
}

BASE_URL = "https://ctext.org/huangdi-neijing"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def fetch_chapter_page(chapter_num):
    """获取章节页面内容"""
    slug = CHAPTER_SLUGS.get(chapter_num)
    if not slug:
        print(f"警告：第{chapter_num}章没有URL映射")
        return None

    url = f"{BASE_URL}/{slug}/zhs"
    print(f"正在获取：第{chapter_num}章 - {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.encoding = "utf-8"
        if response.status_code == 200:
            return response.text
        else:
            print(f"错误：HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"错误：{e}")
        return None


def parse_chapter_content(html):
    """解析章节内容"""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # 提取标题
    title_elem = soup.find("h1")
    title = title_elem.text.strip() if title_elem else ""

    # 提取原文 - ctext.org通常在.ct-text类中
    original_text = ""
    ct_text = soup.find("div", class_="ct-text")
    if ct_text:
        paragraphs = ct_text.find_all("p")
        original_text = "\n".join(
            [p.text.strip() for p in paragraphs if p.text.strip()]
        )

    # 如果没有找到ct-text，尝试其他选择器
    if not original_text:
        # 尝试查找所有段落
        all_ps = soup.find_all("p")
        texts = [
            p.text.strip()
            for p in all_ps
            if p.text.strip() and len(p.text.strip()) > 20
        ]
        if texts:
            original_text = "\n\n".join(texts)

    # 清理文本
    original_text = re.sub(r"\s+", " ", original_text)
    original_text = (
        original_text.replace(" 。", "。\n")
        .replace(" ？", "？\n")
        .replace(" ！", "！\n")
    )
    original_text = re.sub(r"([。？！])\n", r"\1\n", original_text)
    original_text = "\n".join(
        [line.strip() for line in original_text.split("\n") if line.strip()]
    )

    return {
        "title": title,
        "original": original_text,
        "modern_chinese": "",  # ctext.org可能没有白话译文
    }


def scrape_chapters(start=5, end=81):
    """抓取指定范围的章节"""
    results = {}

    for chapter_num in range(start, end + 1):
        print(f"\n{'=' * 60}")
        print(f"处理第{chapter_num}章...")

        html = fetch_chapter_page(chapter_num)
        if html:
            content = parse_chapter_content(html)
            if content["original"]:
                results[chapter_num] = content
                print(f"✓ 第{chapter_num}章抓取成功")
                print(f"  原文长度：{len(content['original'])} 字符")
            else:
                print(f"✗ 第{chapter_num}章内容为空")
        else:
            print(f"✗ 第{chapter_num}章抓取失败")

        # 避免请求过快
        time.sleep(1)

    return results


def update_chapters_json(scraped_data, input_file, output_file):
    """更新chapters.json文件"""
    # 读取现有数据
    print(f"\n读取现有数据：{input_file}")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 更新章节
    updated_count = 0
    for i, chapter in enumerate(data["chapters"]):
        chapter_num = chapter["chapter"]
        if chapter_num in scraped_data:
            new_data = scraped_data[chapter_num]
            # 更新标题、原文
            if new_data["title"]:
                chapter["title"] = new_data["title"]
            if new_data["original"]:
                chapter["original"] = new_data["original"]
            # 如果有白话译文也更新
            if new_data["modern_chinese"]:
                chapter["modern_chinese"] = new_data["modern_chinese"]
            updated_count += 1
            print(f"✓ 更新第{chapter_num}章")

    # 保存更新后的数据
    print(f"\n保存更新后的数据到：{output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ 共更新 {updated_count} 章")
    return updated_count


def main():
    """主函数"""
    input_file = "D:\\项目文件\\daodejing\\data\\huangdi_neijing\\chapters.json"
    output_file = "D:\\项目文件\\daodejing\\data\\huangdi_neijing\\chapters.json"

    print("=" * 60)
    print("黄帝内经素问数据抓取工具")
    print("=" * 60)
    print(f"输入文件：{input_file}")
    print(f"输出文件：{output_file}")
    print(f"抓取范围：第5-81章")
    print("=" * 60)

    # 抓取数据
    scraped_data = scrape_chapters(start=5, end=81)

    if not scraped_data:
        print("\n错误：没有抓取到任何数据")
        return

    # 更新JSON文件
    updated = update_chapters_json(scraped_data, input_file, output_file)

    if updated > 0:
        print("\n" + "=" * 60)
        print(f"✓ 数据抓取和更新完成！")
        print(f"✓ 共更新 {updated} 章")
        print("=" * 60)
    else:
        print("\n错误：没有更新任何数据")


if __name__ == "__main__":
    try:
        # 检查是否安装了必要的库
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        print(f"错误：缺少必要的库")
        print(f"请安装：pip install requests beautifulsoup4")
        print(f"错误详情：{e}")
        exit(1)

    main()
