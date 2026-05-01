# -*- coding: utf-8 -*-
"""
静态生成器配置模块
包含路径常量和配置
"""

from config import BASE_DIR, DATA_DIR

# 静态生成器专用配置
OUTPUT_DIR = BASE_DIR / "dist"
CLASSICS_FILE = DATA_DIR / "classics.json"
IDIOMS_FILE = DATA_DIR / "idioms.json"
