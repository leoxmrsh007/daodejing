# -*- coding: utf-8 -*-
"""
全文搜索服务
实现高性能的全文搜索功能
"""

import re
from collections import defaultdict
from typing import Any, Dict, List

import jieba


class FullTextSearch:
    """
    全文搜索引擎
    使用jieba分词实现中文全文搜索
    """

    def __init__(self, classic_service):
        """
        初始化搜索引擎

        Args:
            classic_service: ClassicService实例
        """
        self.classic_service = classic_service
        self.search_index = {}
        self._build_index()

    def _build_index(self) -> None:
        """构建搜索索引"""
        data = self.classic_service.load_data()
        chapters = data.get("chapters", [])

        # 为每个章节建立索引
        for chapter in chapters:
            chapter_id = chapter.get("chapter")

            # 收集所有可搜索的文本
            searchable_texts = []

            # 原文
            if "original" in chapter:
                searchable_texts.append(chapter["original"])

            # 现代译文
            if "modern_chinese" in chapter:
                searchable_texts.append(chapter["modern_chinese"])

            # 注释
            for key in [
                "wangbi_note",
                "heshanggong_note",
                "wangfuzhi_note",
                "hanshandeqing_note",
                "chengxuanying_note",
                "guoxiang_note",
            ]:
                if key in chapter and chapter[key]:
                    searchable_texts.append(chapter[key])

            # 英文翻译
            for key in ["english_lau", "english_henricks", "english_addiss"]:
                if key in chapter and chapter[key]:
                    searchable_texts.append(chapter[key])

            # 合并所有文本
            full_text = " ".join(searchable_texts)

            # 使用jieba分词
            words = jieba.cut(full_text)
            word_list = [w for w in words if len(w.strip()) > 0]

            # 建立倒排索引
            for word in word_list:
                word_lower = word.lower()
                if word_lower not in self.search_index:
                    self.search_index[word_lower] = []

                if chapter_id not in [
                    item["chapter"] for item in self.search_index[word_lower]
                ]:
                    # 添加章节到索引
                    context = self._get_context(word, full_text)
                    self.search_index[word_lower].append(
                        {
                            "chapter": chapter_id,
                            "title": chapter.get("title", f"第{chapter_id}章"),
                            "context": context,
                            "score": self._calculate_score(word, full_text),
                        }
                    )

    def _get_context(self, word: str, text: str, max_length: int = 100) -> str:
        """
        获取关键词上下文

        Args:
            word: 关键词
            text: 原始文本
            max_length: 最大长度

        Returns:
            上下文字符串
        """
        pos = text.lower().find(word.lower())
        if pos == -1:
            return text[:max_length] + "..."

        start = max(0, pos - 50)
        end = min(len(text), pos + 50)

        context = text[start:end]

        # 高亮关键词
        highlighted = re.sub(
            re.escape(word), f"<mark>{word}</mark>", context, flags=re.IGNORECASE
        )

        return highlighted

    def _calculate_score(self, word: str, text: str) -> float:
        """
        计算搜索相关性得分

        Args:
            word: 搜索词
            text: 文本

        Returns:
            相关性得分 (0-1)
        """
        word_lower = word.lower()
        text_lower = text.lower()

        # 词频
        frequency = text_lower.count(word_lower)

        # 位置权重（出现位置越靠前，权重越高）
        first_pos = text_lower.find(word_lower)
        position_weight = 1.0 - (first_pos / len(text)) if first_pos >= 0 else 0

        # 组合得分
        score = (frequency / 10) * 0.7 + position_weight * 0.3
        return min(score, 1.0)

    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        执行全文搜索

        Args:
            query: 搜索查询
            limit: 返回结果数量限制

        Returns:
            搜索结果列表
        """
        if not query or len(query.strip()) < 1:
            return []

        # 分词
        words = list(jieba.cut(query.strip()))
        words = [w for w in words if len(w.strip()) > 0]

        # 收集所有匹配的章节
        results: Dict[int, Dict[str, Any]] = defaultdict(
            lambda: {"chapters": [], "total_score": 0.0}
        )

        for word in words:
            word_lower = word.lower()
            if word_lower in self.search_index:
                for item in self.search_index[word_lower]:
                    chapter_id: int = item["chapter"]

                    # 累加得分
                    results[chapter_id]["total_score"] += item["score"]
                    results[chapter_id]["chapters"].append(item)

        # 整理结果
        sorted_results = sorted(
            results.items(), key=lambda x: x[1]["total_score"], reverse=True
        )

        # 格式化输出
        output: List[Dict[str, Any]] = []
        for chapter_id, data in sorted_results[:limit]:
            # 取得分最高的章节信息
            chapters_list = data["chapters"]
            best_match = max(chapters_list, key=lambda x: x["score"])
            output.append(
                {
                    "chapter": chapter_id,
                    "title": best_match["title"],
                    "score": data["total_score"],
                    "context": best_match["context"],
                    "matches": len(chapters_list),
                }
            )

        return output


class SearchHistoryManager:
    """
    搜索历史管理器
    管理用户的搜索历史记录
    """

    def __init__(self, max_history: int = 50):
        """
        初始化搜索历史管理器

        Args:
            max_history: 最大历史记录数
        """
        self.max_history = max_history
        self.history_key = "daodejing_search_history"

    def add_search(self, query: str) -> None:
        """
        添加搜索记录

        Args:
            query: 搜索查询
        """
        try:
            history = self.get_history()

            # 移除重复项
            history = [h for h in history if h["query"] != query]

            # 添加到开头
            history.insert(0, {"query": query, "timestamp": self._get_timestamp()})

            # 限制数量
            if len(history) > self.max_history:
                history = history[: self.max_history]

            # 保存 - 客户端实现
            # 注意：这里应该使用更安全的存储方式，暂时使用localStorage模拟
            _ = history  # 避免未使用变量警告

        except Exception as e:
            print(f"保存搜索历史失败: {e}")

    def get_history(self) -> List[Dict[str, Any]]:
        """
        获取搜索历史

        Returns:
            搜索历史列表
        """
        # 从客户端localStorage读取
        # 这里返回空列表，实际从客户端读取
        return []

    def clear_history(self) -> None:
        """清空搜索历史"""
        # 清空客户端localStorage
        pass

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        import time

        return str(int(time.time()))


class PersonalizedRecommender:
    """
    个性化推荐系统
    基于用户行为推荐相关内容
    """

    def __init__(self, classic_service):
        """
        初始化推荐系统

        Args:
            classic_service: ClassicService实例
        """
        self.classic_service = classic_service

    def recommend_chapters(
        self, user_history: List[int], limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        基于阅读历史推荐章节

        Args:
            user_history: 用户阅读历史（章节ID列表）
            limit: 推荐数量

        Returns:
            推荐的章节列表
        """
        if not user_history:
            # 如果没有历史，返回随机推荐
            return self._get_random_recommendations(limit)

        # 分析阅读模式
        self.classic_service.load_data()

        # 找出用户最近阅读的章节
        recent_chapters = user_history[:10]

        # 推荐策略：
        # 1. 推荐相邻章节（用户可能是连续阅读）
        # 2. 推荐相似章节（基于章节内容相似性）
        # 3. 推荐热门章节（基于关键词）

        recommendations = []

        # 策略1：相邻章节
        last_chapter = recent_chapters[0] if recent_chapters else 1
        if last_chapter > 1:
            recommendations.append({"chapter": last_chapter - 1, "reason": "相邻章节"})
        if last_chapter < self.classic_service.chapter_count:
            recommendations.append({"chapter": last_chapter + 1, "reason": "相邻章节"})

        # 策略2：相似章节（基于章节号模式）
        if len(recent_chapters) >= 3:
            # 如果用户跳着读，推荐中间的章节
            min_chapter = min(recent_chapters)
            max_chapter = max(recent_chapters)

            for chapter_id in range(min_chapter + 1, max_chapter):
                if chapter_id not in recent_chapters and len(recommendations) < limit:
                    recommendations.append(
                        {"chapter": chapter_id, "reason": "跳过的章节"}
                    )

        # 策略3：补充到推荐数量
        if len(recommendations) < limit:
            # 推荐经典章节（如第1章、第8章、第81章）
            classic_chapters = [1, 8, 81]
            for chapter_id in classic_chapters:
                if chapter_id not in recent_chapters and chapter_id not in [
                    r["chapter"] for r in recommendations
                ]:
                    recommendations.append(
                        {"chapter": chapter_id, "reason": "经典章节"}
                    )
                    if len(recommendations) >= limit:
                        break

        return recommendations[:limit]

    def _get_random_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """
        获取随机推荐

        Args:
            limit: 推荐数量

        Returns:
            推荐的章节列表
        """
        data = self.classic_service.load_data()
        chapters = data.get("chapters", [])

        # 推荐经典章节
        classic_chapters = [1, 8, 37, 81]
        recommendations = []

        for chapter_id in classic_chapters:
            chapter = next((c for c in chapters if c["chapter"] == chapter_id), None)
            if chapter:
                recommendations.append({"chapter": chapter_id, "reason": "经典章节"})
                if len(recommendations) >= limit:
                    break

        return recommendations
