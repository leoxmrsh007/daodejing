# -*- coding: utf-8 -*-
"""
数据服务 - 加载和处理道德经数据
"""

import json
from typing import Dict, List, Optional, Tuple
from config import DATA_FILE
from services.annotation_service import annotate_difficult_chars


class DataService:
    """数据服务类"""

    _data_cache = None

    @classmethod
    def load_data(cls) -> Dict:
        """
        加载道德经数据（带缓存）

        Returns:
            包含所有章节数据的字典
        """
        if cls._data_cache is not None:
            return cls._data_cache

        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                cls._data_cache = json.load(f)
            return cls._data_cache
        except FileNotFoundError:
            return {"title": "道德经", "chapters": []}
        except json.JSONDecodeError:
            return {"title": "道德经", "chapters": []}

    @classmethod
    def clear_cache(cls):
        """清除数据缓存"""
        cls._data_cache = None

    @classmethod
    def get_chapter(cls, chapter_id: int) -> Optional[Dict]:
        """
        获取指定章节的内容

        Args:
            chapter_id: 章节编号 (1-81)

        Returns:
            章节数据字典，如果不存在则返回 None
        """
        data = cls.load_data()
        chapter = next(
            (c for c in data['chapters'] if c['chapter'] == chapter_id),
            None
        )
        return chapter

    @classmethod
    def get_chapter_with_annotation(cls, chapter_id: int) -> Optional[Dict]:
        """
        获取指定章节的内容（带疑难字标注和相邻章节信息）

        Args:
            chapter_id: 章节编号 (1-81)

        Returns:
            包含标注内容和相邻章节信息的字典，如果不存在则返回 None
        """
        data = cls.load_data()
        chapter = next(
            (c for c in data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if chapter:
            # 为原文添加疑难字标注
            chapter['original_annotated'] = annotate_difficult_chars(
                chapter.get('original', '')
            )

            # 获取相邻章节
            idx = data['chapters'].index(chapter)
            chapter['prev_chapter'] = data['chapters'][idx - 1] if idx > 0 else None
            chapter['next_chapter'] = data['chapters'][idx + 1] if idx < len(data['chapters']) - 1 else None
            chapter['total_chapters'] = len(data['chapters'])

        return chapter

    @classmethod
    def get_all_chapters(cls) -> List[Dict]:
        """
        获取所有章节列表

        Returns:
            章节列表
        """
        data = cls.load_data()
        return data.get('chapters', [])

    @classmethod
    def search_chapters(cls, query: str) -> List[Dict]:
        """
        搜索章节

        Args:
            query: 搜索关键词

        Returns:
            匹配的章节列表
        """
        if not query:
            return []

        data = cls.load_data()
        results = []
        query_lower = query.lower()

        for chapter in data['chapters']:
            # 在原文中搜索
            if query_lower in chapter.get('original', '').lower():
                results.append({
                    'id': chapter['chapter'],
                    'title': f'第{chapter["chapter"]}章',
                    'excerpt': chapter.get('original', '')[:100] + '...'
                })
            # 在现代译文中搜索
            elif query_lower in chapter.get('modern_chinese', '').lower():
                results.append({
                    'id': chapter['chapter'],
                    'title': f'第{chapter["chapter"]}章',
                    'excerpt': chapter.get('modern_chinese', '')[:100] + '...'
                })

        return results


# 向后兼容的函数别名
def load_data():
    """向后兼容：加载数据"""
    return DataService.load_data()


def get_chapter_content(chapter_id):
    """向后兼容：获取章节内容"""
    chapter = DataService.get_chapter_with_annotation(chapter_id)
    data = DataService.load_data()
    return chapter, data
