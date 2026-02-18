# -*- coding: utf-8 -*-
"""
全文搜索服务 (增强版)
实现高性能的全文搜索功能，支持TF-IDF评分、模糊搜索和多维度过滤
"""

import math
import re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

import jieba
from thefuzz import process


class TFIDFCalculator:
    """
    TF-IDF 计算器
    计算词频-逆文档频率，用于衡量词语在文档中的重要性
    """

    def __init__(self) -> None:
        """初始化TF-IDF计算器"""
        # document_frequency: 词 -> 包含该词的文档数
        self.document_frequency: Dict[str, int] = defaultdict(int)
        # total_documents: 总文档数
        self.total_documents: int = 0

    def fit(self, documents: List[List[str]]) -> None:
        """
        训练DF统计

        Args:
            documents: 分词后的文档列表
        """
        self.total_documents = len(documents)

        # 统计每个词出现在多少文档中
        seen_words: Set[str] = set()
        for doc_words in documents:
            seen_words.clear()
            for word in doc_words:
                if word not in seen_words:
                    self.document_frequency[word] += 1
                    seen_words.add(word)

    def calculate_tfidf(self, word: str, document: List[str], doc_length: int) -> float:
        """
        计算TF-IDF值

        Args:
            word: 目标词
            document: 文档所有词列表
            doc_length: 文档长度

        Returns:
            TF-IDF值 (归一化到 0-1)
        """
        if doc_length == 0:
            return 0.0

        # TF (Term Frequency): 词频 / 文档长度
        term_frequency = document.count(word) / doc_length

        # IDF (Inverse Document Frequency): log(总文档数 / 包含该词的文档数)
        # 使用平滑版本：log((总文档数 + 1) / (包含该词的文档数 + 1)) + 1
        idf = (
            math.log(
                (self.total_documents + 1) / (self.document_frequency.get(word, 0) + 1)
            )
            + 1
        )

        # 使用更直观的评分方式：归一化到 0-1
        # 词频权重 (0-0.5): 词出现越多分数越高
        tf_score = min(term_frequency * 10, 0.5)

        # IDF权重 (0-0.5): 词越稀有分数越高
        max_idf = math.log(self.total_documents + 1) + 1
        idf_score = (idf / max_idf) * 0.5

        return min(tf_score + idf_score, 1.0)


