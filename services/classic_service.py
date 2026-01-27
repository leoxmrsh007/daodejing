# -*- coding: utf-8 -*-
"""
经典服务 - 多经典通用服务层
支持道德经、庄子等多部经典古籍
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from config import BASE_DIR, DATA_DIR

# 经典元数据缓存
_classics_metadata_cache = None

# 各经典数据缓存
_classics_data_cache = {}


def load_classics_metadata() -> Dict:
    """
    加载所有经典元数据（带缓存）

    Returns:
        包含所有经典元数据的字典
    """
    global _classics_metadata_cache

    if _classics_metadata_cache is not None:
        return _classics_metadata_cache

    metadata_file = DATA_DIR / "classics.json"

    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            _classics_metadata_cache = json.load(f)
        return _classics_metadata_cache
    except FileNotFoundError:
        # 默认返回道德经作为回退
        return {
            "classics": [
                {
                    "id": "ddj",
                    "name": "道德经",
                    "short_name": "道德经",
                    "author": "老子",
                    "era": "春秋末期",
                    "chapters": 81,
                    "data_file": "data/daodejing.json",
                    "icon": "☯",
                    "color": "#d4a574",
                    "description": "道家哲学奠基之作"
                }
            ],
            "default_classic": "ddj"
        }
    except json.JSONDecodeError:
        return {"classics": [], "default_classic": "ddj"}


def get_classic_metadata(classic_id: str) -> Optional[Dict]:
    """
    获取指定经典的元数据

    Args:
        classic_id: 经典ID (如 'ddj', 'zzj')

    Returns:
        经典元数据字典，如果不存在则返回 None
    """
    metadata = load_classics_metadata()
    for classic in metadata.get("classics", []):
        if classic["id"] == classic_id:
            return classic
    return None


def get_all_classics() -> List[Dict]:
    """
    获取所有经典列表

    Returns:
        经典元数据列表
    """
    metadata = load_classics_metadata()
    return metadata.get("classics", [])


def get_default_classic_id() -> str:
    """
    获取默认经典ID

    Returns:
        默认经典ID
    """
    metadata = load_classics_metadata()
    return metadata.get("default_classic", "ddj")


def validate_classic_id(classic_id: str) -> bool:
    """
    验证经典ID是否有效

    Args:
        classic_id: 经典ID

    Returns:
        是否有效
    """
    metadata = get_classic_metadata(classic_id)
    return metadata is not None


class ClassicService:
    """
    通用经典服务类
    支持加载和管理多部经典的数据
    """

    def __init__(self, classic_id: str = None):
        """
        初始化经典服务

        Args:
            classic_id: 经典ID，如果为None则使用默认经典
        """
        if classic_id is None:
            classic_id = get_default_classic_id()

        self.classic_id = classic_id
        self.metadata = get_classic_metadata(classic_id)

        if self.metadata is None:
            # 回退到道德经
            self.classic_id = get_default_classic_id()
            self.metadata = get_classic_metadata(self.classic_id)

        self.data_file = BASE_DIR / self.metadata.get("data_file", "data/daodejing.json")
        self.chapter_count = self.metadata.get("chapters", 81)

    def load_data(self) -> Dict:
        """
        加载经典数据（带缓存）

        Returns:
            包含所有章节数据的字典
        """
        global _classics_data_cache

        cache_key = f"{self.classic_id}"

        if cache_key in _classics_data_cache:
            return _classics_data_cache[cache_key]

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            _classics_data_cache[cache_key] = data
            return data
        except FileNotFoundError:
            return {
                "title": self.metadata.get("name", ""),
                "chapters": []
            }
        except json.JSONDecodeError:
            return {
                "title": self.metadata.get("name", ""),
                "chapters": []
            }

    def clear_cache(self):
        """清除当前经典的数据缓存"""
        global _classics_data_cache
        cache_key = f"{self.classic_id}"
        if cache_key in _classics_data_cache:
            del _classics_data_cache[cache_key]

    @staticmethod
    def clear_all_cache():
        """清除所有经典的数据缓存"""
        global _classics_data_cache, _classics_metadata_cache
        _classics_data_cache = {}
        _classics_metadata_cache = None

    def get_chapter(self, chapter_id: int) -> Optional[Dict]:
        """
        获取指定章节的内容

        Args:
            chapter_id: 章节编号

        Returns:
            章节数据字典，如果不存在则返回 None
        """
        data = self.load_data()
        chapter = next(
            (c for c in data['chapters'] if c['chapter'] == chapter_id),
            None
        )
        return chapter

    def get_chapter_with_annotation(self, chapter_id: int) -> Optional[Dict]:
        """
        获取指定章节的内容（带疑难字标注和相邻章节信息）

        Args:
            chapter_id: 章节编号

        Returns:
            包含标注内容和相邻章节信息的字典，如果不存在则返回 None
        """
        from services.annotation_service import annotate_difficult_chars

        data = self.load_data()
        chapter = next(
            (c for c in data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if chapter:
            # 为原文添加疑难字标注
            if 'original' in chapter:
                chapter['original_annotated'] = annotate_difficult_chars(
                    chapter.get('original', '')
                )

            # 获取相邻章节
            idx = data['chapters'].index(chapter)
            chapter['prev_chapter'] = data['chapters'][idx - 1] if idx > 0 else None
            chapter['next_chapter'] = data['chapters'][idx + 1] if idx < len(data['chapters']) - 1 else None
            chapter['total_chapters'] = len(data['chapters'])

        return chapter

    def get_all_chapters(self) -> List[Dict]:
        """
        获取所有章节列表

        Returns:
            章节列表
        """
        data = self.load_data()
        return data.get('chapters', [])

    def search_chapters(self, query: str) -> List[Dict]:
        """
        搜索章节

        Args:
            query: 搜索关键词

        Returns:
            匹配的章节列表
        """
        if not query:
            return []

        data = self.load_data()
        results = []
        query_lower = query.lower()

        for chapter in data['chapters']:
            # 在原文中搜索
            if query_lower in chapter.get('original', '').lower():
                results.append({
                    'id': chapter['chapter'],
                    'title': chapter.get('title', f'第{chapter["chapter"]}章'),
                    'excerpt': chapter.get('original', '')[:100] + '...'
                })
            # 在现代译文中搜索
            elif query_lower in chapter.get('modern_chinese', '').lower():
                results.append({
                    'id': chapter['chapter'],
                    'title': chapter.get('title', f'第{chapter["chapter"]}章'),
                    'excerpt': chapter.get('modern_chinese', '')[:100] + '...'
                })

        return results

    def get_commentators(self) -> List[Dict]:
        """
        获取注释家列表

        Returns:
            注释家列表
        """
        return self.metadata.get("commentators", [])

    def get_translators(self) -> List[Dict]:
        """
        获取翻译家列表

        Returns:
            翻译家列表
        """
        return self.metadata.get("translators", [])

    def get_variants(self) -> List[Dict]:
        """
        获取古籍版本列表

        Returns:
            古籍版本列表
        """
        return self.metadata.get("variants", [])

    def to_dict(self) -> Dict:
        """
        将服务配置转换为字典（用于模板渲染）

        Returns:
            配置字典
        """
        return {
            'id': self.classic_id,
            'name': self.metadata.get('name', ''),
            'short_name': self.metadata.get('short_name', ''),
            'author': self.metadata.get('author', ''),
            'era': self.metadata.get('era', ''),
            'chapters': self.chapter_count,
            'icon': self.metadata.get('icon', ''),
            'color': self.metadata.get('color', ''),
            'description': self.metadata.get('description', ''),
            'commentators': self.get_commentators(),
            'translators': self.get_translators(),
            'variants': self.get_variants()
        }


# ============ 向后兼容的 DataService ============

class DataService(ClassicService):
    """
    向后兼容的数据服务类
    保持与原代码的兼容性
    """

    _data_cache = None

    def __init__(self):
        """初始化道德经服务（默认）"""
        super().__init__("ddj")

    @classmethod
    def load_data(cls) -> Dict:
        """
        加载道德经数据（带缓存）- 类方法保持兼容
        """
        # 使用实例方法获取数据
        service = ClassicService("ddj")
        return service.load_data()

    @classmethod
    def clear_cache(cls):
        """清除数据缓存 - 类方法保持兼容"""
        cls._data_cache = None
        ClassicService.clear_all_cache()

    @classmethod
    def get_chapter(cls, chapter_id: int) -> Optional[Dict]:
        """获取指定章节的内容 - 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.get_chapter(chapter_id)

    @classmethod
    def get_chapter_with_annotation(cls, chapter_id: int) -> Optional[Dict]:
        """获取指定章节的内容（带标注）- 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.get_chapter_with_annotation(chapter_id)

    @classmethod
    def get_all_chapters(cls) -> List[Dict]:
        """获取所有章节列表 - 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.get_all_chapters()

    @classmethod
    def search_chapters(cls, query: str) -> List[Dict]:
        """搜索章节 - 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.search_chapters(query)


# ============ 函数别名（向后兼容） ============

def load_data():
    """向后兼容：加载数据"""
    return DataService.load_data()


def get_chapter_content(chapter_id):
    """向后兼容：获取章节内容"""
    service = ClassicService("ddj")
    chapter = service.get_chapter_with_annotation(chapter_id)
    data = service.load_data()
    return chapter, data
