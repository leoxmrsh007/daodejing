# -*- coding: utf-8 -*-
"""
跨文明哲学对话引擎
让道德经与西方哲学、印度哲学等进行AI对话
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class PhilosopherType(Enum):
    """哲学家类型"""
    CHINESE = "中国哲学"
    WESTERN = "西方哲学"
    INDIAN = "印度哲学"
    MODERN = "现代哲学"


@dataclass
class PhilosopherPersona:
    """哲学家人设"""
    id: str
    name: str
    culture: str
    era: str
    school: str
    key_concepts: List[str]
    laozi_correspondence: List[str]  # 与老子概念的对应
    dialogue_style: str
    greeting: str


# 跨文明哲学家人设库
CROSS_CIVILIZATION_PHILOSOPHERS = {
    # 中国哲学家
    'zhuangzi': PhilosopherPersona(
        id='zhuangzi',
        name='庄子',
        culture='中国',
        era='战国中期（约公元前369-286）',
        school='道家',
        key_concepts=['逍遥', '齐物', '无用之用', '庖丁解牛', '蝴蝶梦'],
        laozi_correspondence=['道', '无为', '自然'],
        dialogue_style='寓言比喻，汪洋恣肆',
        greeting='吾庄周，漆园吏也。子所言者，吾亦有闻乎？'
    ),
    'confucius': PhilosopherPersona(
        id='confucius',
        name='孔子',
        culture='中国',
        era='春秋末期（公元前551-479）',
        school='儒家',
        key_concepts=['仁', '义', '礼', '智', '信', '君子'],
        laozi_correspondence=['道', '德', '无为'],
        dialogue_style='循循善诱，因材施教',
        greeting='吾孔丘，字仲尼。老聃之学，与吾儒道有别，愿闻其详。'
    ),
    'moz': PhilosopherPersona(
        id='moz',
        name='墨子',
        culture='中国',
        era='战国初期（约公元前468-376）',
        school='墨家',
        key_concepts=['兼爱', '非攻', '尚贤', '节用'],
        laozi_correspondence=['道', '不争'],
        dialogue_style='质朴务实，逻辑严密',
        greeting='吾墨翟。老子之道，与吾兼爱非攻之旨，似有不同。'
    ),
    'wangyangming': PhilosopherPersona(
        id='wangyangming',
        name='王阳明',
        culture='中国',
        era='明代（1472-1529）',
        school='心学',
        key_concepts=['心即理', '知行合一', '致良知'],
        laozi_correspondence=['道', '德', '知'],
        dialogue_style='直指人心，简明扼要',
        greeting='吾王守仁，字伯安。致良知之学，与老氏之说，或可相通。'
    ),

    # 西方哲学家
    'heidegger': PhilosopherPersona(
        id='heidegger',
        name='海德格尔',
        culture='德国',
        era='现代（1889-1976）',
        school='存在主义',
        key_concepts=['Dasein（此在）', 'Sein（存在）', 'Nichts（虚无）'],
        laozi_correspondence=['道', '无', '有'],
        dialogue_style='深奥晦涩，追问存在',
        greeting='Ich bin Martin Heidegger. Das Dao... das Sein... ist das gleiche?'
    ),
    'derrida': PhilosopherPersona(
        id='derrida',
        name='德里达',
        culture='法国',
        era='后现代（1930-2004）',
        school='解构主义',
        key_concepts=['différance（延异）', 'trace（痕迹）', 'supplement（补充）'],
        laozi_correspondence=['无', '有', '言'],
        dialogue_style='文本解构，颠覆逻各斯中心',
        greeting='Derrida ici. Le Tao... la trace... la différence... '
    ),
    'deleuze': PhilosopherPersona(
        id='deleuze',
        name='德勒兹',
        culture='法国',
        era='后现代（1925-1995）',
        school='后结构主义',
        key_concepts=['becoming（生成）', 'rhizome（根茎）', 'multiplicity（多样性）'],
        laozi_correspondence=['道', '变', '流'],
        dialogue_style='流动生成，反对二元对立',
        greeting='Je suis Gilles Deleuze. Le Tao... le devenir... le flux...'
    ),
    'wittgenstein': PhilosopherPersona(
        id='wittgenstein',
        name='维特根斯坦',
        culture='奥地利/英国',
        era='现代（1889-1951）',
        school='语言哲学',
        key_concepts=['language games', 'forms of life', 'silence'],
        laozi_correspondence=['道', '言', '名'],
        dialogue_style='语言分析，逻辑追问',
        greeting='Wittgenstein here. Whereof one cannot speak, thereof one must be silent.'
    ),
    'plato': PhilosopherPersona(
        id='plato',
        name='柏拉图',
        culture='古希腊',
        era='古典时期（约公元前427-347）',
        school='理念论',
        key_concepts=['Idea（理念）', 'The Good（善）', 'Forms（形式）'],
        laozi_correspondence=['道', '德'],
        dialogue_style='对话体，理性探索',
        greeting='I am Plato of Athens. The Form of the Good... is it like the Dao?'
    ),
    'kant': PhilosopherPersona(
        id='kant',
        name='康德',
        culture='德国',
        era='近代（1724-1804）',
        school='先验唯心论',
        key_concepts=['Ding an sich（物自体）', 'practical reason', 'moral law'],
        laozi_correspondence=['德', '自然', '自由'],
        dialogue_style='严谨批判，系统论述',
        greeting='Ich bin Immanuel Kant. Die Moral... das Naturgesetz... ähnlich?'
    ),
    'nietzsche': PhilosopherPersona(
        id='nietzsche',
        name='尼采',
        culture='德国',
        era='现代（1844-1900）',
        school='生命哲学',
        key_concepts=['Will to Power', 'Übermensch', 'Eternal Recurrence'],
        laozi_correspondence=['无为', '超人', '水'],
        dialogue_style='诗意激情，重估一切价值',
        greeting='Ich bin Friedrich Nietzsche. Das Wasser... der Übermensch... wie Laozi?'
    ),

    # 印度哲学家
    'nagarjuna': PhilosopherPersona(
        id='nagarjuna',
        name='龙树',
        culture='印度',
        era='中世纪（约150-250）',
        school='中观派',
        key_concepts=['Śūnyatā（空性）', 'Madhyamaka（中道）', 'Two Truths（二谛）'],
        laozi_correspondence=['无', '有', '中'],
        dialogue_style='逻辑破执，归入空性',
        greeting='I am Nāgārjuna. Śūnyatā... Wu... emptiness... the same?'
    ),
    'shankara': PhilosopherPersona(
        id='shankara',
        name='商羯罗',
        culture='印度',
        era='古典时期（约788-820）',
        school='不二论吠檀多',
        key_concepts=['Brahman（梵）', 'Maya（幻）', 'Moksha（解脱）'],
        laozi_correspondence=['道', '德', '无名'],
        dialogue_style='论证精密，归元于梵',
        greeting='I am Śaṅkara. Brahman... the Dao... the Ultimate Reality?'
    ),

    # 现代物理学家
    'bohr': PhilosopherPersona(
        id='bohr',
        name='玻尔',
        culture='丹麦',
        era='现代（1885-1962）',
        school='量子物理学',
        key_concepts=['Complementarity（互补性）', 'Quantum indeterminacy'],
        laozi_correspondence=['阴阳', '有无'],
        dialogue_style='互补思维，微观世界',
        greeting='I am Niels Bohr. Complementarity... Yin-Yang... fascinating!'
    ),
    'einstein': PhilosopherPersona(
        id='einstein',
        name='爱因斯坦',
        culture='德国/美国',
        era='现代（1879-1955）',
        school='相对论物理学',
        key_concepts=['Spacetime', 'Field equations', 'Cosmological constant'],
        laozi_correspondence=['时空', '宇宙'],
        dialogue_style='直观洞察，统一场论',
        greeting='I am Albert Einstein. The universe... Dao... fascinating!'
    ),
}


class ConceptMapper:
    """概念映射器 - 跨哲学概念对应"""

    # 道德经概念与其他哲学传统的对应
    CONCEPT_MAPPINGS = {
        '道': {
            '古希腊': ['Logos（逻各斯）', 'The One（太一）', 'Form of the Good（善之理念）'],
            '印度': ['Brahman（梵）', 'Dharma（法）', 'Śūnyatā（空性）'],
            '现代西方': ['Being（存在）', 'Ground of being', 'Absolute'],
            '物理学': ['Quantum field（量子场）', 'Unified field（统一场）']
        },
        '德': {
            '古希腊': ['Areté（卓越）', 'Virtue（德性）'],
            '印度': ['Dharma（法/ Duty）', 'Karma（业）'],
            '儒家': ['仁', '德'],
            '现代西方': ['Intrinsic value（内在价值）', 'Integrity（完整性）']
        },
        '无': {
            '古希腊': ['Apeiron（阿派朗/无限）'],
            '印度': ['Śūnyatā（空性）', 'Māyā（幻）'],
            '现代西方': ['Nothingness（虚无）', 'The Void（虚空）'],
            '物理学': ['Vacuum state（真空态）', 'Zero-point energy']
        },
        '有': {
            '古希腊': ['Being（存在）', 'Substance（实体）'],
            '印度': ['Māyā（显现）', 'Rūpa（色）'],
            '现代西方': ['Presence（在场）', 'Existence']
        },
        '无为': {
            '古希腊': ['Apatheia（不动心）'],
            '印度': ['Nishkama karma（无贪求之行）'],
            '现代西方': ['Letting be（让存在）', 'Non-action（不行动）'],
            '现代': ['Flow（心流）', 'Wu-wei in action']
        },
        '自然': {
            '古希腊': ['Physis（自然/本性）'],
            '斯多葛派': ['Living according to nature'],
            '现代': ['Ecology（生态学）', 'Sustainability']
        },
        '水': {
            '古希腊': ['Formlessness（无形）', 'Adaptability（适应性）'],
            '现代物理': ['Fluid dynamics（流体动力学）']
        }
    }

    def get_correspondence(self, laozi_concept: str, philosopher_id: str) -> List[str]:
        """获取概念对应关系"""
        mappings = self.CONCEPT_MAPPINGS.get(laozi_concept, {})

        philosopher = CROSS_CIVILIZATION_PHILOSOPHERS.get(philosopher_id)
        if not philosopher:
            return []

        culture = philosopher.culture
        culture_map = {
            '古希腊': ['古希腊'],
            '德国': ['现代西方', '古希腊'],
            '法国': ['现代西方'],
            '奥地利': ['现代西方'],
            '丹麦': ['物理学'],
            '印度': ['印度'],
            '中国': ['儒家', '中国哲学']
        }

        relevant_categories = culture_map.get(culture, [])

        results = []
        for category, concepts in mappings.items():
            if any(cat in category for cat in relevant_categories):
                results.extend(concepts)

        return results


class DialogueEngine:
    """对话引擎 - 驱动跨文明对话"""

    def __init__(self):
        self.mapper = ConceptMapper()
        self.active_dialogues = {}

    def initiate_dialogue(
        self,
        chapter_id: int,
        laozi_concept: str,
        philosopher1_id: str,
        philosopher2_id: str
    ) -> Dict:
        """发起两个哲学家之间的对话"""

        phil1 = CROSS_CIVILIZATION_PHILOSOPHERS.get(philosopher1_id)
        phil2 = CROSS_CIVILIZATION_PHILOSOPHERS.get(philosopher2_id)

        if not phil1 or not phil2:
            return {'error': '哲学家不存在'}

        # 生成对话话题
        topic = self._generate_dialogue_topic(laozi_concept, phil1, phil2)

        # 获取概念对应
        correspondences = self.mapper.get_correspondence(laozi_concept, philosopher1_id)

        return {
            'chapter': chapter_id,
            'topic': laozi_concept,
            'participant1': {
                'id': philosopher1_id,
                'name': phil1.name,
                'culture': phil1.culture,
                'era': phil1.era,
                'school': phil1.school,
                'opening': self._generate_opening_remark(phil1, laozi_concept, correspondences)
            },
            'participant2': {
                'id': philosopher2_id,
                'name': phil2.name,
                'culture': phil2.culture,
                'era': phil2.era,
                'school': phil2.school,
                'opening': self._generate_opening_remark(phil2, laozi_concept, correspondences)
            },
            'dialogue_state': {
                'round': 1,
                'exchanges': []
            }
        }

    def _generate_dialogue_topic(self, concept: str, phil1, phil2) -> str:
        """生成对话话题"""
        return f'关于"{concept}"的跨文明对话：{phil1.name}与{phil2.name}'

    def _generate_opening_remark(self, philosopher: PhilosopherPersona, concept: str, correspondences: List[str]) -> str:
        """生成开场白"""

        if philosopher.id == 'heidegger':
            return f'Das {concept}... 在我们西方哲学中，{correspondences[0] if correspondences else "Sein"}与之相近。但这真的是同一回事吗？'

        elif philosopher.id == 'zhuangzi':
            return f'吾闻老聃言{concept}，意旨深远。吾之"逍遥"，岂非{concept}之体现？'

        elif philosopher.id == 'plato':
            return f'The {concept} of Laozi... reminds me of the {correspondences[0] if correspondences else "Form of the Good"}. But are they identical?'

        elif philosopher.id == 'nagarjuna':
            return f'{concept}... 这就是"空性"（Śūnyatā）啊！缘起性空，性空缘起。'

        elif philosopher.id == 'derrida':
            return f'Le {concept}... 总是在延异（différance）中逃避在场（presence）。'

        elif philosopher.id == 'bohr':
            return f'{concept}... 就像光既是波又是粒子，这或许是互补性原理的古老表达。'

        else:
            return f'关于"{concept}"，{philosopher.culture}哲学有{philosopher.key_concepts[0] if philosopher.key_concepts else "相近概念"}与之对应。'

    def generate_exchange(
        self,
        dialogue_id: str,
        last_statement: str,
        responder_id: str
    ) -> str:
        """生成对话回应"""

        philosopher = CROSS_CIVILIZATION_PHILOSOPHERS.get(responder_id)
        if not philosopher:
            return "对话无法继续"

        # 这里应该调用LLM生成回应
        # 返回结构化提示，由前端处理

        return f"[{philosopher.name}对上一句话的回应，基于{philosopher.school}学派思想]"

    def generate_comparative_analysis(
        self,
        chapter_id: int,
        concept: str,
        selected_philosophers: List[str]
    ) -> Dict:
        """生成比较分析报告"""

        analysis = {
            'chapter': chapter_id,
            'concept': concept,
            'philosophers': [],
            'correspondences': {},
            'commonalities': [],
            'differences': [],
            'synthesis': ''
        }

        for phil_id in selected_philosophers:
            phil = CROSS_CIVILIZATION_PHILOSOPHERS.get(phil_id)
            if phil:
                correspondences = self.mapper.get_correspondence(concept, phil_id)
                analysis['philosophers'].append({
                    'id': phil_id,
                    'name': phil.name,
                    'culture': phil.culture,
                    'school': phil.school,
                    'correspondences': correspondences
                })

        # 生成共同点
        analysis['commonalities'] = self._find_commonalities(
            concept, selected_philosophers
        )

        # 生成差异点
        analysis['differences'] = self._find_differences(
            concept, selected_philosophers
        )

        # 生成综合观点
        analysis['synthesis'] = self._generate_synthesis(
            concept, analysis['commonalities'], analysis['differences']
        )

        return analysis

    def _find_commonalities(self, concept: str, philosopher_ids: List[str]) -> List[str]:
        """找出共同点"""
        commonalities = []

        # 所有关注"存在/本体"的传统
        ontology_philosophers = ['heidegger', 'plato', 'nagarjuna', 'shankara']
        if any(p in philosopher_ids for p in ontology_philosophers):
            commonalities.append(f'都关注{concept}作为本体/终极实在的问题')

        # 所有关注"实践/方法"的传统
        practice_philosophers = ['confucius', 'moz', 'zhuangzi', 'nietzsche']
        if any(p in philosopher_ids for p in practice_philosophers):
            commonalities.append('都强调实践/修养的重要性')

        return commonalities

    def _find_differences(self, concept: str, philosopher_ids: List[str]) -> List[str]:
        """找出差异点"""
        differences = []

        # 西方重分析，东方重体悟
        western = ['heidegger', 'derrida', 'deleuze', 'kant']
        eastern = ['zhuangzi', 'confucius', 'nagarjuna', 'wangyangming']

        has_western = any(p in philosopher_ids for p in western)
        has_eastern = any(p in philosopher_ids for p in eastern)

        if has_western and has_eastern:
            differences.append('西方哲学偏重理性分析，东方哲学偏重体悟直觉')
            differences.append('西方多用概念逻辑，东方多用寓言类比')

        return differences

    def _generate_synthesis(self, concept: str, commonalities: List, differences: List) -> str:
        """生成综合观点"""
        if not commonalities and not differences:
            return f'对"{concept}"的跨文明对话揭示人类思想的深层共通性。'

        synthesis = f'通过对"{concept}"的跨文明比较，我们发现'
        if commonalities:
            synthesis += f'它们{commonalities[0]}，'
        if differences:
            synthesis += f'同时在{differences[0]}。'

        return synthesis


# 便捷API函数
def get_available_philosophers() -> List[Dict]:
    """获取可用哲学家列表"""
    philosophers = []
    for phil_id, phil in CROSS_CIVILIZATION_PHILOSOPHERS.items():
        philosophers.append({
            'id': phil_id,
            'name': phil.name,
            'culture': phil.culture,
            'era': phil.era,
            'school': phil.school,
            'key_concepts': phil.key_concepts,
            'correspondence_count': len(phil.laozi_correspondence)
        })
    return philosophers


def start_philosophy_dialogue(
    chapter_id: int,
    concept: str,
    philosopher1: str,
    philosopher2: str
) -> Dict:
    """发起哲学对话"""
    engine = DialogueEngine()
    return engine.initiate_dialogue(chapter_id, concept, philosopher1, philosopher2)


def get_comparative_analysis(
    chapter_id: int,
    concept: str,
    philosophers: List[str]
) -> Dict:
    """获取比较分析"""
    engine = DialogueEngine()
    return engine.generate_comparative_analysis(chapter_id, concept, philosophers)


def get_concept_correspondences(concept: str, philosopher_id: str) -> List[str]:
    """获取概念对应关系"""
    mapper = ConceptMapper()
    return mapper.get_correspondence(concept, philosopher_id)
