# -*- coding: utf-8 -*-
"""
缓存管理工具
提供高效的内存缓存机制，支持TTL、LRU等策略
"""

import threading
import time
from collections import OrderedDict
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar

T = TypeVar("T")


class CacheStats:
    """缓存统计信息"""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0

    @property
    def hit_rate(self) -> float:
        """缓存命中率"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0.0

    def reset(self) -> None:
        """重置统计"""
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.expirations = 0


class LRUCache:
    """
    LRU (Least Recently Used) 缓存实现
    自动驱逐最久未使用的缓存项
    """

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        初始化LRU缓存

        Args:
            max_size: 最大缓存项数
            ttl: 缓存过期时间（秒），0表示永不过期
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self.lock = threading.RLock()
        self.stats = CacheStats()

    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            缓存值，如果不存在或已过期则返回None
        """
        with self.lock:
            if key not in self.cache:
                self.stats.misses += 1
                return None

            value, timestamp = self.cache[key]

            # 检查是否过期
            if self.ttl > 0 and time.time() - timestamp > self.ttl:
                self.cache.pop(key)
                self.stats.expirations += 1
                self.stats.misses += 1
                return None

            # 命中缓存，移到最前面
            self.cache.move_to_end(key)
            self.stats.hits += 1
            return value

    def set(self, key: str, value: Any) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
        """
        with self.lock:
            # 如果键已存在，删除旧的
            if key in self.cache:
                self.cache.pop(key)

            # 如果缓存已满，删除最旧的
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
                self.stats.evictions += 1

            # 添加新值
            self.cache[key] = (value, time.time())

    def delete(self, key: str) -> bool:
        """
        删除缓存值

        Args:
            key: 缓存键

        Returns:
            是否成功删除
        """
        with self.lock:
            if key in self.cache:
                self.cache.pop(key)
                return True
            return False

    def clear(self) -> None:
        """清空缓存"""
        with self.lock:
            self.cache.clear()

    def get_stats(self) -> Dict[str, any]:
        """
        获取缓存统计信息

        Returns:
            统计信息字典
        """
        with self.lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "ttl": self.ttl,
                "hits": self.stats.hits,
                "misses": self.stats.misses,
                "hit_rate": self.stats.hit_rate,
                "evictions": self.stats.evictions,
                "expirations": self.stats.expirations,
            }


# 全局缓存实例
_classics_metadata_cache = LRUCache(max_size=1, ttl=3600)  # 元数据缓存（1个，1小时）
_classics_data_cache = LRUCache(max_size=9, ttl=1800)  # 经典数据缓存（9个，30分钟）
_chapter_cache = LRUCache(max_size=100, ttl=600)  # 章节缓存（100个，10分钟）
_search_cache = LRUCache(max_size=50, ttl=300)  # 搜索缓存（50个，5分钟）


def get_cache(cache_type: str) -> LRUCache:
    """
    获取指定类型的缓存

    Args:
        cache_type: 缓存类型 ('metadata', 'data', 'chapter', 'search')

    Returns:
        LRU缓存实例
    """
    caches = {
        "metadata": _classics_metadata_cache,
        "data": _classics_data_cache,
        "chapter": _chapter_cache,
        "search": _search_cache,
    }
    return caches.get(cache_type, _chapter_cache)


def clear_all_caches() -> None:
    """清空所有缓存"""
    _classics_metadata_cache.clear()
    _classics_data_cache.clear()
    _chapter_cache.clear()
    _search_cache.clear()


def get_all_cache_stats() -> Dict[str, Dict[str, any]]:
    """
    获取所有缓存的统计信息

    Returns:
        各缓存的统计信息
    """
    return {
        "metadata": _classics_metadata_cache.get_stats(),
        "data": _classics_data_cache.get_stats(),
        "chapter": _chapter_cache.get_stats(),
        "search": _search_cache.get_stats(),
    }


def cached(ttl: int = 600, cache_type: str = "default"):
    """
    缓存装饰器

    Args:
        ttl: 缓存过期时间（秒）
        cache_type: 缓存类型

    Usage:
        @cached(ttl=300, cache_type='chapter')
        def get_chapter(chapter_id):
            # 函数体
            pass
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # 生成缓存键
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # 尝试从缓存获取
            cache = get_cache(cache_type)
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # 执行函数
            result = func(*args, **kwargs)

            # 缓存结果
            cache.set(cache_key, result)

            return result

        return wrapper

    return decorator


def reset_all_cache_stats() -> None:
    """重置所有缓存的统计信息"""
    _classics_metadata_cache.stats.reset()
    _classics_data_cache.stats.reset()
    _chapter_cache.stats.reset()
    _search_cache.stats.reset()
