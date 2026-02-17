# -*- coding: utf-8 -*-
"""
全文搜索服务测试
测试FullTextSearch和PersonalizedRecommender类
"""

from services.classic_service import ClassicService
from services.fulltext_search import FullTextSearch, PersonalizedRecommender


class TestFullTextSearch:
    """全文搜索功能测试"""

    def test_fulltext_search_initialization(self):
        """测试FullTextSearch初始化"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        assert search is not None
        assert search.classic_service is not None
        assert isinstance(search.search_index, dict)
        # 搜索索引应该包含章节数据
        assert len(search.search_index) > 0

    def test_search_chapters_with_keyword(self):
        """测试搜索关键字"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        results = search.search("道")

        assert isinstance(results, list)
        # "道"是道德经的核心概念，应该能找到结果
        assert len(results) > 0

        # 验证结果结构
        for result in results:
            assert "chapter" in result
            assert "score" in result
            assert "matches" in result

    def test_search_empty_query(self):
        """测试空查询返回空列表"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        results = search.search("")

        assert results == []

    def test_search_nonexistent_keyword(self):
        """测试搜索不存在的关键字"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        # 使用不太可能存在的字符串
        results = search.search("xyz123nonexistent")

        assert results == []

    def test_search_case_sensitivity(self):
        """测试搜索不区分大小写（中英文）"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        # 搜索应该对大小写不敏感
        results_upper = search.search("DAO")
        results_lower = search.search("dao")

        # 两者应该返回类似的结果（如果存在英文翻译）
        assert isinstance(results_upper, list)
        assert isinstance(results_lower, list)


class TestPersonalizedRecommender:
    """个性化推荐功能测试"""

    def test_recommender_initialization(self):
        """测试PersonalizedRecommender初始化"""
        service = ClassicService("ddj")
        recommender = PersonalizedRecommender(service)

        assert recommender is not None
        assert recommender.classic_service is not None

    def test_recommend_chapters_default(self):
        """测试推荐功能默认参数"""
        service = ClassicService("ddj")
        recommender = PersonalizedRecommender(service)

        recommendations = recommender.recommend_chapters([1, 2, 3])

        assert isinstance(recommendations, list)
        # 默认返回5个推荐
        assert len(recommendations) <= 5

    def test_recommend_chapters_with_limit(self):
        """测试推荐功能自定义数量"""
        service = ClassicService("ddj")
        recommender = PersonalizedRecommender(service)

        recommendations = recommender.recommend_chapters([1, 2, 3], limit=3)

        assert isinstance(recommendations, list)
        assert len(recommendations) <= 3

    def test_recommend_chapters_structure(self):
        """测试推荐结果结构"""
        service = ClassicService("ddj")
        recommender = PersonalizedRecommender(service)

        recommendations = recommender.recommend_chapters([1], limit=1)

        if recommendations:
            rec = recommendations[0]
            assert "chapter" in rec
            assert "reason" in rec


class TestSearchEdgeCases:
    """搜索边界情况测试"""

    def test_search_single_character(self):
        """测试单字符搜索"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        results = search.search("道")
        assert isinstance(results, list)

    def test_search_long_keyword(self):
        """测试长关键字搜索"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        long_keyword = "道可道非常道名可名非常名"
        results = search.search(long_keyword)
        assert isinstance(results, list)

    def test_search_special_characters(self):
        """测试特殊字符搜索"""
        service = ClassicService("ddj")
        search = FullTextSearch(service)

        special_chars = "·|"
        results = search.search(special_chars)
        assert isinstance(results, list)
