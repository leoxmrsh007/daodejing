# -*- coding: utf-8 -*-
"""
经典服务 - 多经典通用服务层
支持道德经、庄子等多部经典古籍
"""

import json
from typing import Any, Dict, List, Optional, Tuple, cast

from config import BASE_DIR, DATA_DIR

# 经典元数据缓存
_classics_metadata_cache: Optional[Dict[str, Any]] = None

# 各经典数据缓存
_classics_data_cache: Dict[str, Dict[str, Any]] = {}

# 全局全文搜索实例（延迟初始化）
_fulltext_search: Optional[Any] = None


def load_classics_metadata() -> Dict[str, Any]:
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
        with open(metadata_file, "r", encoding="utf-8") as f:
            _classics_metadata_cache = json.load(f)
        assert _classics_metadata_cache is not None
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
                    "description": "道家哲学奠基之作",
                }
            ],
            "default_classic": "ddj",
        }
    except json.JSONDecodeError:
        return {"classics": [], "default_classic": "ddj"}


def get_classic_metadata(classic_id: str) -> Optional[Dict[str, Any]]:
    """
    获取指定经典的元数据

    Args:
        classic_id: 经典ID (如 'ddj', 'zzj')

    Returns:
        经典元数据字典，如果不存在则返回 None
    """
    metadata = load_classics_metadata()
    classics = metadata.get("classics", [])
    for classic in classics:
        if classic["id"] == classic_id:
            return cast(Dict[str, Any], classic)
    return None


def get_all_classics() -> List[Dict]:
    """
    获取所有经典列表

    Returns:
        经典元数据列表
    """
    metadata = load_classics_metadata()
    return cast(List[Dict], metadata.get("classics", []))


def get_default_classic_id() -> str:
    """
    获取默认经典ID

    Returns:
        默认经典ID
    """
    metadata = load_classics_metadata()
    return cast(str, metadata.get("default_classic", "ddj"))


