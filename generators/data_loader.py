#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载模块 - 负责加载所有经典数据
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "dist"


def load_classic_data(classic_id: str) -> Optional[Dict[str, Any]]:
    """加载单个经典数据"""
    # 经典ID到文件夹的映射
    folder_map = {
        "ddj": "daodejing",
        "zzj": "zhuangzi",
        "zy": "zy",
        "hdnj": "hdnj",
        "jgj": "jgj",
        "liuzutan": "liuzutan",
        "ss": "ss",
        "cxl": "cxl",
        "ws30": "ws30",
    }

    folder = folder_map.get(classic_id, classic_id)
    data_file = DATA_DIR / folder / "chapters.json"

    if not data_file.exists():
        return None

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ✗ 加载 {classic_id} 失败: {e}")
        return None


def load_all_classics() -> Dict[str, Dict[str, Any]]:
    """加载所有经典数据"""
    classics = {}
    classic_ids = ["ddj", "zzj", "zy", "hdnj", "jgj", "liuzutan", "ss", "cxl", "ws30"]

    for cid in classic_ids:
        data = load_classic_data(cid)
        if data:
            classics[cid] = data

    return classics


def load_classics_metadata() -> Dict[str, Any]:
    """加载经典元数据"""
    metadata_file = DATA_DIR / "classics.json"

    try:
        with open(metadata_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ✗ 加载 classics.json 失败: {e}")
        return {"classics": []}


def load_idioms() -> Dict[str, str]:
    """加载成语数据（已禁用）"""
    # 成语功能已暂时禁用
    return {}