class FullTextSearch:
    """
    全文搜索引擎 (增强版)
    支持TF-IDF评分、模糊搜索、多维度过滤和跨经典搜索
    """

    def __init__(self, classic_services: Dict[str, Any]) -> None:
        """
        初始化搜索引擎

        Args:
            classic_services: 经典服务字典 {classic_id: ClassicService}
        """
        self.classic_services = classic_services
        self.search_index: Dict[str, List[Dict[str, Any]]] = {}

        # TF-IDF相关
        self.tfidf_calculator = TFIDFCalculator()
        self.document_words: Dict[int, List[str]] = {}  # chapter_id -> 分词列表
        self.chapter_to_classic: Dict[int, str] = {}  # chapter_id -> classic_id

        # 构建索引
        self._build_index()

    def _build_index(self) -> None:
        """构建搜索索引"""
        documents: List[List[str]] = []
        chapter_ids: List[int] = []

        # 遍历所有经典
        for classic_id, service in self.classic_services.items():
            try:
                data = service.load_data()
                chapters = data.get("chapters", [])

                for chapter in chapters:
                    chapter_id = chapter.get("chapter")
                    if not chapter_id:
                        continue

                    # 记录章节属于哪个经典
                    self.chapter_to_classic[chapter_id] = classic_id

                    # 收集所有可搜索的文本
                    searchable_texts = self._collect_searchable_texts(chapter)

                    # 合并所有文本
                    full_text = " ".join(searchable_texts)

                    # 使用jieba分词
                    words = list(jieba.cut(full_text))
                    words = [w.lower() for w in words if len(w.strip()) > 0]
                    self.document_words[chapter_id] = words

                    # 记录文档用于TF-IDF训练
                    documents.append(words)
                    chapter_ids.append(chapter_id)

                    # 建立倒排索引
                    self._build_inverted_index(chapter_id, chapter, words)

            except Exception as e:
                print(f"构建索引失败 [{classic_id}]: {e}")

        # 训练TF-IDF
        self.tfidf_calculator.fit(documents)

    def _collect_searchable_texts(self, chapter: Dict[str, Any]) -> List[str]:
        """
        收集章节中所有可搜索的文本

        Args:
            chapter: 章节数据

        Returns:
            文本列表
        """
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
            "zhuxi_note",
            "wangyangming_note",
        ]:
            if key in chapter and chapter[key]:
                searchable_texts.append(chapter[key])

        # 英文翻译
        for key in [
            "english_lau",
            "english_henricks",
            "english_addiss",
            "english_watson",
            "english_ziporyn",
        ]:
            if key in chapter and chapter[key]:
                searchable_texts.append(chapter[key])

        return searchable_texts

    def _build_inverted_index(
        self, chapter_id: int, chapter: Dict[str, Any], words: List[str]
    ) -> None:
        """
        建立倒排索引

        Args:
            chapter_id: 章节ID
            chapter: 章节数据
            words: 分词列表
        """
        # 统计词频
        word_count: Dict[str, int] = defaultdict(int)
        for word in words:
            word_count[word] += 1

        # 为每个词建立索引
        for word, count in word_count.items():
            if word not in self.search_index:
                self.search_index[word] = []

            # 添加章节到索引
            self.search_index[word].append(
                {
                    "chapter": chapter_id,
                    "title": chapter.get("title", f"第{chapter_id}章"),
                    "count": count,
                }
            )

    def search(
        self,
        query: str,
        classic_id: Optional[str] = None,
        commentator: Optional[str] = None,
        content_type: Optional[str] = None,
        limit: int = 20,
        fuzzy_threshold: int = 70,
    ) -> List[Dict[str, Any]]:
        """
        执行全文搜索

        Args:
            query: 搜索查询
            classic_id: 经典ID过滤 (None表示搜索所有经典)
            commentator: 注释家过滤
            content_type: 内容类型过滤 (original/modern/notes/english)
            limit: 返回结果数量限制
            fuzzy_threshold: 模糊搜索相似度阈值 (0-100)

        Returns:
            搜索结果列表
        """
        if not query or len(query.strip()) < 1:
            return []

        query = query.strip()

        # 1. 分词
        query_words = list(jieba.cut(query))
        query_words = [w.lower() for w in query_words if len(w.strip()) > 0]

        if not query_words:
            return []

        # 2. 收集所有匹配的章节 (精确匹配 + 模糊匹配)
        results: Dict[int, Dict[str, Any]] = defaultdict(
            lambda: {
                "total_score": 0.0,
                "matched_words": set(),
                "match_details": [],
            }
        )

        # 2.1 精确匹配
        for word in query_words:
            self._add_exact_matches(word, results)

        # 2.2 模糊匹配 (如果没有精确匹配或结果太少)
        if len(results) < limit // 2:
            self._add_fuzzy_matches(query_words, results, fuzzy_threshold)

        # 3. 应用过滤器
        filtered_results = self._apply_filters(
            results, classic_id, commentator, content_type, query_words
        )

        # 4. 整理结果并按分数排序
        sorted_results = sorted(
            filtered_results.items(), key=lambda x: x[1]["total_score"], reverse=True
        )

        # 5. 格式化输出
        output: List[Dict[str, Any]] = []
        for chapter_id, data in sorted_results[:limit]:
            output.append(self._format_result(chapter_id, data, query_words))

        return output

    def _add_exact_matches(self, word: str, results: Dict[int, Dict[str, Any]]) -> None:
        """
        添加精确匹配结果

        Args:
            word: 搜索词
            results: 结果字典
        """
        if word not in self.search_index:
            return

        for item in self.search_index[word]:
            chapter_id = item["chapter"]
            words = self.document_words.get(chapter_id, [])

            # 计算TF-IDF分数
            tfidf_score = self.tfidf_calculator.calculate_tfidf(word, words, len(words))

            # 累加分数
            results[chapter_id]["total_score"] += tfidf_score
            results[chapter_id]["matched_words"].add(word)
            results[chapter_id]["match_details"].append(
                {
                    "word": word,
                    "type": "exact",
                    "tfidf_score": tfidf_score,
                }
            )

    def _add_fuzzy_matches(
        self,
        query_words: List[str],
        results: Dict[int, Dict[str, Any]],
        threshold: int,
    ) -> None:
        """
        添加模糊匹配结果

        Args:
            query_words: 查询词列表
            results: 结果字典
            threshold: 相似度阈值
        """
        # 收集索引中所有词
        all_index_words = list(self.search_index.keys())

        for query_word in query_words:
            # 使用thefuzz进行模糊匹配
            matches = process.extract(query_word, all_index_words, limit=5)

            for matched_word, similarity in matches:
                if similarity >= threshold:
                    # 将模糊匹配作为近似精确匹配处理
                    self._add_exact_matches(matched_word, results)

                    # 更新匹配类型
                    for chapter_id in results:
                        for detail in results[chapter_id]["match_details"]:
                            if (
                                detail["word"] == matched_word
                                and detail["type"] == "exact"
                            ):
                                detail["type"] = "fuzzy"
                                detail["similarity"] = similarity

    def _apply_filters(
        self,
        results: Dict[int, Dict[str, Any]],
        classic_id: Optional[str],
        commentator: Optional[str],
        content_type: Optional[str],
        query_words: List[str],
    ) -> Dict[int, Dict[str, Any]]:
        """
        应用过滤器

        Args:
            results: 原始结果
            classic_id: 经典ID过滤
            commentator: 注释家过滤
            content_type: 内容类型过滤
            query_words: 查询词列表

        Returns:
            过滤后的结果
        """
        filtered: Dict[int, Dict[str, Any]] = {}

        for chapter_id, data in results.items():
            # 获取章节详情
            chapter_detail = self._get_chapter_detail(chapter_id)
            if not chapter_detail:
                continue

            # 经典过滤
            if classic_id and self.chapter_to_classic.get(chapter_id) != classic_id:
                continue

            # 注释家过滤
            if commentator:
                comment_key = f"{commentator}_note"
                if comment_key not in chapter_detail or not chapter_detail[comment_key]:
                    continue

            # 内容类型过滤
            if content_type:
                # 检查是否在指定内容类型中匹配
                text_to_search = ""
                if content_type == "original":
                    text_to_search = chapter_detail.get("original", "")
                elif content_type == "modern":
                    text_to_search = chapter_detail.get("modern_chinese", "")
                elif content_type == "notes":
                    text_to_search = " ".join(
                        [
                            chapter_detail.get(k, "")
                            for k in chapter_detail
                            if k.endswith("_note")
                        ]
                    )
                elif content_type == "english":
                    text_to_search = " ".join(
                        [
                            chapter_detail.get(k, "")
                            for k in chapter_detail
                            if k.startswith("english_")
                        ]
                    )

                # 检查是否有匹配词
                text_lower = text_to_search.lower()
                has_match = any(word in text_lower for word in query_words)
                if not has_match:
                    continue

            filtered[chapter_id] = data

        return filtered

    def _get_chapter_detail(self, chapter_id: int) -> Optional[Dict[str, Any]]:
        """
        获取章节详情

        Args:
            chapter_id: 章节ID

        Returns:
            章节数据
        """
        classic_id = self.chapter_to_classic.get(chapter_id)
        if not classic_id:
            return None

        service = self.classic_services.get(classic_id)
        if not service:
            return None

        try:
            data = service.load_data()
            chapters = data.get("chapters", [])
            return next(
                (c for c in chapters if c.get("chapter") == chapter_id),
                None,
            )
        except Exception:
            return None

    def _format_result(
        self, chapter_id: int, data: Dict[str, Any], query_words: List[str]
    ) -> Dict[str, Any]:
        """
        格式化搜索结果

        Args:
            chapter_id: 章节ID
            data: 结果数据
            query_words: 查询词列表

        Returns:
            格式化的结果
        """
        chapter_detail = self._get_chapter_detail(chapter_id)
        if not chapter_detail:
            return {
                "chapter": chapter_id,
                "title": f"第{chapter_id}章",
                "score": data["total_score"],
                "context": "",
                "matches": 0,
                "highlighted_context": "",
            }

        classic_id = self.chapter_to_classic.get(chapter_id, "")
        service = self.classic_services.get(classic_id)
        classic_name = service.to_dict().get("name", "") if service else ""

        # 合并所有文本用于提取上下文
        all_text = self._collect_searchable_texts(chapter_detail)
        full_text = " ".join(all_text)

        # 提取上下文并高亮
        highlighted_context = self._get_context_with_highlighting(
            query_words, full_text
        )

        return {
            "chapter": chapter_id,
            "title": chapter_detail.get("title", f"第{chapter_id}章"),
            "classic_id": classic_id,
            "classic_name": classic_name,
            "score": round(data["total_score"], 4),
            "matches": len(data["matched_words"]),
            "matched_words": list(data["matched_words"]),
            "context": self._get_plain_context(full_text),
            "highlighted_context": highlighted_context,
            "match_type": (
                "fuzzy"
                if any(d.get("type") == "fuzzy" for d in data.get("match_details", []))
                else "exact"
            ),
        }

    def _get_context_with_highlighting(
        self, query_words: List[str], text: str, max_length: int = 150
    ) -> str:
        """
        获取带高亮的上下文

        Args:
            query_words: 查询词列表
            text: 原始文本
            max_length: 最大长度

        Returns:
            带高亮的上下文
        """
        if not text:
            return ""

        # 找到最佳匹配位置
        best_pos = -1
        for word in query_words:
            pos = text.lower().find(word.lower())
            if pos != -1 and (best_pos == -1 or pos < best_pos):
                best_pos = pos

        if best_pos == -1:
            return text[:max_length] + ("..." if len(text) > max_length else "")

        # 提取上下文
        context_start = max(0, best_pos - 50)
        context_end = min(len(text), best_pos + max_length - 50)
        context = text[context_start:context_end]

        # 高亮所有匹配词
        highlighted = context
        for word in query_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            highlighted = pattern.sub(
                f'<mark class="search-highlight">{word}</mark>', highlighted
            )

        # 添加省略号
        if context_start > 0:
            highlighted = "..." + highlighted
        if context_end < len(text):
            highlighted = highlighted + "..."

        return highlighted

    def _get_plain_context(self, text: str, max_length: int = 100) -> str:
        """
        获取纯文本上下文（无高亮）

        Args:
            text: 原始文本
            max_length: 最大长度

        Returns:
            纯文本上下文
        """
        if not text:
            return ""
        return text[:max_length] + ("..." if len(text) > max_length else "")


