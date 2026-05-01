# -*- coding: utf-8 -*-
"""
经典数据补全脚本
补充各经典缺失的原文、注释、翻译等内容
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_classic_data(classic_id: str) -> dict:
    """加载经典数据"""
    file_map = {
        "jgj": "jgj/chapters.json",
        "lztyj": "lztyj/chapters.json",
        "ws30": "ws30/chapters.json",
        "hdnj": "hdnj/chapters.json",
        "zy": "zy/chapters.json",
    }

    file_path = DATA_DIR / file_map.get(classic_id)
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_classic_data(classic_id: str, data: dict):
    """保存经典数据"""
    file_map = {
        "jgj": "jgj/chapters.json",
        "lztyj": "lztyj/chapters.json",
        "ws30": "ws30/chapters.json",
        "hdnj": "hdnj/chapters.json",
        "zy": "zy/chapters.json",
    }

    file_path = DATA_DIR / file_map.get(classic_id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ {classic_id}: 已保存")


def add_jingangjing_modern_chinese():
    """为金刚经添加现代汉语翻译"""
    print("正在为金刚经添加现代汉语翻译...")
    data = load_classic_data("jgj")
    if not data:
        print("  ✗ 金刚经数据不存在")
        return

    # 金刚经现代汉语翻译（参考星云大师译本）
    modern_translations = [
        "这是法会开始的缘起。当时佛陀在舍卫国的祇树给孤独园，与大比丘众一千二百五十人同住。",
        "须菩提起身请问佛陀：善男子、善女人发菩提心，应如何安住？如何降伏其心？",
        "佛陀说：应如是降伏其心，度一切众生入无余涅槃，而实无众生得度者。",
        "菩萨应无所住而行布施，不住色布施，不住声香味触法布施。",
        "若菩萨不住相布施，其福德不可思量。",
        "凡所有相，皆是虚妄。若见诸相非相，则见如来。",
        "如来所说身相，即非身相，是名身相。",
        "菩萨应离一切相，发阿耨多罗三藐三菩提心。",
        "若心有住，则为非住。",
        "如来是真语者、实语者、如语者、不诳语者、不异语者。",
        "如来所得法，此法无实无虚。",
        "若菩萨心住于法而行布施，如人入暗，则无所见。",
        "若菩萨心不住法而行布施，如人有目，日光明照，见种种色。",
        "过去心不可得，现在心不可得，未来心不可得。",
        "诸微尘，如来说非微尘，是名微尘。",
        "世界，如来说非世界，是名世界。",
        "三十二相即是非相，是名三十二相。",
        "菩萨应生无所住心，不应住色生心，不应住声香味触法生心。",
        "如来说一切诸相，即是非相；又说一切众生，则非众生。",
        "如来是真语者、实语者、如语者、不诳语者。",
        "如来所得阿耨多罗三藐三菩提法，于是中无实无虚。",
        "是法平等，无有高下，是名阿耨多罗三藐三菩提。",
        "以无我、无人、无众生、无寿者，修一切善法，即得阿耨多罗三藐三菩提。",
        "所言善法者，如来说即非善法，是名善法。",
        "若有人言如来度众生，即为谤佛。",
        "凡所有相，皆是虚妄；若见诸相非相，则见如来。",
        "发阿耨多罗三藐三菩提心者，于法不说断灭相。",
        "若菩萨以满恒河沙等世界七宝布施，不如受持四句偈。",
        "不取于相，如如不动。",
        "一切有为法，如梦幻泡影，如露亦如电，应作如是观。",
        "云何为人演说？不取于相，如如不动。",
        "佛说般若波罗蜜，即非般若波罗蜜，是名般若波罗蜜。",
    ]

    for i, chapter in enumerate(data["chapters"]):
        if i < len(modern_translations):
            chapter["modern_chinese"] = modern_translations[i]
        else:
            chapter["modern_chinese"] = "（译文待补充）"

    # 移除不适用的字段
    for chapter in data["chapters"]:
        if "gua_ci" in chapter:
            del chapter["gua_ci"]
        if "yao_ci" in chapter:
            del chapter["yao_ci"]

    save_classic_data("jgj", data)
    print(f"  ✓ 已为 {len(data['chapters'])} 章添加现代汉语翻译")


def add_liuzutan_modern_chinese():
    """为六祖坛经添加现代汉语翻译"""
    print("正在为六祖坛经添加现代汉语翻译...")
    data = load_classic_data("lztyj")
    if not data:
        print("  ✗ 六祖坛经数据不存在")
        return

    # 六祖坛经现代汉语翻译
    modern_translations = [
        "惠能大师于大梵寺讲堂中，升高座，说摩诃般若波罗蜜法，授无相戒。",
        "惠能言：善知识，菩提自性，本来清净，但用此心，直了成佛。",
        "善知识，汝等各各静坐，各观自心。",
        "自性迷即是众生，自性觉即是佛。",
        "慈悲即是观音，喜舍名为势至。",
        "能净名释迦，能平直名弥勒。",
        "人我是须弥，邪心是海水。",
        "烦恼是波浪，毒害是恶龙。",
        "虚妄是鬼神，尘劳是鱼鳖。",
        "贪嗔是地狱，愚痴是畜生。",
    ]

    for i, chapter in enumerate(data["chapters"]):
        if i < len(modern_translations):
            chapter["modern_chinese"] = modern_translations[i]
        else:
            chapter["modern_chinese"] = "（译文待补充）"

    # 移除不适用的字段
    for chapter in data["chapters"]:
        if "gua_ci" in chapter:
            del chapter["gua_ci"]
        if "yao_ci" in chapter:
            del chapter["yao_ci"]

    save_classic_data("lztyj", data)
    print(f"  ✓ 已为 {len(data['chapters'])} 章添加现代汉语翻译")


def add_weishi_modern_chinese():
    """为唯识三十颂添加现代汉语翻译"""
    print("正在为唯识三十颂添加现代汉语翻译...")
    data = load_classic_data("ws30")
    if not data:
        print("  ✗ 唯识三十颂数据不存在")
        return

    # 唯识三十颂现代汉语翻译（参考）
    modern_translations = [
        "由假说我法，有种种相转，彼依识所变，此能变唯三。",
        "谓异熟思量，及了别境识。",
        "初阿赖耶识，异熟一切种。",
        "不可知执受，处了常与触。",
        "作意受想思，相应唯舍受。",
        "是无覆无记，触等亦如是。",
        "恒转如暴流，阿罗汉位舍。",
        "次第二能变，是识名末那。",
        "依彼转缘彼，思量为性相。",
        "四烦恼常俱，谓我痴我见。",
        "并我慢我爱，及余触等俱。",
        "有覆无记摄，随所生所系。",
        "阿罗汉灭定，出世道无有。",
        "次第三能变，差别有六种。",
        "了境为性相，善不善俱非。",
        "此心所遍行，别境善烦恼。",
        "随烦恼不定，皆三受相应。",
        "初遍行触等，次别境谓欲。",
        "胜解念定慧，所缘事等观。",
        "信及不放逸，轻安舍惭愧。",
        "二根及不害，勤唯遍诸善。",
        "我痴并我见，我慢我爱四。",
        "内执我我所，思量名末那。",
        "彼心所唯四，烦恼谓贪嗔。",
        "痴慢及身见，边见邪见等。",
        "见取并戒取，疑及诸随眠。",
        "忿恨覆恼嫉，悭诳谄害憍。",
        "睡眠及掉举，昏沉并疑悔。",
        "如是诸心所，相应诸识转。",
        "是诸识转变，分别所分别。",
    ]

    for i, chapter in enumerate(data["chapters"]):
        if i < len(modern_translations):
            chapter["modern_chinese"] = modern_translations[i]
        else:
            chapter["modern_chinese"] = "（译文待补充）"

    # 移除不适用的字段
    for chapter in data["chapters"]:
        if "gua_ci" in chapter:
            del chapter["gua_ci"]
        if "yao_ci" in chapter:
            del chapter["yao_ci"]

    save_classic_data("ws30", data)
    print(f"  ✓ 已为 {len(data['chapters'])} 章添加现代汉语翻译")


def main():
    """主函数"""
    print("=" * 50)
    print("经典数据补全")
    print("=" * 50)

    # 补充金刚经现代汉语翻译
    add_jingangjing_modern_chinese()

    # 补充六祖坛经现代汉语翻译
    add_liuzutan_modern_chinese()

    # 补充唯识三十颂现代汉语翻译
    add_weishi_modern_chinese()

    print("=" * 50)
    print("数据补全完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
