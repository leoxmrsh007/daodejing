# -*- coding: utf-8 -*-
"""
知识图谱服务 - 活态注释系统
构建道德经概念关系网络和注释观点谱系
"""

import json
import re
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
import os


class ConceptExtractor:
    """概念提取器 - 从文本中提取核心概念"""

    # 道德经核心概念库
    CORE_CONCEPTS = {
        '一级概念': ['道', '德', '无', '有', '无为', '自然', '朴', '虚', '静'],
        '二级概念': ['天', '地', '万物', '圣人', '百姓', '天下', '身', '心'],
        '修养概念': ['观', '守', '抱', '持', '养', '积', '损', '益'],
        '政治概念': ['治', '国', '民', '王', '侯', '霸', '兵', '战'],
        ' metaphors ': ['水', '谷', '牝', '婴儿', '朴', '舟', '器', '光'],
    }

    # 概念关系类型
    RELATION_TYPES = [
        '包含关系',    # 道 包含 无、有
        '对立统一',    # 无 <-> 有
        '因果关联',    # 无为 → 无不为
        '比喻映射',    # 上善若水
        '实践方法',    # 守中、抱一
        '否定对比',    # 绝圣弃智
    ]

    def __init__(self):
        self.concept_chapters = defaultdict(set)  # 概念出现的章节
        self.concept_cooccurrence = defaultdict(Counter)  # 概念共现

    def extract_from_chapter(self, chapter_id: int, text: str) -> Set[str]:
        """从章节中提取概念"""
        concepts = set()

        # 提取单字概念
        for char in text:
            if char in '道德无为有朴虚静自然治身观守抱持养':
                concepts.add(char)

        # 提取双字概念
        double_concepts = [
            '无为', '自然', '虚静', '守中', '抱一', '归根',
            '复命', '玄同', '玄牝', '谷神', '朴器',
            '圣人', '百姓', '天地', '万物', '天下',
            '上善', '若水', '不争', '柔弱', '知足',
            '清静', '无为', '无事', '无味', '无欲',
            '绝圣', '弃智', '见素', '抱朴', '少私',
            '寡欲', '玄德', '微妙', '玄通', '玄览'
        ]

        for concept in double_concepts:
            if concept in text:
                concepts.add(concept)

        # 记录章节关联
        for concept in concepts:
            self.concept_chapters[concept].add(chapter_id)

        return concepts

    def build_cooccurrence_network(self, chapters_data: List[Dict]) -> Dict:
        """构建概念共现网络"""
        for chapter in chapters_data:
            concepts = self.extract_from_chapter(
                chapter['chapter'],
                chapter.get('original', '') + chapter.get('modern_chinese', '')
            )

            # 记录共现关系
            concept_list = list(concepts)
            for i, c1 in enumerate(concept_list):
                for c2 in concept_list[i+1:]:
                    self.concept_cooccurrence[c1][c2] += 1
                    self.concept_cooccurrence[c2][c1] += 1

        return dict(self.concept_cooccurrence)


