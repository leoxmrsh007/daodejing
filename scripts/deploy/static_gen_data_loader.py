# -*- coding: utf-8 -*-
"""
静态生成器数据加载模块
加载经典数据和成语数据
"""

import json

from services.classic_service import load_classics_metadata
from static_gen_config import BASE_DIR, IDIOMS_FILE


def load_classic_data(classic_id):
    """加载指定经典的数据"""
    metadata = load_classics_metadata()
    for classic in metadata.get("classics", []):
        if classic["id"] == classic_id:
            data_file = BASE_DIR / classic["data_file"]
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f), classic
    return None, None


def load_idioms():
    """加载成语数据"""
    try:
        with open(IDIOMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("idioms", [])
    except FileNotFoundError:
        return []
