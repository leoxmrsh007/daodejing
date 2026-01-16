# -*- coding: utf-8 -*-
"""
疑难字标注服务
"""

# 疑难字标注配置
DIFFICULT_CHARS = {
    "徼": {"pinyin": "jiào", "meaning": "边界，边际"},
    "牝": {"pinyin": "pìn", "meaning": "鸟兽的雌性，喻指柔弱"},
    "玄牝": {"pinyin": "xuán pìn", "meaning": "微妙而神秘的母体"},
    "谷神": {"pinyin": "gǔ shén", "meaning": "形容虚空而神奇的存在"},
    "冲": {"pinyin": "chōng", "meaning": "谦虚，冲和"},
    "渊": {"pinyin": "yuān", "meaning": "深沉，深潭"},
    "湛": {"pinyin": "zhàn", "meaning": "深沉，清澈"},
    "恍": {"pinyin": "huǎng", "meaning": "惚恍，不分明"},
    "惚": {"pinyin": "hū", "meaning": "惚恍，不分明"},
    "窈": {"pinyin": "yǎo", "meaning": "深远，不见踪影"},
    "冥": {"pinyin": "míng", "meaning": "幽暗，深不可测"},
    "橐龠": {"pinyin": "tuó yuè", "meaning": "风箱，比喻虚空而能生风"},
    "刍狗": {"pinyin": "chú gǒu", "meaning": "用草扎的狗，用于祭祀"},
    "歙": {"pinyin": "xī", "meaning": "收缩，收敛"},
    "张": {"pinyin": "zhāng", "meaning": "扩张，张开"},
    "羸": {"pinyin": "léi", "meaning": "瘦弱，衰败"},
    "赘": {"pinyin": "zhuì", "meaning": "多余，累赘"},
    "沌": {"pinyin": "dùn", "meaning": "混沌兮，不分明的样子"},
    "澹": {"pinyin": "dàn", "meaning": "恬静，安定"},
    "飂": {"pinyin": "liù", "meaning": "风声，飘扬"},
    "豫": {"pinyin": "yù", "meaning": "犹豫。容：犹豫，谨慎。"},
    "犹": {"pinyin": "yóu", "meaning": "犹豫，警惕"},
    "俨": {"pinyin": "yǎn", "meaning": "恭敬，庄重"},
    "涣": {"pinyin": "huàn", "meaning": "消散，离散"},
    "敦": {"pinyin": "dūn", "meaning": "淳厚，诚恳"},
    "旷": {"pinyin": "kuàng", "meaning": "空阔，广大"},
    "混": {"pinyin": "hùn", "meaning": "混同，混浊"},
    "浊": {"pinyin": "zhuó", "meaning": "浑浊"},
    "儽": {"pinyin": "lěi", "meaning": "颓丧，疲惫"},
    "孔德": {"pinyin": "kǒng dé", "meaning": "大德，孔指甚、大"},
    "跂": {"pinyin": "qì", "meaning": "踮起脚尖"},
    "跨": {"pinyin": "kuà", "meaning": "迈大步"},
    "瑕谪": {"pinyin": "xiá zhé", "meaning": "过失，缺点"},
    "筹策": {"pinyin": "chóu cè", "meaning": "计数的筹码"},
    "楗": {"pinyin": "jiàn", "meaning": "门栓"},
    "袭明": {"pinyin": "xí míng", "meaning": "承袭光明的智慧"},
    "雄": {"pinyin": "xióng", "meaning": "雄性，刚强"},
    "雌": {"pinyin": "cí", "meaning": "鸟兽的雌性，柔弱"},
    "溪": {"pinyin": "xī", "meaning": "溪涧"},
    "式": {"pinyin": "shì", "meaning": "范式，法式"},
    "忒": {"pinyin": "tè", "meaning": "差错"},
    "谷": {"pinyin": "gǔ", "meaning": "川谷，虚怀"},
    "朴": {"pinyin": "pǔ", "meaning": "朴素，未雕琢的木材"},
    "器": {"pinyin": "qì", "meaning": "器具"},
    "嚣": {"pinyin": "xiāo", "meaning": "喧嚣，吵闹"},
    "垓": {"pinyin": "gāi", "meaning": "极远处，八荒之外"},
}


def annotate_difficult_chars(text: str) -> str:
    """
    为疑难字添加拼音和释义标注

    Args:
        text: 原始文本

    Returns:
        带标注的 HTML 文本
    """
    # 按字数降序排序，先处理长词（如"玄牝"、"谷神"）
    sorted_chars = sorted(DIFFICULT_CHARS.items(), key=lambda x: -len(x[0]))

    # 使用占位符记录已标注的内容，避免嵌套
    placeholders = {}
    temp_text = text

    for char, info in sorted_chars:
        pinyin = info['pinyin']
        meaning = info['meaning']

        # 在临时文本中查找并替换
        start = 0
        while True:
            pos = temp_text.find(char, start)
            if pos == -1:
                break

            # 执行替换，使用占位符
            placeholder = f"___PH_{len(placeholders)}___"
            span_html = f'<span class="difficult" data-pinyin="{pinyin}" data-meaning="{meaning}">{char}</span>'
            temp_text = temp_text[:pos] + placeholder + temp_text[pos + len(char):]
            placeholders[placeholder] = span_html
            start = pos + len(placeholder)

    # 将所有占位符替换回实际的HTML
    result = temp_text
    for placeholder, html in placeholders.items():
        result = result.replace(placeholder, html)

    return result