class CommentryAnalyzer:
    """注释分析器 - 分析历代注释的观点"""

    # 注释家画像
    COMMENTATOR_PROFILES = {
        'wangbi': {
            'name': '王弼',
            'era': '魏晋（226-249）',
            'school': '贵无派',
            'keywords': ['以无为本', '崇本息末', '得意忘象'],
            'style': '思辨哲学',
            'focus': '本体论'
        },
        'heshanggong': {
            'name': '河上公',
            'era': '西汉（公元前2-1世纪）',
            'school': '黄老道家',
            'keywords': ['养生', '治身', '精气神'],
            'style': '养生修炼',
            'focus': '修身治国'
        },
        'hanshandeqing': {
            'name': '憨山德清',
            'era': '明（1546-1623）',
            'school': '佛道融合',
            'keywords': ['性体', '妙用', '工夫'],
            'style': '禅意融合',
            'focus': '心性修养'
        },
        'wangfuzhi': {
            'name': '王夫之',
            'era': '明末清初（1619-1692）',
            'school': '唯物主义',
            'keywords': ['势', '变', '矛盾'],
            'style': '辩证思维',
            'focus': '变动哲学'
        },
        'suzhe': {
            'name': '苏辙',
            'era': '北宋（1039-1112）',
            'school': '理学影响',
            'keywords': ['体用', '常变'],
            'style': '平实通达',
            'focus': '处世哲学'
        },
        'lihanxu': {
            'name': '李涵虚',
            'era': '清（1806-1856）',
            'school': '西派丹法',
            'keywords': ['玄关', '火候', '炼丹'],
            'style': '内丹修炼',
            'focus': '丹道修炼'
        },
        'huangyuanji': {
            'name': '黄元吉',
            'era': '清（？）',
            'school': '中派丹法',
            'keywords': ['玄关', '真意', '神气'],
            'style': '性命双修',
            'focus': '内丹实修'
        },
        'weiyuan': {
            'name': '魏源',
            'era': '清（1794-1857）',
            'school': '经世致用',
            'keywords': ['经世', '变法'],
            'style': '务实改革',
            'focus': '社会改革'
        },
        'xianger': {
            'name': '想尔注',
            'era': '东汉（张陵/张道陵）',
            'school': '早期道教',
            'keywords': ['道教', '戒律', '长生'],
            'style': '宗教教诫',
            'focus': '宗教修行'
        },
        'yanzun': {
            'name': '严遵',
            'era': '西汉（公元前53-18）',
            'school': '黄老学派',
            'keywords': ['无为', '自然', '神明'],
            'style': '宇宙生成',
            'focus': '天道自然'
        },
        'wanganshi': {
            'name': '王安石',
            'era': '北宋（1021-1086）',
            'school': '荆公新学',
            'keywords': ['权时', '变通', '效用'],
            'style': '经世致用',
            'focus': '政治改革'
        }
    }

    def __init__(self):
        self.commentary_views = defaultdict(dict)  # 存储各注释家观点

    def analyze_commentary(self, chapter_id: int, field: str, text: str, commentator: str) -> Dict:
        """分析单条注释"""
        profile = self.COMMENTATOR_PROFILES.get(field, {})

        return {
            'chapter': chapter_id,
            'commentator': field,
            'commentator_name': profile.get('name', field),
            'era': profile.get('era', ''),
            'school': profile.get('school', ''),
            'text': text[:500] if text else '',  # 前500字摘要
            'text_length': len(text) if text else 0,
            'key_concepts': self._extract_key_concepts(text),
            'stance': self._detect_stance(text),
            'focus_area': profile.get('focus', ''),
            'style': profile.get('style', '')
        }

    def _extract_key_concepts(self, text: str) -> List[str]:
        """提取注释中的关键概念"""
        if not text:
            return []

        concepts = []
        key_terms = [
            '气', '神', '虚', '静', '动', '阴阳', '太极',
            '心', '性', '命', '精', '意', '念',
            '治国', '修身', '养生', '炼丹', '性命',
            '本体', '功用', '工夫', '境界',
            '自然', '无为', '有为', '玄妙',
            '天地', '万物', '圣人', '百姓'
        ]

        for term in key_terms:
            if term in text:
                concepts.append(term)

        return concepts[:5]

    def _detect_stance(self, text: str) -> str:
        """检测注释立场倾向"""
        if not text:
            return '中性'

        # 简单关键词检测
        if any(w in text for w in ['气', '丹', '修炼', '精气神', '玄关']):
            return '修炼向'
        if any(w in text for w in ['治国', '帝王', '政治', '天下', '百姓']):
            return '治世向'
        if any(w in text for w in ['理', '性', '心', '本体', '玄妙']):
            return '义理向'
        return '中性'

    def compare_commentators(self, chapter_id: int, commentaries: Dict) -> List[Dict]:
        """比较不同注释家的观点"""
        comparisons = []

        commentators = list(commentaries.keys())
        for i in range(len(commentators)):
            for j in range(i+1, len(commentators)):
                c1, c2 = commentators[i], commentators[j]
                text1 = commentaries.get(c1, '')
                text2 = commentaries.get(c2, '')

                if text1 and text2:
                    similarity = self._calculate_similarity(text1, text2)
                    comparisons.append({
                        'commentator1': c1,
                        'commentator2': c2,
                        'similarity': similarity,
                        'relationship': self._determine_relationship(similarity)
                    })

        return sorted(comparisons, key=lambda x: x['similarity'], reverse=True)

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简化版）"""
        if not text1 or not text2:
            return 0.0

        # 简单的字符级Jaccard相似度
        set1 = set(text1)
        set2 = set(text2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0

    def _determine_relationship(self, similarity: float) -> str:
        """确定关系类型"""
        if similarity > 0.5:
            return '观点相近'
        elif similarity > 0.3:
            return '部分相关'
        elif similarity > 0.1:
            return '有差异'
        else:
            return '角度不同'


class KnowledgeGraphBuilder:
    """知识图谱构建器"""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = None
        self.concept_extractor = ConceptExtractor()
        self.commentary_analyzer = CommentryAnalyzer()

    def load_data(self):
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except FileNotFoundError:
            return {"title": "道德经", "chapters": []}

    def build_concept_graph(self) -> Dict:
        """构建概念图谱"""
        if not self.data:
            return {}

        nodes = []
        edges = []
        concept_map = {}

        # 处理所有章节
        for chapter in self.data['chapters']:
            text = chapter.get('original', '')
            concepts = self.concept_extractor.extract_from_chapter(
                chapter['chapter'], text
            )

            for concept in concepts:
                if concept not in concept_map:
                    # 确定概念层级
                    level = self._get_concept_level(concept)
                    concept_map[concept] = {
                        'id': concept,
                        'label': concept,
                        'level': level,
                        'chapters': list(self.concept_extractor.concept_chapters[concept]),
                        'count': len(self.concept_extractor.concept_chapters[concept])
                    }

        # 构建节点
        for concept_id, info in concept_map.items():
            nodes.append({
                'id': concept_id,
                'label': concept_id,
                'level': info['level'],
                'size': 10 + info['count'] * 2,
                'chapters': info['chapters']
            })

        # 构建边（基于共现关系）
        cooccurrence = self.concept_extractor.concept_cooccurrence
        for c1, related in cooccurrence.items():
            for c2, weight in related.items():
                if weight >= 2:  # 至少共现2次
                    edges.append({
                        'source': c1,
                        'target': c2,
                        'weight': weight,
                        'label': self._infer_relation(c1, c2)
                    })

        return {
            'nodes': nodes,
            'edges': edges,
            'concept_count': len(nodes),
            'edge_count': len(edges)
        }

    def _get_concept_level(self, concept: str) -> int:
        """获取概念层级"""
        if concept in ['道', '德']:
            return 1
        if concept in ['无', '有', '无为', '自然', '朴']:
            return 2
        if concept in ['天', '地', '万物', '圣人']:
            return 3
        return 4

    def _infer_relation(self, c1: str, c2: str) -> str:
        """推断概念关系"""
        known_relations = {
            ('无', '有'): '对立统一',
            ('道', '无'): '包含关系',
            ('道', '有'): '包含关系',
            ('无为', '自然'): '方法关系',
            ('天', '地'): '并列关系',
            ('阴', '阳'): '对立统一',
            ('水', '善'): '比喻关系',
            ('婴儿', '朴'): '比喻关系',
        }

        return known_relations.get((c1, c2)) or known_relations.get((c2, c1)) or '关联关系'

    def build_commentary_spectrum(self, chapter_id: int) -> Dict:
        """构建注释观点谱系"""
        chapter = next(
            (c for c in self.data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if not chapter:
            return {}

        commentaries = {}
        commentary_fields = {
            'wangbi': 'wangbi_note',
            'heshanggong': 'heshanggong_note',
            'wangfuzhi': 'wangfuzhi_note',
            'hanshandeqing': 'hanshandeqing_note',
            'suzhe': 'suzhe_note',
            'lihanxu': 'lihanxu_note',
            'huangyuanji': 'huangyuanji_note',
            'weiyuan': 'weiyuan_note',
            'xianger': 'xianger_note',
            'yanzun': 'yanzun_note',
            'wanganshi': 'wanganshi_note'
        }

        # 收集注释
        for field, text_field in commentary_fields.items():
            text = chapter.get(text_field, '')
            if text and text != '此版本暂未收录':
                commentaries[field] = self.commentary_analyzer.analyze_commentary(
                    chapter_id, field, text, field
                )

        # 比较注释家观点
        comparisons = self.commentary_analyzer.compare_commentators(
            chapter_id, {k: v.get('text', '') for k, v in commentaries.items()}
        )

        # 聚类分析
        clusters = self._cluster_commentaries(commentaries)

        return {
            'chapter': chapter_id,
            'commentaries': commentaries,
            'comparisons': comparisons[:10],  # 前10组比较
            'clusters': clusters,
            'summary': self._generate_summary(commentaries, comparisons)
        }

    def _cluster_commentaries(self, commentaries: Dict) -> List[Dict]:
        """聚类注释观点"""
        clusters = {
            '修炼向': [],
            '治世向': [],
            '义理向': [],
            '中性': []
        }

        for field, info in commentaries.items():
            stance = info.get('stance', '中性')
            clusters[stance].append({
                'commentator': field,
                'name': info.get('commentator_name', field),
                'key_concepts': info.get('key_concepts', [])
            })

        # 转换为列表格式
        return [
            {'type': '修炼向', 'members': clusters['修炼向']},
            {'type': '治世向', 'members': clusters['治世向']},
            {'type': '义理向', 'members': clusters['义理向']},
            {'type': '中性', 'members': clusters['中性']}
        ]

    def _generate_summary(self, commentaries: Dict, comparisons: List) -> str:
        """生成注释概要"""
        count = len(commentaries)
        if count == 0:
            return "本章暂无注释"

        summary_parts = [f"本章共有{count}家注释"]

        # 统计立场分布
        stances = [c.get('stance', '中性') for c in commentaries.values()]
        stance_count = Counter(stances)

        for stance, cnt in stance_count.most_common():
            if cnt > 0 and stance != '中性':
                summary_parts.append(f"{stance}注释{cnt}家")

        return "，".join(summary_parts)


def get_chapter_knowledge_graph(chapter_id: int) -> Dict:
    """获取章节知识图谱（API入口）"""
    graph_builder = KnowledgeGraphBuilder('data/daodejing.json')
    graph_builder.load_data()

    return {
        'concept_graph': graph_builder.build_concept_graph(),
        'commentary_spectrum': graph_builder.build_commentary_spectrum(chapter_id)
    }


def get_all_concepts() -> List[Dict]:
    """获取所有概念列表"""
    graph_builder = KnowledgeGraphBuilder('data/daodejing.json')
    data = graph_builder.load_data()

    concept_extractor = ConceptExtractor()
    for chapter in data['chapters']:
        concept_extractor.extract_from_chapter(
            chapter['chapter'],
            chapter.get('original', '')
        )

    concepts = []
    for concept, chapters in concept_extractor.concept_chapters.items():
        concepts.append({
            'concept': concept,
            'chapter_count': len(chapters),
            'chapters': sorted(list(chapters))
        })

    return sorted(concepts, key=lambda x: x['chapter_count'], reverse=True)
