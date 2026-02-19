# -*- coding: utf-8 -*-
"""
书签、笔记、收藏服务测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest

from services.bookmark_service import BookmarkService, FavoriteService, NoteService


class TestBookmarkService:
    """书签服务测试"""

    def test_bookmark_service_init(self):
        """测试书签服务初始化"""
        service = BookmarkService()
        assert service._bookmarks == {}

    def test_add_bookmark(self):
        """测试添加书签"""
        service = BookmarkService()
        result = service.add_bookmark("user1", "ddj", 1)
        assert result["success"] is True
        assert "bookmark_id" in result

    def test_add_duplicate_bookmark(self):
        """测试添加重复书签"""
        service = BookmarkService()
        service.add_bookmark("user1", "ddj", 1)
        result = service.add_bookmark("user1", "ddj", 1)
        assert result["success"] is True

    def test_delete_bookmark(self):
        """测试删除书签"""
        service = BookmarkService()
        add_result = service.add_bookmark("user1", "ddj", 1)
        assert add_result["success"] is True
        bookmark_id = add_result["bookmark_id"]

        result = service.delete_bookmark("user1", bookmark_id)
        assert result["success"] is True

    def test_get_bookmarks(self):
        """测试获取用户书签"""
        service = BookmarkService()
        service.add_bookmark("user1", "ddj", 1)
        service.add_bookmark("user1", "ddj", 2)
        bookmarks = service.get_bookmarks("user1")
        assert len(bookmarks) == 2


class TestNoteService:
    """笔记服务测试"""

    def test_note_service_init(self):
        """测试笔记服务初始化"""
        service = NoteService()
        assert service._notes == {}

    def test_add_note(self):
        """测试添加笔记"""
        service = NoteService()
        result = service.add_note("user1", "ddj", 1, "这是一条测试笔记")
        assert result["success"] is True
        assert "note_id" in result

    def test_add_empty_note(self):
        """测试添加空笔记"""
        service = NoteService()
        result = service.add_note("user1", "ddj", 1, "")
        # 空笔记应该成功，但内容为空
        assert result["success"] is True

    def test_get_notes(self):
        """测试获取笔记"""
        service = NoteService()
        service.add_note("user1", "ddj", 1, "测试笔记")
        notes = service.get_notes("user1", "ddj")
        assert len(notes) == 1

    def test_delete_note(self):
        """测试删除笔记"""
        service = NoteService()
        add_result = service.add_note("user1", "ddj", 1, "测试笔记")
        assert add_result["success"] is True
        note_id = add_result["note_id"]

        result = service.delete_note("user1", note_id)
        assert result["success"] is True


class TestFavoriteService:
    """收藏服务测试"""

    def test_favorite_service_init(self):
        """测试收藏服务初始化"""
        service = FavoriteService()
        assert service._favorites == {}

    def test_add_favorite(self):
        """测试添加收藏"""
        service = FavoriteService()
        result = service.add_favorite("user1", "ddj", 1)
        assert result["success"] is True
        assert "favorite_id" in result

    def test_delete_favorite(self):
        """测试删除收藏"""
        service = FavoriteService()
        add_result = service.add_favorite("user1", "ddj", 1)
        assert add_result["success"] is True
        favorite_id = add_result["favorite_id"]

        result = service.remove_favorite("user1", favorite_id)
        assert result["success"] is True

    def test_is_favorite(self):
        """测试检查是否收藏"""
        service = FavoriteService()
        service.add_favorite("user1", "ddj", 1)
        is_fav = service.is_favorite("user1", "ddj", 1)
        assert is_fav is True

        is_not_fav = service.is_favorite("user1", "ddj", 2)
        assert is_not_fav is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