def get_fulltext_search() -> Any:
    """
    获取全局全文搜索实例（延迟初始化）

    Returns:
        FullTextSearch实例
    """
    global _fulltext_search

    if _fulltext_search is None:
        # 延迟导入避免循环依赖
        from services.fulltext_search import FullTextSearch

        # 收集所有经典服务
        classic_services: Dict[str, Any] = {}
        for classic in get_all_classics():
            classic_id = cast(str, classic.get("id"))
            classic_services[classic_id] = ClassicService(classic_id)

        # 初始化搜索引擎
        _fulltext_search = FullTextSearch(classic_services)
        print("[ClassicService] 全文搜索引擎初始化完成")

    return _fulltext_search


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

    metadata: Optional[Dict]  # 经典元数据，可能为None但初始化后通常不为None

    def __init__(self, classic_id: Optional[str] = None):
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

        assert self.metadata is not None
        self.data_file = BASE_DIR / self.metadata.get(
            "data_file", "data/daodejing.json"
        )
        self.chapter_count = self.metadata.get("chapters", 81)

    def load_data(self) -> Dict[str, Any]:
        """
        加载经典数据（带缓存）

        Returns:
        包含所有章节数据的字典
        """
        global _classics_data_cache  # noqa: F824
        assert self.metadata is not None

        cache_key = f"{self.classic_id}"

        if cache_key in _classics_data_cache:
            return _classics_data_cache[cache_key]

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
            _classics_data_cache[cache_key] = data
            return data
        except FileNotFoundError:
            return {"title": self.metadata.get("name", ""), "chapters": []}
        except json.JSONDecodeError:
            return {"title": self.metadata.get("name", ""), "chapters": []}

    def clear_cache(self) -> None:
        """清除当前经典的数据缓存"""
        global _classics_data_cache  # noqa: F824
        cache_key = f"{self.classic_id}"
        if cache_key in _classics_data_cache:
            del _classics_data_cache[cache_key]

    @staticmethod
    def clear_all_cache() -> None:
        """清除所有经典的数据缓存"""
        global _classics_data_cache, _classics_metadata_cache
        _classics_data_cache = {}
        _classics_metadata_cache = None

    def warmup_cache(self, count: int = 10) -> None:
        """
        预热缓存，加载前N章节数据
        应用启动时调用，提升首次访问性能

        Args:
            count: 预热的章节数量
        """
        import threading

        def _warmup() -> None:
            try:
                data = self.load_data()
                chapters = data.get("chapters", [])
                # 预热前 count 章
                for i in range(min(count, len(chapters))):
                    chapter_id = chapters[i].get("chapter")
                    if chapter_id:
                        # 触发缓存访问
                        self.get_chapter(chapter_id)
                print(
                    f"[ClassicService] 缓存预热完成: {min(count, len(chapters))} 章节"
                )
            except Exception as e:
                print(f"[ClassicService] 缓存预热失败: {e}")

        # 后台线程预热，不阻塞启动
        warmup_thread = threading.Thread(target=_warmup, daemon=True)
        warmup_thread.start()

        return None

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
            (c for c in data["chapters"] if c["chapter"] == chapter_id), None
        )
        return chapter

    def get_chapter_with_annotation(self, chapter_id: int) -> Optional[Dict]:
        """
        获取指定章节的内容（带疑难字标注和相邻章节信息）

        Args:
            chapter_id: 章节编号

        Returns:
            章节数据字典，如果不存在则返回 None
        """
        data = self.load_data()
        chapter = next(
            (c for c in data["chapters"] if c["chapter"] == chapter_id), None
        )
        return chapter

    def preload_chapters(self, chapter_ids: List[int]) -> None:
        """
        预加载指定章节到缓存
        用于缓存预热，提高访问性能

        Args:
            chapter_ids: 章节ID列表
        """
        data = self.load_data()
        for chapter_id in chapter_ids:
            # 触发缓存访问，数据已在load_data中
            next((c for c in data["chapters"] if c["chapter"] == chapter_id), None)

    def get_all_chapters(self) -> List[Dict]:
        """
        获取所有章节列表

        Returns:
            章节列表
        """
        data = self.load_data()
        return cast(List[Dict], data.get("chapters", []))

    def search_chapters(
        self,
        query: str,
        classic_id: Optional[str] = None,
        commentator: Optional[str] = None,
        content_type: Optional[str] = None,
        fuzzy_threshold: int = 70,
        limit: int = 20,
    ) -> List[Dict]:
        """
        搜索章节（增强版，支持TF-IDF评分、模糊搜索和多维度过滤）

        Args:
            query: 搜索关键词
            classic_id: 经典ID过滤 (None表示搜索所有经典)
            commentator: 注释家过滤
            content_type: 内容类型过滤 (original/modern/notes/english)
            fuzzy_threshold: 模糊搜索相似度阈值 (0-100)
            limit: 返回结果数量限制

        Returns:
            匹配的章节列表
        """
        if not query:
            return []

        try:
            # 使用全局全文搜索实例
            search_engine = get_fulltext_search()
            return search_engine.search(
                query=query,
                classic_id=classic_id or self.classic_id,
                commentator=commentator,
                content_type=content_type,
                fuzzy_threshold=fuzzy_threshold,
                limit=limit,
            )
        except Exception as e:
            # 回退到简单搜索
            print(f"[ClassicService] 搜索失败，使用回退搜索: {e}")
            return self._fallback_search(query, limit)

    def _fallback_search(self, query: str, limit: int) -> List[Dict]:
        """
        回退搜索（简单字符串匹配）

        Args:
            query: 搜索关键词
            limit: 返回结果数量限制

        Returns:
            匹配的章节列表
        """
        data = self.load_data()
        results = []
        query_lower = query.lower()

        for chapter in data["chapters"][:limit]:
            # 在原文中搜索
            if query_lower in chapter.get("original", "").lower():
                results.append(
                    {
                        "id": chapter["chapter"],
                        "title": chapter.get("title", f"第{chapter['chapter']}章"),
                        "excerpt": chapter.get("original", "")[:100] + "...",
                    }
                )
            # 在现代译文中搜索
            elif query_lower in chapter.get("modern_chinese", "").lower():
                results.append(
                    {
                        "id": chapter["chapter"],
                        "title": chapter.get("title", f"第{chapter['chapter']}章"),
                        "excerpt": chapter.get("modern_chinese", "")[:100] + "...",
                    }
                )

        return results

    def get_commentators(self) -> List[Dict]:
        """
        获取注释家列表

        Returns:
            注释家列表
        """
        assert self.metadata is not None
        return cast(List[Dict], self.metadata.get("commentators", []))

    def get_translators(self) -> List[Dict]:
        """
        获取翻译家列表

        Returns:
            翻译家列表
        """
        assert self.metadata is not None
        return cast(List[Dict], self.metadata.get("translators", []))

    def get_variants(self) -> List[Dict]:
        """
        获取古籍版本列表

        Returns:
            古籍版本列表
        """
        assert self.metadata is not None
        return cast(List[Dict], self.metadata.get("variants", []))

    def to_dict(self) -> Dict[str, Any]:
        """
        将服务配置转换为字典（用于模板渲染）

        Returns:
            配置字典
        """
        assert self.metadata is not None
        return {
            "id": self.classic_id,
            "name": self.metadata.get("name", ""),
            "short_name": self.metadata.get("short_name", ""),
            "author": self.metadata.get("author", ""),
            "era": self.metadata.get("era", ""),
            "chapters": self.chapter_count,
            "icon": self.metadata.get("icon", ""),
            "color": self.metadata.get("color", ""),
            "description": self.metadata.get("description", ""),
            "commentators": self.get_commentators(),
            "translators": self.get_translators(),
            "variants": self.get_variants(),
        }