class SearchHistoryManager:
    """
    搜索历史管理器
    管理用户的搜索历史记录
    """

    def __init__(self, max_history: int = 50) -> None:
        """
        初始化搜索历史管理器

        Args:
            max_history: 最大历史记录数
        """
        self.max_history = max_history
        self.history_key = "daodejing_search_history"

    def add_search(self, query: str, filters: Optional[Dict[str, Any]] = None) -> None:
        """
        添加搜索记录

        Args:
            query: 搜索查询
            filters: 搜索过滤器
        """
        try:
            history = self.get_history()

            # 移除重复项
            history = [
                h
                for h in history
                if h["query"] != query or h.get("filters", {}) != (filters or {})
            ]

            # 添加到开头
            history.insert(
                0,
                {
                    "query": query,
                    "filters": filters or {},
                    "timestamp": self._get_timestamp(),
                },
            )

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

    def __init__(self, classic_services: Dict[str, Any]) -> None:
        """
        初始化推荐系统

        Args:
            classic_services: 经典服务字典
        """
        self.classic_services = classic_services

    def recommend_chapters(
        self,
        user_history: List[Tuple[str, int]],
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        基于阅读历史推荐章节

        Args:
            user_history: 用户阅读历史 [(classic_id, chapter_id), ...]
            limit: 推荐数量

        Returns:
            推荐的章节列表
        """
        if not user_history:
            return self._get_random_recommendations(limit)

        recommendations = []

        # 策略1：相邻章节
        last_classic_id, last_chapter_id = user_history[0]
        last_service = self.classic_services.get(last_classic_id)
        if last_service:
            data = last_service.load_data()
            chapter_count = len(data.get("chapters", []))

            # 推荐上一章
            if last_chapter_id > 1:
                recommendations.append(
                    {
                        "classic_id": last_classic_id,
                        "chapter": last_chapter_id - 1,
                        "reason": "相邻章节",
                    }
                )

            # 推荐下一章
            if last_chapter_id < chapter_count:
                recommendations.append(
                    {
                        "classic_id": last_classic_id,
                        "chapter": last_chapter_id + 1,
                        "reason": "相邻章节",
                    }
                )

        # 策略2：推荐跨经典相似章节
        if len(user_history) >= 3:
            recommendations.extend(
                self._recommend_cross_classic_similar(
                    user_history, limit - len(recommendations)
                )
            )

        # 策略3：经典章节
        if len(recommendations) < limit:
            recommendations.extend(
                self._recommend_classic_chapters(
                    user_history, limit - len(recommendations)
                )
            )

        # 填充章节详情
        for rec in recommendations:
            classic_id = str(rec.get("classic_id", ""))
            service = self.classic_services.get(classic_id)
            if service:
                chapter = service.get_chapter(rec.get("chapter", 1))
                if chapter:
                    rec["title"] = chapter.get("title", f"第{rec.get('chapter', 1)}章")
                    rec["classic_name"] = service.to_dict().get("name", "")

        return recommendations[:limit]

    def _recommend_cross_classic_similar(
        self, user_history: List[Tuple[str, int]], limit: int
    ) -> List[Dict[str, Any]]:
        """
        推荐跨经典相似章节

        Args:
            user_history: 用户历史
            limit: 推荐数量

        Returns:
            推荐列表
        """
        recommendations: List[Dict[str, Any]] = []

        # 获取用户最常读的经典
        classic_counts: Dict[str, int] = defaultdict(int)
        for classic_id, _ in user_history:
            classic_counts[classic_id] += 1

        # 为每个经典推荐经典章节
        sorted_classics = sorted(
            classic_counts.items(), key=lambda x: x[1], reverse=True
        )

        for classic_id, _count in sorted_classics[:2]:
            # 跳过用户最常读的经典（因为已经在相邻章节推荐了）
            if classic_id == user_history[0][0]:
                continue

            # 推荐该经典的经典章节
            service = self.classic_services.get(str(classic_id))
            if service:
                classic_chapters = self._get_classic_chapters(service)
                for chapter_id in classic_chapters[
                    : min(2, limit - len(recommendations))
                ]:
                    recommendations.append(
                        {
                            "classic_id": classic_id,
                            "chapter": chapter_id,
                            "reason": f"推荐经典：{service.to_dict().get('name', '')}",
                        }
                    )

                if len(recommendations) >= limit:
                    break

        return recommendations

    def _recommend_classic_chapters(
        self, user_history: List[Tuple[str, int]], limit: int
    ) -> List[Dict[str, Any]]:
        """
        推荐经典章节

        Args:
            user_history: 用户历史
            limit: 推荐数量

        Returns:
            推荐列表
        """
        recommendations = []

        # 用户已读过的章节
        read_chapters = {(cid, ch) for cid, ch in user_history}

        # 遍历所有经典，推荐经典章节
        classic_chapters_map: Dict[str, List[int]] = {
            "ddj": [1, 8, 37, 81],
            "zzj": [1, 6, 7, 33],  # 逍遥游、齐物论、养生主、大宗师
            "jgj": [1],  # 金刚经只有1章
            "ss": [1, 2, 3],  # 大学、中庸、论语
            "cxl": [1, 2, 3],  # 传习录前3条
        }

        for classic_id, chapter_ids in classic_chapters_map.items():
            for chapter_id in chapter_ids:
                if (classic_id, chapter_id) not in read_chapters:
                    recommendations.append(
                        {
                            "classic_id": classic_id,
                            "chapter": chapter_id,
                            "reason": "经典章节",
                        }
                    )

                    if len(recommendations) >= limit:
                        break

            if len(recommendations) >= limit:
                break

        return recommendations

    def _get_classic_chapters(self, service: Any) -> List[int]:
        """
        获取指定经典的经典章节

        Args:
            service: ClassicService实例

        Returns:
            章节ID列表
        """
        classic_id = service.classic_id if hasattr(service, "classic_id") else "ddj"

        classic_chapters_map: Dict[str, List[int]] = {
            "ddj": [1, 8, 37, 81],
            "zzj": [1, 6, 7, 33],
            "jgj": [1],
            "ss": [1, 2, 3],
            "cxl": [1, 2, 3],
        }

        return classic_chapters_map.get(classic_id, [1])

    def _get_random_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """
        获取随机推荐

        Args:
            limit: 推荐数量

        Returns:
            推荐的章节列表
        """
        recommendations: List[Dict[str, Any]] = []

        # 为每个经典推荐1个经典章节
        for classic_id in ["ddj", "zzj", "ss"]:
            service = self.classic_services.get(str(classic_id))
            if service:
                classic_chapters = self._get_classic_chapters(service)
                for chapter_id in classic_chapters[:1]:
                    recommendations.append(
                        {
                            "classic_id": classic_id,
                            "chapter": chapter_id,
                            "reason": "经典章节",
                        }
                    )

                    if len(recommendations) >= limit:
                        break

            if len(recommendations) >= limit:
                break

        # 填充章节详情
        for rec in recommendations:
            service = self.classic_services.get(str(rec["classic_id"]))
            if service:
                chapter = service.get_chapter(rec["chapter"])
                if chapter:
                    rec["title"] = chapter.get("title", f"第{rec['chapter']}章")
                    rec["classic_name"] = service.to_dict().get("name", "")

        return recommendations[:limit]
