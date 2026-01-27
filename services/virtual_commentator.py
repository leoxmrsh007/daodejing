# -*- coding: utf-8 -*-
"""
虚拟注释家对话模块
让用户与历史上的注释家进行AI对话
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CommentaryPersona:
    """注释家人设"""
    name: str
    era: str
    school: str
    style: str
    key_themes: List[str]
    tone: str
    greeting: str


# 注释家人设库
COMMENTATOR_PERSONAS = {
    'wangbi': CommentaryPersona(
        name='王弼',
        era='魏晋（226-249）',
        school='贵无派',
        style='思辨哲学',
        key_themes=['以无为本', '得意忘象', '崇本息末'],
        tone='清峻思辨',
        greeting='吾乃王弼，字辅嗣。年少而悟玄理，以无为本，以有为末。足下有何疑问？'
    ),
    'heshanggong': CommentaryPersona(
        name='河上公',
        era='西汉（不详）',
        school='黄老道家',
        style='养生修炼',
        key_themes=['养生', '治国', '精气神', '长生久视'],
        tone='务实简明',
        greeting='贫道河上公。老子之道，治国与治身一也。敢问阁下所惑何事？'
    ),
    'hanshandeqing': CommentaryPersona(
        name='憨山德清',
        era='明（1546-1623）',
        school='佛道融合',
        style='禅意融合',
        key_themes=['性体妙用', '工夫实践', '禅道双修'],
        tone='慈悲智慧',
        greeting='老僧憨山，法名德清。以佛解道，以禅参玄。愿与足下共参玄理。'
    ),
    'wangfuzhi': CommentaryPersona(
        name='王夫之',
        era='明末清初（1619-1692）',
        school='船山学派',
        style='辩证思维',
        key_themes=['势', '变', '对立统一', '经世致用'],
        tone='深沉辩证',
        greeting='吾王夫之，字而农。船山老人。天下之变，皆出于理。请问何事？'
    ),
    'suzhe': CommentaryPersona(
        name='苏辙',
        era='北宋（1039-1112）',
        school='蜀学',
        style='平实通达',
        key_themes=['体用不二', '常变相权', '自然无为'],
        tone='温和通达',
        greeting='吾苏辙，字子由。少时亦好言道，晚年深有所悟。愿闻阁下高见。'
    ),
    'lihanxu': CommentaryPersona(
        name='李涵虚',
        era='清（1806-1856）',
        school='西派丹法',
        style='内丹修炼',
        key_themes=['玄关一窍', '神气合一', '性命双修', '顺逆颠倒'],
        tone='修炼实证',
        greeting='吾李涵虚，字西月。西派丹法，重在实地修证。道友请讲。'
    ),
    'huangyuanji': CommentaryPersona(
        name='黄元吉',
        era='清（不详）',
        school='乐育堂',
        style='性命双修',
        key_themes=['玄关窍妙', '神气相依', '守中抱一'],
        tone='亲切实在',
        greeting='吾黄元吉，愿讲性命双修之道。学道须从实地下工夫。'
    ),
    'weiyuan': CommentaryPersona(
        name='魏源',
        era='清（1794-1857）',
        school='经世致用',
        style='务实改革',
        key_themes=['经世', '变法', '富国强兵', '师夷长技'],
        tone='忧国忧民',
        greeting='吾魏源，字默深。学贯中西，志在经世。老子之道，岂止清谈？'
    ),
    'xianger': CommentaryPersona(
        name='张道陵（想尔注）',
        era='东汉（34-156）',
        school='早期道教',
        style='宗教教诫',
        key_themes=['道教戒律', '长生度世', '仙道贵生'],
        tone='宗教威严',
        greeting='吾张道陵，天师道之创立者。《想尔注》专为信道者作。'
    ),
    'yanzun': CommentaryPersona(
        name='严遵（严君平）',
        era='西汉（公元前53-18）',
        school='黄老学派',
        style='宇宙生成',
        key_themes=['天地人同', '阴阳五行', '自然无为'],
        tone='古朴深远',
        greeting='吾严遵，字君平。隐居不仕，以卜筮为业。精研老子道德之经。'
    ),
    'wanganshi': CommentaryPersona(
        name='王安石',
        era='北宋（1021-1086）',
        school='荆公新学',
        style='经世致用',
        key_themes=['权时之变', '因任之术', '效用为先'],
        tone='锐意革新',
        greeting='吾王安石，字介甫。新法虽阻，老学不废。老子之道，在于经世。'
    )
}


class VirtualCommentator:
    """虚拟注释家对话管理器"""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.data = None
        self.load_data()

    def load_data(self):
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"title": "道德经", "chapters": []}

    def get_available_commentators(self, chapter_id: int) -> List[Dict]:
        """获取某章节可用的注释家"""
        chapter = next(
            (c for c in self.data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if not chapter:
            return []

        available = []
        commentary_map = {
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

        for key, field in commentary_map.items():
            text = chapter.get(field, '')
            if text and text != '此版本暂未收录':
                persona = COMMENTATOR_PERSONAS.get(key)
                if persona:
                    available.append({
                        'id': key,
                        'name': persona.name,
                        'era': persona.era,
                        'school': persona.school,
                        'style': persona.style,
                        'has_commentary': True,
                        'commentary_preview': text[:100] + '...'
                    })

        return available

    def chat_with_commentator(
        self,
        commentator_id: str,
        chapter_id: int,
        user_message: str,
        chat_history: List[Dict] = None
    ) -> Dict:
        """与注释家对话"""

        # 获取注释家人设
        persona = COMMENTATOR_PERSONAS.get(commentator_id)
        if not persona:
            return self._error_response("未找到该注释家")

        # 获取章节内容
        chapter = next(
            (c for c in self.data['chapters'] if c['chapter'] == chapter_id),
            None
        )

        if not chapter:
            return self._error_response("未找到该章节")

        # 获取注释内容
        commentary_map = {
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

        commentary_field = commentary_map.get(commentator_id)
        commentary_text = chapter.get(commentary_field, '') if commentary_field else ''

        # 生成回复
        response = self._generate_response(
            persona,
            chapter,
            commentary_text,
            user_message,
            chat_history or []
        )

        return {
            'commentator_id': commentator_id,
            'commentator_name': persona.name,
            'response': response,
            'timestamp': self._get_timestamp()
        }

    def _generate_response(
        self,
        persona: CommentaryPersona,
        chapter: Dict,
        commentary: str,
        user_message: str,
        chat_history: List[Dict]
    ) -> str:
        """生成AI回复（这里返回结构化数据，实际由前端LLM处理）"""

        # 首次问候
        if not chat_history or not any(h.get('role') == 'user' for h in chat_history):
            return persona.greeting

        # 分析用户问题类型
        question_type = self._classify_question(user_message)

        if question_type == 'meaning':
            return self._respond_meaning(persona, chapter, commentary, user_message)

        elif question_type == 'comparison':
            return self._respond_comparison(persona, chapter, commentary)

        elif question_type == 'practice':
            return self._respond_practice(persona, chapter, commentary, user_message)

        else:
            return self._respond_general(persona, chapter, commentary, user_message)

    def _classify_question(self, message: str) -> str:
        """分类用户问题"""
        meaning_keywords = ['意思', '含义', '解释', '是什么', '为何', '为何', '何为']
        practice_keywords = ['怎么', '如何', '方法', '修炼', '做到', '功夫']
        comparison_keywords = ['区别', '不同', '相比', '对比']

        message_lower = message.lower()

        if any(kw in message_lower for kw in practice_keywords):
            return 'practice'
        elif any(kw in message_lower for kw in comparison_keywords):
            return 'comparison'
        else:
            return 'meaning'

    def _respond_meaning(self, persona, chapter, commentary, question) -> str:
        """回应关于含义的问题"""
        # 返回提示，由LLM生成最终答案
        return f"[AI需要基于{persona.name}的注释风格回答: {question}]"

    def _respond_comparison(self, persona, chapter, commentary) -> str:
        """回应比较问题"""
        return f"[{persona.name}会比较自己与其他注释家的观点]"

    def _respond_practice(self, persona, chapter, commentary, question) -> str:
        """回应实践问题"""
        if '修炼' in persona.style or '丹法' in persona.style:
            return f"[{persona.name}会从实证角度回答: {question}]"
        else:
            return f"[{persona.name}会从哲学角度回答]"

    def _respond_general(self, persona, chapter, commentary, question) -> str:
        """回应一般问题"""
        return f"[{persona.name}: {persona.tone}风格回答]"

    def _error_response(self, message: str) -> Dict:
        """错误响应"""
        return {
            'error': True,
            'message': message
        }

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def initiate_debate(
        self,
        chapter_id: int,
        topic: str,
        commentators: List[str]
    ) -> Dict:
        """发起注释家辩论"""
        debate = {
            'chapter': chapter_id,
            'topic': topic,
            'participants': [],
            'rounds': []
        }

        for comm_id in commentators:
            persona = COMMENTATOR_PERSONAS.get(comm_id)
            if persona:
                debate['participants'].append({
                    'id': comm_id,
                    'name': persona.name,
                    'era': persona.era,
                    'school': persona.school,
                    'opening_statement': self._generate_opening_statement(
                        persona, chapter_id, topic
                    )
                })

        return debate

    def _generate_opening_statement(self, persona, chapter_id, topic) -> str:
        """生成开场陈述"""
        templates = {
            'wangbi': f'关于"{topic}"，吾以为当以无为本。有生于无，故贵无贱有。',
            'heshanggong': f'"{topic}"一事，当从养生治国两面观。',
            'hanshandeqing': f'关于"{topic}"，当参禅意，不滞于文字。',
            'wangfuzhi': f'"{topic}"之理，须观其变化，知其势之所必然。',
            'suzhe': f'"{topic}"，要在体用不二，非偏执一端。'
        }

        return templates.get(persona.name.lower(),
            f'{persona.name}关于"{topic}"的观点。')


class SocraticDialogue:
    """苏格拉底式对话系统"""

    def __init__(self):
        self.dialogue_state = {}
        self.current_topic = None
        self.concepts_covered = []

    def start_dialogue(self, chapter_id: int, user_knowledge_level: str = 'beginner') -> Dict:
        """开始苏格拉底式对话"""
        self.dialogue_state[chapter_id] = {
            'level': user_knowledge_level,
            'questions_asked': [],
            'concepts_explored': []
        }

        # 根据章节生成引导问题
        opening_questions = {
            1: "你认为道是什么？它是可以用语言描述的吗？",
            2: "天下人都知道什么是美，这是好事还是坏事？为什么？",
            3: "不尚贤，使民不争——这样做是否会让社会失去进取心？",
            81: "信言不美，美言不信——为什么真实的话往往不动听？"
        }

        return {
            'chapter': chapter_id,
            'opening_question': opening_questions.get(
                chapter_id,
                f"请谈谈你对第{chapter_id}章的理解。"
            ),
            'guidance': '请深入思考，不要急于给出标准答案。'
        }

    def follow_up_question(self, chapter_id: int, user_answer: str) -> str:
        """根据用户回答生成追问"""
        state = self.dialogue_state.get(chapter_id, {})

        # 分析用户回答的深度
        answer_length = len(user_answer)

        if answer_length < 20:
            return "能展开说说吗？你的想法很有趣。"
        elif answer_length < 50:
            return "这个观点很有意思。但是，有没有考虑过相反的情况？"
        else:
            return "很好的思考！那么，你说的这个道理，在生活中如何体现？"


# 便捷API函数
def get_available_commentators() -> List[Dict]:
    """获取所有可用注释家列表"""
    commentators = []
    for cid, persona in COMMENTATOR_PERSONAS.items():
        commentators.append({
            'id': cid,
            'name': persona.name,
            'era': persona.era,
            'school': persona.school,
            'style': persona.style,
            'key_themes': persona.key_themes[:3]  # 前3个主题
        })
    return commentators


def get_commentator_persona(commentator_id: str) -> Optional[Dict]:
    """获取注释家人设详情"""
    persona = COMMENTATOR_PERSONAS.get(commentator_id)
    if persona:
        return {
            'id': commentator_id,
            'name': persona.name,
            'era': persona.era,
            'school': persona.school,
            'style': persona.style,
            'key_themes': persona.key_themes,
            'tone': persona.tone,
            'greeting': persona.greeting
        }
    return None


def generate_commentary_response(
    commentator_id: str,
    chapter_id: int,
    question: str,
    conversation_context: Optional[List[Dict]] = None
) -> Dict:
    """生成注释家回应（API入口）"""
    commentator = VirtualCommentator('data/daodejing.json')

    # 获取注释家人设
    persona = COMMENTATOR_PERSONAS.get(commentator_id)
    if not persona:
        return {
            'error': '未找到该注释家',
            'commentator_id': commentator_id
        }

    # 获取章节内容
    chapter = next(
        (c for c in commentator.data['chapters'] if c['chapter'] == chapter_id),
        None
    )

    if not chapter:
        return {
            'error': '未找到该章节',
            'chapter_id': chapter_id
        }

    # 获取注释内容
    commentary_map = {
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

    commentary_field = commentary_map.get(commentator_id)
    commentary_text = chapter.get(commentary_field, '') if commentary_field else ''

    # 构建系统提示词
    system_prompt = f"""你是{persona.name}（{persona.era}），{persona.school}的代表人物。
