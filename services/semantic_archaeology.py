# -*- coding: utf-8 -*-
"""
语义考古学服务
分析道德经文本在历史传播中的语义变迁
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import difflib


class SemanticArchaeology:
    """语义考古分析器"""

    # 文本版本映射
    TEXT_VERSIONS = {
        'guodian': {
            'name': '郭店楚简',
            'period': '战国中期（约公元前4世纪）',
            'characteristics': '最早版本，不避汉讳，字数较少',
            'source': '湖北荆门郭店一号墓'
        },
        'postsilk': {
            'name': '马王堆帛书',
            'period': '西汉早期（约公元前2世纪）',
            'characteristics': '避汉高祖刘邦讳，分甲乙本',
            'source': '长沙马王堆三号汉墓'
        },
        'wangbi': {
            'name': '王弼本（通行本）',
            'period': '魏晋（3世纪）',
            'characteristics': '流传最广，文学性最强',
            'source': '王弼《老子道德经注》'
        },
        'heshanggong': {
            'name': '河上公本',
            'period': '西汉',
            'characteristics': '注重养生治国，章句划分不同',
            'source': '河上公《老子章句》'
        }
    }

    # 已知的关键文字变异
    TEXT_VARIANTS = {
        '常 vs 恒': {
            'guodian': '恒',
            'postsilk': '恒',
            'received': '常',  # 通行本
            'reason': '避汉文帝刘恒讳改为常',
            'significance': '恒意为长久、永恒，比常更贴切老子原意'
        },
        '已 vs 矣': {
            'guodian': '已',
            'postsilk': '已',
            'received': '矣',
            'reason': '字形演变',
            'significance': '虚词用法的变化'
        },
        '邦 vs 国': {
            'guodian': '邦',
            'postsilk': '邦',
            'received': '国',
            'reason': '避汉高祖刘邦讳改为国',
            'significance': '邦更强调政治实体'
        },
        '光 vs 旷': {
            'guodian': '光',
            'postsilk': '光',
            'received': '旷',
            'reason': '文字演变',
            'significance': '词义从光明变为宽广'
        }
    }

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = None

    def load_data(self):
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except FileNotFoundError:
            return {"title": "道德经", "chapters": []}

    def analyze_text_evolution(self, chapter_id: int) -> Dict:
        """分析文本演变"""
        chapter = next(
            (c for c in self.data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if not chapter:
            return None

        evolution = {
            'chapter': chapter_id,
            'versions': [],
            'variants': [],
            'semantic_shifts': []
        }

        # 收集各版本文本
        received_text = chapter.get('original', '')

        # 郭店简本
        if chapter.get('guodian_text'):
            evolution['versions'].append({
                'version': 'guodian',
                'text': chapter.get('guodian_text'),
                'diff_note': chapter.get('guodian_diff', '')
            })

        # 帛书本
        if chapter.get('postsilk_text'):
            evolution['versions'].append({
                'version': 'postsilk',
                'text': chapter.get('postsilk_text'),
                'diff_note': chapter.get('postsilk_diff', '')
            })

        # 通行本
        evolution['versions'].append({
            'version': 'received',
            'text': received_text,
            'diff_note': '原文'
        })

        # 分析文字变异
        evolution['variants'] = self._detect_variants(
            chapter.get('guodian_text', ''),
            chapter.get('postsilk_text', ''),
            received_text
        )

        # 分析语义变迁
        evolution['semantic_shifts'] = self._analyze_semantic_shifts(
            chapter.get('guodian_diff', ''),
            chapter.get('postsilk_diff', '')
        )

        return evolution

    def _detect_variants(self, guodian: str, postsilk: str, received: str) -> List[Dict]:
        """检测文字变异"""
        variants = []

        # 检测已知变异
        for variant_name, variant_info in self.TEXT_VARIANTS.items():
            ancient_char = variant_info['guodian']
            modern_char = variant_info['received']

            if ancient_char in received:
                variants.append({
                    'type': variant_name,
                    'ancient': ancient_char,
                    'modern': modern_char,
                    'found_in': '通行本保留古字',
                    'significance': variant_info['significance']
                })

        # 检测帛书特有变异
        if postsilk and received:
            # 简单的字符级比较
            diff = list(difflib.unified_diff(
                received.split(),
                postsilk.split(),
                lineterm=''
            ))
            if diff:
                variants.append({
                    'type': '句式差异',
                    'description': '帛书本与通行本在句式上存在差异',
                    'diff_sample': ''.join(diff[:50])  # 前50字符
                })

        return variants

    def _analyze_semantic_shifts(self, guodian_diff: str, postsilk_diff: str) -> List[Dict]:
        """分析语义变迁"""
        shifts = []

        if guodian_diff:
            shifts.append({
                'period': '战国→现代',
                'description': guodian_diff,
                'significance': '早期版本的原始语义'
            })

        if postsilk_diff:
            shifts.append({
                'period': '西汉→现代',
                'description': postsilk_diff,
                'significance': '汉代文本的过渡形态'
            })

        return shifts

    def trace_concept_history(self, concept: str) -> Dict:
        """追溯概念的历史演变"""
        # 跨章节分析概念
        concept_evolution = {
            'concept': concept,
            'occurrences': [],
            'semantic_layers': []
        }

        # 这里可以扩展为更复杂的语义演变分析
        # 目前返回基础结构

        return concept_evolution

    def compare_interpretation_history(self, chapter_id: int, concept: str) -> Dict:
        """比较历代对同一概念的阐释历史"""
        chapter = next(
            (c for c in self.data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if not chapter:
            return None

        interpretations = []

        # 河上公（汉代）- 养生治身
        if chapter.get('heshanggong_note'):
            interpretations.append({
                'commentator': '河上公',
                'era': '西汉',
                'interpretation': self._extract_interpretation(
                    chapter['heshanggong_note'], concept
                ),
                'style': '养生修炼'
            })

        # 王弼（魏晋）- 贵无本体
        if chapter.get('wangbi_note'):
            interpretations.append({
                'commentator': '王弼',
                'era': '魏晋',
                'interpretation': self._extract_interpretation(
                    chapter['wangbi_note'], concept
                ),
                'style': '本体思辨'
            })

        # 憨山（明）- 佛道融合
        if chapter.get('hanshandeqing_note'):
            interpretations.append({
                'commentator': '憨山德清',
                'era': '明代',
                'interpretation': self._extract_interpretation(
                    chapter['hanshandeqing_note'], concept
                ),
                'style': '禅意融合'
            })

        # 王夫之（明末清初）- 唯物辩证
        if chapter.get('wangfuzhi_note'):
            interpretations.append({
                'commentator': '王夫之',
                'era': '明末清初',
                'interpretation': self._extract_interpretation(
                    chapter['wangfuzhi_note'], concept
                ),
                'style': '辩证思维'
            })

        return {
            'chapter': chapter_id,
            'concept': concept,
            'interpretations': interpretations,
            'evolution_summary': self._summarize_evolution(interpretations)
        }

    def _extract_interpretation(self, text: str, concept: str) -> str:
        """提取注释中对概念的解释"""
        if not text or concept not in text:
            return "未直接阐释"

        # 简单提取：查找概念前后的句子
        sentences = re.split('[。，；！？]', text)
        for sentence in sentences:
            if concept in sentence:
                # 清理和截取
                cleaned = sentence.strip()
                if len(cleaned) > 100:
                    return cleaned[:100] + "..."
                return cleaned

        return "概念在注释中被提及"

    def _summarize_evolution(self, interpretations: List[Dict]) -> str:
        """总结阐释演变"""
        if not interpretations:
            return "暂无阐释记录"

        styles = [interp.get('style', '') for interp in interpretations]

        if len(styles) >= 2:
            return f"阐释风格从{styles[0]}逐渐向{styles[-1]}演变"
        elif len(styles) == 1:
            return f"主要呈现{styles[0]}风格"

        return "阐释风格多样"


class VectorSemanticAnalyzer:
    """向量语义分析器（用于语义考古）"""

    def __init__(self):
        # 模拟语义向量（实际应用中应使用真实的嵌入模型）
        self.semantic_vectors = {}

    def calculate_semantic_distance(self, text1: str, text2: str) -> float:
        """计算语义距离（简化版）"""
        # 实际应用中应使用BERT/SentenceTransformer
        # 这里使用简化的字符重合度

        set1 = set(text1)
        set2 = set(text2)

        if not set1 or not set2:
            return 1.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return 1.0 - (intersection / union if union > 0 else 0)

    def detect_semantic_drift(self, versions: List[Dict]) -> List[Dict]:
        """检测语义漂移"""
        drifts = []

        if len(versions) < 2:
            return drifts

        for i in range(len(versions) - 1):
            v1 = versions[i]
            v2 = versions[i + 1]

            distance = self.calculate_semantic_distance(
                v1.get('text', ''),
                v2.get('text', '')
            )

            if distance > 0.1:  # 有显著差异
                drifts.append({
                    'from_version': v1.get('version'),
                    'to_version': v2.get('version'),
                    'drift_amount': distance,
                    'significance': '中等差异' if distance < 0.3 else '显著差异'
                })

        return drifts


# 便捷函数
def get_chapter_archaeology(chapter_id: int) -> Dict:
    """获取章节语义考古分析"""
    archaeology = SemanticArchaeology('data/daodejing.json')
    archaeology.load_data()

    return {
        'text_evolution': archaeology.analyze_text_evolution(chapter_id),
        'semantic_drifts': archaeology.analyze_text_evolution(chapter_id)
    }


def get_concept_interpretation_history(chapter_id: int, concept: str) -> Dict:
    """获取概念阐释历史"""
    archaeology = SemanticArchaeology('data/daodejing.json')
    archaeology.load_data()

    return archaeology.compare_interpretation_history(chapter_id, concept)
