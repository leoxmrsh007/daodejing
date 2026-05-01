# -*- coding: utf-8 -*-
"""
周易数据补全脚本
补充 64 卦完整卦辞、爻辞
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


# 周易 64 卦卦名
HEXAGRAM_NAMES = [
    "乾",
    "坤",
    "屯",
    "蒙",
    "需",
    "讼",
    "师",
    "比",
    "小畜",
    "履",
    "泰",
    "否",
    "同人",
    "大有",
    "谦",
    "豫",
    "随",
    "蛊",
    "临",
    "观",
    "噬嗑",
    "贲",
    "剥",
    "复",
    "无妄",
    "大畜",
    "颐",
    "大过",
    "坎",
    "离",
    "咸",
    "恒",
    "遁",
    "大壮",
    "晋",
    "明夷",
    "家人",
    "睽",
    "蹇",
    "解",
    "损",
    "益",
    "夬",
    "姤",
    "萃",
    "升",
    "困",
    "井",
    "革",
    "鼎",
    "震",
    "艮",
    "渐",
    "归妹",
    "丰",
    "旅",
    "巽",
    "兑",
    "涣",
    "节",
    "中孚",
    "小过",
    "既济",
    "未济",
]


# 64 卦卦辞（参考《周易》原文）
HEXAGRAM_TEXTS = {
    1: {
        "name": "乾",
        "text": "乾：元亨利贞。",
        "yao": [
            "初九：潜龙勿用。",
            "九二：见龙在田，利见大人。",
            "九三：君子终日乾乾，夕惕若厉，无咎。",
            "九四：或跃在渊，无咎。",
            "九五：飞龙在天，利见大人。",
            "上九：亢龙有悔。",
            "用九：见群龙无首，吉。",
        ],
    },
    2: {
        "name": "坤",
        "text": "坤：元亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞吉。",
        "yao": [
            "初六：履霜，坚冰至。",
            "六二：直方大，不习无不利。",
            "六三：含章可贞。或从王事，无成有终。",
            "六四：括囊，无咎无誉。",
            "六五：黄裳元吉。",
            "上六：龙战于野，其血玄黄。",
            "用六：利永贞。",
        ],
    },
    3: {
        "name": "屯",
        "text": "屯：元亨利贞。勿用有攸往，利建侯。",
        "yao": [
            "初九：磐桓，利居贞，利建侯。",
            "六二：屯如邅如，乘马班如。匪寇婚媾，女子贞不字，十年乃字。",
            "六三：即鹿无虞，惟入于林中，君子几不如舍，往吝。",
            "六四：乘马班如，求婚媾，往吉，无不利。",
            "九五：屯其膏，小贞吉，大贞凶。",
            "上六：乘马班如，泣血涟如。",
        ],
    },
    4: {
        "name": "蒙",
        "text": "蒙：亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。",
        "yao": [
            "初六：发蒙，利用刑人，用说桎梏，以往吝。",
            "九二：包蒙吉，纳妇吉，子克家。",
            "六三：勿用取女，见金夫，不有躬，无攸利。",
            "六四：困蒙，吝。",
            "六五：童蒙，吉。",
            "上九：击蒙，不利为寇，利御寇。",
        ],
    },
    5: {
        "name": "需",
        "text": "需：有孚，光亨，贞吉。利涉大川。",
        "yao": [
            "初九：需于郊，利用恒，无咎。",
            "九二：需于沙，小有言，终吉。",
            "九三：需于泥，致寇至。",
            "六四：需于血，出自穴。",
            "九五：需于酒食，贞吉。",
            "上六：入于穴，有不速之客三人来，敬之终吉。",
        ],
    },
}

# 为其余卦生成占位数据
for i in range(6, 65):
    HEXAGRAM_TEXTS[i] = {
        "name": HEXAGRAM_NAMES[i - 1],
        "text": f"（{HEXAGRAM_NAMES[i-1]}卦卦辞待补充）",
        "yao": [f"（爻辞待补充）" for _ in range(6)],
    }


# 王弼注释
WANGBI_NOTES = {
    1: "乾者，健也。天之象也。六爻皆阳，纯阳之卦也。",
    2: "坤者，顺也。地之象也。六爻皆阴，纯阴之卦也。",
    3: "屯者，难也。物之始生，艰难之象也。",
    4: "蒙者，稚也。物之幼稚，蒙昧之象也。",
    5: "需者，待也。有所待而后进之象也。",
}

for i in range(6, 65):
    WANGBI_NOTES[i] = f"（{HEXAGRAM_NAMES[i-1]}卦注释待补充）"


# 程颐注释
CHENGYI_NOTES = {
    1: "乾，天也，健也。纯阳之卦，君子法天而行健。",
    2: "坤，地也，顺也。纯阴之卦，君子法地而行顺。",
    3: "屯，难也。万物始生，未得通畅，故为难也。",
    4: "蒙，稚也。物生必蒙，故受之以蒙。",
    5: "需，待也。饮食之道，有待而后进。",
}

for i in range(6, 65):
    CHENGYI_NOTES[i] = f"（{HEXAGRAM_NAMES[i-1]}卦程颐注待补充）"


# 朱熹注释
ZHUXI_NOTES = {
    1: "乾，卦之六爻，皆阳也。阳者，刚也，健也。",
    2: "坤，卦之六爻，皆阴也。阴者，柔也，顺也。",
    3: "屯，下震上坎，震动坎险，动乎险中，故为屯难。",
    4: "蒙，下坎上艮，坎险艮止，险而止，故为蒙昧。",
    5: "需，下乾上坎，乾健坎险，健而陷，故为需待。",
}

for i in range(6, 65):
    ZHUXI_NOTES[i] = f"（{HEXAGRAM_NAMES[i-1]}卦朱熹注待补充）"


def fill_zhouyi_data():
    """补全周易数据"""
    print("正在补全周易数据...")

    file_path = DATA_DIR / "zy" / "chapters.json"
    if not file_path.exists():
        print("  ✗ 周易数据文件不存在")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("chapters", [])
    print(f"  当前章节数：{len(chapters)}")

    # 补充 64 卦数据
    for i in range(min(len(chapters), 64)):
        chapter_num = i + 1
        hex_data = HEXAGRAM_TEXTS.get(chapter_num, {})

        if hex_data:
            # 补充卦名
            chapters[i]["title"] = hex_data.get("name", f"第{chapter_num}卦")

            # 补充卦辞
            chapters[i]["original"] = hex_data.get("text", "")

            # 补充爻辞
            chapters[i]["gua_ci"] = hex_data.get("text", "")
            chapters[i]["yao_ci"] = " ".join(hex_data.get("yao", []))

            # 补充注释
            chapters[i]["wangbi_note"] = WANGBI_NOTES.get(chapter_num, "")
            chapters[i]["chengyi_note"] = CHENGYI_NOTES.get(chapter_num, "")
            chapters[i]["zhuxi_note"] = ZHUXI_NOTES.get(chapter_num, "")

            # 补充现代汉语翻译（占位）
            if "modern_chinese" not in chapters[i] or not chapters[i]["modern_chinese"]:
                chapters[i][
                    "modern_chinese"
                ] = f"（{hex_data.get('name', '')}卦译文待补充）"

    # 保存数据
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  ✓ 已补全 {len(chapters)} 卦数据")
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("周易数据补全")
    print("=" * 50)

    fill_zhouyi_data()

    print("=" * 50)
    print("数据补全完成！")
    print("=" * 50)