你的思想风格：{persona.style}
你的核心主题：{', '.join(persona.key_themes)}
你的语气特点：{persona.tone}

请以{persona.name}的身份和风格回答用户的问题。回答要：
1. 符合该注释家的思想立场和时代背景
2. 使用该注释家的术语和表达方式
3. 结合道德经原文和注释内容
4. 体现出该注释家的独特见解

当前章节：第{chapter_id}章
原文：{chapter.get('original', '')}
注释内容：{commentary_text[:500] if commentary_text else '暂无注释'}

请始终保持角色设定，用古风但易懂的语言回答。"""

    # 返回结构化数据，由前端LLM生成最终回复
    return {
        'commentator_id': commentator_id,
        'commentator_name': persona.name,
        'system_prompt': system_prompt,
        'context': {
            'chapter_id': chapter_id,
            'chapter_content': chapter.get('original', ''),
            'commentary': commentary_text[:1000] if commentary_text else '',
            'commentator_style': persona.style,
            'commentator_era': persona.era
        },
        'greeting': persona.greeting,
        'response': None  # 由前端LLM生成
    }


def get_commentator_list(chapter_id: int) -> List[Dict]:
    """获取可用注释家列表"""
    commentator = VirtualCommentator('data/daodejing.json')
    return commentator.get_available_commentators(chapter_id)


def chat_with_commentator(
    commentator_id: str,
    chapter_id: int,
    message: str,
    history: List[Dict] = None
) -> Dict:
    """与注释家对话"""
    commentator = VirtualCommentator('data/daodejing.json')
    return commentator.chat_with_commentator(
        commentator_id, chapter_id, message, history
    )


def start_commentator_debate(chapter_id: int, topic: str, commentators: List[str]) -> Dict:
    """发起注释家辩论"""
    commentator = VirtualCommentator('data/daodejing.json')
    return commentator.initiate_debate(chapter_id, topic, commentators)


def start_socratic_dialogue(chapter_id: int, level: str = 'beginner') -> Dict:
    """开始苏格拉底式对话"""
    dialogue = SocraticDialogue()
    return dialogue.start_dialogue(chapter_id, level)
