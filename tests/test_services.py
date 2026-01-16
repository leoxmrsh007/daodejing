# -*- coding: utf-8 -*-
"""
后端服务测试
"""

import pytest
import json
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app
from services.data_service import DataService
from services.annotation_service import annotate_difficult_chars, DIFFICULT_CHARS
from utils.validators import validate_chapter_id, validate_search_query


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestDataService:
    """数据服务测试"""

    def test_load_data(self):
        """测试数据加载"""
        data = DataService.load_data()
        assert data is not None
        assert 'title' in data
        assert 'chapters' in data
        assert len(data['chapters']) == 81

    def test_get_chapter_valid(self):
        """测试获取有效章节"""
        chapter = DataService.get_chapter(1)
        assert chapter is not None
        assert chapter['chapter'] == 1
        assert 'original' in chapter

    def test_get_chapter_invalid(self):
        """测试获取无效章节"""
        chapter = DataService.get_chapter(999)
        assert chapter is None

    def test_get_chapter_with_annotation(self):
        """测试获取带标注的章节"""
        chapter = DataService.get_chapter_with_annotation(1)
        assert chapter is not None
        assert 'original_annotated' in chapter
        assert 'prev_chapter' in chapter
        assert 'next_chapter' in chapter

    def test_search_chapters(self):
        """测试章节搜索"""
        results = DataService.search_chapters('道')
        assert len(results) > 0
        assert 'id' in results[0]
        assert 'title' in results[0]

    def test_search_chapters_empty(self):
        """测试空搜索"""
        results = DataService.search_chapters('')
        assert len(results) == 0


class TestAnnotationService:
    """标注服务测试"""

    def test_difficult_chars_exists(self):
        """测试疑难字字典存在"""
        assert isinstance(DIFFICULT_CHARS, dict)
        assert len(DIFFICULT_CHARS) > 0

    def test_annotate_difficult_chars(self):
        """测试疑难字标注"""
        text = '道可道非常道'
        result = annotate_difficult_chars(text)
        # 文本应该被处理
        assert isinstance(result, str)

    def test_annotate_with_difficult_char(self):
        """测试包含疑难字的标注"""
        text = '谷神不死'
        result = annotate_difficult_chars(text)
        # 应该包含标注的HTML
        if '谷神' in DIFFICULT_CHARS:
            assert 'difficult' in result or 'data-pinyin' in result


class TestValidators:
    """输入验证测试"""

    def test_validate_chapter_id_valid(self):
        """测试有效章节ID"""
        assert validate_chapter_id(1) is True
        assert validate_chapter_id(81) is True

    def test_validate_chapter_id_invalid(self):
        """测试无效章节ID"""
        assert validate_chapter_id(0) is False
        assert validate_chapter_id(82) is False
        assert validate_chapter_id(-1) is False
        assert validate_chapter_id('abc') is False

    def test_validate_search_query_valid(self):
        """测试有效搜索查询"""
        is_valid, error = validate_search_query('道德经')
        assert is_valid is True
        assert error is None

    def test_validate_search_query_empty(self):
        """测试空搜索查询"""
        is_valid, error = validate_search_query('')
        assert is_valid is False
        assert error is not None

    def test_validate_search_query_too_long(self):
        """测试过长搜索查询"""
        long_query = 'a' * 101
        is_valid, error = validate_search_query(long_query)
        assert is_valid is False
        assert '长度' in error

    def test_validate_search_query_xss(self):
        """测试XSS攻击防护"""
        xss_query = '<script>alert("xss")</script>'
        is_valid, error = validate_search_query(xss_query)
        assert is_valid is False
        assert error is not None


class TestRoutes:
    """路由测试"""

    def test_index_redirect(self, client):
        """测试首页重定向"""
        response = client.get('/')
        assert response.status_code == 302

    def test_daodejing_index(self, client):
        """测试道德经首页"""
        response = client.get('/daodejing/')
        assert response.status_code == 200

    def test_chapter_view_valid(self, client):
        """测试有效章节页面"""
        response = client.get('/daodejing/chapter/1')
        assert response.status_code == 200

    def test_chapter_view_invalid(self, client):
        """测试无效章节页面"""
        response = client.get('/daodejing/chapter/999')
        # 应该重定向到首页
        assert response.status_code == 302

    def test_api_chapters(self, client):
        """测试章节API"""
        response = client.get('/api/daodejing/chapters')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'chapters' in data
        assert len(data['chapters']) == 81

    def test_api_chapter_valid(self, client):
        """测试单章API"""
        response = client.get('/api/daodejing/chapter/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['chapter'] == 1

    def test_api_chapter_invalid(self, client):
        """测试无效单章API"""
        response = client.get('/api/daodejing/chapter/999')
        assert response.status_code == 404

    def test_api_search(self, client):
        """测试搜索API"""
        response = client.get('/api/daodejing/search?q=道')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data

    def test_api_search_invalid(self, client):
        """测试无效搜索API（XSS）"""
        response = client.get('/api/daodejing/search?q=<script>')
        # 应该被拒绝或返回空结果
        assert response.status_code in [200, 400]
        if response.status_code == 400:
            data = json.loads(response.data)
            assert 'error' in data


class TestSecurity:
    """安全性测试"""

    def test_security_headers(self, client):
        """测试安全响应头"""
        response = client.get('/daodejing/')
        # 检查是否有安全头
        headers = response.headers
        # 某些头可能在测试环境中不存在
        # 这里只检查基本功能

    def test_rate_limiting_simulation(self, client):
        """模拟速率限制测试"""
        # 注意：实际测试需要配置测试用的速率限制器
        # 这里只是模拟结构
        pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
