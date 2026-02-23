#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试 - 数据加载模块测试
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from generators.data_loader import (
    load_all_classics,
    load_classic_data,
    load_classics_metadata,
    load_idioms,
)


class TestDataLoader(unittest.TestCase):
    """测试数据加载功能"""

    def test_load_classic_data_ddj(self):
        """测试加载道德经数据"""
        data = load_classic_data("ddj")
        self.assertIsNotNone(data)
        self.assertIn("chapters", data)
        self.assertEqual(len(data["chapters"]), 81)

    def test_load_classic_data_zy(self):
        """测试加载周易数据"""
        data = load_classic_data("zy")
        self.assertIsNotNone(data)
        self.assertIn("chapters", data)
        self.assertEqual(len(data["chapters"]), 64)

    def test_load_classic_data_hdnj(self):
        """测试加载黄帝内经数据"""
        data = load_classic_data("hdnj")
        self.assertIsNotNone(data)
        self.assertIn("chapters", data)
        self.assertEqual(len(data["chapters"]), 81)

    def test_load_classic_data_invalid(self):
        """测试加载不存在的经典"""
        data = load_classic_data("invalid_id")
        self.assertIsNone(data)

    def test_load_all_classics(self):
        """测试加载所有经典"""
        classics = load_all_classics()
        self.assertEqual(len(classics), 9)
        expected_ids = [
            "ddj",
            "zzj",
            "zy",
            "hdnj",
            "jgj",
            "liuzutan",
            "ss",
            "cxl",
            "ws30",
        ]
        for cid in expected_ids:
            self.assertIn(cid, classics)

    def test_load_classics_metadata(self):
        """测试加载经典元数据"""
        metadata = load_classics_metadata()
        self.assertIn("classics", metadata)
        self.assertEqual(len(metadata["classics"]), 9)

    def test_load_idioms(self):
        """测试加载成语数据"""
        idioms = load_idioms()
        self.assertIsInstance(idioms, dict)
        self.assertGreater(len(idioms), 0)


class TestChapterStructure(unittest.TestCase):
    """测试章节数据结构"""

    def test_chapter_required_fields(self):
        """测试章节必需字段"""
        data = load_classic_data("ddj")
        chapters = data["chapters"]

        for ch in chapters:
            self.assertIn("chapter", ch)
            self.assertIn("title", ch)
            self.assertIn("original", ch)

            # 检查字段类型
            self.assertIsInstance(ch["chapter"], int)
            self.assertIsInstance(ch["title"], str)
            self.assertIsInstance(ch["original"], str)

    def test_chapter_numbering(self):
        """测试章节编号连续性"""
        data = load_classic_data("ddj")
        chapters = data["chapters"]

        for i, ch in enumerate(chapters, 1):
            self.assertEqual(ch["chapter"], i)


if __name__ == "__main__":
    unittest.main()
