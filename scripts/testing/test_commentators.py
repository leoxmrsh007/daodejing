#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试庄子页面注释显示
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app  # noqa: E402


def test_zhuangzi_commentators():
    print("=== 测试庄子页面注释显示 ===")

    # 创建测试应用
    app = create_app()
    client = app.test_client()

    # 测试庄子第一章
    response = client.get("/zzj/chapter/1")

    if response.status_code != 200:
        print(f"错误: 状态码 {response.status_code}")
        return False

    html = response.data.decode("utf-8")

    # 检查关键元素
    tests = [
        ("庄子标题", "庄子" in html),
        ("逍遥游章节", "逍遥游" in html),
        ("多版本对照区域", "多版本对照" in html),
        ("注释家标签-郭象注", "郭象注" in html),
        ("注释家标签-成玄英疏", "成玄英疏" in html),
        ("注释家标签-王夫之", "王夫之" in html),
    ]

    all_passed = True
    for test_name, passed in tests:
        status = "✓" if passed else "✗"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False

    # 检查注释家数量
    import re

    # 查找注释家标签按钮
    commentator_buttons = re.findall(
        r"<button[^>]*>([^<]*注|[^<]*疏|[^<]*王夫之)</button>", html
    )
    print(f"\n找到的注释家按钮: {commentator_buttons}")

    # 检查注释内容
    commentator_contents = []
    for commentator in ["guoxiang", "chengxuanying", "wangfuzhi"]:
        if f'id="{commentator}"' in html:
            commentator_contents.append(commentator)

    print(f"找到的注释家内容区域: {commentator_contents}")

    return all_passed


def test_dao_de_jing_commentators():
    print("\n=== 测试道德经页面注释显示 ===")

    app = create_app()
    client = app.test_client()

    response = client.get("/ddj/chapter/1")

    if response.status_code != 200:
        print(f"错误: 状态码 {response.status_code}")
        return False

    html = response.data.decode("utf-8")

    # 检查11位注释家
    commentators = [
        "王弼注",
        "河上公注",
        "王夫之",
        "憨山德清注",
        "苏辙注",
        "李涵虚注",
        "黄元吉注",
        "魏源注",
        "想尔注",
        "严遵注",
        "王安石注",
    ]

    found_count = 0
    for commentator in commentators:
        if commentator in html:
            found_count += 1
            print(f"✓ 找到 {commentator}")
        else:
            print(f"✗ 未找到 {commentator}")

    print(f"\n总计: {found_count}/11 位注释家")

    return found_count >= 11


if __name__ == "__main__":
    success1 = test_zhuangzi_commentators()
    success2 = test_dao_de_jing_commentators()

    print("\n" + "=" * 50)
    if success1 and success2:
        print("所有测试通过!")
    else:
        print("部分测试失败")
        sys.exit(1)
