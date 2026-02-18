# -*- coding: utf-8 -*-
"""
用户书签、笔记、收藏服务
"""

import secrets
import time
from typing import Any, Dict, List, Optional


class BookmarkService:
    """
    书签服务
    管理用户的章节书签
    """

    def __init__(self) -> None:
        """初始化书签服务"""
        # 内存存储书签数据（生产环境应使用数据库）
        self._bookmarks: Dict[str, List[Dict[str, Any]]] = {}

    def add_bookmark(
        self, user_id: str, classic_id: str, chapter_id: int
    ) -> Dict[str, Any]:
        """
        添加书签

        Args:
            user_id: 用户ID
            classic_id: 经典ID
            chapter_id: 章节ID

        Returns:
            操作结果
        """
        # 生成书签ID
        bookmark_id = secrets.token_hex(16)

        bookmark = {
            "id": bookmark_id,
            "user_id": user_id,
            "classic_id": classic_id,
            "chapter_id": chapter_id,
            "chapter_title": f"第{chapter_id}章",  # 可以从章节服务获取
            "created_at": int(time.time()),
        }

        # 保存书签
        if user_id not in self._bookmarks:
            self._bookmarks[user_id] = []

        self._bookmarks[user_id].append(bookmark)

        return {"success": True, "bookmark_id": bookmark_id, "message": "书签添加成功"}

    def get_bookmarks(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取用户的所有书签

        Args:
            user_id: 用户ID

        Returns:
            书签列表
        """
        return self._bookmarks.get(user_id, [])

    def delete_bookmark(self, user_id: str, bookmark_id: str) -> Dict[str, Any]:
        """
        删除书签

        Args:
            user_id: 用户ID
            bookmark_id: 书签ID

        Returns:
            操作结果
        """
        if user_id not in self._bookmarks:
            return {"success": False, "error": "书签不存在"}

        # 查找并删除书签
        for i, bookmark in enumerate(self._bookmarks[user_id]):
            if bookmark["id"] == bookmark_id:
                del self._bookmarks[user_id][i]
                return {"success": True, "message": "书签删除成功"}

        return {"success": False, "error": "书签不存在"}


class NoteService:
    """
    笔记服务
    管理用户的章节笔记
    """

    def __init__(self) -> None:
        """初始化笔记服务"""
        # 内存存储笔记数据（生产环境应使用数据库）
        self._notes: Dict[str, List[Dict[str, Any]]] = {}

    def add_note(
        self,
        user_id: str,
        classic_id: str,
        chapter_id: int,
        content: str,
    ) -> Dict[str, Any]:
        """
        添加笔记

        Args:
            user_id: 用户ID
            classic_id: 经典ID
            chapter_id: 章节ID
            content: 笔记内容

        Returns:
            操作结果
        """
        # 生成笔记ID
        note_id = secrets.token_hex(16)

        note = {
            "id": note_id,
            "user_id": user_id,
            "classic_id": classic_id,
            "chapter_id": chapter_id,
            "chapter_title": f"第{chapter_id}章",
            "content": content,
            "created_at": int(time.time()),
            "updated_at": int(time.time()),
        }

        # 保存笔记
        if user_id not in self._notes:
            self._notes[user_id] = []

        self._notes[user_id].append(note)

        return {"success": True, "note_id": note_id, "message": "笔记添加成功"}

    def get_notes(
        self, user_id: str, classic_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取用户的所有笔记

        Args:
            user_id: 用户ID
            classic_id: 经典ID（可选，用于过滤）

        Returns:
            笔记列表
        """
        notes = self._notes.get(user_id, [])

        # 如果指定了经典ID，过滤笔记
        if classic_id:
            notes = [n for n in notes if n["classic_id"] == classic_id]

        return notes

    def get_note(self, user_id: str, note_id: str) -> Optional[Dict[str, Any]]:
        """
        获取单个笔记详情

        Args:
            user_id: 用户ID
            note_id: 笔记ID

        Returns:
            笔记详情
        """
        if user_id not in self._notes:
            return None

        for note in self._notes[user_id]:
            if note["id"] == note_id:
                return note

        return None

    def update_note(
        self,
        user_id: str,
        note_id: str,
        content: str,
    ) -> Dict[str, Any]:
        """
        更新笔记

        Args:
            user_id: 用户ID
            note_id: 笔记ID
            content: 新的笔记内容

        Returns:
            操作结果
        """
        if user_id not in self._notes:
            return {"success": False, "error": "笔记不存在"}

        # 查找并更新笔记
        for note in self._notes[user_id]:
            if note["id"] == note_id:
                note["content"] = content
                note["updated_at"] = int(time.time())
                return {"success": True, "message": "笔记更新成功"}

        return {"success": False, "error": "笔记不存在"}

    def delete_note(self, user_id: str, note_id: str) -> Dict[str, Any]:
        """
        删除笔记

        Args:
            user_id: 用户ID
            note_id: 笔记ID

        Returns:
            操作结果
        """
        if user_id not in self._notes:
            return {"success": False, "error": "笔记不存在"}

        # 查找并删除笔记
        for i, note in enumerate(self._notes[user_id]):
            if note["id"] == note_id:
                del self._notes[user_id][i]
                return {"success": True, "message": "笔记删除成功"}

        return {"success": False, "error": "笔记不存在"}


class FavoriteService:
    """
    收藏服务
    管理用户的章节收藏
    """

    def __init__(self) -> None:
        """初始化收藏服务"""
        # 内存存储收藏数据（生产环境应使用数据库）
        self._favorites: Dict[str, List[Dict[str, Any]]] = {}

    def add_favorite(
        self, user_id: str, classic_id: str, chapter_id: int
    ) -> Dict[str, Any]:
        """
        添加收藏

        Args:
            user_id: 用户ID
            classic_id: 经典ID
            chapter_id: 章节ID

        Returns:
            操作结果
        """
        # 检查是否已收藏
        for fav in self._favorites.get(user_id, []):
            if fav["classic_id"] == classic_id and fav["chapter_id"] == chapter_id:
                return {"success": False, "error": "已经收藏了"}

        # 生成收藏ID
        favorite_id = secrets.token_hex(16)

        favorite = {
            "id": favorite_id,
            "user_id": user_id,
            "classic_id": classic_id,
            "chapter_id": chapter_id,
            "chapter_title": f"第{chapter_id}章",
            "created_at": int(time.time()),
        }

        # 保存收藏
        if user_id not in self._favorites:
            self._favorites[user_id] = []

        self._favorites[user_id].append(favorite)

        return {"success": True, "favorite_id": favorite_id, "message": "收藏成功"}

    def get_favorites(
        self, user_id: str, classic_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取用户的所有收藏

        Args:
            user_id: 用户ID
            classic_id: 经典ID（可选，用于过滤）

        Returns:
            收藏列表
        """
        favorites = self._favorites.get(user_id, [])

        # 如果指定了经典ID，过滤收藏
        if classic_id:
            favorites = [f for f in favorites if f["classic_id"] == classic_id]

        return favorites

    def remove_favorite(self, user_id: str, favorite_id: str) -> Dict[str, Any]:
        """
        取消收藏

        Args:
            user_id: 用户ID
            favorite_id: 收藏ID

        Returns:
            操作结果
        """
        if user_id not in self._favorites:
            return {"success": False, "error": "收藏不存在"}

        # 查找并删除收藏
        for i, favorite in enumerate(self._favorites[user_id]):
            if favorite["id"] == favorite_id:
                del self._favorites[user_id][i]
                return {"success": True, "message": "已取消收藏"}

        return {"success": False, "error": "收藏不存在"}

    def is_favorite(self, user_id: str, classic_id: str, chapter_id: int) -> bool:
        """
        检查是否已收藏

        Args:
            user_id: 用户ID
            classic_id: 经典ID
            chapter_id: 章节ID

        Returns:
            是否已收藏
        """
        if user_id not in self._favorites:
            return False

        return any(
            favorite["classic_id"] == classic_id
            and favorite["chapter_id"] == chapter_id
            for favorite in self._favorites[user_id]
        )


# 全局服务实例
_bookmark_service: Optional[BookmarkService] = None
_note_service: Optional[NoteService] = None
_favorite_service: Optional[FavoriteService] = None


def get_bookmark_service() -> BookmarkService:
    """获取全局书签服务实例"""
    global _bookmark_service

    if _bookmark_service is None:
        _bookmark_service = BookmarkService()

    return _bookmark_service


def get_note_service() -> NoteService:
    """获取全局笔记服务实例"""
    global _note_service

    if _note_service is None:
        _note_service = NoteService()

    return _note_service


def get_favorite_service() -> FavoriteService:
    """获取全局收藏服务实例"""
    global _favorite_service

    if _favorite_service is None:
        _favorite_service = FavoriteService()

    return _favorite_service