# ============ 向后兼容的 DataService ============


class DataService(ClassicService):  # type: ignore[misc]
    """
    向后兼容的数据服务类
    保持与原代码的兼容性
    """

    _data_cache = None

    def __init__(self) -> None:
        """初始化道德经服务（默认）"""
        super().__init__("ddj")

    @classmethod  # type: ignore[misc]
    def load_data(cls) -> Dict:
        """
        加载道德经数据（带缓存）- 类方法保持兼容
        """
        # 使用实例方法获取数据
        service = ClassicService("ddj")
        return service.load_data()

    @classmethod  # type: ignore[misc]
    def clear_cache(cls) -> None:
        """清除数据缓存 - 类方法保持兼容"""
        cls._data_cache = None
        ClassicService.clear_all_cache()

    @classmethod  # type: ignore[misc]
    def get_chapter(cls, chapter_id: int) -> Optional[Dict]:
        """获取指定章节的内容 - 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.get_chapter(chapter_id)

    @classmethod  # type: ignore[misc]
    def get_chapter_with_annotation(cls, chapter_id: int) -> Optional[Dict]:
        """获取指定章节的内容（带标注）- 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.get_chapter_with_annotation(chapter_id)

    @classmethod  # type: ignore[misc]
    def get_all_chapters(cls) -> List[Dict]:
        """获取所有章节列表 - 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.get_all_chapters()

    @classmethod  # type: ignore[misc]
    def search_chapters(
        cls,
        query: str,
        classic_id: Optional[str] = None,
        commentator: Optional[str] = None,
        content_type: Optional[str] = None,
        fuzzy_threshold: int = 70,
        limit: int = 20,
    ) -> List[Dict]:
        """搜索章节 - 类方法保持兼容"""
        service = ClassicService("ddj")
        return service.search_chapters(
            query,
            classic_id=classic_id,
            commentator=commentator,
            content_type=content_type,
            fuzzy_threshold=fuzzy_threshold,
            limit=limit,
        )


# ============ 函数别名（向后兼容） ============


def load_data() -> Dict[str, Any]:
    """向后兼容：加载数据"""
    return DataService.load_data()


def get_chapter_content(chapter_id: int) -> Tuple[Optional[Dict], Dict[str, Any]]:
    """向后兼容：获取章节内容"""
    service = ClassicService("ddj")
    chapter = service.get_chapter_with_annotation(chapter_id)
    data = service.load_data()
    return chapter, data
