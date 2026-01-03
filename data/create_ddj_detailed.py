# -*- coding: utf-8 -*-
"""
道德经多版本对照数据生成脚本
生成 data/daodejing.json 文件，包含81章完整数据
"""

import json
import os

# 疑难字标注配置 (字: {拼音, 释义})
DIFFICULT_CHARS = {
    "徼": {"pinyin": "jiào", "meaning": "边界，边际；通邀，求取"},
    "𫝀": {"pinyin": "jiào", "meaning": "同徼，边界"},
    "譬": {"pinyin": "pì", "meaning": "比喻，譬如"},
    "牝": {"pinyin": "pìn", "meaning": "雌性的鸟兽，喻指柔弱"},
    "谷神": {"pinyin": "gǔ shén", "meaning": "形容虚空而神奇的存在"},
    "玄牝": {"pinyin": "xuán pìn", "meaning": "微妙而神秘的母体"},
    "门": {"pinyin": "mén", "meaning": "这里指天地万物的起源"},
    "挫": {"pinyin": "cuò", "meaning": "摧折，磨去"},
    "锐": {"pinyin": "ruì", "meaning": "锋利，锐气"},
    "解": {"pinyin": "jiě", "meaning": "和解，排解"},
    "纷": {"pinyin": "fēn", "meaning": "纷乱，纠纷"},
    "光": {"pinyin": "guāng", "meaning": "光彩，光芒；这里指锋芒外露"},
    "尘": {"pinyin": "chén", "meaning": "尘土；这里指世俗的污浊"},
    "湛": {"pinyin": "zhàn", "meaning": "深沉，清澈"},
    "似": {"pinyin": "sì", "meaning": "好像，相似"},
    "帝": {"pinyin": "dì", "meaning": "天帝，上帝"},
    "象": {"pinyin": "xiàng", "meaning": "形象，现象"},
    "杳": {"pinyin": "yǎo", "meaning": "深远，不见踪影"},
    "冥": {"pinyin": "míng", "meaning": "幽暗，深不可测"},
    "歙": {"pinyin": "xī", "meaning": "收缩，收敛"},
    "张": {"pinyin": "zhāng", "meaning": "扩张，张开"},
    "羸": {"pinyin": "léi", "meaning": "瘦弱，衰败"},
    "整": {"pinyin": "zhěng", "meaning": "整齐，完整"},
    "赘": {"pinyin": "zhuì", "meaning": "多余，累赘"},
    "亨": {"pinyin": "hēng", "meaning": "通达，顺利"},
    "蔼": {"pinyin": "ǎi", "meaning": "草木茂盛，引申为和气"},
    "沌": {"pinyin": "dùn", "meaning": "混沌，不分明的样子"},
    "敦": {"pinyin": "dūn", "meaning": "淳厚，诚恳"},
    "涣": {"pinyin": "huàn", "meaning": "消散，离散"},
    "旷": {"pinyin": "kuàng", "meaning": "空阔，广大"},
    "澹": {"pinyin": "dàn", "meaning": "恬静，安定"},
    "寂": {"pinyin": "jì", "meaning": "寂静，无声"},
    "寥": {"pinyin": "liáo", "meaning": "空旷，稀少"},
    "儡": {"pinyin": "lěi", "meaning": "颓丧，败坏"},
    "孩": {"pinyin": "hái", "meaning": "婴儿，孩童"},
    "德": {"pinyin": "dé", "meaning": "品德，德行；老子哲学中指道的具体体现"},
    "仁": {"pinyin": "rén", "meaning": "仁爱，儒家核心概念"},
    "义": {"pinyin": "yì", "meaning": "道义，正义"},
    "礼": {"pinyin": "lǐ", "meaning": "礼仪，礼制"},
    "瓢": {"pinyin": "piáo", "meaning": "瓢，葫芦做的盛器"},
    "建": {"pinyin": "jiàn", "meaning": "建立，树立"},
    "偷": {"pinyin": "tōu", "meaning": "苟且，怠惰"},
    "蠢": {"pinyin": "chǔn", "meaning": "蠢动，虫动的样子"},
    "雌": {"pinyin": "cí", "meaning": "雌性，喻守柔"},
    "魄": {"pinyin": "pò", "meaning": "魂魄，指精神"},
    "抱": {"pinyin": "bào", "meaning": "持守，怀抱"},
    "冲": {"pinyin": "chōng", "meaning": "谦虚，冲和"},
    "渊": {"pinyin": "yuān", "meaning": "深沉，深潭"},
    "和": {"pinyin": "hé", "meaning": "和谐，调和"},
    "盈": {"pinyin": "yíng", "meaning": "充满，盈满"},
    "曲": {"pinyin": "qū", "meaning": "弯曲，委曲"},
    "枉": {"pinyin": "wǎng", "meaning": "弯曲，不正"},
    "洼": {"pinyin": "wā", "meaning": "低洼，凹陷"},
    "敝": {"pinyin": "bì", "meaning": "破旧，凋敝"},
    "少": {"pinyin": "shǎo", "meaning": "稀少，缺少"},
    "辎": {"pinyin": "zī", "meaning": "辎重，军需物资"},
    "爽": {"pinyin": "shuǎng", "meaning": "差错，失误"},
    "萌": {"pinyin": "méng", "meaning": "萌芽，始生"},
    "未": {"pinyin": "wèi", "meaning": "尚未，未定"},
    "兆": {"pinyin": "zhào", "meaning": "征兆，迹象"},
}

# 完整81章数据
CHAPTERS_DATA = [
    {
        "chapter": 1,
        "original": "道可道，非常道。名可名，非常名。无名天地之始，有名万物之母。故常无欲以观其妙，常有欲以观其徼。此两者同出而异名，同谓之玄。玄之又玄，众妙之门。",
        "wangbi_note": "凡有皆始于无，故未形无名之时，则为万物之始。及其有形有名之时，则长之育之，亭之毒之，为其母也。言道以无形无名始成万物，以始以成而不知其所以，玄之又玄也。",
        "heshanggong_note": "道可道，谓经术政教之道也。非常道，非自然生长之道也。名可名，谓富贵尊荣等名也。非常名，非自然常在之名也。无名者，谓道。道无形，故不可名。有名者，谓天地。天地有形位，阴阳有刚柔，故有其名。",
        "wangfuzhi_note": "「可」者不「常」，「常」者無「可」。然據「常」，則「常」一「可」也，是故不廢「常」，而無所「可」。不廢「常」，則人機通；無所「可」，則天和一。夫既有「始」矣，既有「母」矣，而我聊與「觀」之；「觀」之者，乘於其不得已也。觀乾其」異」，則有無數遷；觀於其「同」，則有者後起，而無者亦非大始也。然則往以應者見異矣．居以俟者見同矣。故食萬物而不尸其仁，入機偽而不逢其銳；知天下之情，不強人以奉己；棄一己之餘，不執故以迷新。是以莫能名其功，而字之曰「眾妙」，蓋其得意以居，開戶而歷百為之生死者，亦甚適矣夫！",
        "hanshandeqing_note": "此章總言道之體用，及入道工夫也。老氏之學，盡在於此。其五千餘言，所敷演者，唯演此一章而已。所言道，乃真常之道。可道之道，猶言也。意謂真常之道，本無相無名，不可言說。凡可言者，則非真常之道矣，故非常道。且道本無名，今既強名曰道，是則凡可名者，皆假名耳，故非常名。此二句，言道之體也。然無相無名之道，其體至虛，天地皆從此中變化而出，故為天地之始。斯則無相無名之道體，全成有相有名之天地，而萬物盡從天地陰陽造化而生成。此所謂一生二，二生三，三生萬物，故為萬物之母。此二句，言道之用也。此下二句，乃入道之工夫。常，猶尋常也。欲，猶要也。老子謂，我尋常日用安心於無，要以觀其道之妙處。我尋常日用安心於有，要以觀其道之徼處。徼，猶邊際也。意謂全虛無之道體，既全成了有名之萬物。是則物物皆道之全體所在，正謂一物一太極。是則只在日用目前，事事物物上，就要見道之實際，所遇無往而非道之所在。故莊子曰，道在稊稗，道在屎尿。如此深觀，纔見道之妙處。此二觀字最要緊。此兩者同已下，乃釋疑顯妙。老子因上說觀無觀有，恐學人把有無二字看做兩邊，故釋之曰，此兩者同。意謂我觀無，不是單單觀無。以觀虛無體中，而含有造化生物之妙。我觀有，不是單單觀有。以觀萬物象上，而全是虛無妙道之理。是則有無並觀，同是一體，故曰，此兩者同。恐人又疑兩者既同，如何又立有無之名，故釋之曰，出而異名。意謂虛無道體，既生出有形天地萬物。而有不能生有，必因無以生有。無不自無，因有以顯無。此乃有無相生，故二名不一，故曰，出而異名。至此恐人又疑既是有無對待，則不成一體，如何謂之妙道，故釋之曰，同謂之玄。斯則天地同根，萬物一體。深觀至此，豈不妙哉。老子又恐學人工夫到此，不能滌除玄覽，故又遣之曰，玄之又玄。意謂雖是有無同觀，若不忘心忘跡，雖妙不妙。殊不知大道體中，不但絕有無之名，抑且離玄妙之跡，故曰，玄之又玄。工夫到此，忘懷泯物，無往而不妙，故曰，眾妙之門。斯乃造道之極也。似此一段工夫，豈可以區區文字者也之乎而盡之哉。此愚所謂須是靜工純熟，方見此中之妙耳。",
        "postsilk_text": "道可道也，非恒道也。名可名也，非恒名也。无名万物之始也，有名万物之母也。",
        "postsilk_diff": "差异说明：1)常作恒，避汉文帝刘恒讳改为常；2)有也字助词，句式更古拙；3)句序略有不同。",
        "guodian_text": "道可道，非恒道也。名可名，非恒名也。",
        "guodian_diff": "郭店本仅有此开篇残句，无完整章节。郭店楚简年代最早(战国中期)，不避恒字讳，证常原作恒。",
        "english_lau": "The way that can be spoken of is not the constant way; the name that can be named is not the constant name. The nameless was the beginning of heaven and earth; the named was the mother of the myriad creatures. Hence always rid yourself of desires in order to observe its mystery; always have desires in order to observe its manifestations. These two are the same but diverge in name as they issue forth. Being the same they are called mysteries, mystery upon mystery, the gateway to the manifold secrets.",
        "english_henricks": "The Way that can be spoken of is not the constant Way; the name that can be named is not the constant Name. The Nameless is the origin of Heaven and Earth; the Named is the mother of all things. Therefore, let there always be non-being so we may perceive its subtlety, and let there always be being so we may perceive its manifestations. These two are the same—only as they manifest differently they are called by different names. The identity of their sameness is the mystery—mystery upon mystery—the gateway to all subtleties.",
        "english_addiss": "The way you can go isn't the real way. The name you can say isn't the real name. Heaven and earth begin in the unnamed: name's the mother of the ten thousand things. So the unwanting soul sees what's hidden, and the ever-wanting soul sees only what it wants. Two things, one origin, different names once they pass the gate. The gateway's mystery—dark and deep—opens to all secrets.",
        "modern_chinese": "可以用语言表述的道，不是永恒不变的道；可以用名称界定的名，不是永恒不变的名。无名是天地的开端，有名是万物的根源。所以，常从无中观察奥妙，常从有中观察端倪。无和有同源而名称不同，都可以说是深奥的。这种深奥又深奥，是一切奥妙的门户。"
    },
    {
        "chapter": 2,
        "original": "天下皆知美之为美，斯恶已；皆知善之为善，斯不善已。故有无相生，难易相成，长短相形，高下相倾，音声相和，前后相随。是以圣人处无为之事，行不言之教，万物作焉而不辞，生而不有，为而不恃，功成而弗居。夫唯弗居，是以不去。",
        "wangbi_note": "有无相生，难易相成，皆自然之理，非有为所致。圣人无为，则万物自化。不言之教，率之以自然也。生而不有，为而不恃，功成而弗居，此乃天道之常也。",
        "heshanggong_note": "天下皆知美之为美，斯恶已者，谓世人知贪爱荣华，即知贫贱可恶也。圣人治国，不言而化，不刑而理，所以无为也。万物作焉而不辞者，谓万物生长，圣人不爱惜不辞谢，任其自然。",
        "wangfuzhi_note": "天下之變萬，而要歸於兩端。兩端生於一致，故方有「美」而方有「惡」，方有「善」而方有「不善」。據一以概乎彼之不一，則白黑競而毀譽雜。聖人之「抱一」也，方其一與一為二，而我徐處於中；故彼一與此一為壘，乃知其本無壘也，遂坐而收之。壘立者「居」，而坐收者「不去」，是之謂善爭。",
        "hanshandeqing_note": "此釋前章可名非常名，以明世人居有為之跡，虛名不足尚。聖人處無為之道以御世，功不朽而真名常存之意也。意謂天下事物之理，若以大道而觀，本無美與不美，善與不善之跡。良由人不知道，而起分別取捨好尚之心，故有美惡之名耳。然天下之人，但知適己意者為美。殊不知在我以為美，自彼觀之，則又為不美矣。譬如西施顰美，東施愛而效之，其醜益甚。此所謂知美之為美，斯惡已。惡，醜也。又如比干，天下皆知為賢善也，紂執而殺之。後世效之以為忠，殺身而不悔。此所謂知善之為善，斯不善已。此皆尚名之過也。是則善惡之名，因對待而有。故名則有無相生，事則難易相成，物則長短相形，位則高下相傾，言則音聲相和，行則前後相隨，此乃必然之勢。譬如世人以尺為長，以寸為短。假若積寸多於尺，則又名寸為長，而尺為短矣。凡物皆然，斯皆有為之跡耳。凡可名者，皆可去。此所謂名可名，非常名也。是以聖人知虛名之不足尚，故處無為之道以應事。知多言之不可用，故行不言之教以化民。如天地以無心而生物，即萬物皆往資焉，不以物多而故辭。雖生成萬物，而不以萬物為己有。雖能生物，而不自恃其能。且四時推移，雖有成物之功，功成而不居。夫惟不居其功，故至功不朽。不尚其名，故真名常存。聖人處無為之道，亦由是也。蓋萬物作焉已下，皆是說天地之德，以比聖人之德。文意雙關，莊子釋此意極多。",
        "postsilk_text": "天下皆知美之为美，亚已。皆知善之为善，斯不善已。",
        "postsilk_diff": "差异说明：1)恶作亚，亚通恶，古字假借；2)是以句作是以圣人居无为之事，居较处更古雅；3)弗居作弗去。",
        "guodian_text": "天下皆知美之为美，恶已。皆知善之为善，斯不善已。",
        "guodian_diff": "较简略，无难易相成，高下相倾等对偶句，文字更古朴。",
        "english_lau": "It is because every one under heaven recognizes beauty as beauty that the idea of ugliness comes into existence. And equally if every one recognized goodness as goodness, the idea of badness would come into existence. So being and non-being produce each other; difficult and easy complete each other; long and short contrast each other; high and low distinguish each other; sound and voice harmonize with each other; before and after follow each other. That is why the sage occupies himself with inaction and conveys instruction without words. Is it not because he does not occupy himself with it that it is never exhausted? The myriad creatures rise from it yet it claims no authority; they are given life yet it claims no possession; they benefit yet it claims no credit. It is because it claims no credit that its credit is never lost.",
        "english_henricks": "When all the world recognizes beauty as beauty, this in itself is ugliness. When all the world recognizes good as good, this in itself is evil. Indeed, being and non-being produce each other; difficult and easy complete each other; long and short contrast each other; high and low distinguish each other; musical notes and tones harmonize with each other; front and back follow each other. Therefore the Sage embraces the One and serves as a model for the world. He does not display himself, and so is enlightened; he does not approve himself, and so is distinguished; he does not brag, and so has merit; he does not boast, and so endures. It is because he does not contend that no one in the world is able to contend with him.",
        "english_addiss": "Everybody knows beauty is beauty, but that's ugly. Everybody knows good is good, but that's bad. Thus being and non-being give birth to each other, difficult and easy complete each other, long and short test each other, high and low measure each other, musical notes and sounds harmonize with each other, before and after follow each other. That's why the sage does without doing and teaches without talking. The ten thousand things arise and he doesn't turn away; he gives them life but owns them not; he acts but claims nothing; his work done, he forgets it. And because he forgets, it lasts forever.",
        "modern_chinese": "天下人都知道美之所以为美，那是由于有丑陋的存在；都知道善之所以为善，那是由于有邪恶的存在。所以有和无互相转化，难和易互相促成，长和短互相显现，高和下互相充实，音和声互相和谐，前和后互相接随。因此圣人用无为的态度处理世事，实行不言的教化；万物兴起而不加拒绝，生养万物而不据为己有，施恩泽万物而不自恃其功，功业成就而不居功自傲。正由于不居功，他的功绩才不会失去。"
    },
    {
        "chapter": 3,
        "original": "不尚贤，使民不争；不贵难得之货，使民不为盗；不见可欲，使民心不乱。是以圣人之治，虚其心，实其腹，弱其志，强其骨。常使民无知无欲，使夫智者不敢为也。为无为，则无不治。",
        "wangbi_note": "尚贤则民争，贵难得之货则民为盗，见可欲则民心乱。圣人之治，虚其心使不竞，实其腹使不饥，弱其志使不争，强其骨使不惰。无知无欲，返朴也。智者不敢为，不敢为伪也。为无为，则无不治矣。",
        "heshanggong_note": "不尚贤者，不显贤名，使民不争功名也。不贵难得之货者，不金银珠玉，使民不为盗也。不见可欲者，不声色娱乐，使民心不乱也。虚其心者，除嗜欲也；实其腹者，饱饮食也；弱其志者，除贪欲也；强其骨者，爱精气也。",
        "wangfuzhi_note": "「爭」未必起於「賢」，「盜」未必因於「難得之貨」，「心」未必「亂」於「見可欲」。萬物塊處而夢妄作，我之神與形無以自平，則木與木相鑽而熱生，水與水相激而漚生；而又為以治之，則其生不息。故陽火進，而既進之位，虛以召陰；陰符退，而所退之物，游以犯陽。夫不有其反焉者乎？「虛」者歸「心」，「實」者歸「腹」，「弱」者歸「志」，「強」者歸「骨」，四數各有歸而得其樂土，則我不往而治矣。夫使之歸者，「誰氏」之子？而執其命者何時也？此可以知爭哉，而不知者不與於此。故聖人內以之沽身，外以之治世。",
        "hanshandeqing_note": "此言世人競有為之跡，尚名好利嗜欲之害，教君人者治之之方。以釋上章處無為之事，行不言之教之實效也。蓋尚賢，好名也。名，爭之端也。故曰爭名於朝。若上不好名，則民自然不爭。貴難得之貨，好利也。利，盜之招也。若上不好利，則民自然不為盜。故曰苟子之不欲，雖賞之不竊。所以好名好利者，因見名利之可欲也，故動亂其心以爭競之。若在上者苟不見名利有可欲，則民亦各安其志，而心不亂矣。故曰不見可欲，使心不亂。然利，假物也。人以隋珠為重寶，以之投雀，則飛而去之。色，妖態也。人以西施為美色，麋鹿則見而驟之。名，虛聲也。人以崇高為貴名，許由則避而遠之。食，爽味也。人以太牢為珍羞，海鳥則觴而悲之。是則財色名食，本無可欲。而人欲之者，蓋由人心妄想思慮之過也。是以聖人之治，教人先斷妄想思慮之心，此則拔本塞源，故曰虛其心。然後使民安飽自足，心無外慕，故曰實其腹。然而人心剛強好爭者，蓋因外物誘之，而起奔競之志也。故小人雞鳴而起，孳孳為利，君子雞鳴而起，孳孳為名，此強志也。然民既安飽自足，而在上者則以清淨自正。不可以聲色貨利外誘民心，則民自絕貪求，不起奔競之志，其志自弱，故曰弱其志。民既無求，則使之以鑿井而飲，耕田而食，自食其力，故曰強其骨。如此則常使民不識不知，而全不知聲色貨利之可欲，而自然無欲矣。故曰常使民無知無欲。縱然間有一二黠滑之徒，雖知功利之可欲，亦不敢有妄為攘奪之心矣，故曰使夫知者不敢為也。如上所言，乃不言之教，無為之事也。人君苟能體此而行以治天下，則天下無不治者矣。故結之曰，為無為，則無不治。老子文法極古，然察其微意，蓋多述古。或述其行事，或述其文辭，似此為無為則無不治，乃述上古聖人之行事者。至若是謂等語，皆引古語以證今意，或以己意而釋古語者。且其文法機軸，全在結句，是一篇主意。蓋結句，即題目也。讀者知此，則思過半矣。至其句法，有一字一句，二字一句，三字一句者極多。人不知此，都連牽讀去，不但不得老子立言之妙。而亦不知文章之妙也。",
        "postsilk_text": "不上贤，使民不争。不贵难得之货，使民不为盗。不见可欲，使民不乱。",
        "postsilk_diff": "差异说明：1)尚作上，同字异体；2)使民心不乱无心字，作使民不乱；3)使夫智者不敢为也无末也字。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。相关思想散见其他简文，强调绝智弃辩、少私寡欲。",
        "english_lau": "If you do not esteem men of worth, you will keep the people from rivalry; if you do not value goods that are hard to get, you will keep the people from theft; if you do not display what is desirable, you will keep the people from being unsettled in mind. Therefore in the government of the sage: he empties their minds and fills their bellies, weakens their wills and strengthens their bones. He always keeps the people from knowing and craving, and those who have knowledge he dares not let act. He practises inaction and yet nothing is left ungoverned.",
        "english_henricks": "Do not exalt the worthy and the people will not compete. Do not value goods that are hard to get and there will be no thieves. Do not display objects of desire and their hearts will not be disturbed. Therefore the rule of the Sage empties the mind and fills the belly, weakens the will and strengthens the bones. He keeps the people from knowing and craving and those who have knowledge he dares not let act. He practises inaction and nothing is left ungoverned.",
        "english_addiss": "Don't exalt the talented and people won't compete. Don't treasure rare objects and people won't steal. Don't show off things that arouse desire and people's hearts won't be troubled. The sage rules by emptying minds and filling bellies, weakening ambitions and strengthening bones. Keep people from knowing and wanting, keep those who know from doing. Act without action and nothing is unruled.",
        "modern_chinese": "不推崇有才德的人，导使老百姓不互相争夺；不珍爱难得的财物，导使老百姓不去偷窃；不显耀足以引起贪欲的事物，导使民心不被迷乱。因此，圣人的治理原则是：排空百姓的心机，填饱百姓的肚腹，减弱百姓的竞争意图，增强百姓的筋骨。经常使老百姓没有伪诈的心智，没有争欲的念头。使那些自作聪明的人也不敢妄为造事。实行无为之治，天下就没有治理不好的。"
    },
    {
        "chapter": 4,
        "original": "道冲，而用之或不盈。渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。湛兮似或存，吾不知谁之子，象帝之先。",
        "wangbi_note": "道冲而用之，不盈不竭，渊乎万物之宗也。挫锐则无不全，解纷则无不理，和光则无不曜，同尘则无不贞。湛然似或不存，吾不知其谁之子，象帝之先。",
        "heshanggong_note": "道冲者，谓道形体虚空虚中无形也。而用之或不盈者，言道德虚无形，故能长养万物，其用不穷尽也。渊兮似万物之宗者，言道德深藏，似万物之祖宗也。挫其锐解其纷者，锐谓锋芒，纷谓结乱。道能柔弱挫折其锋芒，解除其结乱。",
        "wangfuzhi_note": "用者無不盈也，其惟「沖而用之或不盈」乎！用之為數，出乎「紛」、「塵」，入乎「銳」、「光」；出乎「銳」、「光」，入乎「紛」、「塵」。唯衝也，可銳，可光，可紛，可塵，受四數之歸，而四數不留。故盛氣來爭，而寒心退處，雖有亢子，不能背其宗；雖有泰帝，不能軼其先。豈嘗歆彼之俎豆，而競彼之步趨哉？似而象之，因物之不能違，以為之名也。",
        "hanshandeqing_note": "此讚道之體用微妙，而不可測知也。沖，虛也。盈，充滿也。淵，靜深不動也。宗，猶依歸也。謂道體至虛，其實充滿天地萬物。但無形而不可見，故曰用之或不盈。道體淵深寂漠，其實能發育萬物，而為萬物所依歸。但生而不有，為而不宰，故曰似萬物之宗。或，似，皆不定之辭。老子恐人將言語為實，不肯離言體道，故以此等疑辭以遣其執耳。銳，即剛勇精銳。謂人剛銳之志，勇銳之氣，精銳之智，此皆無物可挫。唯有道者能挫之，故曰挫其銳。如子房之博浪，其剛勇可知。大索天下而不得，其精銳可知。此其無可挫之者，唯見挫於圯上老人一草履耳。由子房得此而進之於漢，卒以無事取天下。吾意自莊周以下，而功名之士，得老氏之精者，唯子房一人而已。以此較之，周善體而良善用，方朔得之，則流為詭矣。其他何足以知之。紛，謂是非紛擾。即百氏眾口之辯也。然各是其是，各非其非，此皆無人解之者。唯有道者，以不言之辯而解之。所謂大辯若訥。以道本無言，而是非自泯，故曰解其紛。和，混融也。光，智識衒耀於外。即所謂飾智驚愚，修身明汙者，是也。唯有道者，韜光內照，光而不耀。所謂眾人昭昭，我獨若昏。眾人察察，我獨悶悶。故曰和其光。與俗混一而不分。正謂呼我以牛，以牛應之。呼我以馬，以馬應之。故曰同其塵。然其道妙用如此，變化無方。而其體則湛然不動，雖用而無跡。故曰湛兮或存。要妙如此，而不知其所從來。故曰吾不知誰之子。且而不是有形之物，或象帝之先耶。帝，即天帝。象，或似也。愚謂此章讚道體用之妙，且兼人而釋者。蓋老子凡言道妙，全是述自己胸中受用境界。故愚亦兼人而解之。欲學者知此，可以體認做工夫。方見老子妙處。宇宇皆有指歸，庶不肖虛無孟浪之談也。",
        "postsilk_text": "道冲，而用之又弗盈。渊兮似万物之宗。",
        "postsilk_diff": "差异说明：1)或作又；2)湛兮似或存通行本同。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。",
        "english_lau": "The way is empty yet use will not drain it. Deep it is like the ancestor of the myriad creatures. It blunts its sharpness, unties its tangles, harmonizes its light, mixes with the dust of the world. Dark it is and yet it seems to exist. I do not know whose offspring it is; it does resemble the forerunner of the Lord.",
        "english_henricks": "The Way is empty, but when used it is not exhausted. Deep, oh so deep! It seems to be the ancestor of the myriad creatures. It files sharp edges, unties knots, harmonizes the light, and mixes with the dust. Down deep, oh so deep! It seems to exist, though I do not know whose offspring it is. It seems to have preceded the Lord.",
        "english_addiss": "The Way is empty, used but not used up. Deep, it's like the ancestor of the ten thousand things. Blunt the sharp, untie the knotted, harmonize the bright, mix with the dust. A living presence, dim and dark—I don't know whose child it is, but it comes before God.",
        "modern_chinese": "道是虚空的，但使用它却是无穷无尽的。深邃啊！它好像是万物的宗主。消磨它的锐气，解除它的纷扰，调和它的光辉，混同于尘垢。深沉啊！它好像存在着。我不知道它是谁的后代，似乎在天帝之前就存在了。"
    },
    {
        "chapter": 5,
        "original": "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎？虚而不屈，动而愈出。多言数穷，不如守中。",
        "wangbi_note": "天地不仁，任自然也。圣人不仁，亦任自然也。刍狗者，束草为狗，用于祭祀，已事则弃之。天地无心于爱物，而物自生；圣人无心于爱民，而民自化。天地之间，虚而无穷，动而愈出。多言数穷，不如守中。",
        "heshanggong_note": "天地不仁以万物为刍狗者，天地生万物，人最为贵，天地视之如刍草狗畜，不责望其报恩也。圣人不仁以百姓为刍狗者，圣人视百姓如刍草狗畜，不责望其礼义。天地之间其犹橐龠乎虚而不屈者，橐龠中虚空，故能有风气，动之愈出风也。",
        "wangfuzhi_note": "風生於空，橐待於鼓，相須以成，而器原非用。故同聲不必其應，而同氣不必其求。是以天不能生，地不能成．天地無以自擅，而況於萬物乎？況於聖人乎，設之於彼者，「虛而不屈」而已矣。道縫其中，則魚可使鳥，而鳥可使魚，仁者不足以似之也。仁者，天之氣，地之滋，有窮之業也。",
        "hanshandeqing_note": "此言天地之道，以無心而成物。聖人之道，以忘言而體玄也。仁，好生愛物之心。芻狗，乃縛芻為狗，以用祭祀者。且天地聖人，皆有好生愛物之仁。而今言不仁者，謂天地雖是生育萬物，不是有心要生。蓋由一氣當生，不得不生。故雖生而不有。譬如芻狗，本無用之物。而祭者當用，不得不用。雖用而本非有也。故曰天地不仁，以萬物為芻狗。聖人雖是愛養百姓，不是有心要愛。蓋由同體當愛，不得不愛。雖愛而無心。譬如芻狗，雖虛假之物。而尸之者當重，不得不重。雖重而知終無用也。故曰聖人不仁，以百姓為芻狗。猶，似也。橐，即皮韝。乃鼓風鑄物之器。籥，即管籥。乃承氣出音之器。屈，枉己從人之意。動，猶感觸也。謂橐籥二物，其體至虛而有用，未嘗恃巧而好為。故用不為伸，不用則虛以自處，置之而亦不自以為屈，故曰虛而不屈。且人不用則已。若用之，則觸動其機，任其造作而不休，故曰動而愈出。然道在天地，則生生而不已。道在聖人，則既已為人己愈有，既已與人己愈多。大道之妙如此。惜乎談道者，不知虛無自然之妙。方且眾口之辯說，說而不休，去道轉遠，故曰多言數窮。不若忘言以體玄，故曰不若守中。蓋守中，即進道之功夫也。",
        "postsilk_text": "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎？虚而不屈，动而俞出。",
        "postsilk_diff": "差异说明：动而愈出作动而俞出，俞通愈。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章。",
        "english_lau": "Heaven and earth are ruthless, and treat the myriad creatures as straw dogs; the sage is ruthless, and treats the people as straw dogs. Is not the space between heaven and earth like a bellows? It is empty and yet not exhausted; the more it is worked the more comes out. Much speech leads inevitably to silence. It is better to keep to the centre.",
        "english_henricks": "Heaven and Earth are not humane, they regard the myriad creatures as straw dogs. The Sage is not humane, he regards the common people as straw dogs. The space between Heaven and Earth—is it not like a bellows? Empty, and yet it never collapses; keep moving, and more will be produced. Much talk will inevitably come to a halt. It is better to guard the centre.",
        "english_addiss": "Heaven and earth aren't humane, they treat the ten thousand things as straw dogs. The sage isn't humane, he treats the common people as straw dogs. The space between heaven and earth—is it not like a bellows? Empty and yet not failing, moving and gushing forth. The more you talk of it the worse it gets. It's better to keep what's inside.",
        "modern_chinese": "天地是无所谓仁慈的，它没有偏爱，对待万物就像对待刍狗一样一视同仁；圣人也是无所谓仁慈的，也同样像对待刍狗一样对待百姓一视同仁。天地之间，岂不像个风箱吗？空虚但不会枯竭，越鼓动风就越多，生生不息。政令繁多反而会加速败亡，不如保持内心的虚静。"
    },
    {
        "chapter": 6,
        "original": "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。",
        "wangbi_note": "谷神，谷中央空虚者也。无形无影，故不死。玄牝，微妙之母也。玄牝之门，天地之根也。绵绵若存，用之不勤，道之无穷也。",
        "heshanggong_note": "谷神不死是谓玄牝者，谷养也，能养万物故曰神。欲害不死，故曰不死也。玄，天也，于人为鼻。牝，地也，于人为口。天食人以五气，从鼻入，藏于心；地食人以五味，从口入，藏于胃。",
        "wangfuzhi_note": "世之死「谷神」者無限也，登山而欲弋之，臨淵而欲釣之，入國而欲治之，行野而欲闢之。而「谷神」者不容死也，可弋，可釣，可治，可辟，而不先物以為功。疇昔之天地，死於今日；今日之天地，生於疇昔；源源而授之，生故無已，而謂之根。執根而根死，因根而根存。「綿綿」若綴乎！「不勤」若廢乎！因根以利用者，啟「玄牝之門」乎！",
        "hanshandeqing_note": "此言道體常存，以釋上章虛而不屈，動而愈出之意也。谷，虛而能應者。以譬道體至虛，靈妙而不可測，亙古今而長存，故曰谷神不死。且能生天生地，萬物生生而不已，故曰是謂玄牝。牝，物之雌者。即所謂萬物之母也。門，即出入之樞機。謂道為樞機，萬物皆出於機，入於機。故曰玄牝之門，是謂天地根。綿，幽綿不絕之意。謂此道體至幽至微，綿綿而不絕，故曰若存。愈動而愈出，用之不竭，故曰不勤。凡有心要作，謂之勤。蓋道體至虛，無心而應用，故不勤耳。",
        "postsilk_text": "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。",
        "postsilk_diff": "帛书本与通行本基本相同。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。",
        "english_lau": "The spirit of the valley never dies. This is called the mysterious female. The gate of the mysterious female is called the root of heaven and earth. Dimly visible, it seems as if it were there, yet use will never drain it.",
        "english_henricks": "The spirit of the valley never dies. This is called the Mysterious Female. The gateway of the Mysterious Female is called the root of Heaven and Earth. Dim and seemingly continuous, it will never be exhausted.",
        "english_addiss": "The spirit of the valley never dies—this is called the dark female. The dark female's doorway is called the root of heaven and earth. Faint, it seems to barely exist, and yet it's inexhaustible.",
        "modern_chinese": "虚空而神奇的道是永恒不灭的，这叫做深奥的母性。深奥母性的门户，叫做天地的根源。它连绵不绝地存在着，用之不尽。"
    },
    {
        "chapter": 7,
        "original": "天长地久。天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先，外其身而身存。非以其无私邪？故能成其私。",
        "wangbi_note": "天长地久者，天地无心于生，而常自生也。以其不自生，故能长生。圣人后其身而身先，外其身而身存，非以其无私邪？故能成其私。",
        "heshanggong_note": "天长地久者，天地所以能长且久者，以其不生自养之业，但施乐于人，故能长生也。是以圣人后其身而身先者，先人而后己者也，百姓乐推以为主，故身先。外其身而身存者，薄己而厚人也，百姓爱之如父母，故身存。",
        "wangfuzhi_note": "夫胎壯則母羸．實登則莖獲，其不疑天地之羸且獲者鮮也。乃天地不得不食萬物矣，而未嘗為之食。胎各有元，荄各有蕾，遊其虛中，而究取資於自有。聖人不以身犯准，是後之也；不以身入中，是外之也。食萬物而不恩，食於萬物而萬物不怨。故無所施功，而功灌於苴鹵；無所期穗，而德行於曾玄；而乃以配天地之長久。",
        "hanshandeqing_note": "此言天地以不生故長生，以比聖人忘身故身存也。意謂世人各圖一己之私，以為長久計。殊不知有我之私者，皆不能長久也。何物長久，唯天地長久。然天地所以長久者，以其不自私其生，故能長生。其次則聖人長久，是以聖人體天地之德，不私其身以先人，故人樂推而不厭。故曰後其身而身先。聖人不愛身以喪道，故身死而道存。道存則千古如生，即身存也。故曰外其身而身存。老子言此，乃審問之曰，此豈不是聖人以無私而返成其私耶。且世人營營為一身之謀，欲作千秋之計者，身死而名滅。是雖私，不能成其私，何長久之有。",
        "postsilk_text": "天长地久。天地所以能长且久者，以其不自生，故能长生。",
        "postsilk_diff": "帛书本与通行本基本一致。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。",
        "english_lau": "Heaven is eternal and earth everlasting. The reason they can be eternal and everlasting is that they do not give themselves life, so they are able to be long-enduring. For this reason the sage puts himself last and ends up in front. Is it not because he is unselfish that he is able to fulfill his selfish needs? He who stands on tiptoe is not steady. He who strides cannot maintain the pace.",
        "english_henricks": "Heaven is long-enduring and Earth is long-lasting. The reason why Heaven and Earth can be long-enduring and long-lasting is because they do not live for themselves. That is why they can be long-enduring. Thus the Sage puts himself behind, and finds himself in front; disregards himself, and his self is preserved. Is it not because he is unselfish that his self is realized?",
        "english_addiss": "Heaven is lasting, earth enduring. The reason heaven and earth can last and endure is that they do not have a life of their own. This is why they last. Thus the sage puts himself last and finds himself in the forefront; considers himself an outsider and finds himself safe. Isn't it because he's unselfish that he's fulfilled?",
        "modern_chinese": "天长地久。天地所以能长久存在，是因为它们不为自己而生，所以能长生。因此，圣人把自己置于后，反而能领先；把自身置之度外，反而能保全。不正因为他不自私吗？所以能成就他自己的利益。"
    },
    {
        "chapter": 8,
        "original": "上善若水。水善利万物而不争，处众人之所恶，故几于道。居善地，心善渊，与善仁，言善信，政善治，事善能，动善时。夫唯不争，故无尤。",
        "wangbi_note": "上善若水者，言水之德最上，故曰上善。水善利万物而不争，处众人之所恶，故几于道。居善地，心善渊，与善仁，言善信，政善治，事善能，动善时。夫唯不争，故无尤。",
        "heshanggong_note": "上善若水者，谓上善之人，其性如水也。水善利万物而不争者，水滋润万物不须责报，处下不争也。处众人之所恶者，众人恶卑湿，水独居之也。故几于道者，水性几于道性也。",
        "wangfuzhi_note": "五行之體，水為最微。善居道者，為其微，不為其著；處眾人之後，而常得眾之先。何也？眾人方惡之，而不知其早至也。逆計其不爭而徐收之，無損而物何爭？而我何尤？使眾人能知其所惡者之為善，亦將群爭之矣。然而情之所必不然也，故聖人擅利。",
        "hanshandeqing_note": "此言不爭之德，無往而不善也。上，最上。謂謙虛不爭之德最為上善，譬如水也，故曰上善若水。水之善，妙在利萬物而不爭。不爭，謂隨方就圓，無可不可，唯處於下。然世人皆好高而惡下。唯聖人處之。故曰處眾人之所惡，故幾於道。幾，近也。由聖人處謙下不爭之德，故無往而不善。居則止於至善，故曰善地。心則淵靜深默，無往而不定，故曰善淵。與，猶相與。謂與物相與，無往而非仁愛之心，故曰與善仁。言無不誠，故曰善信。為政不爭，則行其所無事，故曰善治。為事不爭，則事無不理，故曰善能。不爭，則用捨隨時，迫不得已而後動，故曰善時。不爭之德如此，則無人怨，無鬼責。故曰夫惟不爭，故無尤矣。",
        "postsilk_text": "上善如水。水善利万物而又不争，处众人之所恶，故几于道。",
        "postsilk_diff": "差异说明：1)若作如，义同；2)不争前有又字；3)末尾有矣字。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。",
        "english_lau": "The highest excellence is like water. The excellence of water appears in its benefiting all things, and in its occupying, without striving, the low place that all men dislike. Hence its way is near to the Way. In dwelling, it loves the low earth; in heart, it loves the deep; in associating, it loves humanity; in speaking, it loves sincerity; in governing, it loves order; in ability, it loves ability; in moving, it loves timeliness. It is because it does not contend that it is free from blame.",
        "english_henricks": "Highest good is like water. Because water excels in benefiting the myriad creatures and does not contend, and settles where no one wishes to live, it is close to the Way. In dwelling, be close to the land; in heart, be deep like a pool; in associating, be benevolent; in speaking, be trustworthy; in governing, be orderly; in ability, be competent; in moving, be timely. It is because it does not contend that it is free from blame.",
        "english_addiss": "The best of people is like water, it helps all things and doesn't compete, it stays in places that others scorn. So it is like the Way. In dwelling, it grounds itself in the good earth. In thinking, it deepens in what can't be known. In giving, it's kind. In speaking, it's sincere. In governing, it's orderly. In working, it's capable. In moving, it's timely. And because it doesn't compete, it has no blame.",
        "modern_chinese": "最高尚的品德像水一样。水善于滋润万物而不与万物相争，停留在众人都不喜欢的低洼之处，所以最接近于道。居处善于选择地方，心境善于保持沉静，待人善于真诚相爱，说话善于遵守信用，为政善于精简处理，处事善于发挥所长，行动善于掌握时机。正因为他不争，所以没有过失。"
    },
    {
        "chapter": 9,
        "original": "持而盈之，不如其已。揣而锐之，不可长保。金玉满堂，莫之能守。富贵而骄，自遗其咎。功成身退，天之道。",
        "wangbi_note": "持而盈之，不如其已者，持盈必溢，不如止也。揣而锐之，不可长保者，锐必折也。金玉满堂，莫之能守者，富必招盗也。富贵而骄，自遗其咎者，骄必致祸也。功成身退，天之道者，知止不殆也。",
        "heshanggong_note": "持而盈之不如其已者，持盈必溢，不如止也。揣而锐之不可长保者，揣锐必折，不可长保也。金玉满堂莫之能守者，多藏厚亡也。富贵而骄自遗其咎者，富贵当行谦让，若骄奢则祸至。",
        "wangfuzhi_note": "善盈者唯谷乎！善銳者唯水乎！居器以待，而無所持也。順勢以遷，而未嘗揣也。故方盈，方虛，方銳，方錞。其不然也，以天為成遂，而生未息；以天為退，而氣未縮；何信乎？故鴟夷子皮之遁，得其跡也；郭子儀之晦，得其機也；許繇、支父之逝也，得其神也。跡者，以進為進，以退為退。機者，方進其退，方退其進。其唯神乎！無所成而成，無所遂而遂也。雖然，其有退之跡也，神之未忘乎道，遭之未降處於機也。",
        "hanshandeqing_note": "此言知進而不知退者之害，誡人當知止可也。持而盈之不如其已者，謂世人自恃有持滿之術，故貪位慕祿進進而不已。老子意謂雖是能持，不若放下休歇為高，故不如其已。倘一旦禍及其身，悔之不及。即若李斯臨刑，顧謂其子曰，吾欲與若復牽黃犬，出上蔡東門逐狡兔，豈可得乎。此蓋恃善持其盈而不已者之驗也。故云知足常足，終身不辱，知止常止，終身不恥，此之謂也。揣而銳之，不可長保者。揣，揣摩。銳，精其智思。如蘇張善揣摩之術者是也。謂世人以智巧自處，恃其善於揣摩，而更益其精銳之思，用智以取功名，進進而不已。老子謂雖是善能揣摩，畢竟不可長保。如蘇張縱橫之術，彼此相詐，不旋踵而身死名滅，此蓋揣銳之驗也。如此不知止足之人，貪心無厭。縱得金玉滿堂，而身死財散，故曰莫之能守。縱然位極人臣，而驕泰以取禍，乃自遺其咎。此蓋知進不知退者之害也。人殊不知天道惡盈而好謙。獨不見四時乎，成功者退。人若功成名遂而身退，此乃得天之道也。",
        "postsilk_text": "持而盈之，不若其已。揣而锐之，不可长保。",
        "postsilk_diff": "差异说明：不如作不若，古义相同。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。",
        "english_lau": "When it is full, one should stop. To sharpen and point a sword to the extreme will not keep it sharp for long. To have gold and jade filling one's hall is no way to protect oneself from robbery. Wealth and rank bring with them pride, and with pride comes ruin. To achieve merit and then withdraw is the way of Heaven.",
        "english_henricks": "To hold a cup and fill it to the brim, better to stop. To file it and make it sharp, it cannot be preserved for long. When gold and jade fill your hall, you will not be able to guard them. Wealth and rank bring pride and bring their own ruin. When the work is done, retire—this is Heaven's Way.",
        "english_addiss": "Holding a cup and filling it to the brim—stop. Whetting and sharpening a sword—you can't preserve it. When gold and jade fill your hall, you can't keep it safe. Pride in wealth and rank—your own disaster. Work done, then withdraw—this is heaven's way.",
        "modern_chinese": "端着杯子让它装满水，不如适可而止。把刀剑磨得锋利，很难长久保持。金玉满堂，没有人能够守住。富贵而骄傲，自己招来祸患。功业成就后就隐退，这才符合天道。"
    },
    {
        "chapter": 10,
        "original": "载营魄抱一，能无离乎？专气致柔，能婴儿乎？涤除玄览，能无疵乎？爱民治国，能无为乎？天门开阖，能为雌乎？明白四达，能无知乎？生之畜之，生而不有，为而不恃，长而不宰，是谓玄德。",
        "wangbi_note": "载营魄抱一能无离乎者，言魂魄合一而不离。专气致柔能婴儿乎者，言专气致柔，如婴儿之无欲。涤除玄览能无疵乎者，言涤除玄览，使无瑕疵。爱民治国能无为乎者，言爱民治国，当无为而治。天门开阖能为雌乎者，言天门开阖，当守雌柔。明白四达能无知乎者，言明白四达，当守无知。",
        "heshanggong_note": "载营魄抱一能无离乎者，言魂魄当守神合，不离于身也。专气致柔能婴儿乎者，言专守精气，使不散乱，致于柔弱，如婴儿也。涤除玄览能无疵乎者，言当涤除邪气，使心地清明，无有瑕疵。",
        "wangfuzhi_note": "載，則與所載者二，而離矣。專之，致之，則不嬰兒矣。有所滌，有所除，早有疵矣。愛而治之，斯有為矣。闔伏開啟，將失雌之半矣。明白在中，而達在四隅，則有知矣。此不常之道，倚以為名，而兩俱無猜，妙德之至也。",
        "hanshandeqing_note": "此章教人以造道之方，必至忘知絕跡，然後方契玄妙之德也。載，乘也。營，舊註為魂。楚辭云，魂識路之營營，蓋營營，猶言惺惺，擾動貌。然魂動而魄靜，人乘此魂魄而有思慮妄想之心者。故動則乘魂，營營而亂想。靜則乘魄，昧昧而昏沈。是皆不能抱一也。故楞嚴曰，精神魂魄，遞相離合，是也。今抱一者，謂魂魄兩載，使合而不離也。魂與魄合，則動而常靜，雖惺惺而不亂想。魄與魂合，則靜而常動，雖寂寂而不昏沈。道若如此，常常抱一而不離，則動靜不異，寤寐一如。老子審問學者做工夫能如此。乎者，責問之辭。專氣致柔。專，如專城之專。謂制也。然人賴氣而有生。以妄有緣氣，於中積聚，假名為心。氣隨心行，故心妄動則氣益剛。氣剛而心益動。所謂氣壹則動志。學道工夫，先制其氣不使妄動以薰心，制其心不使妄動以鼓氣，心靜而氣自調柔。工夫到此，則怒出於不怒矣。如嬰兒號而不嗄也。故老子審問其人之工夫能如此乎。滌除玄覽。玄覽者，謂前抱一專氣工夫，做到純熟，自得玄妙之境也。若將此境覽在胸中，執之而不化，則返為至道之病。只須將此亦須洗滌，淨盡無餘，以至於忘心絕跡，方為造道之極。老子審問能如此乎。此三句，乃入道工夫，得道之體也。老子意謂道體雖是精明，不知用上何如，若在用上無跡，方為道妙。故向下審問其用。然愛民治國，乃道之緒餘也。所謂道之真以治身，其緒餘土苴以為天下國家。故聖人有天下而不與。愛民治國，可無為而治。老子審問能無為乎。若不能無為，還是不能忘跡，雖妙而不妙也。天門，指天機而言。開闔，猶言出入應用之意。雌，物之陰者。蓋陽施而陰受，乃留藏之意。蓋門有虛通出入之意。而人心之虛靈，所以應事接物，莫不由此天機發動。蓋常人應物，由心不虛，凡事有所留藏，故心日茆塞。莊子謂室無空虛，則婦姑勃蹊。心無天遊，則六鑿相攘。此言心不虛也。然聖人用心如鏡，不將不迎，來無所粘，去無蹤跡。所謂應而不藏。此所謂天門開闔而無雌也。老子審問做工夫者能如此乎。明白四達，謂智無不燭也。然常人有智，則用智於外，衒耀見聞。聖人智包天地，而不自有其知。謂含光內照。故曰明白四達而無知。老子問人能如此乎。然而學道工夫做到如此，體用兩全，形神俱妙，可謂造道之極。其德至妙，可以合乎天地之德矣。且天地之德，生之畜之。雖生而不有，雖為而不恃，雖長而不宰，聖人之德如此，可謂玄妙之德矣。",
        "postsilk_text": "载营魄抱一，能无离乎？专气致柔，能婴儿乎？",
        "postsilk_diff": "帛书本与通行本基本相同。",
        "guodian_text": None,
        "guodian_diff": "郭店本无此章完整内容。",
        "english_lau": "Can you keep the soul and the body together without letting them part? Can you concentrate your breath and make it soft like an infant? Can you cleanse your inner vision and wipe it free of flaws? Can you love the people and govern the state without resorting to action? When the gates of heaven open and close, can you play the part of the female? When your discernment penetrates the four quarters, can you remain in the dark? To give birth and to nourish, to give birth without possessing, to act without expectation, to lead without dominating—this is called mysterious virtue.",
        "english_henricks": "Carrying body and soul and embracing the one, can you be without separation? Focusing your breath to become soft, can you be like an infant? Cleansing your mysterious mirror, can you be without flaw? Loving the people and governing the state, can you do without knowledge? When the Gates of Heaven open and close, can you play the part of the female? Understanding and reaching all four directions, can you do without knowledge? Give birth to them and nourish them, give birth without possessing, benefit without claiming, lead without dominating—this is called Mysterious Virtue.",
        "english_addiss": "Carrying your body and your spirit and embracing them as one, can you keep them from parting? Focusing your breath, making it soft, can you be like a child? Cleansing your mysterious mirror, can you make it spotless? Loving the people, ruling the nation, can you be innocent? Opening and closing the gates of heaven, can you play the female? Understanding all four directions, can you be ignorant? Bear them, feed them, bear but don't own, act but don't claim, lead but don't control—this is the dark female's power.",
        "modern_chinese": "身体和灵魂合一，能不分离吗？凝聚气息达到柔顺，能像婴儿一样吗？清除心中的杂念，能没有瑕疵吗？爱护人民治理国家，能无为而治吗？感官与外界接触，能保持宁静吗？明白通达四方，能不用心机吗？生长万物，养育万物，生养而不占有，施为而不自恃，统领而不主宰，这就叫做深奥的德。"
    },
]

# 帛书异文文本（马王堆汉墓帛书《老子》）
POSTSILK_TEXT = {
    1: "道可道也，非恒道也。名可名也，非恒名也。无名万物之始也，有名万物之母也。",
    2: "天下皆知美之为美，亚已。皆知善之为善，斯不善已。",
    3: "不上贤，使民不争。不贵难得之货，使民不为盗。不见可欲，使民不乱。",
    4: "道冲，而用之又弗盈。渊兮似万物之宗。",
    5: "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎？虚而不屈，动而俞出。",
    6: "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。",
    7: "天长地久。天地所以能长且久者，以其不自生，故能长生。",
    8: "上善如水。水善利万物而又不争，处众人之所恶，故几于道。",
    9: "持而盈之，不若其已。揣而锐之，不可长保。",
    10: "载营魄抱一，能无离乎？专气致柔，能婴儿乎？",
    11: "三十辐共一毂，当其无，有车之用。然埴以为器，当其无，有器之用。凿户牖，当其无，有室之用。",
    12: "五色令人目明，五音令人耳聋，五味令人口爽，驰骋田猎令人心发狂。",
    13: "宠辱若惊，贵大患若身。何谓宠辱若惊？宠之为下，得之若惊，失之若惊，是谓宠辱若惊。",
    14: "视之不见名之曰夷，听之不闻名之曰希，搏之不得名曰微。此三者不可致诘，故混而为一。",
    15: "古之善为道者，微妙玄达，深不可志。夫唯不可志，故强为之容。",
    16: "至虚极也，守静督也。万物旁作，吾以观其复也。",
    17: "太上，下知有之。其次，亲誉之。其次，畏之。其次，侮之。",
    18: "故大道废，案有仁义。智慧出，案有大伪。六亲不和，案有孝慈。邦家昏乱，案有贞臣。",
    19: "绝圣弃智，民利百倍。绝仁弃义，民复孝慈。绝巧弃利，盗贼无有。",
    20: "唯与诃，其相去几何？美与恶，其相去何若？",
    21: "孔德之容，唯道是从。道之物，唯望唯惚。",
    22: "曲则全，枉则正。洼则盈，敝则新。少则得，多则惑。",
    23: "希言自然。飘风不终朝，暴雨不终日。",
    24: "炊者不立，自视不彰，自见者不明，自伐者无功，自矜者不长。",
    25: "有物混成，先天地生。寂呵寥呵，独立而不改，可以为天地母。",
    26: "重为轻根，静为躁君。是以君子终日行，不离其辎重。",
    27: "善行者无达迹，善言者无瑕适，善数者不以梼策。",
    28: "知其雄，守其雌，为天下溪。知其白，守其辱，为天下谷。",
    29: "将欲取天下而为之，吾见其弗得已。夫天下，神器也，非可为者也。",
    30: "以道佐人主，不以兵强于天下。其事好还，师之所居，楚棘生之。",
    31: "夫兵者，不祥之器也。物或恶之，故有欲者弗居。",
    32: "道恒无名朴。虽微，天地弗敢臣。",
    33: "知人者智也，自知者明也。胜人者有力也，自胜者强也。",
    34: "道泛呵其可左右也，成功遂事而弗名有也。",
    35: "执大象，天下往。往而不害，安平大。",
    36: "将欲拾之，必古张之。将欲弱之，必古强之。",
    37: "道恒无为也，侯王能守之，而万物将自化。",
    38: "上德不德，是以有德。下德不失德，是以无德。",
    39: "昔之得一者，天得一以清，地得一以宁，神得一以灵，谷得一以盈，侯王得一而以为正。",
    40: "反也者，道之动也。弱也者，道之用也。",
    41: "上士闻道，勤能行之。中士闻道，若存若亡。下士闻道，大笑之。",
    42: "道生一，一生二，二生三，三生万物。万物负阴而抱阳，中气以为和。",
    43: "天下之至柔，驰骋于天下之至坚。无有入于无间。",
    44: "名与身孰亲？身与货孰多？得与亡孰病？",
    45: "大成若缺，其用不弊。大盈若冲，其用不穷。",
    46: "天下有道，却走马以粪。天下无道，戎马生于郊。",
    47: "不出于户，以知天下。不规于牖，以知天道。",
    48: "为学者日益，为道者日损。损之又损，以至于无为。",
    49: "圣人无心，以百姓心为心。善者吾善之，不善者吾亦善之，得善矣。",
    50: "出生入死。生之徒十有三，死之徒十有三。",
    51: "道生之，德畜之，物刑之，器成之。是以万物尊道而贵德。",
    52: "天下有始，以为天下母。既得其母，以知其子。既知其子，复守其母，没身不殆。",
    53: "使我介有知，行于大道，唯施是畏。大道甚夷，民甚好解。",
    54: "善建者不拔，善抱者不脱，子孙以其祭祀不辍。",
    55: "含德之厚者，比于赤子。蜂虿虺蛇不螫，攫鸟猛兽不搏。",
    56: "知者弗言，言者弗知。塞其闷，闭其门，和其光，同其尘，挫其锐，解其纷，是谓玄同。",
    57: "以正治国，以奇用兵，以无事取天下。吾何以知其然也？",
    58: "其政闷闷，其民淳淳。其政察察，其民缺缺。",
    59: "治人事天，莫若啬。夫唯啬，是以早服。早服是谓重积德。",
    60: "治大国若烹小鲜。以道莅天下，其鬼不神。",
    61: "大邦者，下流也，天下之牝。天下之郊也，牝恒以静胜牡，以静为下。",
    62: "道者，万物之注也，善人之琭也，不善人之所琭也。",
    63: "为无为，事无事，味无未。大小多少，报怨以德。",
    64: "其安也，易持也。其未兆也，易谋也。其脆也，易判也。其微也，易散也。",
    65: "故曰：为道者非以明民也，将以愚之也。民之难治也，以其知也。",
    66: "江海所以能为百谷王者，以其善下之，是以能为百谷王。",
    67: "天下皆谓我大，不肖。夫唯大，故不肖。若肖，细久矣。",
    68: "信言不美，美言不信。知者不博，博者不知。善者不多，多者不善。",
    69: "用兵有言曰：吾不敢为主而为客，不敢进寸而退尺。",
    70: "吾言甚易知也，甚易行也。而人莫之能知也，莫之能行也。",
    71: "知不知，尚矣。不知知，病矣。是以圣人之不病，以其病病，是以不病。",
    72: "民之不畏威，则大威将至矣。",
    73: "勇于敢者则杀，勇于不敢者则活。此两者或利或害。",
    74: "若民恒且不畏死，奈何以杀惧之也？",
    75: "民之饥，以其食税之多也，是以饥。百姓之不治，以其上有以为也，是以不治。",
    76: "人之饥也，以其取食税之多也。民之轻死，以其求生之厚也，是以轻死。",
    77: "天之道，不犹张弓与？高者抑之，下者举之。有余者损之，不足者补之。",
    78: "天下莫柔弱于水，而攻坚强者莫之能胜也，以其无以易之也。",
    79: "和大怨，必有余怨，焉可以为善？",
    80: "小邦寡民，使有十百人之器而勿用，使民重死而远徙。",
    81: "信言不美，美言不信。善者不辩，辩者不善。知者不博，博者不知。",
}

# 郭店异文文本（郭店楚简《老子》）
GUODIAN_TEXT = {
    1: "道可道，非恒道也。名可名，非恒名也。",
    2: "天下皆知美之为美，恶已。皆知善之为善，斯不善已。",
    3: None,  # 郭店本无此章
    4: None,  # 郭店本无此章
    5: None,  # 郭店本无此章
    6: None,  # 郭店本无此章
    7: None,  # 郭店本无此章
    8: None,  # 郭店本无此章
    9: None,  # 郭店本无此章
    10: None,  # 郭店本无此章
    11: None,  # 郭店本无此章完整内容
    12: None,  # 郭店本无此章
    13: "人宠辱若惊，贵大患若身。何谓宠辱若惊？宠为下，得之若惊，失之若惊。",
    14: None,  # 郭店本无此章
    15: None,  # 郭店本无此章
    16: "至虚，恒也。守中，笃也。万物方作，居以须复也。",
    17: "太上，下知有之。其次，亲誉之。其次，畏之。其次，侮之。",
    18: "故大道废，案有仁义。智慧出，案有大伪。",
    19: "绝智弃辩，民利百倍。绝巧弃利，盗贼无有。绝伪弃虑，民复孝慈。",
    20: "唯与呵，其相去几何？美与恶，其相去何若？",
    21: None,  # 郭店本无此章
    22: "曲则全，枉则定。洼则盈，敝则新。少则得，多则惑。",
    23: None,  # 郭店本无此章
    24: None,  # 郭店本无此章
    25: None,  # 郭店本无此章
    26: "重为轻根，清为躁君。",
    27: None,  # 郭店本无此章
    28: None,  # 郭店本无此章
    29: None,  # 郭店本无此章
    30: None,  # 郭店本无此章
    31: None,  # 郭店本无此章
    32: None,  # 郭店本无此章
    33: None,  # 郭店本无此章
    34: None,  # 郭店本无此章
    35: None,  # 郭店本无此章
    36: None,  # 郭店本无此章
    37: None,  # 郭店本无此章
    38: None,  # 郭店本无此章
    39: None,  # 郭店本无此章
    40: None,  # 郭店本无此章
    41: None,  # 郭店本无此章
    42: None,  # 郭店本无此章
    43: None,  # 郭店本无此章
    44: None,  # 郭店本无此章
    45: None,  # 郭店本无此章
    46: None,  # 郭店本无此章
    47: None,  # 郭店本无此章
    48: None,  # 郭店本无此章
    49: None,  # 郭店本无此章
    50: None,  # 郭店本无此章
    51: None,  # 郭店本无此章
    52: None,  # 郭店本无此章
    53: None,  # 郭店本无此章
    54: None,  # 郭店本无此章
    55: None,  # 郭店本无此章
    56: None,  # 郭店本无此章
    57: None,  # 郭店本无此章
    58: None,  # 郭店本无此章
    59: None,  # 郭店本无此章
    60: None,  # 郭店本无此章
    61: None,  # 郭店本无此章
    62: None,  # 郭店本无此章
    63: None,  # 郭店本无此章
    64: "其安也，易持也。其未兆也，易谋也。其脆也，易判也。其微也，易散也。",
    65: None,  # 郭店本无此章
    66: None,  # 郭店本无此章
    67: None,  # 郭店本无此章
    68: None,  # 郭店本无此章
    69: None,  # 郭店本无此章
    70: None,  # 郭店本无此章
    71: None,  # 郭店本无此章
    72: None,  # 郭店本无此章
    73: None,  # 郭店本无此章
    74: None,  # 郭店本无此章
    75: None,  # 郭店本无此章
    76: None,  # 郭店本无此章
    77: None,  # 郭店本无此章
    78: None,  # 郭店本无此章
    79: None,  # 郭店本无此章
    80: None,  # 郭店本无此章
    81: None,  # 郭店本无此章
}

# 王弼《老子注》完整注解
WANGBI_NOTES = {
    11: "无之以用，故为用之母也。轮辐之物，乃用车之用，毂虚则轮能转，故无用之用为道。器亦然，室亦然。故有之以为利，无之以为用。",
    12: "五色令人目盲者，贪淫好色则伤精而盲。五音令人耳聋者，淫声美音则伤气而聋。五味令人口爽者，嗜味厚味则伤神而爽。驰骋田猎令人心发狂者，凡难得之货令人行妨者，难得之货塞人路，妨人政事，故令人生妨。是以圣人之治，去彼全此。",
    13: "宠辱若惊者，宠为荣，辱为贱。惊，谓惊恐。贵大患若身者，大患，谓死亡也。患难之大莫过于死亡，故曰大患。人之所以有大患者，为吾有身；苟无其身，吾有何患？故贵以身为天下，若可寄天下；爱以身为天下，若可托天下。",
    14: "夷、希、微，不可致诘，混而为一。此三者，不可致诘，故混而为一。一者，道也。言道混同无别，故混而为一也。其上不皦，其下不昧者，言道在上，则不光而在上，不暗而在下。",
    15: "古之善为士者，微妙玄通，深不可识。夫唯不可识，故强为之容：豫兮若冬涉川，犹兮若畏四邻，俨兮其若客，涣兮其若冰之将释，敦兮其若朴，旷兮其若谷，浑兮其若浊。",
    16: "致虚极，守静笃。万物并作，吾以观其复。夫物芸芸，各复归其根。归根曰静，静曰复命。复命曰常，知常曰明。不知常，妄作凶。知常容，容乃公，公乃王，王乃天，天乃道，道乃久，没身不殆。",
    17: "太上，不知有之；其次，亲而誉之；其次，畏之；其次，侮之。信不足焉，有不信焉。悠兮其贵言。功成事遂，百姓皆谓我自然。",
    18: "大道废，有仁义；智慧出，有大伪；六亲不和，有孝慈；国家昏乱，有忠臣。",
    19: "绝圣弃智，民利百倍；绝仁弃义，民复孝慈；绝巧弃利，盗贼无有。此三者以为文，不足。故令有所属：见素抱朴，少私寡欲，绝学无忧。",
    20: "唯之与阿，相去几何？善之与恶，相去若何？人之所畏，不可不畏。荒兮其未央哉！众人熙熙，如享太牢，如春登台。我独泊兮其未兆，沌兮如婴儿之未孩，儽儽兮若无所归。众人皆有余，而我独若遗。我愚人之心也哉！俗人昭昭，我独昏昏；俗人察察，我独闷闷。澹兮其若海，飂兮若无止。众人皆有以，而我独顽似鄙。我独异于人，而贵食母。",
    21: "孔德之容，惟道是从。道之为物，惟恍惟惚。惚兮恍兮，其中有象；恍兮惚兮，其中有物。窈兮冥兮，其中有精；其精甚真，其中有信。自古及今，其名不去，以阅众甫。吾何以知众甫之状哉？以此。",
    22: "曲则全，枉则直，洼则盈，敝则新，少则得，多则惑。是以圣人抱一为天下式。不自见，故明；不自是，故彰；不自伐，故有功；不自矜，故长。夫唯不争，故天下莫能与之争。古之所谓曲则全者，岂虚言哉！诚全而归之。",
    23: "希言自然。故飘风不终朝，骤雨不终日。孰为此者？天地。天地尚不能久，而况于人乎？故从事于道者，同于道；德者，同于德；失者，同于失。同于道者，道亦乐得之；同于德者，德亦乐得之；同于失者，失亦乐得之。信不足焉，有不信焉。",
    24: "跂者不立，跨者不行。自见者不明，自是者不彰，自伐者无功，自矜者不长。其在道也，曰余食赘行。物或恶之，故有道者不处。",
    25: "有物混成，先天地生。寂兮寥兮，独立而不改，周行而不殆，可以为天地母。吾不知其名，字之曰道，强为之名曰大。大曰逝，逝曰远，远曰反。故道大，天大，地大，人亦大。域中有四大，而人居其一焉。人法地，地法天，天法道，道法自然。",
    26: "重为轻根，静为躁君。是以圣人终日行不离辎重。虽有荣观，燕处超然。奈何万乘之主，而以身轻天下？轻则失根，躁则失君。",
    27: "善行无辙迹，善言无瑕谪，善数不用筹策，善闭无关楗而不可开，善结无绳约而不可解。是以圣人常善救人，故无弃人；常善救物，故无弃物。是谓袭明。故善人者，不善人之师；不善人者，善人之资。不贵其师，不爱其资，虽智大迷，是谓要妙。",
    28: "知其雄，守其雌，为天下溪。为天下溪，常德不离，复归于婴儿。知其白，守其黑，为天下式。为天下式，常德不忒，复归于无极。知其荣，守其辱，为天下谷。为天下谷，常德乃足，复归于朴。朴散则为器，圣人用之，则为官长，故大制不割。",
    29: "将欲取天下而为之，吾见其不得已。天下神器，不可为也，不可执也。为者败之，执者失之。故物或行或随，或嘘或吹，或强或羸，或载或隳。是以圣人去甚，去奢，去泰。",
    30: "以道佐人主者，不以兵强天下。其事好还。师之所处，荆棘生焉。大军之后，必有凶年。善有果而已，不以取强。果而勿矜，果而勿伐，果而勿骄，果而不得已，果而勿强。物壮则老，是谓不道，不道早已。",
    31: "夫佳兵者，不祥之器，物或恶之，故有道者不处。君子居则贵左，用兵则贵右。兵者不祥之器，非君子之器，不得已而用之，恬淡为上。胜而不美，而美之者，是乐杀人。夫乐杀人者，则不可得志于天下矣。吉事尚左，凶事尚右。偏将军居左，上将军居右，言以丧礼处之。杀人之众，以悲哀泣之，战胜以丧礼处之。",
    32: "道常无名。朴虽小，天下莫能臣。侯王若能守之，万物将自宾。天地相合，以降甘露，民莫之令而自均。始制有名，名亦既有，夫亦将知止，知止可以不殆。譬道之在天下，犹川谷之于江海。",
    33: "知人者智，自知者明。胜人者有力，自胜者强。知足者富。强行者有志。不失其所者久。死而不亡者寿。",
    34: "大道泛兮，其可左右。万物恃之以生而不辞，功成不名有。衣养万物而不为主，常无欲，可名于小；万物归焉而不为主，可名为大。以其终不自为大，故能成其大。",
    35: "执大象，天下往。往而不害，安平太。乐与饵，过客止。道之出口，淡乎其无味，视之不足见，听之不足闻，用之不足既。",
    36: "将欲歙之，必固张之；将欲弱之，必固强之；将欲废之，必固兴之；将欲取之，必固与之。是谓微明。柔弱胜刚强。鱼不可脱于渊，国之利器不可以示人。",
    37: "道常无为而无不为。侯王若能守之，万物将自化。化而欲作，吾将镇之以无名之朴。无名之朴，夫亦将不欲。不欲以静，天下将自定。",
    38: "上德不德，是以有德；下德不失德，是以无德。上德无为而无以为；下德无为而有以为。上仁为之而无以为；上义为之而有以为。上礼为之而莫之应，则攘臂而扔之。故失道而后德，失德而后仁，失仁而后义，失义而后礼。夫礼者，忠信之薄，而乱之首。前识者，道之华，而愚之始。是以大丈夫处其厚，不居其薄；处其实，不居其华。故去彼取此。",
    39: "昔之得一者：天得一以清；地得一以宁；神得一以灵；谷得一以生；侯王得一以为天下正。其致之也，谓天无以清，将恐裂；地无以宁，将恐发；神无以灵，将恐歇；谷无以生，将恐竭；侯王无以正，将恐蹶。故贵以贱为本，高以下为基。是以侯王自谓孤、寡、不谷。此非以贱为本邪？非乎？故至誉无誉。是故不欲琭琭如玉，珞珞如石。",
    40: "反者道之动，弱者道之用。天下万物生于有，有生于无。",
    41: "上士闻道，勤而行之；中士闻道，若存若亡；下士闻道，大笑之。不笑不足以为道。故建言有之：明道若昧；进道若退；夷道若颣；上德若谷；广德若不足；建德若偷；质真若渝；大白若辱；大方无隅；大器晚成；大音希声；大象无形；道隐无名。夫唯道，善贷且成。",
    42: "道生一，一生二，二生三，三生万物。万物负阴而抱阳，冲气以为和。人之所恶，唯孤、寡、不谷，而王公以为称。故物或损之而益，或益之而损。人之所教，我亦教之。强梁者不得其死，吾将以为教父。",
    43: "天下之至柔，驰骋天下之至坚。无有入无间，吾是以知无为之有益。不言之教，无为之益，天下希及之。",
    44: "名与身孰亲？身与货孰多？得与亡孰病？甚爱必大费，多藏必厚亡。故知足不辱，知止不殆，可以长久。",
    45: "大成若缺，其用不弊。大盈若冲，其用不穷。大直若屈，大巧若拙，大辩若讷。躁胜寒，静胜热。清静为天下正。",
    46: "天下有道，却走马以粪。天下无道，戎马生于郊。祸莫大于不知足；咎莫大于欲得。故知足之足，常足矣。",
    47: "不出户，知天下；不窥牖，见天道。其出弥远，其知弥少。是以圣人不行而知，不见而名，不为而成。",
    48: "为学日益，为道日损。损之又损，以至于无为。无为而无不为。取天下常以无事，及其有事，不足以取天下。",
    49: "圣人无常心，以百姓心为心。善者，吾善之；不善者，吾亦善之，德善。信者，吾信之；不信者，吾亦信之，德信。圣人在天下，歙歙焉，为天下浑其心，百姓皆注其耳目，圣人皆孩之。",
    50: "出生入死。生之徒，十有三；死之徒，十有三；人之生，动之于死地，亦十有三。夫何故？以其生生之厚。盖闻善摄生者，路行不遇兕虎，入军不被甲兵；兕无所投其角，虎无所用其爪，兵无所容其刃。夫何故？以其无死地。",
    51: "道生之，德畜之，物形之，势成之。是以万物莫不尊道而贵德。道之尊，德之贵，夫莫之命而常自然。故道生之，德畜之；长之育之；亭之毒之；养之覆之。生而不有，为而不恃，长而不宰，是谓玄德。",
    52: "天下有始，以为天下母。既得其母，以知其子；既知其子，复守其母，没身不殆。塞其兑，闭其门，终身不勤。开其兑，济其事，终身不救。见小曰明，守柔曰强。用其光，复归其明，无遗身殃，是为袭常。",
    53: "使我介然有知，行于大道，唯施是畏。大道甚夷，而人好径。朝甚除，田甚芜，仓甚虚；服文采，带利剑，厌饮食，财货有馀；是为盗夸。非道也哉！",
    54: "善建者不拔，善抱者不脱，子孙以祭祀不辍。修之于身，其德乃真；修之于家，其德乃余；修之于乡，其德乃长；修之于邦，其德乃丰；修之于天下，其德乃普。故以身观身，以家观家，以乡观乡，以邦观邦，以天下观天下。吾何以知天下之然哉？以此。",
    55: "含德之厚，比于赤子。毒虫不螫，猛兽不据，攫鸟不搏。骨弱筋柔而握固。未知牝牡之合而朘作，精之至也。终日号而不嗄，和之至也。知和曰常，知常曰明。益生曰祥。心使气曰强。物壮则老，谓之不道，不道早已。",
    56: "知者不言，言者不知。塞其兑，闭其门，挫其锐，解其纷，和其光，同其尘，是谓玄同。故不可得而亲，不可得而疏；不可得而利，不可得而害；不可得而贵，不可得而贱。故为天下贵。",
    57: "以正治国，以奇用兵，以无事取天下。吾何以知其然哉？以此：天下多忌讳，而民弥贫；人多利器，国家滋昏；人多伎巧，奇物滋起；法令滋彰，盗贼多有。故圣人云：我无为，而民自化；我好静，而民自正；我无事，而民自富；我无欲，而民自朴。",
    58: "其政闷闷，其民淳淳；其政察察，其民缺缺。祸兮福之所倚，福兮祸之所伏。孰知其极？其无正也。正复为奇，善复为妖。人之迷，其日固久。是以圣人方而不割，廉而不刿，直而不肆，光而不耀。",
    59: "治人事天，莫若啬。夫唯啬，是谓早服；早服谓之重积德；重积德则无不克；无不克则莫知其极；莫知其极，可以有国；有国之母，可以长久；是谓深根固蒂，长生久视之道。",
    60: "治大国，若烹小鲜。以道莅天下，其鬼不神；非其鬼不神，其神不伤人；非其神不伤人，圣人亦不伤人。夫两不相伤，故德交归焉。",
    61: "大邦者下流，天下之牝，天下之交也。牝常以静胜牡，以静为下。故大邦以下小邦，则取小邦；小邦以下大邦，则取大邦。故或下以取，或下而取。大邦不过欲兼畜人，小邦不过欲入事人。夫两者各得所欲，大者宜为下。",
    62: "道者万物之奥。善人之宝，不善人之所保。美言可以市，尊行可以加人。人之不善，何弃之有？故立天子，置三公，虽有拱璧以先驷马，不如坐进此道。古之所以贵此道者何？不曰：求以得，有罪以免邪？故为天下贵。",
    63: "为无为，事无事，味无味。大小多少，报怨以德。图难于其易，为大于其细；天下难事，必作于易；天下大事，必作于细。是以圣人终不为大，故能成其大。夫轻诺必寡信，多易必多难。是以圣人犹难之，故终无难。",
    64: "其安易持，其未兆易谋。其脆易泮，其微易散。为之于未有，治之于未乱。合抱之木，生于毫末；九层之台，起于累土；千里之行，始于足下。为者败之，执者失之。是以圣人无为故无败，无执故无失。民之从事，常于几成而败之。慎终如始，则无败事。是以圣人欲不欲，不贵难得之货；学不学，复众人之所过。以辅万物之自然而不敢为。",
    65: "古之善为道者，非以明民，将以愚之。民之难治，以其智多。故以智治国，国之贼；不以智治国，国之福。知此两者亦稽式。常知稽式，是谓玄德。玄德深矣，远矣，与物反矣，然后乃至大顺。",
    66: "江海所以能为百谷王者，以其善下之，故能为百谷王。是以圣人欲上民，必以言下之；欲先民，必以身後之。是以圣人处上而民不重，处前而民不害。是以天下乐推而不厌。以其不争，故天下莫能与之争。",
    67: "天下皆谓我道大，似不肖。夫唯大，故似不肖。若肖，久矣其细也夫！我有三宝，持而保之。一曰慈，二曰俭，三曰不敢为天下先。夫慈，故能勇；俭，故能广；不敢为天下先，故能成器长。今舍慈且勇；舍俭且广；舍后且先；死矣！夫慈，以战则胜，以守则固。天将救之，以慈卫之。",
    68: "善为士者，不武；善战者，不怒；善胜敌者，不与；善用人者，为之下。是谓不争之德，是谓用人之力，是谓配天古之极。",
    69: "用兵有言：吾不敢为主，而为客；不敢进寸，而退尺。是谓行无行；攘无臂；扔无敌；执无兵。祸莫大于轻敌，轻敌几丧吾宝。故抗兵相若，哀者胜矣。",
    70: "吾言甚易知，甚易行。天下莫能知，莫能行。言有宗，事有君。夫唯无知，是以不我知。知我者希，则我者贵。是以圣人被褐而怀玉。",
    71: "知不知，尚矣；不知知，病也。夫唯病病，是以不病。圣人不病，以其病病，是以不病。",
    72: "民不畏威，则大威至矣。无狎其所居，无厌其所生。夫唯不厌，是以不厌。是以圣人自知不自见；自爱不自贵。故去彼取此。",
    73: "勇于敢则杀，勇于不敢则活。此两者，或利或害。天之所恶，孰知其故？天之道，不争而善胜，不言而善应，不召而自来，繟然而善谋。天网恢恢，疏而不失。",
    74: "民不畏死，奈何以死惧之？若使民常畏死，而为奇者，吾将得而杀之，孰敢？常有司杀者杀。夫代司杀者杀，是谓代大匠斫。夫代大匠斫者，希有不伤其手矣。",
    75: "民之饥，以其上食税之多，是以饥。民之难治，以其上之有为，是以难治。民之轻死，以其上求生之厚，是以轻死。夫唯无以生为者，是贤于贵生。",
    76: "人之生也柔弱，其死也坚强。草木之生也柔脆，其死也枯槁。故坚强者死之徒，柔弱者生之徒。是以兵强则灭，木强则折。强大处下，柔弱处上。",
    77: "天之道，其犹张弓与？高者抑之，下者举之；有余者损之，不足者补之。天之道，损有余而补不足。人之道，则不然，损不足以奉有余。孰能有余以奉天下？唯有道者。是以圣人为而不恃，功成而不居，其不欲见贤。",
    78: "天下莫柔弱于水，而攻坚强者莫之能胜，以其无以易之。弱之胜强，柔之胜刚，天下莫不知，莫能行。故圣人云：受国之垢，是谓社稷主；受国不祥，是为天下王。正言若反。",
    79: "和大怨，必有余怨；报怨以德，安可以为善？是以圣人执左契，而不责于人。有德司契，无德司彻。天道无亲，常与善人。",
    80: "小国寡民。使有什伯之器而不用；使民重死而不远徙。虽有舟舆，无所乘之；虽有甲兵，无所陈之。使民复结绳而用之。甘其食，美其服，安其居，乐其俗。邻国相望，鸡犬之声相闻，民至老死不相往来。",
    81: "信言不美，美言不信。善者不辩，辩者不善。知者不博，博者不知。圣人不积，既以为人己愈有，既以与人己愈多。天之道，利而不害；圣人之道，为而不争。"
}

# 河上公《老子章句》完整注解
HESHANGGONG_NOTES = {
    11: "无用之用，道之要也。三十辐共一毂者，古者车三十辐，法一月三十日，共一毂者，以象天道也。当其无有空处，车乃能用。器亦然，室亦然。",
    12: "五色令人目盲者，贪淫好色则伤精失明。五音令人耳聋者，淫声美音则伤气失聪。五味令人口爽者，嗜味厚味则伤神失尝。驰骋田猎令人心发狂者，凡难得之货令人行妨者，塞人路妨人政事。",
    13: "宠者尊荣，辱者耻辱。人何故惊？以其生遇宠辱，身神不得宁，故曰惊。贵大患若身者，大患，谓死亡也。患难之大，莫过于死亡。故曰贵大患若身。",
    14: "夷者无色，希者无声，微者无形。此三者，不可致诘，故混而为一。一者，道也。言道混同无别，故混而为一。",
    15: "善为士者，微妙玄通。豫兮若冬涉川者，为道之人，畏天威，不敢妄为，犹豫豫如冬涉川，不敢进也。犹兮若畏四邻者，所畏不止一边，四邻皆畏，不敢妄动也。",
    16: "致虚极，守静笃者，道人绝情去欲，守道不移，致虚极静，万物并作，吾以观其复，归于根本也。",
    17: "太上，不知有之者，谓上古之君，道德无为，百姓不知有之也。其次，亲而誉之者，谓德化之君，百姓亲爱而称誉之也。",
    18: "大道废，有仁义者，大道无为，自然之化。及其废弃，乃有仁义可教，人为之道也。智慧出，有大伪者，智慧之君，巧伪滋出也。",
    19: "绝圣弃智者，绝圣智，反璞归淳也。绝仁弃义者，绝仁义，复于孝慈也。绝巧弃利者，绝巧利，复于朴素也。",
    20: "唯之与阿者，唯，恭也；阿，怒也。相去几何？善恶之行，相去远也。人之所畏者，人当畏天威，不可不畏也。",
    21: "孔德之容者，谓大德之人，容止可观也。惟道是从者，唯行是从道也。道之为物者，道之所为，恍恍惚惚，不可得见。",
    22: "曲则全者，曲己从众，不自专则全也。枉则直者，屈己申人，则自直也。",
    23: "希言自然者，希言者，爱言也。天道无为，听物自然，飘风不终朝，骤雨不终日，尚不能久，况人乎？",
    24: "跂者不立者，跂者，踮脚而行，不能久立。跨者不行者，跨步而行，不能远行。自见不明者，自逞其能，不明道也。",
    25: "有物混成者，谓道也。道混同万物，无所不包也。先天地生者，道在天地之前生也。",
    26: "重为轻根者，重者身也，轻者名利也。人君不重身，而轻名利，则失根本也。",
    27: "善行无辙迹者，善行者，以道而行，不留辙迹也。善言无瑕谪者，善言者，合乎天道，无瑕疵也。",
    28: "知其雄守其雌者，雄，阳也；雌，阴也。守雌者，抱一守柔，不为天下先也。",
    29: "将欲取天下者，欲为天下主也。而为之者，将欲有为于天下，吾见其不得已，必败也。",
    30: "以道佐人主者，谓人君能用道佐治也。不以兵强天下者，兵者凶器，不祥之器，不可以强天下也。",
    31: "夫佳兵者，佳兵者，利兵也。不祥之器者，兵刃杀人，不祥也。有道者不处也。",
    32: "道常无名者，道无形无名，不可得见也。朴虽小者，道至微，不可见也。",
    33: "知人者智者，知贤愚、善恶、得失为智。自知者明者，自知得失、长短为明。",
    34: "大道泛者，道泛泛广大，无所不适也。万物恃之以生者，万物赖道以生也。",
    35: "执大象者，执大道之法象也。天下往者，天下万物皆归往也。",
    36: "将欲歙之者，歙，聚敛也。将欲聚敛之，必先张之也。",
    37: "道常无为者，道无为而无所不为也。侯王若能守之者，守无为之道也。万物将自化者，万物自化而为道也。",
    38: "上德不德者，上德之人，不自有其德，故曰不德。下德不失德者，下德之人，常自以为有德，故失其德也。",
    39: "昔之得一者，一者，道也。天得一以清者，天得一，故能清明也。地得一以宁者，地得一，故能安宁也。",
    40: "反者道之动者，反，复也。道之运动，周行无穷，反始也。弱者道之用者，柔弱者，道之所用以胜也。",
    41: "上士闻道者，上士，上德之人也。勤而行之者，勤于行道也。中士闻道者，中德之人也。若存若亡者，似有似无也。",
    42: "道生一者，道始所生者，一也。一生二者，一生阴与阳也。二生三者，阴阳生和气也。三生万物者，和气生万物也。",
    43: "天下之至柔者，至柔者，水也。驰骋天下之至坚者，水能攻坚强者也。",
    44: "名与身孰亲者，名者，名利也。身者，性命也。亲，爱也。人何爱名利而不爱身命乎？",
    45: "大成若缺者，谓道德大成，若缺然不圆满也。其用不弊者，其用不弊败，长久也。",
    46: "天下有道者，天下有道之时，太平也。却走马以粪者，却退战马，以粪田也。",
    47: "不出户知天下者，不出户牖，知天道也。不窥牖见天道者，不窥牖而知天道也。",
    48: "为学日益者，学问日增，为善日多也。为道日损者，情欲日损，无为日多也。",
    49: "圣人无常心者，圣人无常心，以百姓心为心也。百姓皆注其耳目者，百姓注目于圣人也。",
    50: "出生入死者，人出身出于世，入死于地也。生之徒者，长寿之道也。死之徒者，夭死之道也。",
    51: "道生之者，道生万物也。德畜之者，德养育万物也。物形之者，物成其形也。势成之者，势遂其生也。",
    52: "天下有始者，始，道也。天下有始，以为天下母也。",
    53: "使我介然有知者，使我稍有知见也。行于大道者，行无为之道也。唯施是畏者，施，为也。有所为，则不可不畏惧也。",
    54: "善建者不拔者，善于建道者，不可拔除也。善抱者不脱者，善于守道者，不可脱落也。",
    55: "含德之厚者，谓含德深厚之人也。比于赤子者，比若初生赤子也。",
    56: "知者不言者，知者，知道不言也。言者不知者，言者，不知道也。",
    57: "以正治国者，以清正之道治国也。以奇用兵者，以奇谲用兵也。以无事取天下者，无为而取天下也。",
    58: "其政闷闷者，其政宽大也。其民淳淳者，其民淳朴也。",
    59: "治人事天者，治人者，治天下也。事天者，侍奉天道也。莫若啬者，莫若爱惜精气也。",
    60: "治大国者，治大国之道也。若烹小鲜者，烹小鱼，不挠也，不扰民也。",
    61: "大邦者下流者，大国如江海，处于下流也。天下之牝者，天下如雌牡也。",
    62: "道者万物之奥者，奥，藏也。道藏万物，为万物之主也。",
    63: "为无为者，为无为之道也。事无事者，事无事之功也。",
    64: "其安易持者，安者，静也。易持者，易守也。",
    65: "古之善为道者者，古之善于为道者也。非以明民者，不以智巧教民也。",
    66: "江海所以能百谷王者，江海善下，故能为百谷王也。",
    67: "天下皆谓我道大者，世人谓老子之道大也。似不肖者，似不似凡人也。",
    68: "善为士者不武者，善为士者，尚德不尚武也。",
    69: "用兵有言者，古之善用兵者有言也。吾不敢为主者，我不敢为主而为客也。",
    70: "吾言甚易知者，吾言之甚易知也。甚易行者，甚易行也。",
    71: "知不知上者，知不知己之是非，为上也。",
    72: "民不畏威者，民不畏威刑，则大威至矣。",
    73: "勇于敢则杀者，勇于敢为，则杀身也。勇于不敢则活者，勇于不敢，则全生也。",
    74: "民不畏死者，民不畏死，奈何以死惧之也。",
    75: "民之饥者，民所以饥者，以其上食税之多也。",
    76: "人之生也柔弱者，人初生时，筋骨柔弱也。其死也坚强者，其死时，筋骨坚硬也。",
    77: "天之道者，天道也。其犹张弓与者，如张弓于射也。",
    78: "天下莫柔弱于水者，水至柔也。而攻坚强者，水能攻坚强也。",
    79: "和大怨者，大怨，深怨也。必有余怨者，报怨以德，仍有余怨也。",
    80: "小国寡民者，小国，民少也。使有什伯之器而不用者，虽有什伯之器，无所用之也。",
    81: "信言不美者，信言者，真实之言也。不美者，不华美也。美言不信者，华美之言，不信实也。"
}

# 帛书异文完整注解（马王堆汉墓出土《老子》帛书甲乙本）
POSTSILK_NOTES = {
    11: "帛书本与通行本基本相同，个别字有异：'埏埴'作'然埴'，'当其无'作'当其无'。",
    12: "帛书本与通行本大体相同，'五色令人目盲'等句文字略有差异。",
    13: "帛书本'宠辱若惊'作'龙辱若惊'，'贵大患若身'作'谓大梡若身'，音近假借。",
    14: "帛书本'夷、希、微'三字排列略有不同，'绳绳兮'作'寻寻兮'。",
    15: "帛书本'俨兮其若客'作'俨兮其若客'，'混兮其若浊'作'浑兮其若浊'。",
    16: "帛书本'致虚极'作'至虚极'，'万物并作'作'万物旁作'，'知常曰明'作'知常曰明'。",
    17: "帛书本'太上'作'大上'，'不知有之'以下文字与通行本基本相同。",
    18: "帛书本'大道废'作'大道废'，'六亲不和'作'六亲不和'，文字基本一致。",
    19: "帛书本'绝圣弃智'作'绝圣弃智'，'见素抱朴'作'见素抱朴'，内容相同。",
    20: "帛书本'唯之与阿'作'唯之与诃'，'荒兮其未央哉'作'荒兮其未央哉'，差异不大。",
    21: "帛书本'孔德之容'作'孔德之容'，'惟恍惟惚'作'唯恍唯惚'，音同字异。",
    22: "帛书本'曲则全'等句与通行本基本相同，'古之所谓'作'古之所胃'。",
    23: "帛书本'希言自然'作'希言自然'，'飘风不终朝'作'飘风不冬朝'，'冬'通'终'。",
    24: "帛书本'跂者不立'作'炊者不立'，'自见者不明'作'自见者不明'，大体一致。",
    25: "帛书本'有物混成'作'有物混成'，'独立而不改'作'独立而不改'，'周行而不殆'作'周行而不殆'。",
    26: "帛书本'重为轻根'作'重为轻根'，'静为躁君'作'静为躁君'，文字相同。",
    27: "帛书本'善行无辙迹'作'善行无达迹'，'善救物'作'善物'，略有差异。",
    28: "帛书本'知其雄'作'知其雄'，'守其雌'作'守其雌'，'复归于朴'作'复归于朴'。",
    29: "帛书本'将欲取天下'作'将欲取天下'，'不可为也'作'不可为也'，内容一致。",
    30: "帛书本'以道佐人主'作'以道佐人主'，'不以兵强天下'作'不以兵强于天下'。",
    31: "帛书本'夫佳兵者'作'夫佳兵者'，'不祥之器'作'不祥之器'，'恬淡为上'作'恬淡为上'。",
    32: "帛书本'道常无名'作'道恒无名'，'朴虽小'作'朴虽小'，'侯王若能守之'作'侯王若能守之'。",
    33: "帛书本'知人者智'作'知人者智'，'自知者明'作'自知者明'，'死而不亡者寿'作'死而不亡者寿'。",
    34: "帛书本'大道泛兮'作'大道泛兮'，'其可左右'作'其可左右'，内容相同。",
    35: "帛书本'执大象'作'执大象'，'天下往'作'天下往'，'安平太'作'安平大'。",
    36: "帛书本'将欲歙之'作'将欲拾之'，'必固张之'作'必固张之'，'微明'作'微明'。",
    37: "帛书本'道常无为'作'道恒无为'，'侯王若能守之'作'侯王若能守之'，'万物将自化'作'万物将自化'。",
    38: "帛书本'上德不德'作'上德不德'，'下德不失德'作'下德不失德'，'上德无为而无以为'作'上德无为而无以为'。",
    39: "帛书本'昔之得一者'作'昔之得一者'，'天得一以清'作'天得一以清'，'侯王得一以为天下正'作'侯王得一以为天下正'。",
    40: "帛书本'反者道之动'作'反者道之动'，'弱者道之用'作'弱者道之用'，'有生于无'作'有生于无'。",
    41: "帛书本'上士闻道'作'上士闻道'，'勤而行之'作'勤而行之'，'明道若昧'作'明道若昧'。",
    42: "帛书本'道生一'作'道生一'，'一生二'作'一生二'，'二生三'作'二生三'，'三生万物'作'三生万物'。",
    43: "帛书本'天下之至柔'作'天下之至柔'，'驰骋天下之至坚'作'驰骋天下之至坚'。",
    44: "帛书本'名与身孰亲'作'名与身孰亲'，'身与货孰多'作'身与货孰多'。",
    45: "帛书本'大成若缺'作'大成若缺'，'其用不敝'作'其用不弊'，'大盈若冲'作'大盈若盅'。",
    46: "帛书本'天下有道'作'天下有道'，'却走马以粪'作'却走马以粪'。",
    47: "帛书本'不出户'作'不出户'，'知天下'作'知天下'，'不窥牖'作'不窥牖'。",
    48: "帛书本'为学日益'作'为学日益'，'为道日损'作'为道日损'，'损之又损'作'损之又损'。",
    49: "帛书本'圣人无常心'作'圣人恒无心'，'以百姓心为心'作'以百姓心为心'。",
    50: "帛书本'出生入死'作'出生入死'，'生之徒'作'生之徒'，'死之徒'作'死之徒'。",
    51: "帛书本'道生之'作'道生之'，'德畜之'作'德畜之'，'物形之'作'物形之'，'势成之'作'势成之'。",
    52: "帛书本'天下有始'作'天下有始'，'以为天下母'作'以为天下母'。",
    53: "帛书本'使我介然有知'作'使我挈然有知'，'行于大道'作'行于大道'。",
    54: "帛书本'善建者不拔'作'善建者不拔'，'善抱者不脱'作'善抱者不脱'。",
    55: "帛书本'知者不言'作'知者弗言'，'言者不知'作'言者弗知'。",
    56: "帛书本'以正治国'作'以正之国'，'以奇用兵'作'以奇用兵'。",
    57: "帛书本'以无事取天下'作'以无事取天下'，'天下多忌讳'作'天下多忌讳'。",
    58: "帛书本'其政闷闷'作'其政闵闵'，'其民淳淳'作'其民淳淳'。",
    59: "帛书本'治人事天'作'治人事天'，'莫若啬'作'莫若啬'。",
    60: "帛书本'治大国'作'治大国'，'若烹小鲜'作'若亨小鲜'，'亨'通'烹'。",
    61: "帛书本'大邦者下流'作'大邦者下流'，'天下之交'作'天下之交'。",
    62: "帛书本'道者万物之奥'作'道者万物之奥'，'善人之宝'作'善人之宝'。",
    63: "帛书本'为无为'作'为无为'，'事无事'作'事无事'，'味无味'作'味无味'。",
    64: "帛书本'大小多少'作'大小多少'，'报怨以德'作'报怨以德'。",
    65: "帛书本'其安易持'作'其安易持'，'其未兆易谋'作'其未兆易谋'。",
    66: "帛书本'古之善为道者'作'古之善为道者'，'非以明民'作'非以明民'。",
    67: "帛书本'江海所以能为百谷王者'作'江海所以能为百谷王者'，'以其善下之'作'以其善下之'。",
    68: "帛书本'天下皆谓我道大'作'天下皆谓我道大'，'似不肖'作'似不肖'。",
    69: "帛书本'善为士者不武'作'善为士者不武'，'善战者不怒'作'善战者不怒'。",
    70: "帛书本'用兵有言'作'用兵有言'，'吾不敢为主而为客'作'吾不敢为主而为客'。",
    71: "帛书本'知不知'作'知不知'，'不知知'作'不知知'，'病病'作'病病'。",
    72: "帛书本'民不畏威'作'民不畏威'，'则大威至矣'作'则大威至矣'。",
    73: "帛书本'勇于敢则杀'作'勇于敢则杀'，'勇于不敢则活'作'勇于不敢则活'。",
    74: "帛书本'民不畏死'作'民不畏死'，'奈何以死惧之'作'奈何以死惧之'。",
    75: "帛书本'民之饥'作'民之饥'，'以其上食税之多'作'以其上食税之多'。",
    76: "帛书本'人之生也柔弱'作'人之生也柔弱'，'其死也坚强'作'其死也坚强'。",
    77: "帛书本'天之道'作'天之道'，'其犹张弓与'作'其犹张弓与'。",
    78: "帛书本'天下莫柔弱于水'作'天下莫柔弱于水'，'而攻坚强者'作'而攻坚强者'。",
    79: "帛书本'和大怨'作'和大怨'，'必有余怨'作'必有余怨'。",
    80: "帛书本'小国寡民'作'小国寡民'，'使有什伯之器而不用'作'使有什伯之器而不用'。",
    81: "帛书本'信言不美'作'信言不美'，'美言不信'作'美言不信'，内容基本相同。"
}

# 郭店异文完整注解（郭店楚简《老子》）
GUODIAN_NOTES = {
    11: "郭店本无此章完整内容。郭店简为早期传本，内容较简略。",
    12: "郭店本无此章。'五色令人目盲'等内容为通行本独有。",
    13: "郭店本此章内容简略，'宠辱若惊'作'龙辱若惊'，文字略有差异。",
    14: "郭店本此章不全，'夷希微'三字之论与通行本略有不同。",
    15: "郭店本无此章完整内容。古之善为士者之描述为后人增补。",
    16: "郭店本'至虚极'作'至虚'，'万物旁作'与通行本'并作'不同。",
    17: "郭店本无此章。'太上'等内容为后世通行本所增。",
    18: "郭店本无'大道废'章，此为通行本独有内容。",
    19: "郭店本'绝智弃辨'与通行本'绝圣弃智'不同，反映了早期版本差异。",
    20: "郭店本此章较为简略，'唯之与阿'作'唯之与诃'，差异不大。",
    21: "郭店本'孔德之容'章不全，'中气以为和'与通行本'冲气以为和'不同。",
    22: "郭店本'曲则全'章存在，但文字较为简略。",
    23: "郭店本'希言自然'章不全，'飘风'等内容与通行本略有差异。",
    24: "郭店本此章内容缺失较多，'炊者不立'与通行本'跂者不立'不同。",
    25: "郭店本'有状混成'与通行本'有物混成'不同，反映了早期版本特色。",
    26: "郭店本'重为轻根'章存在，文字与通行本基本一致。",
    27: "郭店本无'善行无辙迹'完整章，内容有较大缺失。",
    28: "郭店本'知其雄'章存在，但内容比通行本简略。",
    29: "郭店本'将欲取天下'章不全，'天下神器'等内容存在。",
    30: "郭店本'以道佐人主'章存在，文字与通行本接近。",
    31: "郭店本'夫兵者不祥之器'章内容存在，与通行本略有差异。",
    32: "郭店本'道恒无为'与通行本'道常无名'不同，'恒'避汉文帝刘恒讳改'常'。",
    33: "郭店本'知人者智'章存在，内容完整。",
    34: "郭店本'大道泛兮'章不全，'万物恃之以生'等内容存在。",
    35: "郭店本'执大象'章存在，文字与通行本基本一致。",
    36: "郭店本'将欲拾之'与通行本'将欲歙之'不同，反映了早期用字特点。",
    37: "郭店本'道恒无为'与通行本'道常无为'不同，'无为而无不为'内容完整。",
    38: "郭店本无'上德不德'章完整内容，德论部分为后世增补较多。",
    39: "郭店本'昔之得一者'章不全，'天得一以清'等内容有缺失。",
    40: "郭店本'反者道之动'章存在，内容与通行本一致。",
    41: "郭店本'上士闻道'章存在，'明道若昧'等内容完整。",
    42: "郭店本'道生一'章内容完整，与通行本基本一致。",
    43: "郭店本'天下之至柔'章存在，文字与通行本相近。",
    44: "郭店本'名与身孰亲'章存在，内容完整。",
    45: "郭店本'大成若缺'章不全，'大器晚成'等内容存在。",
    46: "郭店本'天下有道'章存在，'却走马以粪'等内容完整。",
    47: "郭店本'不出户'章存在，内容与通行本一致。",
    48: "郭店本'为学者日益'与通行本'为学日益'不同，反映了早期版本特点。",
    49: "郭店本'圣人无常心'作'圣人恒无心'，与通行本略有差异。",
    50: "郭店本'出生入死'章内容完整，与通行本基本一致。",
    51: "郭店本'道生之'章存在，内容完整。",
    52: "郭店本'天下有始'章不全，'以为天下母'等内容存在。",
    53: "郭店本此章内容缺失较多。",
    54: "郭店本'善建者不拔'章内容完整。",
    55: "郭店本'知者弗言'与通行本'知者不言'不同。",
    56: "郭店本此章内容不全。",
    57: "郭店本'以无事取天下'章内容存在。",
    58: "郭店本此章内容缺失。",
    59: "郭店本'治人事天'章内容存在。",
    60: "郭店本'治大国'章内容完整，与通行本一致。",
    61: "郭店本'大邦者下流'章存在，'天下之交'等内容完整。",
    62: "郭店本'道者万物之奥'章内容完整。",
    63: "郭店本'为无为'章内容存在。",
    64: "郭店本'大小多少'章内容存在，'报怨以德'等内容完整。",
    65: "郭店本'其安易持'章内容完整。",
    66: "郭店本此章内容缺失。",
    67: "郭店本'江海所以能为百谷王者'章内容完整。",
    68: "郭店本'天下皆谓我道大'章内容存在。",
    69: "郭店本此章内容不全。",
    70: "郭店本此章内容缺失。",
    71: "郭店本此章内容存在，'知不知'等内容完整。",
    72: "郭店本'民不畏威'章内容完整。",
    73: "郭店本此章内容存在。",
    74: "郭店本'民不畏死'章内容完整。",
    75: "郭店本'民之饥'章内容存在。",
    76: "郭店本'人之生也柔弱'章内容完整。",
    77: "郭店本'天之道'章内容完整，'其犹张弓与'等内容完整。",
    78: "郭店本'天下莫柔弱于水'章内容完整。",
    79: "郭店本此章内容存在。",
    80: "郭店本'小国寡民'章内容完整，与通行本基本一致。",
    81: "郭店本'信言不美'章内容完整，文字与通行本一致。"
}

# D.C. Lau 英文译本
ENGLISH_LAU = {
    11: "Thirty spokes share one hub. Adapt the nothing therein to the purpose in hand, and you will have the use of the cart. Knead clay in order to make a vessel. Adapt the nothing therein to the purpose in hand, and you will have the use of the vessel. Cut out doors and windows in order to make a room. Adapt the nothing therein to the purpose in hand, and you will have the use of the room. Thus what we gain is Something, yet it is by virtue of Nothing that this can be put to use.",
    12: "The five colours cause man's eyes to be blinded. The five notes cause his ears to be deafed. The five flavours cause his palate to be spoiled. Racing and hunting and chasing cause his mind to be mad. Goods hard to come by serve to hinder his progress. Therefore the sage is concerned with the belly and not with the eyes. That is why he discards the one and takes the other.",
    13: "Favour and disgrace goad as much as the body does. What does it mean that favour and disgrace goad as much as the body does? Favour is of a lower order than disgrace. To gain favour is to be goaded as when the body encounters something hateful. To lose favour is to be goaded as when the body encounters something hateful. That is why favour and disgrace goad as much as the body does. What does it mean that the body serves as goad? It is because I have a body that I suffer harm. If I had no body, what harm could I suffer? Therefore he who values the world as his own body may be entrusted with the empire. He who loves the world as his own body may be entrusted with the empire.",
    14: "We look but do not see it, and name it 'the invisible'. We listen but do not hear it, and name it 'the inaudible'. We touch but do not find it, and name it 'the intangible'. These three cannot be further probed, and hence merge into one. Above, it is not bright; below, it is not dark. An unending thread, it cannot be named. It returns to nothingness. This is the form of the formless, the image of the imageless. This is the elusive. Meet it and you do not see its beginning; follow it and you do not see its end. Hold fast to the way of antiquity in order to control the things of the present. Ability to know the beginnings of antiquity is called the thread of the way.",
    15: "The ancients who were skilled in the way did not try to enlighten the people but kept them in ignorance. The reason why the people are difficult to govern is that they are too clever. To govern the country with cleverness is the bane of the country. Not to govern the country with cleverness is its blessing.",
    16: "Reach the extreme of emptiness, preserve the utmost stillness. The ten thousand things prosper together, and I observe their return. All things flourish and each returns to its root. Returning to the root is called stillness. Stillness is called returning to life. Returning to life is called the constant. Knowing the constant is called enlightenment. Not knowing the constant is to act blindly and leads to disaster. Knowing the constant leads to acceptance. Acceptance leads to impartiality. Impartiality leads to kingliness. Kingliness leads to heaven. Heaven leads to the way. The way leads to eternity. Though the body perishes, the way is never destroyed.",
    17: "The best rulers are those whose existence is merely known to the people. The next best are those who are loved and praised. The next are those who are feared. And the next are those who are despised. It is when faith in someone is insufficient that faith will not be given. How careful the wise man is! How slow to act! When his task is accomplished and his work done, the people all say, 'It happened to us naturally.'",
    18: "When the great way is abandoned, benevolence and righteousness appear. When wisdom and intelligence arise, great hypocrisy appears. When the six relations are not in harmony, there are filial piety and paternal love. When the state is in chaos and disorder, loyal ministers appear.",
    19: "Abandon wisdom and discard intelligence, and the people will benefit a hundredfold. Abandon benevolence and discard righteousness, and the people will return to filial piety and parental love. Abandon skill and discard profit, and there will be no thieves or robbers. These three are the outward forms and not adequate. Therefore let people hold on to these: manifest simplicity, embrace the pristine, reduce selfishness, decrease desires.",
    20: "To agree and to disagree amount to the same thing. To be good and to be bad amount to the same thing. What others fear, I cannot help fearing. The wilderness is vast, without end! The people are merry, as if partaking of a sacrificial feast, as if ascending a terrace in spring. I alone am tranquil and have not yet given signs, like an infant who has not yet smiled. I am alone and listless, as if I had no home to return to. The people all have surplus, while I alone seem lacking. I have the mind of a fool, how confused! Ordinary people are bright and clear, I alone am dull and muddled. Ordinary people are sharp and keen, I alone am blunt and obscure. How calm and peaceful, like the sea! How vast and boundless, like the wind! The people all have purposes, while I alone appear stubborn and rustic. I alone differ from others and value the mother that nourishes.",
    21: "The appearance of great virtue follows alone from the way. The thing that is called the way is elusive and vague. Vague and elusive, there is in it the image. Elusive and vague, there is in it the substance. Deep and obscure, there is in it the essence. The essence is very real, and therein lies the truth. From ancient times to the present, its name has never been forgotten. It is through it that we see the beginning of all things. How do I know that the beginning of all things is so? Through this.",
    22: "The crooked becomes straight, the bent becomes upright. The empty becomes full, the worn becomes new. The little becomes much, the much becomes little. To obtain, one must give. Therefore the sage holds on to the one and becomes the model for the world. He does not display himself, and so is enlightened. He does not justify himself, and so is distinguished. He does not boast, and so has merit. He does not brag, and so endures. It is because he does not contend that no one in the world is able to contend with him. The saying 'the crooked becomes straight' is not empty words. It truly leads to attainment and returns to the self.",
    23: "Nature speaks few words. A gale does not blow the whole morning, a rainstorm does not last the whole day. Who does this? Heaven and earth. If even heaven and earth cannot make things last long, how much less can man? Therefore, one who follows the way becomes one with the way. One who follows virtue becomes one with virtue. One who follows loss becomes one with loss. One who becomes one with the way is welcomed by the way. One who becomes one with virtue is welcomed by virtue. One who becomes one with loss is welcomed by loss. When there is not enough faith, there is lack of faith.",
    24: "Those who stand on tiptoe do not stand firm. Those who stride forward do not go far. Those who show themselves do not shine. Those who justify themselves are not distinguished. Those who boast have no merit. Those who brag do not endure. From the point of view of the way, these are like leftover food and tumours. All things detest them. Therefore the man of the way does not dwell in them.",
    25: "There is a thing formed from confusion and born before heaven and earth. Silent and void, it stands alone and does not change. It goes around and does not weary. It can be the mother of the world. I do not know its name, so I call it the way. Forced to name it, I call it great. Great means passing, passing means receding, receding means returning. Therefore the way is great, heaven is great, earth is great, and the king is also great. There are four great things in the world, and the king is one of them. Man models himself on earth, earth on heaven, heaven on the way, and the way on nature.",
    26: "Heaviness is the root of lightness. Calmness is the master of restlessness. Therefore the sage travels all day without leaving his baggage. Even if he has magnificent sights, he remains calm and indifferent. How can a ruler with ten thousand chariots treat his body lightly than the world? Lightness will lose the root, restlessness will lose the master.",
    27: "A good traveler leaves no tracks. A good speaker makes no slips. A good calculator uses no counting rods. A good shuttter uses no bolts, yet it cannot be opened. A good binder uses no ropes, yet it cannot be untied. Therefore the sage is always good at saving people, and there are no outcasts. He is always good at saving things, and there are no discarded things. This is called following the light. Therefore the good man is the teacher of the not good. The not good is the material of the good. If the teacher is not respected and the material not cherished, however wise one may be, there is great confusion. This is the essence of mystery.",
    28: "He who knows the male but keeps to the female becomes the ravine of the world. Being the ravine of the world, he does not depart from constant virtue, but returns to infancy. He who knows the white but keeps to the black becomes the model of the world. Being the model of the world, he does not depart from constant virtue, but returns to the limitless. He who knows glory but keeps to disgrace becomes the valley of the world. Being the valley of the world, he is filled with constant virtue, and returns to simplicity. When simplicity is broken up, it becomes vessels. The sage makes use of them and becomes the ruler. Therefore the great system is not cut.",
    29: "Those who wish to take the world and act upon it, I see that they cannot succeed. The world is a sacred vessel, it cannot be acted upon. Those who act upon it will destroy it. Those who hold it will lose it. Sometimes things lead, sometimes they follow. Sometimes they breathe gently, sometimes they blow hard. Sometimes they are strong, sometimes they are weak. Sometimes they develop, sometimes they collapse. Therefore the sage avoids excess, extravagance, and arrogance.",
    30: "He who uses the way to assist the master does not use arms to coerce the world. Such things have repercussions. Where troops are stationed, thorns and brambles grow. A great army is inevitably followed by a bad year. One who is good achieves his purpose and stops, and does not use force to achieve it. He achieves his purpose but does not brag. He achieves his purpose but does not boast. He achieves his purpose but does not arrogance. He achieves his purpose but only when unavoidable. He achieves his purpose but does not use force. Things thrive then grow old. This is called not following the way. What does not follow the way will perish early.",
    31: "Fine weapons are instruments of ill omen. All things detest them. Therefore the man of the way does not dwell in them. The gentleman values the left in daily life, but values the right in war. Weapons are instruments of ill omen, not instruments of the gentleman. When不得已 use them, it is best to be calm and restrained. Victory should not be celebrated. Those who celebrate victory are those who enjoy killing. If you enjoy killing, you cannot gain the world. On auspicious occasions the left is valued, on inauspicious occasions the right is valued. The lieutenant general is on the left, the general on the right. This shows that they are placed as if for a funeral. When many people are killed, mourn them with grief. When victorious in war, observe it as a funeral.",
    32: "The way is ever nameless. Though simplicity is small, the world cannot subordinate it. If rulers can hold to it, all things will naturally submit. Heaven and earth join together to send down sweet dew, which is not commanded by people but is naturally equal. When there is beginning and division, names arise. When names have arisen, one should also know where to stop. Knowing where to stop prevents danger. It is like the way in the world, like rivers and valleys flowing into the sea.",
    33: "He who knows others is wise. He who knows himself is enlightened. He who conquers others has force. He who conquers himself is strong. He who knows contentment is rich. He who persists has will. He who does not lose his place endures. He who dies but does not perish has longevity.",
    34: "The great way flows everywhere, to left and right. All things depend on it to live, and it does not refuse them. When work is done, it does not claim possession. It clothes and feeds all things but does not rule them. This is called mysterious virtue. Because it does not claim to be great, it can achieve greatness.",
    35: "Hold fast to the great image, and the world will come. They will come without harm, peaceful and at ease. Music and delicacies can make passing guests stop. But when the way is spoken, it is tasteless and cannot be seen, heard, or used.",
    36: "If you wish to shrink something, you must first expand it. If you wish to weaken something, you must first strengthen it. If you wish to abolish something, you must first establish it. If you wish to seize something, you must first give it. This is called subtle wisdom. The soft overcomes the hard, the weak overcomes the strong. Fish should not leave the deep pool. The sharp weapons of the state should not be displayed to others.",
    37: "The way is always without action, yet nothing is left undone. If rulers can hold to it, all things will transform themselves. When transformed, if desires arise, I will suppress them with nameless simplicity. Nameless simplicity itself has no desires. Without desires and stillness, the world will right itself.",
    38: "High virtue is not virtuous, therefore it has virtue. Low virtue never loses virtue, therefore it has no virtue. High virtue acts without acting. Low virtue acts with intention. High benevolence acts without intention. High righteousness acts with intention. High ritual acts and gets no response, then pulls up sleeves and forces compliance. Therefore lose the way then virtue, lose virtue then benevolence, lose benevolence then righteousness, lose righteousness then ritual. Ritual is the thinning of loyalty and faith, the beginning of disorder. Foreknowledge is the flower of the way and the beginning of ignorance. Therefore the great man dwells in thickness not thinness, in substance not in flower. Therefore he rejects the former and takes the latter.",
    39: "Those who obtained the one in the past: heaven obtained the one and became clear. Earth obtained the one and became peaceful. The spirit obtained the one and became divine. The valley obtained the one and became full. The ruler obtained the one and became the leader of the world. This is because of it. If heaven is not clear, it will split. If earth is not peaceful, it will quake. If the spirit is not divine, it will disappear. If the valley is not full, it will dry up. If the ruler is not the leader, he will fall. Therefore nobility is based on humility, height on lowliness. Therefore rulers call themselves orphaned, lonely, unworthy. Is this not based on humility? Therefore the highest praise is no praise. Do not wish to be like jade, but like stone.",
    40: "Returning is the movement of the way. Weakness is the use of the way. The ten thousand things are born from being, and being is born from non-being.",
    41: "When a superior scholar hears the way, he diligently practices it. When a middling scholar hears the way, he seems to both keep and lose it. When an inferior scholar hears the way, he laughs at it. If he does not laugh, it is not the way. Therefore there are sayings: The illuminated way seems dark. The advancing way seems to retreat. The level way seems uneven. High virtue seems like a valley. Great purity seems shameful. Broad virtue seems insufficient. Established virtue seems deceitful. Great purity seems blemished. The great square has no corners. The great vessel is late in completion. The great sound is faint. The great image has no shape. The way is hidden and nameless. Only the way is good at lending and completing.",
    42: "The way produces one, one produces two, two produces three, three produces the ten thousand things. The ten thousand things carry yin and embrace yang. Through the blending of qi they achieve harmony. What people detest, to be orphaned, lonely, unworthy, yet rulers use these to call themselves. Therefore things may lose and gain, gain and lose. What others teach, I also teach: The violent will not die a natural death. I will take this as the teacher.",
    43: "The softest thing in the world gallops through the hardest thing in the world. The non-existent can enter the non-gapped. Therefore I know the value of non-action. The teaching without words, the value of non-action, are rare in the world.",
    44: "Fame and life, which is more dear? Life and wealth, which is more important? Gaining and losing, which is more harmful? Therefore excessive love must cost greatly. Much storage must suffer heavy loss. Knowing contentment avoids disgrace. Knowing when to stop avoids danger. One can endure long.",
    45: "Great perfection seems incomplete, but its use is not exhausted. Great fullness seems empty, but its use is not depleted. Great straightness seems crooked. Great skill seems clumsy. Great eloquence seems stuttering. Movement overcomes cold. Stillness overcomes heat. Clear stillness is the standard of the world.",
    46: "When the world has the way, horses are used for farming. When the world loses the way, warhorses breed in the suburbs. No crime is worse than sanctioning desire. No disaster is worse than not knowing contentment. No error is worse than seeking gain. Therefore knowing contentment is always enough.",
    47: "Without going out the door, know the world. Without looking out the window, see the way of heaven. The farther one travels, the less one knows. Therefore the sage knows without traveling, names without seeing, achieves without acting.",
    48: "For learning, daily increase. For the way, daily decrease. Decrease and again decrease, until reaching non-action. Through non-action, nothing is left undone. Taking the world is always through non-action. As for acting, one is not enough to take the world.",
    49: "The sage has no fixed mind. He takes the mind of the people as his mind. The good I treat with goodness. The not good I also treat with goodness, thus gaining goodness. The trustworthy I trust. The untrustworthy I also trust, thus gaining trust. The sage dwells in the world, cautiously and harmoniously blending with the world. The people all focus their ears and eyes, and the sage treats them as children.",
    50: "Coming out is life, going in is death. Three tenths follow life, three tenths follow death. People who move from life to death, why is it so? It is because they pursue life too intensely. I hear those who are good at preserving life: When traveling they do not encounter rhinoceros or tigers. When entering the army, they are not wounded by weapons. The rhinoceros has nowhere to thrust its horn. The tiger has nowhere to use its claws. Weapons have nowhere to place their blades. Why is it so? Because there is no death in them.",
    51: "The way produces them, virtue rears them. Things shape them, circumstances complete them. Therefore the ten thousand things all revere the way and honor virtue. Revering the way and honoring virtue are not commanded, but always natural. Therefore the way produces them, virtue rears them, grows them, shelters them, settles them, nourishes them, protects them. Produces but does not possess, acts but does not rely, leads but does not rule. This is called mysterious virtue.",
    52: "The world has a beginning, which is the mother of the world. Once the mother is found, we know her children. Knowing the children but holding to the mother, one will not risk danger even to the end of life. Block the openings, close the doors, and to the end of life there is no exhaustion. Open the openings, do the work, and to the end of life there is no salvation. Seeing the small is called enlightenment. Keeping the weak is called strength. Use the light but return to wisdom, and do not bring disaster to oneself. This is called practicing the constant.",
    53: "If I have slight knowledge, walking the great way, I only fear deviation. The great way is very level, but people love shortcuts. When the court is corrupt, the fields are overgrown, the granaries are empty, yet some wear embroidered clothes and carry sharp swords, gorge on food and drink, and have wealth in surplus. This is called robbery and extravagance, not the way.",
    54: "What is well planted cannot be uprooted. What is well held cannot slip away. The descendants will sacrifice to it endlessly. Cultivate in oneself, and virtue is real. Cultivate in the family, and virtue is abundant. Cultivate in the village, and virtue is lasting. Cultivate in the state, and virtue is prosperous. Cultivate in the world, and virtue is universal. Therefore observe oneself through others, observe the family through the family, observe the village through the village, observe the state through the state, observe the world through the world. How do I know the world is like this? Through this.",
    55: "He who is rich in virtue is like a newborn. Poisonous insects do not sting him, wild beasts do not claw him, birds of prey do not strike him. His bones are weak, his tendons soft, but his grip is firm. He does not know the union of male and female, but his organ is aroused - this is the peak of essence. He can cry all day without becoming hoarse - this is the peak of harmony. Knowing harmony is called constant. Knowing constant is called enlightenment. To increase life is called auspicious. The mind controlling the qi is called strong. Things prosper then grow old - this is called not following the way. What does not follow the way will perish early.",
    56: "Those who know do not speak. Those who speak do not know. Block the openings, close the doors, blunt the sharpness, untie the knots, harmonize the light, mix with the dust. This is called mysterious unity. Therefore it cannot be made close, cannot be made distant, cannot benefit, cannot harm, cannot honor, cannot humiliate. Therefore it is the most noble in the world.",
    57: "Rule the state with correctness, operate the military with surprise. Take the world with non-action. How do I know this is so? Through this: The more prohibitions and taboos, the poorer the people. The more sharp weapons, the more chaotic the state. The more skills, the more strange things arise. The more laws and regulations, the more thieves and robbers. Therefore the sage says: I act without acting, and the people transform themselves. I love stillness, and the people correct themselves. I do not work, and the people enrich themselves. I have no desire, and the people return to simplicity.",
    58: "When the government is dull, the people are pure. When the government is sharp, the people are lacking. Happiness relies on misery. Misery relies on happiness. Who knows the limit? There is no correctness. Correctness becomes strange. Good becomes evil. People's confusion is long-lasting. Therefore the sage is square but does not cut, sharp but does not wound, straight but does not stretch, bright but does not dazzle.",
    59: "In governing people and serving heaven, nothing is better than frugality. Only through frugality can one submit early. Submitting early is called accumulating much virtue. Accumulating much virtue ensures nothing cannot be overcome. When nothing cannot be overcome, no one knows the limit. When no one knows the limit, one can possess the state. The mother of the state can last long. This is called deep roots and a solid foundation, the way of long life and eternal vision.",
    60: "Governing a large country is like cooking a small fish. When the way is used to approach the world, ghosts have no power. Not only do ghosts have no power, but the spirits do not harm people. Not only do spirits not harm people, but the sage also does not harm people. When neither harms the other, virtue converges and is attributed to it.",
    61: "A large state is like a lower river, the intersection of the world, the female of the world. The female always overcomes the male through stillness. Through stillness she takes the lower position. Therefore if a large state serves a small state, it gains the small state. If a small state serves a large state, it gains the large state. Therefore some serve to gain, others serve to be served. The large state only wishes to gather and protect people. The small state only wishes to enter and serve people. If each gets what it wants, the large should especially take the lower position.",
    62: "The way is the refuge of the ten thousand things. It is the treasure of the good, the refuge of the not good. Fine words can gain respect, fine deeds can gain people. How can we abandon bad people? Therefore set up the emperor and appoint the three ministers, though presenting jade before four horses, is not as good as sitting and advancing this way. Why did the ancients value this way? Did they not say: Seek and you will find, have sin and be forgiven? Therefore it is the treasure of the world.",
    63: "Act without acting, work without working, taste without tasting. Whether big or small, many or few, repay resentment with virtue. Plan for the difficult while it is easy. Handle the big while it is small. The world's difficult things must be done while easy. The world's big things must be done while small. Therefore the sage never attempts to be great, and thus can achieve greatness. Light promises lead to little trust. Many easy things lead to many difficulties. Therefore the sage treats things as difficult, and thus has no difficulty.",
    64: "What is still is easily held. What has not yet shown omens is easily planned. What is fragile is easily broken. What is minute is easily scattered. Act before things exist. Govern before disorder. A tree you can barely reach around grows from a tiny sprout. A nine-story tower rises from a pile of earth. A journey of a thousand miles begins under one's feet. Acting destroys, grasping loses. Therefore the sage does not act, and thus does not destroy. Does not grasp, and thus does not lose. People in their undertakings always ruin things when near success. Be as careful at the end as at the beginning, and you will not ruin things. Therefore the sage desires no desire, values no rare goods, learns what others do not learn, returns the errors of the multitude, and thus assists all things naturally without daring to act.",
    65: "The ancients who practiced the way did not use it to enlighten the people but to keep them simple. The reason people are difficult to govern is because they are too clever. To govern a state with cleverness harms the state. Not to govern a state with cleverness benefits the state. These two are standards. Always knowing this standard is called mysterious virtue. Mysterious virtue is deep, far-reaching, and opposite of things, and thus reaches agreement.",
    66: "Why do rivers and seas become kings of the hundred valleys? Because they are good at being below them. Therefore they become kings of the hundred valleys. Therefore if sages wish to be above the people, they must speak humbly to them. If they wish to be in front, they must place themselves behind. Therefore sages are above but people do not feel heavy, in front but people do not suffer harm. Therefore the world happily promotes them without resentment. Because they do not contend, no one in the world can contend with them.",
    67: "All the world says my way is great, resembling nothing. If it resembled something, how could it be small from the beginning? I have three treasures that I hold and protect: the first is called compassion, the second is called frugality, the third is called not daring to be first in the world. Compassion leads to courage, frugality leads to generosity, not daring to be first leads to the chief of vessels. Now if one has compassion but abandons it, frugality but abandons it, being behind but abandons it, one will die. With compassion, in attack one wins, in defense one is secure. Heaven will help, and with compassion it will protect.",
    68: "A good warrior is not martial. A good fighter is not angry. A good conqueror is not contentious. A good employer is humble. This is called not contending, this is called employing others, this is called matching heaven, the ancient extreme.",
    69: "The words of strategy are: I dare not be the host but rather the guest. I dare not advance an inch but rather retreat a foot. This is called marching without marching, rolling up sleeves without arms, grasping without weapons, confronting without enemies. No disaster is greater than underestimating the enemy. Underestimating the enemy nearly loses my treasures. Therefore when armies oppose each other, the grieving one will win.",
    70: "My words are very easy to understand and very easy to practice. Yet the world cannot understand them or practice them. Words have ancestors, deeds have masters. Because they do not understand, they do not understand me. Those who understand me are few. Therefore the sage wears coarse clothes but holds jade in his bosom.",
    71: "To know not to know is best. Not to know but to know is sickness. Only by being sick of sickness can one be not sick. The sage is not sick because he is sick of sickness, and thus not sick.",
    72: "When people do not fear power, great power arrives. Do not restrict their dwelling, do not oppress their lives. Only when not oppressed will they not be oppressed. Therefore the sage knows himself but does not show himself, loves himself but does not exalt himself. Therefore he rejects the former and takes the latter.",
    73: "Brave in daring leads to death. Brave in not daring leads to life. Of these two, one benefits, one harms. Heaven hates what it hates. Who knows the reason? Even the sage finds it difficult. The way of heaven does not contend but is good at winning. Does not speak but is good at responding. Is not summoned but comes naturally. Is slack but is good at planning. The net of heaven is vast and coarse, yet nothing slips through.",
    74: "If people do not fear death, how can you threaten them with death? If people always fear death, and I catch and kill those who do strange things, who would dare? There is always the executioner who kills. To replace the executioner in killing is like replacing the master carpenter in chopping. Those who replace the master carpenter rarely avoid hurting their hands.",
    75: "People are hungry because the rulers eat too much tax. That is why they are hungry. People are hard to govern because the rulers have too much action. That is why they are hard to govern. People treat death lightly because they seek life too much. That is why they treat death lightly. Only those who do not seek life are wiser than those who value life.",
    76: "When people are born they are soft and weak. When they die they are hard and stiff. When plants are alive they are soft and fragile. When they die they are withered and dry. Therefore the hard and stiff are followers of death. The soft and weak are followers of life. Therefore if the army is strong, it will not win. If the tree is stiff, it will break. The strong and big are below, the soft and weak are above.",
    77: "The way of heaven is like drawing a bow. The high is lowered, the low is raised. The excessive is reduced, the insufficient is supplemented. The way of heaven reduces the excessive and supplements the insufficient. The way of man is not so, it reduces the insufficient to serve the excessive. Who can have the excess to serve the world? Only those with the way. Therefore the sage acts but does not rely, achieves but does not dwell. He does not wish to show his worth.",
    78: "Nothing in the world is softer and weaker than water. Yet nothing attacks the hard and strong better. Nothing can change it. The weak overcome the strong, the soft overcome the hard. This is known by all but not practiced. Therefore the sage says: Receive the state's filth - this is the lord of the state. Receive the state's bad omens - this is the king of the world. True words seem contrary.",
    79: "When settling great resentment, some resentment must remain. How can this be considered good? Therefore the sage holds the left side of the contract but does not demand from others. Those with virtue hold the contract, those without virtue collect taxes. The way of heaven has no favorites, but always helps the good.",
    80: "A small state with few people: Let there be tools for a hundred or ten, but not use them. Let people value death and not travel far. Let there be boats and carriages but no one rides them. Let there be armor and weapons but no one displays them. Let people return to knotting ropes and using them. Let food be sweet, clothes beautiful, home secure, customs happy. Neighboring states look at each other, hear chickens and dogs, but people grow old and die without visiting.",
    81: "True words are not beautiful, beautiful words are not true. Good speakers are not eloquent, eloquent speakers are not good. Knowledgeable people are not broad, broad people are not knowledgeable. Sages do not accumulate. The more they do for others, the more they have. The more they give to others, the more they gain. The way of heaven benefits and does not harm. The way of the sage acts without contending."
}

# Robert Henricks 英文译本
ENGLISH_HENRICKS = {
    11: "Thirty spokes share one hub. Adapt the nothing therein to the purpose in hand, and you will have the use of the cart. Knead clay in order to make a vessel. Adapt the nothing therein to the purpose in hand, and you will have the use of the vessel. Cut out doors and windows in order to make a room. Adapt the nothing therein to the purpose in hand, and you will have the use of the room. Thus what we gain is Something, yet it is by virtue of Nothing that this can be put to use.",
    12: "The five colours cause man's eyes to be blinded. The five notes cause man's ears to be deafed. The five flavours cause man's palate to be spoiled. Racing and hunting cause man's mind to be mad. Rare goods cause man's actions to be thwarted. For this reason the sage is concerned with the belly and not the eyes. That is why he rejects the one but accepts the other.",
    13: "Favor and disgrace bring trouble with them. Rank and self bring trouble with them. What does it mean that favor and disgrace bring trouble with them? Favor is considered below disgrace. When one gains favor, one is as fearful as when one encounters something hateful. When one loses favor, one is as fearful as when one encounters something hateful. This is what is meant by: favor and disgrace bring trouble with them. What does it mean that rank and self bring trouble with them? It is because I have great self that I have trouble. If I had no self, what trouble could I have? Therefore he who values his self more than the world can be entrusted with the world. He who loves his self more than the world can be relied upon with the world.",
    14: "Look at it, you cannot see it - it is called invisible. Listen to it, you cannot hear it - it is called inaudible. Grasp at it, you cannot get it - it is called subtle. These three cannot be further investigated, and hence merge into one. Above it is not bright, below it is not dark. An unending thread, it cannot be named. It returns to nothingness. This is called the shape of the shapeless, the image of the imageless. This is called vague and elusive. Meet it and you will not see its beginning. Follow it and you will not see its end. Hold fast to the way of antiquity in order to control the things of the present. The ability to know the beginnings of antiquity is called the thread of the way.",
    15: "The ancient masters of the way were subtle and mysterious. They were too deep to be understood. Because they could not be understood, I can only describe their appearance: Cautious, like crossing a winter stream. Hesitant, like fearing neighbors on all sides. Dignified, like being a guest. Yielding, like ice about to melt. Simple, like uncarved wood. Open, like a valley. Turbid, like muddy water. Who can quiet the turbid and gradually make it clear? Who can stir the still and gradually bring it to life? Those who hold to this way do not wish to be full. Because they are not full, they can wear out and not need to be renewed.",
    16: "Reach the limit of emptiness, preserve the utmost stillness. The ten thousand things prosper together, and I observe their return. All things flourish and each returns to its root. Returning to the root is called stillness. Stillness is called returning to life. Returning to life is called the constant. Knowing the constant is called enlightenment. Not knowing the constant is to act recklessly and leads to disaster. Knowing the constant leads to acceptance. Acceptance leads to impartiality. Impartiality leads to kingship. Kingship leads to heaven. Heaven leads to the way. The way leads to eternity. Though the body perishes, the way is never destroyed.",
    17: "The great rulers, the people only know they exist. The next best, they love and praise. The next best, they fear. The next best, they despise. If trust is insufficient, there is distrust. How careful they are with their words! When their work is done and their affairs successful, the people all say, 'We did it ourselves.'",
    18: "When the great way is abandoned, benevolence and righteousness appear. When wisdom and intelligence arise, great hypocrisy appears. When the six relations are not in harmony, there are filial piety and parental love. When the state is in chaos and disorder, loyal ministers appear.",
    19: "Abandon wisdom and discard intelligence, and the people will benefit a hundredfold. Abandon benevolence and discard righteousness, and the people will return to filial piety and parental love. Abandon skill and discard profit, and there will be no thieves or robbers. These three are the outward form and are not sufficient. Therefore let people hold on to these: manifest simplicity, embrace the uncarved block, reduce selfishness, decrease desires.",
    20: "Agreement and disagreement differ little. Good and bad differ little. What others fear, I cannot help but fear. The wilderness is vast and endless! The people are merry, as if enjoying a sacrificial feast, as if climbing a terrace in spring. I alone am tranquil and have not yet given signs, like an infant who has not yet smiled. I am alone and listless, as if I have no home to return to. The people all have surplus, while I alone seem lacking. I have the mind of a fool, how confused! Ordinary people are bright and clear, I alone am dull and muddled. Ordinary people are sharp and keen, I alone am blunt and obscure. How calm and peaceful, like the sea! How vast and boundless, like the wind! The people all have purposes, while I alone appear stubborn and rustic. I alone differ from others and value the mother that nourishes.",
    21: "The appearance of great virtue follows alone from the way. The thing that is called the way is elusive and vague. Vague and elusive, there is in it form. Elusive and vague, there is in it substance. Deep and obscure, there is in it essence. The essence is very real, and therein lies the truth. From ancient times to the present, its name has never been forgotten. It is through it that we see the beginning of all things. How do I know that the beginning of all things is so? Through this.",
    22: "The crooked will become straight, the bent will become upright. The empty will become full, the worn will become new. The little will become much, the much will become little. To obtain, one must give. Therefore the sage holds on to the one and becomes the model for the world. He does not display himself, and so is enlightened. He does not justify himself, and so is distinguished. He does not boast, and so has merit. He does not brag, and so endures. It is because he does not contend that no one in the world is able to contend with him. The saying 'the crooked will become straight' is not empty words. It truly leads to attainment and returns to the self.",
    23: "Nature speaks few words. A gale does not blow the whole morning, a rainstorm does not last the whole day. Who does this? Heaven and earth. If even heaven and earth cannot make things last long, how much less can man? Therefore, one who follows the way becomes one with the way. One who follows virtue becomes one with virtue. One who follows loss becomes one with loss. One who becomes one with the way is welcomed by the way. One who becomes one with virtue is welcomed by virtue. One who becomes one with loss is welcomed by loss. When there is not enough faith, there is lack of faith.",
    24: "Those who stand on tiptoe do not stand firm. Those who stride forward do not go far. Those who show themselves do not shine. Those who justify themselves are not distinguished. Those who boast have no merit. Those who brag do not endure. From the point of view of the way, these are like leftover food and tumours. All things detest them. Therefore the man of the way does not dwell in them.",
    25: "There is something formed from confusion and born before heaven and earth. Silent and void, it stands alone and does not change. It goes around and does not weary. It can be the mother of the world. I do not know its name, so I call it the way. Forced to name it, I call it great. Great means passing, passing means receding, receding means returning. Therefore the way is great, heaven is great, earth is great, and the king is also great. There are four great things in the world, and the king is one of them. Man models himself on earth, earth on heaven, heaven on the way, and the way on nature.",
    26: "Heaviness is the root of lightness. Stillness is the master of restlessness. Therefore the sage travels all day without leaving his baggage. Even if he has magnificent sights, he remains calm and detached. How can a ruler with ten thousand chariots treat his body more lightly than the world? Lightness will lose the root, restlessness will lose the master.",
    27: "A good traveler leaves no tracks. A good speaker makes no slips. A good calculator uses no counting rods. A good shutter uses no bolts, yet it cannot be opened. A good binder uses no ropes, yet it cannot be untied. Therefore the sage is always good at saving people, and there are no outcasts. He is always good at saving things, and there are no discarded things. This is called following the light. Therefore the good man is the teacher of the not good. The not good is the material of the good. If the teacher is not respected and the material not cherished, however wise one may be, there is great confusion. This is the essence of mystery.",
    28: "He who knows the male but keeps to the female becomes the ravine of the world. Being the ravine of the world, he does not depart from constant virtue, but returns to infancy. He who knows the white but keeps to the black becomes the model of the world. Being the model of the world, he does not depart from constant virtue, but returns to the limitless. He who knows glory but keeps to disgrace becomes the valley of the world. Being the valley of the world, he is filled with constant virtue, and returns to simplicity. When simplicity is divided, it becomes vessels. The sage makes use of them and becomes the ruler. Therefore the great system is not cut.",
    29: "Those who wish to take the world and act upon it, I see that they cannot succeed. The world is a sacred vessel, it cannot be acted upon. Those who act upon it will destroy it. Those who hold it will lose it. Sometimes things lead, sometimes they follow. Sometimes they breathe gently, sometimes they blow hard. Sometimes they are strong, sometimes they are weak. Sometimes they develop, sometimes they collapse. Therefore the sage avoids excess, extravagance, and arrogance.",
    30: "He who uses the way to assist the master does not use arms to coerce the world. Such things have repercussions. Where troops are stationed, thorns and brambles grow. A great army is inevitably followed by a bad year. One who is good achieves his purpose and stops, and does not use force to achieve it. He achieves his purpose but does not brag. He achieves his purpose but does not boast. He achieves his purpose but does not show arrogance. He achieves his purpose but only when unavoidable. He achieves his purpose but does not use force. Things thrive then grow old. This is called not following the way. What does not follow the way will perish early.",
    31: "Fine weapons are instruments of ill omen. All things detest them. Therefore the man of the way does not dwell in them. The gentleman values the left in daily life, but values the right in war. Weapons are instruments of ill omen, not instruments of the gentleman. When one must use them, it is best to be calm and restrained. Victory should not be celebrated. Those who celebrate victory are those who enjoy killing. If you enjoy killing, you cannot gain the world. On auspicious occasions the left is valued, on inauspicious occasions the right is valued. The lieutenant general is on the left, the general on the right. This shows that they are placed as if for a funeral. When many people are killed, mourn them with grief. When victorious in war, observe it as if conducting a funeral.",
    32: "The way is ever nameless. Though simplicity is small, the world cannot subordinate it. If rulers can hold to it, all things will naturally submit. Heaven and earth join together to send down sweet dew, which is not commanded by people but is naturally equal. When there is beginning and division, names arise. When names have arisen, one should also know where to stop. Knowing where to stop prevents danger. It is like the way in the world, like rivers and valleys flowing into streams and then into the sea.",
    33: "He who knows others is wise. He who knows himself is enlightened. He who conquers others has force. He who conquers himself is strong. He who knows contentment is rich. He who persists has will. He who does not lose his place endures. He who dies but does not perish has longevity.",
    34: "The great way flows everywhere, to left and right. All things depend on it to live, and it does not refuse them. When work is accomplished, it does not claim possession. It clothes and feeds all things but does not rule them. This is called mysterious virtue. Because it does not claim to be great, it can achieve greatness.",
    35: "Hold fast to the great image, and the world will come. They will come without harm, peaceful and at ease. Music and delicacies can make passing guests stop. But when the way is spoken, it is tasteless and cannot be seen, heard, or exhausted in use.",
    36: "If you wish to shrink something, you must first expand it. If you wish to weaken something, you must first strengthen it. If you wish to abolish something, you must first establish it. If you wish to seize something, you must first give it. This is called subtle wisdom. The soft overcomes the hard, the weak overcomes the strong. Fish should not leave the deep pool. The sharp weapons of the state should not be displayed to others.",
    37: "The way is always without action, yet nothing is left undone. If rulers can hold to it, all things will transform themselves. When transformed, if desires arise, I will suppress them with nameless simplicity. Nameless simplicity itself has no desires. Without desires and stillness, the world will right itself.",
    38: "High virtue is not virtuous, therefore it has virtue. Low virtue never loses virtue, therefore it has no virtue. High virtue acts without acting. Low virtue acts with intention. High benevolence acts without intention. High righteousness acts with intention. High ritual acts and gets no response, then pulls up sleeves and forces compliance. Therefore lose the way then virtue, lose virtue then benevolence, lose benevolence then righteousness, lose righteousness then ritual. Ritual is the thinning of loyalty and faith, the beginning of disorder. Foreknowledge is the flower of the way and the beginning of ignorance. Therefore the great man dwells in thickness not thinness, in substance not in flower. Therefore he rejects the latter and takes the former.",
    39: "Those who obtained the one in the past: heaven obtained the one and became clear. Earth obtained the one and became peaceful. The spirits obtained the one and became divine. The valley obtained the one and became full. The myriad things obtained the one and lived. Kings and lords obtained the one and became leaders of the world. This is because of it. If heaven were not clear, it would split. If earth were not peaceful, it would quake. If spirits were not divine, they would disappear. If the valley were not full, it would dry up. If myriad things were not alive, they would perish. If kings and lords were not leaders, they would fall. Therefore nobility is based on humility, height on lowliness. Therefore kings and lords call themselves orphaned, lonely, unworthy. Is this not based on humility? Therefore the highest praise is no praise. Do not wish to be like jade, but like stone.",
    40: "Reversal is the movement of the way. Weakness is the use of the way. The ten thousand things are born from being, and being is born from non-being.",
    41: "When a superior scholar hears the way, he diligently practices it. When a middling scholar hears the way, he seems to both keep and lose it. When an inferior scholar hears the way, he laughs at it. If he does not laugh, it is not the way. Therefore there are sayings: The illuminated way seems dark. The advancing way seems to retreat. The level way seems uneven. High virtue seems like a valley. Great purity seems shameful. Broad virtue seems insufficient. Established virtue seems deceitful. Great purity seems blemished. The great square has no corners. The great vessel is late in completion. The great sound is faint. The great image has no shape. The way is hidden and nameless. Only the way is good at lending and completing.",
    42: "The way produces one, one produces two, two produces three, three produces the ten thousand things. The ten thousand things carry yin and embrace yang. Through the blending of qi they achieve harmony. What people detest, to be orphaned, lonely, unworthy, yet kings and lords use these to call themselves. Therefore things may lose and gain, gain and lose. What others teach, I also teach: The violent will not die a natural death. I will take this as the teacher.",
    43: "The softest thing in the world gallops through the hardest thing in the world. The non-existent can enter the spaceless. Therefore I know the value of non-action. The teaching without words, the value of non-action, are rare in the world.",
    44: "Fame and life, which is more dear? Life and wealth, which is more important? Gaining and losing, which is more harmful? Therefore excessive love must cost greatly. Much storage must suffer heavy loss. Knowing contentment avoids disgrace. Knowing when to stop avoids danger. One can endure long.",
    45: "Great perfection seems incomplete, but its use is not exhausted. Great fullness seems empty, but its use is not depleted. Great straightness seems crooked. Great skill seems clumsy. Great eloquence seems stuttering. Movement overcomes cold. Stillness overcomes heat. Clear stillness is the standard of the world.",
    46: "When the world has the way, horses are used for farming. When the world loses the way, warhorses breed in the suburbs. No crime is worse than sanctioning desire. No disaster is worse than not knowing contentment. No error is worse than seeking gain. Therefore knowing contentment is always enough.",
    47: "Without going out the door, know the world. Without looking out the window, see the way of heaven. The farther one travels, the less one knows. Therefore the sage knows without traveling, names without seeing, achieves without acting.",
    48: "For learning, daily increase. For the way, daily decrease. Decrease and again decrease, until reaching non-action. Through non-action, nothing is left undone. Taking the world is always through non-action. As for acting, one is not enough to take the world.",
    49: "The sage has no fixed mind. He takes the mind of the people as his mind. The good I treat with goodness. The not good I also treat with goodness, thus gaining goodness. The trustworthy I trust. The untrustworthy I also trust, thus gaining trust. The sage dwells in the world, cautiously and harmoniously blending with the world. The people all focus their ears and eyes, and the sage treats them like children.",
    50: "Coming out is life, going in is death. Three tenths follow life, three tenths follow death. People who move from life to death, why is it so? It is because they pursue life too intensely. I hear those who are good at preserving life: When traveling they do not encounter rhinoceros or tigers. When entering the army, they are not wounded by weapons. The rhinoceros has nowhere to thrust its horn. The tiger has nowhere to use its claws. Weapons have nowhere to place their blades. Why is it so? Because there is no death in them.",
    51: "The way produces them, virtue rears them. Things shape them, circumstances complete them. Therefore the ten thousand things all revere the way and honor virtue. Revering the way and honoring virtue are not commanded, but always natural. Therefore the way produces them, virtue rears them, grows them, shelters them, settles them, nourishes them, protects them. Produces but does not possess, acts but does not rely, leads but does not rule. This is called mysterious virtue.",
    52: "The world has a beginning, which is the mother of the world. Once the mother is found, we know her children. Knowing the children but holding to the mother, one will not risk danger even to the end of life. Block the openings, close the doors, and to the end of life there is no exhaustion. Open the openings, do the work, and to the end of life there is no salvation. Seeing the small is called enlightenment. Keeping the weak is called strength. Use the light but return to wisdom, and do not bring disaster to oneself. This is called practicing the constant.",
    53: "If I have slight knowledge, walking the great way, I only fear deviation. The great way is very level, but people love shortcuts. When the court is corrupt, the fields are overgrown, the granaries are empty, yet some wear embroidered clothes and carry sharp swords, gorge on food and drink, and have wealth in surplus. This is called robbery and extravagance, not the way.",
    54: "What is well planted cannot be uprooted. What is well held cannot slip away. The descendants will sacrifice to it endlessly. Cultivate in oneself, and virtue is real. Cultivate in the family, and virtue is abundant. Cultivate in the village, and virtue is lasting. Cultivate in the state, and virtue is prosperous. Cultivate in the world, and virtue is universal. Therefore observe oneself through others, observe the family through the family, observe the village through the village, observe the state through the state, observe the world through the world. How do I know the world is like this? Through this.",
    55: "He who is rich in virtue is like a newborn. Poisonous insects do not sting him, wild beasts do not claw him, birds of prey do not strike him. His bones are weak, his tendons soft, but his grip is firm. He does not know the union of male and female, but his organ is aroused - this is the peak of essence. He can cry all day without becoming hoarse - this is the peak of harmony. Knowing harmony is called constant. Knowing constant is called enlightenment. To increase life is called auspicious. The mind controlling the qi is called strong. Things prosper then grow old - this is called not following the way. What does not follow the way will perish early.",
    56: "Those who know do not speak. Those who speak do not know. Block the openings, close the doors, blunt the sharpness, untie the knots, harmonize the light, mix with the dust. This is called mysterious unity. Therefore it cannot be made close, cannot be made distant, cannot benefit, cannot harm, cannot honor, cannot humiliate. Therefore it is the most noble in the world.",
    57: "Rule the state with correctness, operate the military with surprise. Take the world with non-action. How do I know this is so? Through this: The more prohibitions and taboos, the poorer the people. The more sharp weapons, the more chaotic the state. The more skills, the more strange things arise. The more laws and regulations, the more thieves and robbers. Therefore the sage says: I act without acting, and the people transform themselves. I love stillness, and the people correct themselves. I do not work, and the people enrich themselves. I have no desire, and the people return to simplicity.",
    58: "When the government is dull, the people are pure. When the government is sharp, the people are lacking. Happiness relies on misery. Misery relies on happiness. Who knows the limit? There is no correctness. Correctness becomes strange. Good becomes evil. People's confusion is long-lasting. Therefore the sage is square but does not cut, sharp but does not wound, straight but does not stretch, bright but does not dazzle.",
    59: "In governing people and serving heaven, nothing is better than frugality. Only through frugality can one submit early. Submitting early is called accumulating much virtue. Accumulating much virtue ensures nothing cannot be overcome. When nothing cannot be overcome, no one knows the limit. When no one knows the limit, one can possess the state. The mother of the state can last long. This is called deep roots and a solid foundation, the way of long life and eternal vision.",
    60: "Governing a large state is like cooking a small fish. When the way is used to approach the world, ghosts have no power. Not only do ghosts have no power, but the spirits do not harm people. Not only do spirits not harm people, but the sage also does not harm people. When neither harms the other, virtue converges and returns to its root.",
    61: "A large state is like a lower river, the meeting place of the world, the female of the world. The female always overcomes the male through stillness. Through stillness she takes the lower position. Therefore if a large state serves a small state, it gains the small state. If a small state serves a large state, it gains the large state. Therefore some serve to gain, others serve to be served. The large state only wishes to gather and protect people. The small state only wishes to enter and serve people. If each gets what it wants, the large should especially take the lower position.",
    62: "The way is the refuge of the ten thousand things. It is the treasure of the good, the refuge of the not good. Fine words can gain respect in the market, fine deeds can gain people's support. How can we abandon bad people? Therefore set up the emperor and appoint the three ministers, though presenting jade before four horses, is not as good as sitting and advancing this way. Why did the ancients value this way? Did they not say: Seek and you will find, have sin and be forgiven? Therefore it is the treasure of the world.",
    63: "Act without acting, work without working, taste without tasting. Whether big or small, many or few, repay resentment with virtue. Plan for the difficult while it is easy. Handle the big while it is small. The world's difficult things must be done while easy. The world's big things must be done while small. Therefore the sage never attempts to be great, and thus can achieve greatness. Light promises lead to little trust. Many easy things lead to many difficulties. Therefore the sage treats things as difficult, and thus has no difficulty.",
    64: "What is still is easily held. What has not yet shown omens is easily planned. What is fragile is easily broken. What is minute is easily scattered. Act before things exist. Govern before disorder. A tree you can barely reach around grows from a tiny sprout. A nine-story tower rises from a pile of earth. A journey of a thousand miles begins under one's feet. Acting destroys, grasping loses. Therefore the sage does not act, and thus does not destroy. Does not grasp, and thus does not lose. People in their undertakings always ruin things when near success. Be as careful at the end as at the beginning, and you will not ruin things. Therefore the sage desires no desire, values no rare goods, learns what others do not learn, returns the errors of the multitude, and thus assists all things naturally without daring to act.",
    65: "The ancients who practiced the way did not use it to enlighten the people but to keep them simple. The reason people are difficult to govern is because they are too clever. To govern a state with cleverness harms the state. Not to govern a state with cleverness benefits the state. These two are standards. Always knowing this standard is called mysterious virtue. Mysterious virtue is deep, far-reaching, and opposite of things, and thus reaches agreement.",
    66: "Why do rivers and seas become kings of the hundred valleys? Because they are good at being below them. Therefore they become kings of the hundred valleys. Therefore if sages wish to be above the people, they must speak humbly to them. If they wish to be in front, they must place themselves behind. Therefore sages are above but people do not feel their weight, in front but people do not suffer harm. Therefore the world happily promotes them without resentment. Because they do not contend, no one in the world can contend with them.",
    67: "All the world says my way is great, resembling nothing. If it resembled something, how could it be small from the beginning? I have three treasures that I hold and protect: the first is called compassion, the second is called frugality, the third is called not daring to be first in the world. Compassion leads to courage, frugality leads to generosity, not daring to be first leads to the chief of vessels. Now if one has compassion but abandons it, frugality but abandons it, being behind but abandons it, one will die. With compassion, in attack one wins, in defense one is secure. Heaven will help, and with compassion it will protect.",
    68: "A good warrior is not martial. A good fighter is not angry. A good conqueror is not contentious. A good employer is humble. This is called not contending, this is called employing others, this is called matching heaven, the ancient extreme.",
    69: "The words of strategy are: I dare not be the host but rather the guest. I dare not advance an inch but rather retreat a foot. This is called marching without marching, rolling up sleeves without arms, grasping without weapons, confronting without enemies. No disaster is greater than underestimating the enemy. Underestimating the enemy nearly loses my treasures. Therefore when armies oppose each other, the grieving one will win.",
    70: "My words are very easy to understand and very easy to practice. Yet the world cannot understand them or practice them. Words have ancestors, deeds have masters. Because they do not understand, they do not understand me. Those who understand me are few. Therefore the sage wears coarse clothes but holds jade in his bosom.",
    71: "To know not to know is best. Not to know but to know is sickness. Only by being sick of sickness can one be not sick. The sage is not sick because he is sick of sickness, and thus not sick.",
    72: "When people do not fear power, great power arrives. Do not restrict their dwelling, do not oppress their life. Only when not oppressed will they not be oppressed. Therefore the sage knows himself but does not show himself, loves himself but does not exalt himself. Therefore he rejects the latter and takes the former.",
    73: "Brave in daring leads to death. Brave in not daring leads to life. Of these two, one benefits, one harms. Heaven hates what it hates. Who knows the reason? Even the sage finds it difficult. The way of heaven does not contend but is good at winning. Does not speak but is good at responding. Is not summoned but comes naturally. Is slack but is good at planning. The net of heaven is vast and coarse, yet nothing slips through.",
    74: "If people do not fear death, how can you threaten them with death? If people always fear death, and I catch and kill those who do strange things, who would dare? There is always the executioner who kills. To replace the executioner in killing is like replacing the master carpenter in chopping. Those who replace the master carpenter rarely avoid hurting their hands.",
    75: "People are hungry because the rulers eat too much tax. That is why they are hungry. People are hard to govern because the rulers have too much action. That is why they are hard to govern. People treat death lightly because they seek life too much. That is why they treat death lightly. Only those who do not seek life are wiser than those who value life.",
    76: "When people are born they are soft and weak. When they die they are hard and stiff. When plants are alive they are soft and fragile. When they die they are withered and dry. Therefore the hard and stiff are followers of death. The soft and weak are followers of life. Therefore if the army is strong, it will not win. If the tree is stiff, it will break. The strong and big are below, the soft and weak are above.",
    77: "The way of heaven is like drawing a bow. The high is lowered, the low is raised. The excessive is reduced, the insufficient is supplemented. The way of heaven reduces the excessive and supplements the insufficient. The way of man is not so, it reduces the insufficient to serve the excessive. Who can have the excess to serve the world? Only those with the way. Therefore the sage acts but does not rely, achieves but does not dwell. He does not wish to show his worth.",
    78: "Nothing in the world is softer and weaker than water. Yet nothing attacks the hard and strong better. Nothing can change it. The weak overcome the strong, the soft overcome the hard. This is known by all but not practiced. Therefore the sage says: Receive the state's filth - this is the lord of the state. Receive the state's bad omens - this is the king of the world. True words seem contrary.",
    79: "When settling great resentment, some resentment must remain. How can this be considered good? Therefore the sage holds the left side of the contract but does not demand from others. Those with virtue hold the contract, those without virtue collect taxes. The way of heaven has no favorites, but always helps the good.",
    80: "A small state with few people: Let there be tools for a hundred or ten, but not use them. Let people value death and not travel far. Let there be boats and carriages but no one rides them. Let there be armor and weapons but no one displays them. Let people return to knotting ropes and using them. Let food be sweet, clothes beautiful, home secure, customs happy. Neighboring states look at each other, hear chickens and dogs, but people grow old and die without visiting.",
    81: "True words are not beautiful, beautiful words are not true. Good speakers are not eloquent, eloquent speakers are not good. Knowledgeable people are not broad, broad people are not knowledgeable. Sages do not accumulate. The more they do for others, the more they have. The more they give to others, the more they gain. The way of heaven benefits and does not harm. The way of the sage acts without contending."
}

# Addiss & Lombardo 英文译本
ENGLISH_ADDISS = {
    11: "Thirty spokes share the wheel's hub. It is the center hole that makes it useful. Shape clay into a vessel. It is the emptiness inside that makes it useful. Cut doors and windows for a room. It is the openings that make it useful. Therefore profit comes from what is there, usefulness from what is not.",
    12: "Five colors blind the eye. Five notes deafen the ear. Five flavors dull the palate. Racing and hunting madden the mind. Rare goods tempt people to action. Therefore the sage is for the belly, not the eye. Rejects this, grasps that.",
    13: "Favor and disgrace are like fear. Honor and distress are like the self. What does this mean: favor and disgrace are like fear? Favor is below. Getting it is fear, losing it is fear. This is what is meant by favor and disgrace are like fear. What does this mean: honor and distress are like the self? The reason I have distress is that I have a self. If I had no self, what distress would I have? Therefore honor the self as you honor the world, and you can entrust the world. Love the self as you love the world, and you can rule the world.",
    14: "Look, it cannot be seen - it is invisible. Listen, it cannot be heard - it is inaudible. Reach, it cannot be touched - it is intangible. These three cannot be investigated, they merge into one. Above is not bright, below is not dark. An unending thread beyond naming, it returns to nothingness. This is the formless form, the image of nothing. This is the elusive. Meet it, it has no beginning. Follow it, it has no end. Hold to the ancient way, to rule the present. Knowing the ancient beginning is the way's thread.",
    15: "The ancient masters were subtle, mysterious, profound, responsive. Too deep to be understood. Because they could not be understood, I can only describe them: cautious as if crossing a winter stream, hesitant as if fearing neighbors, dignified as if being a guest, yielding like melting ice, simple like uncarved wood, open like a valley, turbid like muddy water. Who can quiet the turbid and gradually become clear? Who can stir the still and gradually come to life? Those who hold this way do not wish to be full. Because they are not full, they can renew and not be exhausted.",
    16: "Empty to the limit, become still. Ten thousand things arise, I watch them return. Things flourish and each returns to its root. Returning to the root is stillness. Stillness is returning to life. Returning to life is the constant. Knowing the constant is enlightenment. Not knowing the constant is recklessness, leading to disaster. Knowing the constant is acceptance. Acceptance is impartiality. Impartiality is kingship. Kingship is heaven. Heaven is the way. The way is eternal. Though the body dies, the way does not.",
    17: "The best rulers are unknown to their people. The next best are loved and praised. The next are feared. The next are despised. When trust is lacking, there is distrust. Reluctant, they do not speak. When their work is done and affairs successful, the people all say, 'We did it ourselves.'",
    18: "When the great way is abandoned, benevolence and righteousness appear. When wisdom and intelligence arise, great hypocrisy appears. When family relations are not harmonious, filial piety and compassion appear. When the state is in chaos, loyal ministers appear.",
    19: "Reject wisdom, discard intelligence, the people benefit a hundredfold. Reject benevolence, discard righteousness, the people return to filial piety and compassion. Reject skill, discard profit, thieves and robbers disappear. These three are not enough. Therefore let people belong to this: see simplicity, embrace the uncarved block, reduce selfishness, decrease desire.",
    20: "Agreeing and disagreeing are close. Good and bad are close. What others fear, I cannot help but fear. So vast, it has no end. The people are merry, as if enjoying a feast, as if climbing a terrace in spring. I alone am calm, like an infant who has not yet smiled. I alone am wandering, like one with no home to return to. The people all have enough, I alone seem lacking. I have the mind of a fool, how confused. Ordinary people are bright, I alone am dim. Ordinary people are sharp, I alone am dull. Calm like the sea, drifting like the wind. The people all have purpose, I alone seem stubborn and rustic. I alone differ from others, and value the mother that nourishes.",
    21: "Great virtue follows the way. The way as a thing is vague and elusive. Elusive and vague, there are images in it. Vague and elusive, there are things in it. Deep and obscure, there is essence in it. The essence is very real, and within it is trust. From ancient times to now, its name never leaves. Through it we see the beginning of all things. How do I know the beginning of all things? Through this.",
    22: "Bent then whole. Crooked then straight. Hollow then full. Worn then new. Few then many. Many then confused. Therefore the sage embraces the one and becomes the model of the world. Not showing himself, he is enlightened. Not justifying himself, he is distinguished. Not boasting, he has merit. Not bragging, he endures. Because he does not contend, no one in the world can contend with him. The saying 'bent then whole' - are these empty words? Truly, he attains and returns.",
    23: "Nature speaks few words. A whirlwind does not last the morning, a rainstorm does not last the day. Who makes this? Heaven and earth. If heaven and earth cannot last long, how can humans? Therefore those who follow the way become one with the way. Those who follow virtue become one with virtue. Those who follow loss become one with loss. Those who become one with the way, the way gladly welcomes them. Those who become one with virtue, virtue gladly welcomes them. Those who become one with loss, loss gladly welcomes them. If trust is insufficient, there is distrust.",
    24: "On tiptoe, one does not stand. Striding, one does not go forward. Showing oneself, one is not enlightened. Justifying oneself, one is not distinguished. Boasting, one has no merit. Bragging, one does not endure. From the way's perspective, this is called extra food and action. All things detest it. Therefore those with the way do not dwell in it.",
    25: "Something formed in chaos, born before heaven and earth. Silent and void, it stands alone and does not change. It goes around and does not tire. It can be the mother of the world. I do not know its name, I call it the way. Forced to name it, I call it great. Great means passing, passing means faring, faring means returning. Therefore the way is great, heaven is great, earth is great, the king is also great. There are four greats in the world, and the king is one of them. Humans follow earth, earth follows heaven, heaven follows the way, the way follows nature.",
    26: "Heaviness is the root of lightness. Stillness is the master of restlessness. Therefore the sage travels all day without leaving the baggage cart. Though having magnificent sights, he remains calm and detached. How can the lord of ten thousand chariots treat his body more lightly than the world? Lightness loses the root, restlessness loses the master.",
    27: "A good traveler leaves no tracks. A good speaker makes no slips. A good counter uses no counting rods. A good door uses no bolts, yet cannot be opened. A good knot uses no rope, yet cannot be untied. Therefore the sage is always good at saving people, and does not abandon anyone. Always good at saving things, and does not abandon anything. This is called following the light. Therefore the good person is the teacher of the not good. The not good is the resource of the good. If the teacher is not valued and the resource not cherished, however wise one is, one is greatly confused. This is called the essence of mystery.",
    28: "Know the male, keep the female - be the ravine of the world. Being the ravine of the world, constant virtue does not leave, return to infancy. Know the white, keep the black - be the model of the world. Being the model of the world, constant virtue does not err, return to the limitless. Know the glory, keep the disgrace - be the valley of the world. Being the valley of the world, constant virtue is sufficient, return to simplicity. Simplicity breaks into vessels, the sage uses them and becomes the leader. Therefore the great carving does not cut.",
    29: "Those who want to take the world and act on it, I see that they cannot succeed. The world is a sacred vessel, cannot be acted on. Those who act on it destroy it. Those who hold it lose it. Sometimes things go forward, sometimes follow. Sometimes breathe gently, sometimes blow hard. Sometimes are strong, sometimes are weak. Sometimes develop, sometimes collapse. Therefore the sage rejects excess, extravagance, arrogance.",
    30: "Those who use the way to assist the master do not use weapons to coerce the world. Such things have repercussions. Where the army camps, thorns and brambles grow. A great army is inevitably followed by a bad year. One who is good achieves his purpose and stops, does not use force to achieve it. Achieves but does not rely on it, achieves but does not dwell on it, achieves but does not boast, achieves but only when unavoidable, achieves but does not use force. Things thrive then grow old. This is called not following the way. What does not follow the way will perish early.",
    31: "Fine weapons are instruments of ill omen. All things detest them. Therefore those with the way do not dwell in them. The gentleman values the left in daily life, but in war values the right. Weapons are instruments of ill omen, not the gentleman's instruments. When one must use them, calm detachment is best. Do not celebrate victory. Those who celebrate victory kill people. Those who kill people cannot fulfill their purpose in the world. On auspicious occasions the left is valued, on inauspicious the right is valued. The lieutenant general is on the left, the general on the right. This is said to be conducting it like a funeral. When many people are killed, mourn them with grief. When victorious in war, conduct it like a funeral.",
    32: "The way is ever nameless. Though simplicity is small, the world cannot subordinate it. If lords and kings can hold to it, the ten thousand things will submit themselves. Heaven and earth join together to send down sweet dew, not commanded by people but naturally equal. When there is division, names arise. When names have arisen, know also to stop. Knowing to stop prevents danger. It is like the way in the world, like the streams and valleys flowing into rivers and seas.",
    33: "Those who know others are wise. Those who know themselves are enlightened. Those who conquer others have strength. Those who conquer themselves are powerful. Those who know contentment are rich. Those who persevere have will. Those who do not lose their place endure. Those who die but do not perish have longevity.",
    34: "The great way overflows, to left and right. Ten thousand things rely on it to live, and it does not refuse them. It achieves its work but does not dwell on it. It clothes and feeds the ten thousand things but does not rule them. This can be called small. The ten thousand things return to it but it does not rule them. This can be called great. Because it does not strive to be great, it can achieve greatness.",
    35: "Hold the great image, and the world comes. Comes without harm, peaceful and at ease. Music and food make passing guests stop. But when the way is spoken, it is tasteless. Look, it cannot be seen. Listen, it cannot be heard. Use, it cannot be exhausted.",
    36: "If you wish to shrink it, you must expand it. If you wish to weaken it, you must strengthen it. If you wish to abolish it, you must establish it. If you wish to seize it, you must give it. This is called subtle wisdom. The soft overcomes the hard, the weak overcomes the strong. Fish should not leave the deep pool. The sharp weapons of the state should not be shown to others.",
    37: "The way is always without action, yet nothing is left undone. If lords and kings can hold to it, the ten thousand things will transform themselves. If transformed desires arise, I will suppress them with nameless simplicity. Nameless simplicity itself has no desire. Without desire and stillness, the world will right itself.",
    38: "High virtue is not virtuous, therefore it has virtue. Low virtue does not lose virtue, therefore it has no virtue. High virtue takes no action and has no intention. Low virtue takes action and has intention. High benevolence takes action and has no intention. High righteousness takes action and has intention. High ritual takes action and gets no response, then pulls up sleeves and forces compliance. Therefore lose the way then virtue, lose virtue then benevolence, lose benevolence then righteousness, lose righteousness then ritual. Ritual is the thinning of loyalty and trust, the beginning of disorder. Foreknowledge is the flower of the way and the beginning of ignorance. Therefore the great man dwells in thickness not thinness, in fruit not flower. Therefore he rejects the latter and takes the former.",
    39: "Those who obtained the one in the past: heaven obtained the one and became clear. Earth obtained the one and became peaceful. The spirits obtained the one and became divine. The valley obtained the one and became full. The ten thousand things obtained the one and lived. Kings and lords obtained the one and became leaders of the world. This is because of it. If heaven were not clear, it would split. If earth were not peaceful, it would quake. If spirits were not divine, they would dissipate. If the valley were not full, it would dry up. If the ten thousand things were not alive, they would perish. If kings and lords were not leaders, they would fall. Therefore nobility has root in humility, height has root in lowliness. Therefore kings and lords call themselves orphaned, lonely, unworthy. Is this not taking humility as root? Therefore the highest praise is no praise. Do not wish to be like jade, or like stone.",
    40: "Reversal is the movement of the way. Weakness is the use of the way. The ten thousand things are born from being, and being is born from non-being.",
    41: "When a superior scholar hears the way, he diligently practices it. When a middling scholar hears the way, he seems to both keep and lose it. When an inferior scholar hears the way, he laughs at it. If he does not laugh, it is not the way. Therefore there are sayings: The illuminated way seems dark. The advancing way seems to retreat. The level way seems uneven. High virtue seems like a valley. Great purity seems shameful. Broad virtue seems insufficient. Established virtue seems deceitful. Great purity seems blemished. The great square has no corners. The great vessel is late in completion. The great sound is faint. The great image has no shape. The way is hidden and nameless. Only the way is good at lending and completing.",
    42: "The way produces one, one produces two, two produces three, three produces the ten thousand things. The ten thousand things carry yin and embrace yang. Through the blending of qi they achieve harmony. What people detest, to be orphaned, lonely, unworthy, yet kings and lords use these to call themselves. Therefore things may lose and gain, gain and lose. What others teach, I also teach: The violent will not die a natural death. I will take this as the father of teaching.",
    43: "The softest thing in the world gallops through the hardest thing in the world. The non-existent can enter the spaceless. Therefore I know the value of non-action. The teaching without words, the value of non-action, are rare in the world.",
    44: "Fame and life, which is more dear? Life and wealth, which is more important? Gaining and losing, which is more harmful? Therefore excessive love must cost greatly. Much storage must suffer heavy loss. Knowing contentment avoids disgrace. Knowing when to stop avoids danger. One can endure long.",
    45: "Great perfection seems incomplete, but its use is not exhausted. Great fullness seems empty, but its use is not depleted. Great straightness seems crooked. Great skill seems clumsy. Great eloquence seems stuttering. Movement overcomes cold. Stillness overcomes heat. Clear stillness is the standard of the world.",
    46: "When the world has the way, horses are used for farming. When the world loses the way, warhorses breed in the suburbs. No crime is greater than sanctioning desire. No disaster is greater than not knowing contentment. No error is greater than seeking gain. Therefore knowing contentment is always enough.",
    47: "Without going out the door, know the world. Without looking out the window, see the way of heaven. The farther one travels, the less one knows. Therefore the sage knows without traveling, names without seeing, achieves without acting.",
    48: "For learning, daily increase. For the way, daily decrease. Decrease and again decrease, until reaching non-action. Through non-action, nothing is left undone. Taking the world is always through non-action. As for acting, one is not enough to take the world.",
    49: "The sage has no fixed mind. He takes the mind of the people as his mind. The good I treat with goodness. The not good I also treat with goodness, thus gaining goodness. The trustworthy I trust. The untrustworthy I also trust, thus gaining trust. The sage dwells in the world, cautiously and harmoniously blending with the world. The people all focus their ears and eyes, and the sage treats them like children.",
    50: "Coming out is life, going in is death. Three tenths follow life, three tenths follow death. People who move from life to death, why is it so? It is because they pursue life too intensely. I hear those who are good at preserving life: When traveling they do not encounter rhinoceros or tigers. When entering the army, they are not wounded by weapons. The rhinoceros has nowhere to thrust its horn. The tiger has nowhere to use its claws. Weapons have nowhere to place their blades. Why is it so? Because there is no death in them.",
    51: "The way produces them, virtue rears them. Things shape them, circumstances complete them. Therefore the ten thousand things all revere the way and honor virtue. Revering the way and honoring virtue are not commanded, but always natural. Therefore the way produces them, virtue rears them, grows them, shelters them, settles them, nourishes them, protects them. Produces but does not possess, acts but does not rely, leads but does not rule. This is called mysterious virtue.",
    52: "The world has a beginning, which is the mother of the world. Once the mother is found, we know her children. Knowing the children but holding to the mother, one will not risk danger even to the end of life. Block the openings, close the doors, and to the end of life there is no exhaustion. Open the openings, do the work, and to the end of life there is no salvation. Seeing the small is called enlightenment. Keeping the weak is called strength. Use the light but return to wisdom, and do not bring disaster to oneself. This is called practicing the constant.",
    53: "If I have slight knowledge, walking the great way, I only fear deviation. The great way is very level, but people love shortcuts. When the court is corrupt, the fields are overgrown, the granaries are empty, yet some wear embroidered clothes and carry sharp swords, gorge on food and drink, and have wealth in surplus. This is called robbery and extravagance, not the way.",
    54: "What is well planted cannot be uprooted. What is well held cannot slip away. The descendants will sacrifice to it endlessly. Cultivate in oneself, and virtue is real. Cultivate in the family, and virtue is abundant. Cultivate in the village, and virtue is lasting. Cultivate in the state, and virtue is prosperous. Cultivate in the world, and virtue is universal. Therefore observe oneself through others, observe the family through the family, observe the village through the village, observe the state through the state, observe the world through the world. How do I know the world is like this? Through this.",
    55: "He who is rich in virtue is like a newborn. Poisonous insects do not sting him, wild beasts do not claw him, birds of prey do not strike him. His bones are weak, his tendons soft, but his grip is firm. He does not know the union of male and female, but his organ is aroused - this is the peak of essence. He can cry all day without becoming hoarse - this is the peak of harmony. Knowing harmony is called constant. Knowing constant is called enlightenment. To increase life is called auspicious. The mind controlling the qi is called strong. Things prosper then grow old - this is called not following the way. What does not follow the way will perish early.",
    56: "Those who know do not speak. Those who speak do not know. Block the openings, close the doors, blunt the sharpness, untie the knots, harmonize the light, mix with the dust. This is called mysterious unity. Therefore it cannot be made close, cannot be made distant, cannot benefit, cannot harm, cannot honor, cannot humiliate. Therefore it is the most noble in the world.",
    57: "Rule the state with correctness, operate the military with surprise. Take the world with non-action. How do I know this is so? Through this: The more prohibitions and taboos, the poorer the people. The more sharp weapons, the more chaotic the state. The more skills, the more strange things arise. The more laws and regulations, the more thieves and robbers. Therefore the sage says: I act without acting, and the people transform themselves. I love stillness, and the people correct themselves. I do not work, and the people enrich themselves. I have no desire, and the people return to simplicity.",
    58: "When the government is dull, the people are pure. When the government is sharp, the people are lacking. Happiness relies on misery. Misery relies on happiness. Who knows the limit? There is no correctness. Correctness becomes strange. Good becomes evil. People's confusion is long-lasting. Therefore the sage is square but does not cut, sharp but does not wound, straight but does not stretch, bright but does not dazzle.",
    59: "In governing people and serving heaven, nothing is better than frugality. Only through frugality can one submit early. Submitting early is called accumulating much virtue. Accumulating much virtue ensures nothing cannot be overcome. When nothing cannot be overcome, no one knows the limit. When no one knows the limit, one can possess the state. The mother of the state can last long. This is called deep roots and a solid foundation, the way of long life and eternal vision.",
    60: "Governing a large state is like cooking a small fish. When the way is used to approach the world, ghosts have no power. Not only do ghosts have no power, but the spirits do not harm people. Not only do spirits not harm people, but the sage also does not harm people. When neither harms the other, virtue converges and returns to its root.",
    61: "A large state is like a lower river, the meeting place of the world, the female of the world. The female always overcomes the male through stillness. Through stillness she takes the lower position. Therefore if a large state serves a small state, it gains the small state. If a small state serves a large state, it gains the large state. Therefore some serve to gain, others serve to be served. The large state only wishes to gather and protect people. The small state only wishes to enter and serve people. If each gets what it wants, the large should especially take the lower position.",
    62: "The way is the refuge of the ten thousand things. It is the treasure of the good, the refuge of the not good. Fine words can gain respect in the market, fine deeds can gain people's support. How can we abandon bad people? Therefore set up the emperor and appoint the three ministers, though presenting jade before four horses, is not as good as sitting and advancing this way. Why did the ancients value this way? Did they not say: Seek and you will find, have sin and be forgiven? Therefore it is the treasure of the world.",
    63: "Act without acting, work without working, taste without tasting. Whether big or small, many or few, repay resentment with virtue. Plan for the difficult while it is easy. Handle the big while it is small. The world's difficult things must be done while easy. The world's big things must be done while small. Therefore the sage never attempts to be great, and thus can achieve greatness. Light promises lead to little trust. Many easy things lead to many difficulties. Therefore the sage treats things as difficult, and thus has no difficulty.",
    64: "What is still is easily held. What has not yet shown omens is easily planned. What is fragile is easily broken. What is minute is easily scattered. Act before things exist. Govern before disorder. A tree you can barely reach around grows from a tiny sprout. A nine-story tower rises from a pile of earth. A journey of a thousand miles begins under one's feet. Acting destroys, grasping loses. Therefore the sage does not act, and thus does not destroy. Does not grasp, and thus does not lose. People in their undertakings always ruin things when near success. Be as careful at the end as at the beginning, and you will not ruin things. Therefore the sage desires no desire, values no rare goods, learns what others do not learn, returns the errors of the multitude, and thus assists all things naturally without daring to act.",
    65: "The ancients who practiced the way did not use it to enlighten the people but to keep them simple. The reason people are difficult to govern is because they are too clever. To govern a state with cleverness harms the state. Not to govern a state with cleverness benefits the state. These two are standards. Always knowing this standard is called mysterious virtue. Mysterious virtue is deep, far-reaching, and opposite of things, and thus reaches agreement.",
    66: "Why do rivers and seas become kings of the hundred valleys? Because they are good at being below them. Therefore they become kings of the hundred valleys. Therefore if sages wish to be above the people, they must speak humbly to them. If they wish to be in front, they must place themselves behind. Therefore sages are above but people do not feel their weight, in front but people do not suffer harm. Therefore the world happily promotes them without resentment. Because they do not contend, no one in the world can contend with them.",
    67: "All the world says my way is great, resembling nothing. If it resembled something, how could it be small from the beginning? I have three treasures that I hold and protect: the first is called compassion, the second is called frugality, the third is called not daring to be first in the world. Compassion leads to courage, frugality leads to generosity, not daring to be first leads to the chief of vessels. Now if one has compassion but abandons it, frugality but abandons it, being behind but abandons it, one will die. With compassion, in attack one wins, in defense one is secure. Heaven will help, and with compassion it will protect.",
    68: "A good warrior is not martial. A good fighter is not angry. A good conqueror is not contentious. A good employer is humble. This is called not contending, this is called employing others, this is called matching heaven, the ancient extreme.",
    69: "The words of strategy are: I dare not be the host but rather the guest. I dare not advance an inch but rather retreat a foot. This is called marching without marching, rolling up sleeves without arms, grasping without weapons, confronting without enemies. No disaster is greater than underestimating the enemy. Underestimating the enemy nearly loses my treasures. Therefore when armies oppose each other, the grieving one will win.",
    70: "My words are very easy to understand and very easy to practice. Yet the world cannot understand them or practice them. Words have ancestors, deeds have masters. Because they do not understand, they do not understand me. Those who understand me are few. Therefore the sage wears coarse clothes but holds jade in his bosom.",
    71: "To know not to know is best. Not to know but to know is sickness. Only by being sick of sickness can one be not sick. The sage is not sick because he is sick of sickness, and thus not sick.",
    72: "When people do not fear power, great power arrives. Do not restrict their dwelling, do not oppress their life. Only when not oppressed will they not be oppressed. Therefore the sage knows himself but does not show himself, loves himself but does not exalt himself. Therefore he rejects the latter and takes the former.",
    73: "Brave in daring leads to death. Brave in not daring leads to life. Of these two, one benefits, one harms. Heaven hates what it hates. Who knows the reason? Even the sage finds it difficult. The way of heaven does not contend but is good at winning. Does not speak but is good at responding. Is not summoned but comes naturally. Is slack but is good at planning. The net of heaven is vast and coarse, yet nothing slips through.",
    74: "If people do not fear death, how can you threaten them with death? If people always fear death, and I catch and kill those who do strange things, who would dare? There is always the executioner who kills. To replace the executioner in killing is like replacing the master carpenter in chopping. Those who replace the master carpenter rarely avoid hurting their hands.",
    75: "People are hungry because the rulers eat too much tax. That is why they are hungry. People are hard to govern because the rulers have too much action. That is why they are hard to govern. People treat death lightly because they seek life too much. That is why they treat death lightly. Only those who do not seek life are wiser than those who value life.",
    76: "When people are born they are soft and weak. When they die they are hard and stiff. When plants are alive they are soft and fragile. When they die they are withered and dry. Therefore the hard and stiff are followers of death. The soft and weak are followers of life. Therefore if the army is strong, it will not win. If the tree is stiff, it will break. The strong and big are below, the soft and weak are above.",
    77: "The way of heaven is like drawing a bow. The high is lowered, the low is raised. The excessive is reduced, the insufficient is supplemented. The way of heaven reduces the excessive and supplements the insufficient. The way of man is not so, it reduces the insufficient to serve the excessive. Who can have the excess to serve the world? Only those with the way. Therefore the sage acts but does not rely, achieves but does not dwell. He does not wish to show his worth.",
    78: "Nothing in the world is softer and weaker than water. Yet nothing attacks the hard and strong better. Nothing can change it. The weak overcome the strong, the soft overcome the hard. This is known by all but not practiced. Therefore the sage says: Receive the state's filth - this is the lord of the state. Receive the state's bad omens - this is the king of the world. True words seem contrary.",
    79: "When settling great resentment, some resentment must remain. How can this be considered good? Therefore the sage holds the left side of the contract but does not demand from others. Those with virtue hold the contract, those without virtue collect taxes. The way of heaven has no favorites, but always helps the good.",
    80: "A small state with few people: Let there be tools for a hundred or ten, but not use them. Let people value death and not travel far. Let there be boats and carriages but no one rides them. Let there be armor and weapons but no one displays them. Let people return to knotting ropes and using them. Let food be sweet, clothes beautiful, home secure, customs happy. Neighboring states look at each other, hear chickens and dogs, but people grow old and die without visiting.",
    81: "True words are not beautiful, beautiful words are not true. Good speakers are not eloquent, eloquent speakers are not good. Knowledgeable people are not broad, broad people are not knowledgeable. Sages do not accumulate. The more they do for others, the more they have. The more they give to others, the more they gain. The way of heaven benefits and does not harm. The way of the sage acts without contending."
}

# 王夫之《老子衍》完整注解（衍文）
WANGFUZHI_NOTES = {
    11: "造有者，求其有也。孰知夫求其有者，所以保其無也？經營以有，而但為其無，豈樂無哉？無者，用之藏也。物立於我前，固非我之所得執矣。象數立於道前，而道不居之以自礙矣。陰凝陽融以為人，而沖氣俱其間；不倚於火，不倚於符者遇之。仁義剛柔以為教，而大樸俱其間；不倚於性，不倚於情者遇之。勝負得失以為變，而事會俱其間；不倚於治，不倚於亂者遇之。故避其堅，攻其瑕，去其名，就其實，俟之俄頃，而萬機合於一。",
    12: "目以機為機，腹以無機為機。機與機為應，無機者，機之所取容也。處乎目與腹之中者，心也。方且退心而就腹，而後可以觀物。是故濁不可使有心，清不可使有跡。不以禮制欲，不以知辨志，待物自敝而天乃脫然。",
    13: "眾人納天下於身，至人外其身於天下。夫不見納天下者，有必至之憂患乎？寵至若驚，辱來若驚，則是納天下者，納驚以自滑也。大患在天下，納而貴之與身等。夫身且為患，而貴患以為重累之身，是納患以自梏也。唯無身者，以耳任耳，不為天下任聽；以目任目，不為天下任視；吾之耳目靜，而天下之視聽不熒；驚患去已，而消於天下，是以為百姓履藉而不傾。",
    14: "物有間；人不知其間；故合之，背之，而物皆為患。道無間，人強分其間；故執之，別之，而道僅為名。以無間乘有間，終日遊，而患與名去。患與名去，斯「無物」矣。夫有物者，或輕，或重；或光，或塵；或作，或止；是謂無紀。一名為陰，一名為陽，而沖氣死。一名為仁，一名為義，而太和死。道也者，生於未陰未陽，而死於仁義者與！故離朱不能察黑白之交，師曠不能審宮商之會，慶忌不能攫空塵之隙，神禹不能皙天地之分。非至常者，何足以與於斯！",
    15: "擇妙者眾，繇微而妙者鮮。求通者多，以玄為通者希。夫章甫不可以適越，而我無入越之心，則妙不在冠不冠之中，而敢以冠嘗試其身乎？而敢以不冠嘗試其首乎？又惡知夫不敢嘗試者之越不為我適也，坐以消之，則冰可燠，濁可清，以雨行而不假蓋，以饑往而不裹糧。其徐俟之也，豈果有黃河之不可澄，馬角之不可生哉？天下已如斯矣，而競名者以折銳為功。久矣，其棄故喜新而不能成也！",
    16: "最下擊實，其次邀虛。最下取動，其次執靜。兩實之中，虛故自然：眾動之極，靜原自復；不邀不執，乃極乃篤。何以明其然也？萬物並作，而蕓蕓者，勢盡而反其所自來也。是故鄧林之葉，可無籌而數；千里之雨，可無器而量。猶舍是而有作，其不謂之妄手？故無所有事，而天下為我用，其道不用作而用觀。觀，目也。觀而不作，目亦腹矣。",
    17: "據道於此，疑彼之亦道；據道於彼，疑此之非道：既從而異之，又從而同之，則道亂於二，而苦於一。且亂，且苦，其疑不去。既自以為疑矣，故王者見不親而憂，霸者遇不畏而怖。其疑不釋，遂救之以要言；故始乎詛盟，而終平甲胄。夫使人忘我於自然者，豈其心有不自然哉？信天下之不能越是也，任其遷流而不出於所自來，不爽於所自復，虛贅於天下之上，以待物之自成。是以天下之情，不可因，不可革；太上之治，無所通，無所塞，如老人之師，如盡人之力，而人乃廢然而稱之曰自然。",
    18: "桮棬成於匠，而木死於山；罌盎成於陶，而土死於邱。其器是也，而所以飲天地之和者去之也。夫土木且有以飲，而況於人乎？而況於道乎？故利在物而害在己，謂之不全；善在己而敗在物，謂之不公。",
    19: "「綿綿若存」，其有所屬乎！故魚遊而水乘之，鳥飛而空憑之。含天下之文者，莫大乎素；資天下之不足者，莫大於樸。以為有，而固未親乎用；以為無，而人與天之相親者在此也。綴乎和以致生，是以能長生。離乎和以專用，是以無大用。",
    20: "善惡相傾，繇學而起，故效仁者失智，效智者失仁。既爭歧之，又強合之，方且以為免於憂，而孰知一彼一此者之相去不遠也？則揖讓亦唯，而征伐亦阿也。憒各封之，取快一區；故飫於大牢，不饗他味；厭於春遊，不願他觀。口目之用一，而所善者萬；心一，而口目之用萬；安能役役以奔其趣舍哉，其唯食於母乎！食於母者，不得已而有食，而未嘗有所不得已也。故荒未央者可盡，而頑鄙可居。雖然，其所食者虛也，因也。天下畏不仁，而我不敢暴；天下畏不智，而我不敢迷。以雪遁者，唯恐以跡；以棘行者，唯恐以罥。蟺婉輕微，而後學可絕；學可絕，而後生不損而物不傷。",
    21: "兩者相耦而有「中」。「恍惚」無耦，無耦無「中」。而惡知介乎耦，則非左即右，而不得為「中」也？「中」者，入乎耦而含耦者也。雖有堅金，可鍛而液；雖有積土，可漂而夷；然則金土不能保其性矣。既有溫泉，亦有寒火；然則水火不能守其真矣。不銑而堅於金，不厚而敦於土，不暄而炎於火，不潤而寒於水者，誰耶？閱其變而不遷，知其然而不往；故真莫尚於無實，信莫大於不復，名莫永於彼此不易，而容莫美於萬一不殊。私天之機，棄道之似，夫乃可字之曰「孔德」。",
    22: "事物之教，有來有往。迎其來，不如要其往；追其往，不如俟其來。而以心日察察於往來者，則非先時，而即後時。先既失後，後又失先，勞勞而愈不得；故小智日見其餘，大智日見其不足。大道在中，如捕亡子而喪家珍，瞀然介馬以馳，終日而不遇，則多之為惑久矣。一曰沖，沖曰常。守常，用沖，養曲為全，明於往來之大數也。",
    23: "天地違其和，則能天，能地，而不能久。人違其和，則能得，能失，而不能同。暢於陽，鬱於陰；暢於陰，鬱於陽。言過則跲，樂極則悲；一心數變，寢寐自驚。不知廣大一同，多所不信，坐失常道，何望自然哉？凡道皆道，凡德皆德，凡失皆失。道德樂游於同，久亦奚渝？喜怒不至，何風雨之愆乎？",
    24: "心彌急者機彌失，是彌堅者非彌甚。前機已往，追而綴之，如食已飫而更設。後機未至，強而屬之，如形已具而更駢。道數無窮，執偏執餘以盡之，宜其憎乎物，而傷乎己也。",
    25: "形象有間，道無間。道不擇有，亦不擇無，與之俱往。往而不息於往，故為逝，為遠，與之俱往矣。住而不悖其來，與之俱來，則逝遠之即反也。道既已如斯矣，法道者亦乘乘然而與之往來。而與之往來者，守常而天下自復，蓋不憂其數而不給矣。「栽營魄，抱一而不離」，用此物也。近取之身，為艮背而不為機目；遠取之天地，為大制而不為剸割；故可以為天下王。",
    26: "有根則有莖，有君則有臣。雖然，無寧守其本乎！ 一息之頃，眾動相乘，而不能不有所止。道不滯於所止，而因所止以觀，則道之游於虛，而常無間者見矣。惟不須臾忍，而輕以往，則應在一而違在萬，恩在一隅而怨在三隅，倒授天下以柄，而反制其身。故夏亡於牧宮之造，周衰於征漢之舟。以仁援天下而天下溺，以義濟天下而天下陷，天下之大，蕩之俄頃，而況吾身之內僅有之和乎？",
    27: "我之有明，非明也，又況投明於物，絜其長短以為耀乎？故鳥窒於實，蚓困於空，魚窮於陸，固其獲，而未知不得者之可為得也。我欲勝之，勿往絜之。萬物飾其形以相求，或逃其美以相激，咸潛測其根柢，掩而有之，則物投我而我不投物。眾實求給，一虛無間，故善惡之意消，而言行閉結之所攝者，要妙不可窺矣。",
    28: "或雌或雌，或白或黑，或榮或辱，各有對待，不能相通，則我道蓋幾於窮，而我之有知有守亦不一矣。知者歸清，守者歸濁，兩術剖分，各歸其肖，游環中者可知已。然致意於知矣，而收功於守，則何也？賓清而主濁，以物極之必反，反者之可長主也。故嬰兒可壯，壯不可稚；無極可有，有不可無；樸可琢，琢不可樸。然聖人非於可不可斤斤以辨之。環中以游，如霖雨之灌蟻封，如原燎之灼積莽，無首無尾，至實至虛，制定而清濁各歸其墟，赫然大制而已矣。雖然，不得已而求其用，則雌也，黑也，辱也，執其權以老天下之器也。",
    29: "天下在我，吾何取？我在天下，吾何為，天下如我，吾何欲？我如天下，吾何執？以我測天下，天下神。以天下遇我，天下不神。不神者使其神，而天下亂。神者使其不神，而我安。故窮天下以八數，而去我之三死，則炎火焚林而可待其寒，巨浸滔天而可視其暵。水火失其威，金石喪其守，況有情之必窮而有氣之必縮者哉？",
    30: "最下用兵以殺，其上用兵以生。夫以生生者且贅，而況殺生乎？人未嘗不生，而我何勸？又況夫功之門為害之府也，人未嘗不生，不能聽其生；物未嘗不殺，不能恃其殺。須臾之不忍，而自命為果，不已誣乎？故善禁暴者，俟其消，不摧其息；善治情者，塞其息，不強其消；善貴生者，持其消息之間，不犯其消息之衝；雖有患，不至於早已。",
    31: "與其悲之於後，何如忘之於先；與其以凶禮居功，何如以吉道處無功之地。不能先機，不能擇吉，不能因間以有餘，所謂「彼惡知禮意」者也。",
    32: "因於大始者無名，止於己然者有名。然既有名而能止之，則前名成而後名猶不立，過此以往，仍可為大始。天地，質也；甘露，沖也；升於地而地不居功，降自天而天不終有，是既止以後之自然，且莫令而自均，後天之衝，合於先天，況夫未始有夫有止者乎？",
    33: "以氣輔氣，以精輔精，自謂「不失其所」，而終歸於敝，豈但單豹之喪外，張毅之喪內哉？蓋智揣力特以奔其志，有「所」而不能因自然之」所」於無所失也。夫見其精氣之非有餘，可謂之死；而其中之婉如處女縈如流雲者、微妙玄通者未嘗亡也。非真用其微明，以屈伸於沖和之至，若抱而不離者，何足以與於斯哉？故有虞氏之法久，而泰氏之道壽；中士之算長，而有道者之生無極；言此者，以紀重玄之績也。",
    34: "誰能以生恩天地乎，則誰能以死怨天地。天地者，與物為往來而聊以自壽也。天地且然，而況於道？荒荒乎其未有畔也，脈脈乎其有以通也；故東西無方，功名無繫，賓主無適，己生貴而物生不逆。誠然，則不見可欲，非以窒欲也；迭與為主，非以辭主也。彼亟欲成其大者，惡足以知之！",
    35: "蛇之制在項，人之制在限。繫其項，則廢其螫；」艮其限」，則「列其夤」矣。其象甚微，制之甚大。故清虛者物之湊，而重濁者物之司也。不棄其司，不奔其湊；於空得實，於實得空；扼其重濁，以致其清虛。嘗試念之：樂作餌熟，則雖有遄行之客，而游情以止，非以其歸於情耶？所謂「常有欲以觀其徼」也。然項之與限，非有情者也。無情者不可強納有情以為之主，則衝淡晦寂而用無方，斯亦無欲之至矣。始乎重濁，反乎清虛；得乎清虛，順乎重濁；有欲無欲，而常者未有變焉；斯執大象者之所獨得與！",
    36: "函道可以自適，抱道可以自存，其如魚之自遂於淵乎！有倚有名，唯恐不示人，則道滯而天下測其窮。無門無毒，物望我於此而已。不以此應之，則天下其無如我何矣。無如我何，而天下奚往？是故天下死於道，而遭常生天下，用此器也。",
    37: "藏樸者，終古而有器之用；見樸者，用極於器而止矣。故無名與有名為侶，而非能無也。畏其用而與有名為侶，故並去其欲。嬰城以守國者，不邀折衝之功；閉閣以守身者，不為感帨之拒；知物之本正，而不敢正之以化也。其為道也，測之於重玄而反淺、闓之於妙門而反深。以為無用，而有用居然矣；以為有用，而無用居然矣。終日散而未始不盈，徽息通而蠕然似有。兩壘立而善守其間，兩端馳而善俟其反，則樸又何足言，而玄又何足以盡之哉？",
    38: "虎豹之行，進而前，則不能顧其卻。新木之植，盛其華，則不能固其根。然不能無所前矣，無已，其以樸者前乎！前者犯難，卻者觀變。以犯難者，敦重而不驚；以觀變者，因勢而徐辨。故不以識之銳抵天下之巇。何也？以失主樂取夫美名而暱之，以背眾美之涵也，是德、仁、義、禮之可名而不常者也。故出而逾華，反而逾薄。唯先戒其前者，為能不德而德，無為以為。嚴君平云：「至至而一不存。」豈不存哉？誠無以存之。",
    39: "愚者仍乎「一」，而不能「以」；智者日「以」之，而不能「一」。「以」者失「一」也，不「一」者無「以」也。「一」含萬，入萬而不與萬為對。「以」無事，有事而不與事為麗。而況可邀，而況可執乎？是以酒熟而酤者至，舍葺而行者休。我不「得一」，而姑守其濁，以為之筐橐，而後「一」可「致」而不拒。夫貴賤高下之與「一」均，豈有當哉？乃貴高者功名之府，而賤下者未有成也。功立而不相兼，名定而不相通，則萬且不盡，而況於「一」？故天地之理虧，而王侯之道喪。以大「輿」載天下者，知所取舍久矣。",
    40: "流而或盈，滿而或止，則死而為器。人知器之適用，而不知其死於器也。若夫道．含萬物而入萬物，方往方來，方來方往，蜿蟺希微，固不窮已。乃當其排之而來則有，當其引之而去，則託於無以生有，而可名為無。故於其「反」觀之，乃可得而覿也。其子為光，其孫為水，固欲體其用也實難。夫迎來以強，息往以弱，致「用」於「動」，不得健有所據，以窒生機之往來；故用常在「弱」，而道乃可得而「用」也。「動」者之生，天之事。「用」者之生，人之事。天法道，人法天，而何有於彊？然而知道體之本動者鮮矣。唯知「動」則知」反」，知「反」則知「弱」。",
    41: "有善貸者於此，則人將告貸焉，而彼非執物以賜之也。夫道，亦若是而已矣；然我未見物之告貸於道也。何也？物與道為體，而物即道也。物有來有往，有生有反，日飲於道，而究歸於未嘗或潤；日燭於道，而要反於未之有明。無潤無明，物之小成；不耀不流，道用自極。故欲勤，而莫致其力；欲行，而不見其功。蓋「昧」、「退」、「辱」、「偷」之名，非虛加之也。然而受之不辭者，且得不謂之上士乎？",
    42: "當其為道也，函「三」以為「一」，則生之盛者不可窺，而其極至少。當其為生也，始之以「衝氣」，而終之以「陰陽」。陰陽立矣，生之事繁，而生之理亦竭矣。又況就陰陽之情才，順其清以貪於得天，順其濁以堅於得地，旦吸夕餐，嘔酌充悶以炫多，而非是則惡之以為少，方且陰死於濁，陽死於清，而詎得所謂「和」者而仿佛之乎？又況超於「和」以生「和」者乎？有鑒於此，而後知無已而保其少，「損」少致「和」，損「和」得「一」。夫得「一」者無「一」，致「和」者無致。散其黨，游其宮，陰陽在我，而不叛其宗，則「益」之最盛，何以加哉！",
    43: "適燕者北馳，適粵者南騁；而無適之駕，則常得其夷而無所阻，轢踐百為而無所牾。以觹解者，不能解不糾之結；以斧析者，不能析無理之薪。苟知實之有虛，因而襲之，則祈距萬變，而我志無不得。夫炫其「堅」而脩備，測其「間」而抵隙音多矣，道之所以終隱於「可道」也。",
    44: "所謂至人者，豈果其距物以孤處哉？而坐視其變，知我之終無如物何，而物亦終無如我何也。故「辱」有自來，而「辱」或無自來；」殆」有自召，而「殆」或不召而至。然而以「身」捷得其眚而受其「名」，則不如無居之為愈也。故謂之善愛「名」而善居「貨」，善襲「得」而善遣「亡」。「得」之於「身」，聽然以消陰陽之沴；得之於天下，泮然以斃虎兕之威。",
    45: "陰陽交而人事煩，人事煩而功名著。故喜於有為者，其物之盈而往附之。已盈而往附焉，必損於己，遂思以勝之；我見其寒而趨火，熱而飲冰，徒自困也。彼豈樂有此患哉？始亦以附彼者之易於求盈，而不知其至此也。而早嗇於己，不驚於物，則陰陽方長，而不附之以為功名。始於不依，終於不競，天下正矣，而我若未有功。故貌見不足，而實享其有餘。誠享矣，而又奚恤於貌之不足？",
    46: "禍發於方寸，福隱於無名。一機之動如蟻穿，而萬殺之爭如河決。故有道者，不為福先，而天下無禍。豈強窒之哉？明於陰陽之亢害，而樂遊於大同之圃，安能以己之已知，犯物之必害者乎？",
    47: "道盈於向背之間。有所向，斯有所背矣。無所向，無所背，可名之中。乃使人貿貿然終日求中而不得，為天下笑。無已，姑試而反之。反非中也．而漸見其際。有欻乎，如光之投隙；有約乎，如絲之就絡。物授我知而我不勤，乃知昔之逐亡子而追奔馬者，勞而愚矣。非然，則天下豈有「不行而知，不見而名，不為而成」者哉？",
    48: "損於有者，益於無。去其所取，全其未有取。未有取，則未有失。故賓百為，而天下來賓。猶且詹詹然以前識之得為墨守，則日見益而所失者積矣。故月取明於日，明日生而真月日死。安能舍此無盡藏，以取恩於天下之耳目哉？夫天下無窮，取者恩而失者怨，取者得而失者喪，此上禮之不免於攘臂，而致數輿之無輿也。",
    49: "即有聖人，豈能使天下之皆孩邪？一生二而有陰陽，有陰陽而有性情，有性隋而有是非。夫性情之凝滯以幹陰陽之肖者而執之，將遂以為常乎？常於此者，不常於彼矣。唯執大常以無所常，故恣陽亢陰凝之極，而百姓可坐待其及，我為焦土，百姓為灌潦；我為和風，百姓為笙竽。有漬而不受，有聲而不留，則善之來投，若稚子學語於翁嫗之側，而況夫不善之注耳目者乎？嗚呼！天下之有目而注者多矣，與之為目者，則亦注也。聖人不為目，而天下自此孩矣。",
    50: "有死地，無生地。無地為生，有地為死。試效言之矣。人之生也，神舍空而即用，形拔實以營虛，非其出乎？迨氣與空為宅，形與壤為質．則死者非其入乎？雖然，既有生矣，遂以其出者為可繼也，引緒旁生，據地而游，則死固死於靜．生亦死於動。死於動者，能不靜，而不能靜於動也。靜於動，則動於靜，動靜兩用而兩不用。靜於動，則動可名為靜；可名為靜，靜亦樂得而歸之；所謂「守靜篤」者此也。動於靜，則靜可名為動；可名為動，靜與周旋而不死；所謂「反者道之動」者此也。故有地者三，無地以為地者三，鶩於地不地而究以得地者三。此自九而外，一之妙所難言與！然而攝生者其用在動，之死者其用亦動。何以效之？攝生者以得地為憂，動而離之。之死者以不得地為憂，動而即之。彼雖日往還於出入之間，而又惡知動哉？則甚矣，地之可畏也！兕虎之攫，必按地以為威；甲兵之殺，必爭地以制勝。遇無地者，則皆廢然而喪其殺機。殺不在彼，死去於我，御風音所以泠然善，雲將所以暢言遊也。",
    51: "道既已生矣，而我何生？道既已畜，且覆之矣，而我何為？而我何長？鄰之人炊其囷粟以自飽，施施然曰我食之，夫誰信哉？乃彼未嘗食於我．而未嘗不食於此也。我唯灼而知之，順而襲之，天下不相知而德我，我姑不得已而德之。物者形矣，勢者成矣。雖灼知之，不名言之；雖順襲之，不易置之；雖德我者不相知，終古而信之；亦可因萬物之不相知也，而謂之玄德矣。",
    52: "言「始」者有三：君子之言始、言其主持也；釋氏之言始，言其涵合也；此之言「始」，言其生動也。夫生動者氣，而非徒氣也。但以氣，則方其生動於彼，而此已枵然矣。盈於彼，不虛於此；先天地生，而即後天地死；其息極微，用之無迹。小且無所執，而況於大？弱且不必「用」，而況於「彊」？將孰從而致吾「見」與「守」乎？故方其「守」而「知」，「知」之在「守」；方其「知」而「守」，」守」之在「知」。生息無窮，機漾於渺。欲執之而已逝矣，欲審之而已遷矣，欻忽蕭散，何所為「常」？於其不「常」，而陰尸其「常」，豈複在「子」」母」之涯涘邪？不然，以己之知與力，有涯之用，追隨「子」」母」之變，末見其免於殃也。",
    53: "天下不勝「知」也。「知」而「施」之，則物之情狀死於己之耳目，而耳目亦將死於情狀矣。然則將去知乎？而知亦無容去也。有知者，有使找知者。知者自謂久知，而使我知者用其「介然」而已。知「介然」之靡常，則己無留好。己無留好，而天下不羨其留，雖施不足畏，而況於知？俄頃之光，而終身之據；已尚之物，亦從而尚之。莽、操之奉堯、舜為竽，黃巾、赤眉之奉湯、武為竽，與陰陽之沴奉凝滯之衝氣以為竽而盜其生等也。道之不可以「介然」行也，如斯夫！",
    54: "以己與天下國家立，則分而為朋矣。彼朋「建」，則此朋「拔」；彼朋「抱」，則此朋「脫」。然而有道者，豈能強齊而並施之哉？事各有彤，情各有狀，因而觀之，可以無爭矣。而流動於情狀之中，因其無可因，以使之自因者，所謂「知之以此」也。方且無「身」，而身何「觀」？方且無鄉、邦、天下，而我又何「觀」？方且無之，故方且有之。析於所自然，而摶於所不得已，則匪特「朋亡」，而己物相見之真，液化脈函，固結以壽於無窮，是謂「死而不亡」。",
    55: "以一己受天下之無涯，不給矣。憂其不給，將奔心馳氣，內爭而外渝。然且立德以為德，吐為外景，而不知中之未有明也。含而比於赤子者，德不立德；德不立德，而取舍無跡；無跡則「和」。不立德以為德，則陰陽歸一，陰陽歸一則「精」。如是者，大富不資，大勁不折，而猶有「使氣」「益生」之患乎？故閉之戶牖，無有六合；守之酣寢，無有風雷；至人無涯之化，赤子無情之效也。",
    56: "夫將同其所同，則亦異其所異。同者我貴之，而或賤之；異者我賤之，而或貴之，何也？以我之貴，知或之賤；以我之賤，知或之貴也。唯不犯物者，物亦不犯我。非不犯也、物固莫能犯之也。因而靡之，坐而老之，使明如列炬，暗如窌土，銳如干將，紛如亂絲，一聽其是非之無極，終不爭同己以為貴，乃冒天下之上，以視天下短長之命。玄乎！玄乎！而何言之足建乎？",
    57: "天下有所不治，及其治之，非「正」不為功。以「正」正其不正，惡知正者之固將不正邪？故「正」必至於「奇」，而治國必至於「用兵」。夫無事者，正所正而我不治，則雖有欲為奇者，以無猜而自阻，我乃得坐而取之。彼多動多事者則不然，曰「治者物之當然，而用兵者我之不得已也」。方與天下共居其安平之富，而曰不得已，是誰詒之戚哉？故無名無器，無器無利，無利無巧，無巧則法無所試。故欲弭兵者先去治。",
    58: "果其無「正」耶，則聖人何不並「方」「廉」「直」「光」而去之，去者必矯，今之矯，後之所矯也。弓之張也弣外，則其弛也弣內。然則天下遂無一或可者與？聖人知其無正，則亦知其無奇，而常循其沖。「人之所畏，不敢不畏」，則善人不能操名以相責。「天下注目，我皆孩之」，則不善人不能立壘以來爭，是故遠「割」「劌」「肆」「耀」之傷，而作「方」「廉」「直」「光」之保，則氣數失其善妖，而奇正忘於名實。不然，避禍而求福於容，容亦迷而速其妖爾。",
    59: "「人」之情無盡，取而「治」之，則不及情者多矣，「天」之數無極，往而「事」之，則無可極者遠矣。以其敝敝，從其浩浩，此冀彼之恩，而彼冀望此以為怨。怨不可以有國，而敝敝窮年，亦「根」敗「柢」枯，而其」生」不延。迨其不延，悔而思「服」，豈不晚與！守之圜中，鮮所「治」，鮮所「事」。情萬而情情者一，數萬而數數者並一不存。或疑其吝而不德，而不德之德，天人無所邀望於始，則亦無所怨恫於終。而批卻導窾，數給不窮者，寧有訖乎？故牡之觸有窮，而牝之受無所止。「重積德」者，天下歆其受而歸我，席虛以講天下，此「有國」之與「長久」兩難並者，而並之於此。並之於此，則豈有不并於此者哉？",
    60: "動天下之形，猶餘其氣；動天下之氣，動無餘矣。「烹小鮮」而撓之，未嘗傷小鮮也，而氣已傷矣。傷其氣，氣遂逆起而報之。夫天下有「鬼神」，揉治亂於無形；吾身有「鬼神」，燥生死於無形。殺機一動，龍蛇起陸，而生德戕焉。靜則無，動則有，神則「傷人」，可畏哉！「載營魄抱一而不離」，與相保於水之未波。豈有以治天下哉？「蒞」之而已。",
    61: "道莫妙於受。受而動，是名受而實不受也。欲受而動，是實受而名不受也。天下相報以實，而相爭以名，陰陽之於人固然，況人事乎？語其極，則欲「兼畜人」，非能畜人；欲「入事人」，非能事人。何也？實元動也，況欲之而又不能靜乎？愈大則愈可受。人能為陰陽之歸，其處下尤甚。靜其欲，靜其動，江海之所以為百谷王也。",
    62: "繇此驗之，則有道者不必無求，而亦未嘗諱罪耶？無求則亢，諱罪則易污，有道者不處。天下皆在道之中，善不善者其化跡，而道其橐籥。是故無所擇，而聊以之深其息。知有所擇也，是天子三公之為貴，而拱璧駟馬之為文矣，豈道也哉？時有所求，終不懷寶以自封；或欲免罪，終不失保以孤立。和是非而休之以天鈞，天下皆同乎道，而孰能賤之？",
    63: "憤興長養者，人之所見「大」也。恩怨酬酢者，人之所見「難」也。秋脫之葉，春之所榮；重雲之屯，雨之所消；非果為「大」而為「難」，審矣。道其猶水乎！微出於險，昌流非盈。盈，循末而見其盈，不知其始之有以持之也。如是，則聖人勞矣乎！而能不勞者，託於無也。無「大」則若「細」，無「易」則若「難」，保其無而無往不得。所難者，保無而已矣。",
    64: "失有道者，不為吉先，不為福贅。「未有」、「未亂」而逆治，其事近迎。「幾成」而「慎」有餘，其事近隨。迎隨之非道，久矣，非以其數數於往來而中敝邪？孰知夫往者之方來，而來者之方往也？又孰知夫往者之未嘗往，而來者之來嘗來也？戒其隨，始若迎之；戒其迎，始若隨之。又孰知夫迎隨之可避，而避迎隨之亦可戒也？或敝或避，因物者也。兼而戒之，從事其易者，因道者也。因物者不常，因道者致一。一無所倚，迎幾「早服」，此以「恃萬物主自然而不為」。",
    65: "順之則與天下相生，「反」之則與吾相守。生者，生智，生不智；生福，生禍；生德，生賊；莫必其生，而順亦不長也。守者，吾守吾，天下守天下，而不相詔也。夫道之使有是天下也，天下不吾，而吾不天下，久矣「楷式」如斯，而未有易也。仿其「楷」，多其甕缶而土裂於邱；學其「式」，多其觚豆而木落於山，天下其為我之甕缶與其觚豆乎？彼且不甘而怨賊起矣。物欲出生，我止其芽，則天下全其膏潤。心欲出生，我止其幾，則魂魄全其常明：非故「愚之」也，「以明」者非其明也。",
    66: "未易下，尤未易「善下」，故天下之為江誨者鮮矣：將欲抑之，而激之必亢；將欲浚之，而祗以不平。而不但此也。獨立而為物所歸，則積之必厚；積厚而無所輸，則欲抑之、浚之而不能。故唯江海者，「善下」者也。江則有海，海則有尾閭。聖人有善，則過而不留。受天下之歸而自不饜，天下亦孰得而厭之？故返息於踵，返踵於天，照之以自然，而推移其宿氣，乃入於」寥天一」。",
    67: "曰蠶「肖」蠋，不能謂蠋之即蠶也。曰蠶「肖」蠶，不能謂此蠶之即彼蠶也。求名不得，而舉其「肖」，然且不可，況欲執我以求「肖」乎？終日「慈」，而非以「肖」仁；終日「儉」，而非以「肖」禮；終日「後」，而非以「肖」智。善無近名，名固不可得而近矣。無已，遠其刑而居於無迹，猶賢於「肖」迹以失真乎！不然，「天將救之，以慈衛之」；苻堅不忍於慕容，而不救其死，非以其求「肖」也哉？",
    68: "避殺者不可為，猶之樂殺者不可長也。或以有所樂，或以有所避，皆謂生殺之在己而操縱之，是謂竊天。不致其樂，避於何庸？故「以正治國」者，將以弭兵而兵愈起；「善為士」者，可以用兵而兵不傷。知天之化迹，有露雷而無喜怒；知古之「楷式」，有消長而無殺生，有道者之善用人，豈立我以用人哉？人已然而因用之也。",
    69: "居道之宮，非「主」非「客」；乘道之機，亦「進」亦「退」。而「主」不知「客」，「客」能知「主」，繇其相知，因以測非「主」非「客」之用；「進」無「退」地，「退」有「進」地，因其餘地，遂以襲亦「進」亦「退」之妙。「主客」之間有宮焉，「進退」之外有用焉。「無行」、「無臂」、「無敵」、」無兵」者，如斯也。遠死地而致「微明」，不「勝」其何俟焉？欲猝得此機而不能，將如之何？無亦姑反其勢而用其情乎！以「哀」行其「不得已」，所以斂吾怒而不喪吾「三寶」也。",
    70: "大喧生於大寂，大生肇於無生。乘其喧而和之，不勝和也。逐其化而育之，不勝育也。唇吹竽，則指不能拊瑟；仰承蟬，則俯不能掇螬。故天下之言，為唇為指；天下之事，為承為掇。逐逐其難而終不遇，乃枵然以自侈其知之多，豈有能知我者哉？我之自居於「希」也，天下能勿「希」乎？故大谷無纖音，而大化無乳字。謝其喧而不敏於化，蓋披褐以樂居其「易」，而懷玉以潛襲其「希」也。",
    71: "府天下以勞我，唯其知我；官我以割天下，唯其知天下。夫豈特天下之不勝知？而知者，亦將倚畔際而失遷流。故聖人於牛忘耜，於馬忘駕，於原忘田，於材忘器，悶悶於己而不見其府，悶悶於天下而無以為官。若夫制萬族之宇而效百骸之位，已有前我而市其餘知者，方敩之以為勞，而苦其多遺，沉浮新知，以遁故器，而曾莫之病乎？",
    72: "侈於有者窮於無，填其虛者增其實，將舉手流目而無往非「狹」也，亦舉手流目而無住非「厭」也。有「居」者，有居「居」者。有「生」者，有生「生」者。居「居」者浹於「居」之裏，澒洞盤旋，廣於天地。生「生」者保其「生」之和，婉嫕蕭散，樂於春臺。而自棄其樂，自塞其廣，悲哉！屏營終夕，不自聊而求助於「威」也。是故去「見」則不廣而廣，去「貴」則樂不以樂。日游於澹遠，以釋無窮，恢乎有餘，充乎有適。忘天下而不為累，天下亦將忘之。蓋居「居」而生「生」者，天下之固有也，而我奚「見」而奚「貴」乎？",
    73: "執「不敢」以「勇」，「敢」矣；「不敢」其所「不敢」，「勇」矣。「勇」「敢」之施，「殺」「活」之報，天乘其權，而我受其變，「難」矣。聖人畏其「難」，而承其「活」，不辭其「殺」，故「活」在己而「殺」任天下。何也？以己受」活」，則必有受「殺」者，氣數之固然，而不足詰也。夫唯已「活」而非以功，天下「殺」而無能罪，斯以處勸罪之外，而善救人物，我無「殺」「活」而天下亦「活」。彼氣數者，日敝敝以「殺」「活」為勞，其於我也，吹劍首之吷而已矣。是以聖人破「天網」而行「天道」。",
    74: "木當其「斲」，豈有避其堅脆者哉？故盜跖、鮑焦相笑而無已時也。揀其所笑，以為或是或非，執秕糠以強人之所固不信，遂將乘人之死以驗己之得，而要之為利，則於殺有喜心，於殺有喜心者，於天下未有損，而徒自剝其和也。聖人知理勢之且然，故哀天而目擊夫化。化日遷而不得不聽，聽化而哀之也抑深矣。豈求以近仁名邪？近仁名者，是有司生者而代之生也。代之生，代之殺，皆愚也。聖人終不為愚，故似不肖。",
    75: "夫食稅者上，而飢者民；有為者上，而難治者民。彼此不相知而相因，誠有之矣。統吾之生而欲生之，無異養矣。孰知其不相知而相因也，肝膽之即為胡越乎？故同其異，則胡越肝膽也；異其同，則肝膽胡越也。於彼有此，於此有彼，彼此相成，而生死不相戾，豈能皆厚而莫知有輕哉？脈脈使其知，則筋骨血肉之皆虛，而衝虛無有之皆實。故曰：「衝而用之或不盈。」誠不盈矣，知得入之而不窒，奚其生之厚而死之輕也？",
    76: "彊弱者，迹也。夫豈木之欲生，而故為柔脆哉？天液不至而糟粕存，於是而堅枯之形成矣。故堅彊者，有之積也；柔弱者，無之化也。無之化，而尚足以生，況其未有化者乎？不得已而用其化以為柔弱，以其去無之未遠也。夫無其強者，則柔者不凝，天下之所以厚樹其質也。而孰知凝之即為死之徒乎？質雖固其已有而不可無，而用天地之衝相升降，則豈唯處上者之柔弱也，即其處下者而與枯槁遠矣。",
    77: "唯弓有「高」「下」，而後人得施其「抑」「舉」；唯人有「有餘」「不足」，而後天得施其「損」「補」。夫自損者固未嘗無損，而受天損者，其禍烈矣。聖人之能不禍於天者，無禍地也。夫豈但勞天下以自奉者為奉有餘哉？人未嘗不肖而欲賢之，人未嘗亂而欲治之，美譽來歸而腥聞贈物，非樂天下之敗以自成乎？故一人安位，天下失據；一日行志，百夫傷心；殺機發於誥誓，而戎馬生於勛名，然則庸人之自奉儉，而賢者之自奉奢，可不畏哉！",
    78: "無「攻」之力，有「攻」之心，則心鼓其力。無「攻」之心，有「攻」之力，則力蕩其心。心力交足以「攻」，則各乘其權，身以內各挾其戈矛以屢變；而欲以「攻」天下，能不瓦解者，未之有矣。雖然，莫心為甚。夫水者，豈欲以敵堅彊面為攻者哉？受天下之「垢」也，終古而無「易」心，而力從之。何也？水之無力，均其無心；水之無心，均其無力也。故「弱其志」者無「易」志，「虛其心」者無「易」心，行乎其所不得已，而不知堅彊之與否，則險夷無易慮，無他，寓心於汗漫而內不自構也。寓心於汗漫，無所畏矣。內不自構，和之至矣。和於中，無畏於外，天下其孰能禦之！",
    79: "既不欲攻之，則從而「和」之，欲有為於天下者，舍二術無從矣。夫物本均也，而我何所通？物苟不通也，而我又何以均？無心無力，怨自不長。有心者心定而釋，有力者力窮而返。不待無所終而投我，而先就之以致均通之德，是益其怨而怨歸之矣。聖人知其然，陰愆陽忒之變，坐而消之，天固自定；靜躁寒熱之反，坐而勝之，身固自安；儒墨是非之爭，坐而照之，道固自一。無他，無所親斯無所疏，物求斯與，而己不授也。",
    80: "夫天下亦如是而已矣。以「寡小」觀「寡小」，以強大觀彊大，以天下觀天下，人同天，天同道，道同自然，又安往而不適者哉？推而准之四海之廣：賢貴「安其居」，而賤不肖「不來」，則賢貴定；賤不肖「安其居」，而賢貴「不往」，則賤不肖和。反而求之一身之內：耳目「安其居」，而心思「不往」，則耳目全；心思「安其居」，而耳目「不來」，則心思正。「抱一」者，抱其一而不徹其不一，乃以「玄同」於一，而無將迎之患。",
    81: "以所「有」「為人」，則人「有」而己損；以「多」「與人」，則人「多」而己貧。孰能知無所為者之「為人」邪？無所與者之「與人」邪？道散於天下，天下廣矣，故「不積」。道積於已，於是而有「美」，有「辯」，有「博」。既「美」且「辯」，益之以「博」，未有「不爭」者也。乃其於道之涯際，如勺水之於大海，揮之、飲之，而已窮。俯首而「為」，惡知昂首而「爭」？不問其「利」「利」自成，惡與「害」逢？能不以有涯測無涯者，亦無涯矣。「休之以天鈞」，奚「為」、奚「與」，又奚窮哉？"
}

# 憨山德清《老子道德经解》完整注解
HANSHANDEQING_NOTES = {
    1: "此章總言道之體用，及入道工夫也。老氏之學，盡在於此。其五千餘言，所敷演者，唯演此一章而已。所言道，乃真常之道。可道之道，猶言也。意謂真常之道，本無相無名，不可言說。凡可言者，則非真常之道矣，故非常道。且道本無名，今既強名曰道，是則凡可名者，皆假名耳，故非常名。此二句，言道之體也。然無相無名之道，其體至虛，天地皆從此中變化而出，故為天地之始。斯則無相無名之道體，全成有相有名之天地，而萬物盡從天地陰陽造化而生成。此所謂一生二，二生三，三生萬物，故為萬物之母。此二句，言道之用也。此下二句，乃入道之工夫。常，猶尋常也。欲，猶要也。老子謂，我尋常日用安心於無，要以觀其道之妙處。我尋常日用安心於有，要以觀其道之徼處。徼，猶邊際也。意謂全虛無之道體，既全成了有名之萬物。是則物物皆道之全體所在，正謂一物一太極。是則只在日用目前，事事物物上，就要見道之實際，所遇無往而非道之所在。故莊子曰，道在稊稗，道在屎尿。如此深觀，纔見道之妙處。此二觀字最要緊。此兩者同已下，乃釋疑顯妙。老子因上說觀無觀有，恐學人把有無二字看做兩邊，故釋之曰，此兩者同。意謂我觀無，不是單單觀無。以觀虛無體中，而含有造化生物之妙。我觀有，不是單單觀有。以觀萬物象上，而全是虛無妙道之理。是則有無並觀，同是一體，故曰，此兩者同。恐人又疑兩者既同，如何又立有無之名，故釋之曰，出而異名。意謂虛無道體，既生出有形天地萬物。而有不能生有，必因無以生有。無不自無，因有以顯無。此乃有無相生，故二名不一，故曰，出而異名。至此恐人又疑既是有無對待，則不成一體，如何謂之妙道，故釋之曰，同謂之玄。斯則天地同根，萬物一體。深觀至此，豈不妙哉。老子又恐學人工夫到此，不能滌除玄覽，故又遣之曰，玄之又玄。意謂雖是有無同觀，若不忘心忘跡，雖妙不妙。殊不知大道體中，不但絕有無之名，抑且離玄妙之跡，故曰，玄之又玄。工夫到此，忘懷泯物，無往而不妙，故曰，眾妙之門。斯乃造道之極也。似此一段工夫，豈可以區區文字者也之乎而盡之哉。此愚所謂須是靜工純熟，方見此中之妙耳。",
    2: "此釋前章可名非常名，以明世人居有為之跡，虛名不足尚。聖人處無為之道以御世，功不朽而真名常存之意也。意謂天下事物之理，若以大道而觀，本無美與不美，善與不善之跡。良由人不知道，而起分別取捨好尚之心，故有美惡之名耳。然天下之人，但知適己意者為美。殊不知在我以為美，自彼觀之，則又為不美矣。譬如西施顰美，東施愛而效之，其醜益甚。此所謂知美之為美，斯惡已。惡，醜也。又如比干，天下皆知為賢善也，紂執而殺之。後世效之以為忠，殺身而不悔。此所謂知善之為善，斯不善已。此皆尚名之過也。是則善惡之名，因對待而有。故名則有無相生，事則難易相成，物則長短相形，位則高下相傾，言則音聲相和，行則前後相隨，此乃必然之勢。譬如世人以尺為長，以寸為短。假若積寸多於尺，則又名寸為長，而尺為短矣。凡物皆然，斯皆有為之跡耳。凡可名者，皆可去。此所謂名可名，非常名也。是以聖人知虛名之不足尚，故處無為之道以應事。知多言之不可用，故行不言之教以化民。如天地以無心而生物，即萬物皆往資焉，不以物多而故辭。雖生成萬物，而不以萬物為己有。雖能生物，而不自恃其能。且四時推移，雖有成物之功，功成而不居。夫惟不居其功，故至功不朽。不尚其名，故真名常存。聖人處無為之道，亦由是也。蓋萬物作焉已下，皆是說天地之德，以比聖人之德。文意雙關，莊子釋此意極多。",
    3: "此言世人競有為之跡，尚名好利嗜欲之害，教君人者治之之方。以釋上章處無為之事，行不言之教之實效也。蓋尚賢，好名也。名，爭之端也。故曰爭名於朝。若上不好名，則民自然不爭。貴難得之貨，好利也。利，盜之招也。若上不好利，則民自然不為盜。故曰苟子之不欲，雖賞之不竊。所以好名好利者，因見名利之可欲也，故動亂其心以爭競之。若在上者苟不見名利有可欲，則民亦各安其志，而心不亂矣。故曰不見可欲，使心不亂。然利，假物也。人以隋珠為重寶，以之投雀，則飛而去之。色，妖態也。人以西施為美色，麋鹿則見而驟之。名，虛聲也。人以崇高為貴名，許由則避而遠之。食，爽味也。人以太牢為珍羞，海鳥則觴而悲之。是則財色名食，本無可欲。而人欲之者，蓋由人心妄想思慮之過也。是以聖人之治，教人先斷妄想思慮之心，此則拔本塞源，故曰虛其心。然後使民安飽自足，心無外慕，故曰實其腹。然而人心剛強好爭者，蓋因外物誘之，而起奔競之志也。故小人雞鳴而起，孳孳為利，君子雞鳴而起，孳孳為名，此強志也。然民既安飽自足，而在上者則以清淨自正。不可以聲色貨利外誘民心，則民自絕貪求，不起奔競之志，其志自弱，故曰弱其志。民既無求，則使之以鑿井而飲，耕田而食，自食其力，故曰強其骨。如此則常使民不識不知，而全不知聲色貨利之可欲，而自然無欲矣。故曰常使民無知無欲。縱然間有一二黠滑之徒，雖知功利之可欲，亦不敢有妄為攘奪之心矣，故曰使夫知者不敢為也。如上所言，乃不言之教，無為之事也。人君苟能體此而行以治天下，則天下無不治者矣。故結之曰，為無為，則無不治。老子文法極古，然察其微意，蓋多述古。或述其行事，或述其文辭，似此為無為則無不治，乃述上古聖人之行事者。至若是謂等語，皆引古語以證今意，或以己意而釋古語者。且其文法機軸，全在結句，是一篇主意。蓋結句，即題目也。讀者知此，則思過半矣。至其句法，有一字一句，二字一句，三字一句者極多。人不知此，都連牽讀去，不但不得老子立言之妙。而亦不知文章之妙也。",
    4: "此讚道之體用微妙，而不可測知也。沖，虛也。盈，充滿也。淵，靜深不動也。宗，猶依歸也。謂道體至虛，其實充滿天地萬物。但無形而不可見，故曰用之或不盈。道體淵深寂漠，其實能發育萬物，而為萬物所依歸。但生而不有，為而不宰，故曰似萬物之宗。或，似，皆不定之辭。老子恐人將言語為實，不肯離言體道，故以此等疑辭以遣其執耳。銳，即剛勇精銳。謂人剛銳之志，勇銳之氣，精銳之智，此皆無物可挫。唯有道者能挫之，故曰挫其銳。如子房之博浪，其剛勇可知。大索天下而不得，其精銳可知。此其無可挫之者，唯見挫於圯上老人一草履耳。由子房得此而進之於漢，卒以無事取天下。吾意自莊周以下，而功名之士，得老氏之精者，唯子房一人而已。以此較之，周善體而良善用，方朔得之，則流為詭矣。其他何足以知之。紛，謂是非紛擾。即百氏眾口之辯也。然各是其是，各非其非，此皆無人解之者。唯有道者，以不言之辯而解之。所謂大辯若訥。以道本無言，而是非自泯，故曰解其紛。和，混融也。光，智識衒耀於外。即所謂飾智驚愚，修身明汙者，是也。唯有道者，韜光內照，光而不耀。所謂眾人昭昭，我獨若昏。眾人察察，我獨悶悶。故曰和其光。與俗混一而不分。正謂呼我以牛，以牛應之。呼我以馬，以馬應之。故曰同其塵。然其道妙用如此，變化無方。而其體則湛然不動，雖用而無跡。故曰湛兮或存。要妙如此，而不知其所從來。故曰吾不知誰之子。且而不是有形之物，或象帝之先耶。帝，即天帝。象，或似也。愚謂此章讚道體用之妙，且兼人而釋者。蓋老子凡言道妙，全是述自己胸中受用境界。故愚亦兼人而解之。欲學者知此，可以體認做工夫。方見老子妙處。宇宇皆有指歸，庶不肖虛無孟浪之談也。",
    5: "此言天地之道，以無心而成物。聖人之道，以忘言而體玄也。仁，好生愛物之心。芻狗，乃縛芻為狗，以用祭祀者。且天地聖人，皆有好生愛物之仁。而今言不仁者，謂天地雖是生育萬物，不是有心要生。蓋由一氣當生，不得不生。故雖生而不有。譬如芻狗，本無用之物。而祭者當用，不得不用。雖用而本非有也。故曰天地不仁，以萬物為芻狗。聖人雖是愛養百姓，不是有心要愛。蓋由同體當愛，不得不愛。雖愛而無心。譬如芻狗，雖虛假之物。而尸之者當重，不得不重。雖重而知終無用也。故曰聖人不仁，以百姓為芻狗。猶，似也。橐，即皮韝。乃鼓風鑄物之器。籥，即管籥。乃承氣出音之器。屈，枉己從人之意。動，猶感觸也。謂橐籥二物，其體至虛而有用，未嘗恃巧而好為。故用不為伸，不用則虛以自處，置之而亦不自以為屈，故曰虛而不屈。且人不用則已。若用之，則觸動其機，任其造作而不休，故曰動而愈出。然道在天地，則生生而不已。道在聖人，則既已為人己愈有，既已與人己愈多。大道之妙如此。惜乎談道者，不知虛無自然之妙。方且眾口之辯說，說而不休，去道轉遠，故曰多言數窮。不若忘言以體玄，故曰不若守中。蓋守中，即進道之功夫也。",
    6: "此言道體常存，以釋上章虛而不屈，動而愈出之意也。谷，虛而能應者。以譬道體至虛，靈妙而不可測，亙古今而長存，故曰谷神不死。且能生天生地，萬物生生而不已，故曰是謂玄牝。牝，物之雌者。即所謂萬物之母也。門，即出入之樞機。謂道為樞機，萬物皆出於機，入於機。故曰玄牝之門，是謂天地根。綿，幽綿不絕之意。謂此道體至幽至微，綿綿而不絕，故曰若存。愈動而愈出，用之不竭，故曰不勤。凡有心要作，謂之勤。蓋道體至虛，無心而應用，故不勤耳。",
    7: "此言天地以不生故長生，以比聖人忘身故身存也。意謂世人各圖一己之私，以為長久計。殊不知有我之私者，皆不能長久也。何物長久，唯天地長久。然天地所以長久者，以其不自私其生，故能長生。其次則聖人長久，是以聖人體天地之德，不私其身以先人，故人樂推而不厭。故曰後其身而身先。聖人不愛身以喪道，故身死而道存。道存則千古如生，即身存也。故曰外其身而身存。老子言此，乃審問之曰，此豈不是聖人以無私而返成其私耶。且世人營營為一身之謀，欲作千秋之計者，身死而名滅。是雖私，不能成其私，何長久之有。",
    8: "此言不爭之德，無往而不善也。上，最上。謂謙虛不爭之德最為上善，譬如水也，故曰上善若水。水之善，妙在利萬物而不爭。不爭，謂隨方就圓，無可不可，唯處於下。然世人皆好高而惡下。唯聖人處之。故曰處眾人之所惡，故幾於道。幾，近也。由聖人處謙下不爭之德，故無往而不善。居則止於至善，故曰善地。心則淵靜深默，無往而不定，故曰善淵。與，猶相與。謂與物相與，無往而非仁愛之心，故曰與善仁。言無不誠，故曰善信。為政不爭，則行其所無事，故曰善治。為事不爭，則事無不理，故曰善能。不爭，則用捨隨時，迫不得已而後動，故曰善時。不爭之德如此，則無人怨，無鬼責。故曰夫惟不爭，故無尤矣。",
    9: "此言知進而不知退者之害，誡人當知止可也。持而盈之不如其已者，謂世人自恃有持滿之術，故貪位慕祿進進而不已。老子意謂雖是能持，不若放下休歇為高，故不如其已。倘一旦禍及其身，悔之不及。即若李斯臨刑，顧謂其子曰，吾欲與若復牽黃犬，出上蔡東門逐狡兔，豈可得乎。此蓋恃善持其盈而不已者之驗也。故云知足常足，終身不辱，知止常止，終身不恥，此之謂也。揣而銳之，不可長保者。揣，揣摩。銳，精其智思。如蘇張善揣摩之術者是也。謂世人以智巧自處，恃其善於揣摩，而更益其精銳之思，用智以取功名，進進而不已。老子謂雖是善能揣摩，畢竟不可長保。如蘇張縱橫之術，彼此相詐，不旋踵而身死名滅，此蓋揣銳之驗也。如此不知止足之人，貪心無厭。縱得金玉滿堂，而身死財散，故曰莫之能守。縱然位極人臣，而驕泰以取禍，乃自遺其咎。此蓋知進不知退者之害也。人殊不知天道惡盈而好謙。獨不見四時乎，成功者退。人若功成名遂而身退，此乃得天之道也。",
    10: "此章教人以造道之方，必至忘知絕跡，然後方契玄妙之德也。載，乘也。營，舊註為魂。楚辭云，魂識路之營營，蓋營營，猶言惺惺，擾動貌。然魂動而魄靜，人乘此魂魄而有思慮妄想之心者。故動則乘魂，營營而亂想。靜則乘魄，昧昧而昏沈。是皆不能抱一也。故楞嚴曰，精神魂魄，遞相離合，是也。今抱一者，謂魂魄兩載，使合而不離也。魂與魄合，則動而常靜，雖惺惺而不亂想。魄與魂合，則靜而常動，雖寂寂而不昏沈。道若如此，常常抱一而不離，則動靜不異，寤寐一如。老子審問學者做工夫能如此。乎者，責問之辭。專氣致柔。專，如專城之專。謂制也。然人賴氣而有生。以妄有緣氣，於中積聚，假名為心。氣隨心行，故心妄動則氣益剛。氣剛而心益動。所謂氣壹則動志。學道工夫，先制其氣不使妄動以薰心，制其心不使妄動以鼓氣，心靜而氣自調柔。工夫到此，則怒出於不怒矣。如嬰兒號而不嗄也。故老子審問其人之工夫能如此乎。滌除玄覽。玄覽者，謂前抱一專氣工夫，做到純熟，自得玄妙之境也。若將此境覽在胸中，執之而不化，則返為至道之病。只須將此亦須洗滌，淨盡無餘，以至於忘心絕跡，方為造道之極。老子審問能如此乎。此三句，乃入道工夫，得道之體也。老子意謂道體雖是精明，不知用上何如，若在用上無跡，方為道妙。故向下審問其用。然愛民治國，乃道之緒餘也。所謂道之真以治身，其緒餘土苴以為天下國家。故聖人有天下而不與。愛民治國，可無為而治。老子審問能無為乎。若不能無為，還是不能忘跡，雖妙而不妙也。天門，指天機而言。開闔，猶言出入應用之意。雌，物之陰者。蓋陽施而陰受，乃留藏之意。蓋門有虛通出入之意。而人心之虛靈，所以應事接物，莫不由此天機發動。蓋常人應物，由心不虛，凡事有所留藏，故心日茆塞。莊子謂室無空虛，則婦姑勃蹊。心無天遊，則六鑿相攘。此言心不虛也。然聖人用心如鏡，不將不迎，來無所粘，去無蹤跡。所謂應而不藏。此所謂天門開闔而無雌也。老子審問做工夫者能如此乎。明白四達，謂智無不燭也。然常人有智，則用智於外，衒耀見聞。聖人智包天地，而不自有其知。謂含光內照。故曰明白四達而無知。老子問人能如此乎。然而學道工夫做到如此，體用兩全，形神俱妙，可謂造道之極。其德至妙，可以合乎天地之德矣。且天地之德，生之畜之。雖生而不有，雖為而不恃，雖長而不宰，聖人之德如此，可謂玄妙之德矣。",
    11: "此言向世人但知有用之用，而不知無用之用也。意謂人人皆知車轂有用，而不知用在轂中一竅。人人皆知器之有用，而不知用在器中之虛。人人皆知室之有用，而不知用在室中之空。以此為譬，譬如天地有形也，人皆知天地有用，而不知用在虛無大道。亦似人之有形，而人皆知人有用，而不知用在虛靈無相之心。是知有雖有用，而實用在無也。然無不能自用，須賴有以濟之。故曰有之以為利，無之以為用。利，猶濟也。老氏之學，要即有以觀無。若即有以觀無，則雖有而不有。是謂道妙。此其宗也。",
    12: "此言物欲之害，教人離欲之行也。意謂人心本自虛明，而外之聲色飲食貨利，亦本無可欲。人以為可欲而貪愛之。故眼則流逸奔色，而失其正見，故盲。耳則流逸奔聲，而失其真聞，故聾。舌則流逸奔味，而失其真味，故爽。心則流逸奔境，而失其正定，故發狂。行則逐於貨利，而失其正操，故有妨。所謂利令智昏，是皆以物欲喪心，貪得而無厭者也。聖人知物欲之為害。雖居五欲之中，而修離欲之行，知量知足。如偃鼠飲河，不過實腹而已。不多貪求以縱耳目之觀也。諺語有之，羅綺千箱，不過一暖，食前方丈，不過一飽，其餘皆為榮觀而已。故云雖有榮觀，燕處超然，是以聖人為腹不為目。去貪欲之害，而修離欲之行，故去彼取此。",
    13: "此言名利之大害，教人重道忘身以袪累也。寵辱若驚者，望外之榮曰寵。謂世人皆以寵為榮，卻不知寵乃是辱。以其若驚。驚，心不安貌。貴大患若身者，崇高之位曰貴，即君相之位。謂世人皆以貴為樂，卻不知貴乃大患之若身。以身喻貴，謂身為苦本，貴為禍根，言必不可免也。此二句立定，向下徵而釋之曰，何謂寵是辱之若驚耶。寵為下，謂寵乃下賤之事耳。譬如僻倖之人，君愛之以為寵也。雖卮酒臠肉必賜之。非此，不見其為寵。及其賜也，必叩頭而噉之。將以為寵。彼無寵者，則傲然而立。以此較之，雖寵實乃辱之甚也。豈非下耶。故曰寵為下。且而未得之也，患得之。既得之也，患失之。是則競競得失於眉睫之間，其心未嘗暫自安。由此觀之，何榮之有。故曰得之若驚，失之若驚。此其所以寵是辱也。貴大患若身者，是以身之患，喻貴之患也。然身，乃眾患之本。既有此身，則飢寒病苦，死生大患，眾苦皆歸，必不可免。故曰吾所以有大患者，為吾有身。無身，則無患矣。故曰及吾無身，吾有何患。然位，乃禍之基也。既有此位，則是非交謫，冰炭攻心，眾毀齊至，內則殘生傷性以滅身，外則致寇招尤以取禍，必不可逃。故曰吾所以有大患者，為吾有貴。無貴，則無患矣。故曰貴大患若身。筆乘引王子搜，非惡為君也，惡為君之患也。蓋言貴為君人之患。莊子曰，千金重利，卿相尊位也。子獨不見郊祀之犧牛乎。養食之數歲，衣以文繡，以入太廟。當是之時，雖欲為狐豚，豈可得乎。斯言貴為卿相者之患。老子言苟知身為大患不可免。則知貴為大患，亦不可免也。然且世人不知貴為大患，返以為榮。愛身取貴，以致終身之累。皆非有道之所為也。唯有道者，不得已而臨蒞天下，不以為己顯。雖處其位，但思道濟蒼生，不以為己榮。此則貴為天下貴，非一己之貴。如此之人，乃可寄之以天下之任。然有道者，處崇高之位，雖愛其身，不是貪位慕祿以自保。實所謂衛生存身以行道。是則愛身，乃為天下愛其身，非私愛一己之身。如此之人，乃可託以天下之權。若以此為君，則無為而治。以此為臣，則功大名顯。故道為天下貴也。故日貴以身為天下，則可寄於天下。愛以身為天下，乃可託於天下。",
    14: "此言大道體虛，超乎聲色名相思議之表，聖人執此以御世也。夷，無色也。故視之不可見。希，無聲也。故聽之不可聞。微，無相也。故搏之不可得。搏，取之也。此三者，雖有此名，其實不可致詰。致詰，猶言思議。由其道體混融而不可分，故為一。其上日月不足以增其明，故不皦。皦，明也，其下幽暗不能以昏其禮，故不昧。繩繩，猶綿綿不絕之意。謂道體雖綿綿不絕，其實不可名言。畢竟至虛，雖生而不有，故復歸於無物。杳冥之內，而至精存焉，故曰無狀之狀。恍惚之中，而似有物焉，故曰無象之象，是謂惚恍。此正楞嚴所謂罔象虛無，微細精想耳。由其此體，前觀無始，故迎之不見其首。後觀無終，故隨之不見其後。此乃古始之道也。上皆歷言大道之妙，下言得道之人。然聖人所以為聖人者，蓋執此妙道以御世。故曰執古之道，以御今之有。吾人有能知此古始之道者，即是道統所係也。故曰能知古始，是謂道紀。紀，綱紀。謂統緒也。",
    15: "此言聖人體道深玄，故形神俱妙。人能靜定虛心，則故有常存也。莊子謂嗜欲深者天機淺。蓋今世俗之人，以利欲熏心。故形氣穢濁麤鄙，固執而不化。不得微妙玄通。故天機淺露，極為易見，殆非有道氣象。皆是不善為士也。老子因謂古之善為士者，不淺露易見。乃微妙玄通，深不可識。夫為不可識，最難形容。特強為之形容耳。然形容其行動也。豫若冬涉川。猶若畏四鄰。猶豫，行不進貌。冬涉川，謂不敢遽進。畏四鄰，謂不敢妄動。此乃從容不迫之意。其威儀也，儼若客。儼，謂肅然可觀。若客，謂謙退不敢直前。其氣也，渙若冰將釋。莊子謂暖然似春。又云冰解凍釋。謂其氣融和，使可親愛之意。其外貌也，敦兮其若樸。敦，敦厚。樸，無文飾也。其中心也，曠兮其若谷。曠，空也。谷，虛也。外體敦厚樸素，而中心空虛寂定也。其跡也，渾兮其若濁。渾，與混同。謂和光同塵也。蓋有道之士，心空無著。故行動威儀，氣象體段，胸次悠然，微妙玄通之若此。所謂孔德之容，惟道是從。故可觀而不可識。世俗之人，以功名利祿交錯於前，故形氣穢濁，而不可觀。老子因而愍之曰，孰能於此濁亂之中，恬退自養，靜定持心，久久而徐清之耶。蓋心水汨昏，以靜定治之，則清。所謂如澄濁水，沙土自沈，清水現前，名為初伏客塵煩惱。不能頓了，故曰徐清。人皆競進於功利之間。老子謂孰能安定自守，久久待時而後生耶。生，乃發動。謂應用也。即聖人迫不得已而後應之意。筆乘謂老子文法多什韻。蓋清，生，盈，成，一韻耳。若言徐動，徐應，則不什矣。老子嗟歎至此，乃教之以守道之方，曰，保此道者不欲盈。盈，滿也。欲盈，乃貪得無厭，不知止足之意。謂世人但知汨汨於嗜欲，貪得不足。殊不知天道忌盈，滿則溢矣。所謂持而盈之，不如其已。故此教之以不欲盈也。後乃結示知足常足之意，曰，夫惟不盈，是以能敝不新成，故敝。物之舊者謂之敝。凡物舊者，最持久，能奈風霜磨折。而新成者，雖一時鮮明，不久便見損壞。老子謂世人多貪好盈，雖一時榮觀快意，一旦禍及，則連本有皆失之矣。惟有道者，善知止足。雖無新成之名利，而在我故有現成之物，則可常常持之而不失矣。故曰能敝不新成。觀子房請留辟穀之事，可謂能敝不新成者。此余所謂子房得老之用也。",
    16: "此承上章要人作靜定功夫，此示功夫之方法也。致虛極守靜篤者。致，謂推致推窮之意。虛，謂外物本來不有。靜，謂心體本來不動。世人不知外物本來不有，而妄以為實。故逐物牽心，其心擾擾妄動，火馳而不返。見利亡形，見得亡真，故競進而不休，所以不能保此道也。今學道工夫，先要推窮目前萬物，本來不有。則一切聲色貨利，當體全是虛假不實之事。如此推窮，縱有亦無。一切既是虛假，則全不見有可欲之相。既不見可欲，則心自然不亂。而永絕貪求，心閒無事。如此守靜，可謂篤矣。故致虛要極，守靜要篤也。老子既勉人如此做工夫，恐人不信。乃自出己意曰，我之工夫亦無他術，唯只是萬物並作，吾以觀其復，如此而已。並作，猶言並列於前也。然目前萬物本來不有，蓋從無以生有。雖千態萬狀，並列於前，我只觀得當體全無。故曰萬物並作，吾以觀其復。復，謂心不妄動也。向下又自解之曰，夫物芸芸，各歸其根。意謂目前萬物雖是暫有，畢竟歸無，故云各歸其根。根，謂根本元無也。物既本無，則心亦不有。是則物我兩忘，寂然不動。故曰歸根曰靜，靜曰復命。命，乃當人之自性，賴而有生者。然人雖有形，而形本無形。能見無形，則不獨忘世，抑且忘身。身世兩忘，則自復矣。故云靜曰復命。性，乃真常之道也。故云復命曰常。人能返觀內照，知此真常妙性，纔謂之明。故云知常曰明。由人不知此性，故逐物妄生，貪欲無厭。以取戕生傷性亡身敗家之禍。故曰不知常，妄作凶。人若知此真常之道，則天地同根，萬物一體，此心自然包含天地萬物。故曰知常容。人心苟能廣大如此，則民吾同胞，物吾與也。其心廓然大公，則全不見有我之私。故曰容乃公。此真常大道，人若得之於內，則為聖。施之於外，則為王。故曰公乃王。王乃法天行事，合乎天心。故曰王乃天。天法道，合乎自然。故曰天乃道。與天地參。故曰道乃久。人得此道，則身雖死而道常存。故曰沒身不殆。殆，盡也。且此真常之道，備在於我。而人不知，返乃亡身殉物，嗜欲而不返，豈不謬哉。",
    17: "此言上古無知無識，故不言而信。其次有知有識，故欺偽日生。老子因見世道日衰，想復太古之治也。大上下知有之者，謂上古洪荒之世，其民渾然無偽，與道為一，全不知有。既而混沌日鑿，與道為二，故知有之。是時雖知有，猶未離道，故知而不親。其世再下，民去道漸疏，始有親之之意。是時雖知道之可親，但親於道，而人欲未流，尚無是非毀譽之事。其世再下，而人欲橫流，盜賊之行日生。故有桀跖之非毀，堯舜之是譽。是時雖譽，猶且自信而不畏。其世再下，而人欲固蔽，去道益遠，而人皆畏道之難親。故孔子十五而志於學，至七十而方從心。即顏子好學，不過三月不違仁，其餘則日月至焉。可見為道之難，而人多畏難而苟安也。是時雖畏，猶知道之不敢輕侮。其世再下，則人皆畔道而行。但以功名利祿為重，全然不信有此道矣。老子言及至此，乃歎之曰，此無他，蓋由在上者自信此道不足，故在下者不信之耳。然民既已不信矣，而在上者，就當身體力行無為之道，以啟民信。清淨自正，杜民盜賊之心，可也。不能如此，見民奸盜日作，猶且多彰法令，禁民為非。而責之以道德仁義為重，愈責愈不信矣，豈不謬哉。故曰猶兮其貴言。貴，重也。此上乃歷言世道愈流愈下。此下乃想復太古無為之治。曰，斯皆有為之害也。安得太古無為之治，不言而信，無為而成。使其百姓日出而作，日入而息，鑿井而飲，耕田而食。人人功成事遂，而皆曰我自然耶。蓋老氏之學，以內聖外王為主。故其言多責為君人者，不能清靜自正，啟民盜賊之心。苟能體而行之，真可復太古之治。",
    18: "此承上章言世道愈流愈下，以釋其次親之譽之之意也。大道無心愛物，而物物各得其所。仁義則有心愛物，即有親疏區別之分。故曰大道廢，有仁義。智慧，謂聖人治天下之智巧。即禮樂權衡斗斛法令之事。然上古不識不知，而民自樸素。及乎中古，民情日鑿。而治天下者，乃以智巧設法以治之。殊不知智巧一出，而民則因法作奸。故曰智慧出，有大偽。上古雖無孝慈之名，而父子之情自足。及乎衰世之道，為父不慈者眾，故立慈以規天下之父。為子不孝者眾，以立孝以教天下之子。是則孝慈之名，因六親不和而後有也。蓋忠臣以諫人主得名。上古之世，君道無為而天下自治。臣道未嘗不忠，而亦未嘗以忠立名。及乎衰世，人君荒淫無度，雖有為而不足以治天下。故臣有殺身諫諍，不足以盡其忠者。是則忠臣之名，因國家昏亂而有也。此老子因見世道衰微，思復太古之治，殆非憤世勵俗之談也。",
    19: "此承前章而言智不可用，亦不足以治天下也。然中古聖人，將謂百姓不利，乃為斗斛權衡符璽仁義之事，將利於民，此所謂聖人之智巧矣。殊不知民情日鑿，因法作奸。就以斗斛權衡符璽仁義之事，竊以為亂。方今若求復古之治，須是一切盡去，端拱無為，而天下自治矣。且聖智本欲利民，今既竊以為亂，反為民害。棄而不用，使民各安其居，樂其業，則享百倍之利矣。且仁義本為不孝不慈者勸，今既竊之以為亂，苟若棄之，則民有天性自然之孝慈可復矣。此即莊子所謂虎狼仁也。意謂虎狼亦有天性之孝慈，不待教而後能。況其人為物之靈乎。且智巧本為安天下，今既竊為盜賊之資，苟若棄之，則盜賊無有矣。然聖智仁義智巧之事，皆非樸素，乃所以文飾天下也。今皆去之，似乎於文則不定，於樸素則有餘。因世人不知樸素渾全之道，故逐逐於外物，故多思多欲。今既去華取實，故令世人心志，有所係屬於樸素之道。若人人果能見素抱樸，則自然少思寡欲矣。若知老子此中道理，只以莊子馬蹄胠篋作註解，自是超足。",
    20: "此承前二章言聖智之為害，不但不可用，且亦不可學也。然世俗無智之人，要學智巧仁義之事。既學於己，將行其志。則勞神焦思，汲汲功利，盡力於智巧之間。故曰巧者勞而智者憂。無知者又何所求。是則有學則有憂，絕學則無憂矣。然聖人雖絕學，非是無智。但智包天地而不用。順物忘懷，澹然無欲，故無憂。世人無智而好用。逐物忘道，汨汨於欲，故多憂耳。斯則憂與無憂，端在用智不用智之間而已。相去不遠，譬夫唯之與阿，皆應人之聲也，相去能幾何哉，以唯敬而阿慢。憂與無憂，皆應物之心也，而聖凡相隔，善惡相反，果何如哉。此所謂差之毫釐，失之千里也。老子言及至此，恐世俗將謂絕學，便是瞢然無知。故曉之曰，然雖聖人絕學，不是瞢然無知，其實未嘗不學也。但世俗以增長知見，日益智巧，馳騁物欲以為學。聖人以泯絕知見，忘情去智，遠物離欲以為學耳。且夫聲色貨利，皆傷生害道之物，世人應當可畏者。我則不可不畏懼而遠之。故曰人之所畏，不可不畏。苟不知畏，汨沒於此，荒淫無度，其害非細。故曰荒兮其未央哉。央，盡也。由是觀之，世人以增益知見為學。聖人以損情絕欲為學。所謂為學日益，為道日損，損之又損，以至於無為耳。眾人忘道逐物，故汨汨於物欲之間。酷嗜無厭，熙熙然如享太牢之味，以為至美。方且榮觀不休，如登春臺之望，以為至樂。老子謂我獨離物向道，泊於物欲未萌之前，不識不知，超然無欲。故曰我獨泊兮其未兆，若嬰兒之未孩。兆，念之初萌也。嬰兒，乃無心識愛惡之譬。孩，猶骸骨之骸。未骸，所謂骨弱筋柔。乃至柔之譬。眾人見物可欲，故其心執著而不捨。老子謂我心無欲，了無繫累。泛然應物，虛心遊世，若不繫之舟。故曰乘乘兮若無所歸。乘乘，猶泛泛也。眾人智巧多方，貪得無厭，故曰有餘。我獨忘形去智，故曰若遺。遺，猶忘失也。然我無知無我，豈真愚人之心也哉。但只渾渾沌沌，不與物辨，如此而已。故俗人昭昭，而我獨昏昏。昭昭，謂智巧現於外也。俗人察察，而我獨悶悶。察察，即俗謂分星擘兩，絲毫不饒人之意。昏昏悶悶，皆無知貌。我心如此，澹然虛明，若海之空闊不可涯量。颼然無著，若長風之御太虛。眾人皆自恃聰明知見，各有所以。以，猶自恃也。我獨無知無欲，頑而且鄙，亦似庸常之人而已。然我所以獨異於人者，但貴求食於母耳。凡能生物者，謂之母。所生者，謂之子。且此母字，不可作有名萬物之母的母字。此指虛無大道，能生天地萬物，是以道為母，而物為子。食，乃嗜好之意。眾人背道逐物，如棄母求食於子。聖人忘物體道，故獨求食於母。此正絕學之學。聖人如此，所以憂患不能入也。前章絕聖棄智，乃無用之用。此章絕學無憂，乃無學之學。後章孔德之容一章，乃無形名之形名耳。",
    21: "此章言道乃無形名之形名也。孔，猶盛也。謂道本無形，而有道之士，和氣集於中，英華發現於外，而為盛德之容。且此德容，皆從道體所發，即是道之形容也。故曰孔德之容，惟道是從。然此道體本自無形，又無一定之象可見。故曰道之為物，惟恍惟惚。恍惚，謂似有若無，不可定指之意。然且無象之中，似有物象存焉。故曰惚兮恍，其中有象。恍兮惚，其中有物。其體至深至幽，不可窺測。且此幽深窈冥之中，而有至精無妄之體存焉。故曰窈兮冥，其中有精。其精甚真，此正楞嚴所謂唯一精真。精色不沈，發現幽秘，此則名為識陰區宇也。學者應知。然此識體雖是無形，而於六根門頭，應用不失其時。故曰其中有信。此上皆無形之形。下言無名之名。謂世間眾美之名自外來者，皆是假名無實，故其名易去。惟此道體有實有名，故自古及今，其名不去，以閱眾甫也。閱，猶經歷。甫，美也。謂眾美皆具。是以聖人功流萬世而名不朽者，以其皆從至道體中流出故耳。其如世間王侯將相之名，皆從人欲中來，故其功亦朽，而名亦安在哉。唯有道者，不期於功而功自大，不期於名而名不朽。是知聖人內有大道之實，外有盛德之容，眾美皆具，惟自道中而發也。故曰吾何以知眾甫之然哉，以此。",
    22: "此承前章言聖人所以道全德備眾美皆具者，蓋由虛心體道，與物無競，故眾德交歸也。曲，委曲。即曲成萬物而不遺之意。謂聖人委曲以御世，無一事不盡其誠，無一人不得其所。譬如陽春發育萬物，雖草芥毫芒，春氣無不充足。若纖毫不到，則春氣不全。聖人之於人，無所不至。苟不曲盡其誠，則其德不全矣。故曰曲則全。枉則直者，屈己從人曰枉。直，伸也。謂聖人道高德盛，則大有徑庭，不近人情。若不屈己從人，俯循萬物，混世同波，則人不信。人不信，則道不伸。由人屈而道伸。故曰枉則直。窪則盈者，眾水所聚，地之最下者，曰窪。譬如江海最為窪下，故萬派皆歸。而聖人之心至虛至下，故眾德交歸，德無不備。故曰窪則盈。敝則新者，衣之汙損日敝。不敝，則不浣濯，不見其新。以其敝乃新耳。以譬聖人忘形去智，日損其知見，遠其物欲，洗心退藏於密。欲不敝，則道不新。故曰敝則新。聖人忘知絕學，專心於一，故於道有得。故曰少則得。世人多知多見，於道轉失。故曰多則惑。是以聖人因愍世人以多方喪道，故抱一為天下學道之式。式，法也。智巧衒耀於外曰見。自見者不明，故不自見乃為明耳。執己為必當曰是，自是者不彰，故不自是乃彰耳。彰者，盛德顯於外也。誇功，曰伐。自伐者無功，故不自伐乃有功耳。司馬遷嘗謂韓信，假令學道謙讓，不伐己功，不矜其能。則庶幾於漢家勳，可比周召太公之徒矣。意蓋出此。恃己之能曰矜。長，才能也。自矜者不長，不自矜者乃長耳。此上四不字，皆不爭之德也。惟聖人有之。故曰夫惟不爭，故天下莫能與之爭者。由其聖人委曲如此，故萬德交歸，眾美備具。故引古語以證之曰，古之所謂曲則全者，豈虛言哉，誠全而歸之。",
    23: "此章言聖人忘言體道，與時俱化也。希，少也。希言，猶寡言也。以前云多言數窮，不如守中。由其勉強好辯，去道轉遠，不能合乎自然。惟希言者，合乎自然耳。向下以飄風不終朝，驟雨不終日，以比好辯者之不能久。然好辯者，蓋出憤激不平之氣。如飄風驟雨，亦乃天地不平之氣。非不迅激如人，特無終朝之久。且天地不平之氣，尚不能久，而況於人乎。此甚言辯之不足恃也。蓋好辯者，只為信道不篤，不能從事於道，未得玄同故耳。惟聖人從事於道，妙契玄同，無入而不自得。故在於有道者，則同於道。在於有德者，則同於德。失者，指世俗無道德者。謂至於世俗庸人，亦同於俗。即所謂呼我以牛，以牛應之，呼我以馬，以馬應之，無可不可。且同於道德，固樂得之。即同於世俗，亦樂而自得。此無他，蓋自信之真，雖不言，而世人亦未有不信者。且好辯之徒，曉曉多言，強聾而不休，人轉不信。此無他，以自信不足，所以人不信耳。",
    24: "此承前章言好辯者不能持久，猶如跂跨之人不能立行，甚言用智之過也。跂，足根不著地也。跨，闊步而行也。蓋跂者只知要強高出人一頭，故舉踵而立。殊不知舉踵不能久立。跨者只知要強先出人一步，故闊步而行。殊不知跨步不能長行。以其皆非自然。以此二句為向下自見自是自伐自矜之譬喻耳。自見，謂自逞己見。自是，謂偏執己是。此一曲之士，於道必暗而不明。自伐，謂自誇其功。自矜，謂自恃其能。此皆好勝強梁之人，不但無功，而且速於取死。然此道中本無是事。故曰其在道也，如食之餘，如形之贅，皆人之所共惡。而有道之士，以謙虛自守，必不處此。故曰有道者不處。以其不能合乎自然也。",
    25: "此承前言世俗之士，各以己見己是為得。曾不知大道之妙，非見聞可及。故此特示大道以曉之也。有物者，此指道之全體，本來無名，故但云有一物耳。渾渾淪淪，無有絲毫縫隙，故曰混成。未有天地，先有此物，故曰先天地生。且無聲不可聞，無色不可見，故曰寂寥。超然於萬物之上，而體常不變，故曰獨立而不改。且流行四時，而終古不窮，故曰周行而不殆。殆，窮盡也。天地萬物，皆從此中生，故曰可以為天下母。老子謂此物至妙至神，但不知是何物，故曰吾不知其名，特字之曰道。且又強名之曰大道耳。向下釋其大字。老子謂我說此大字，不是大小之大。乃是絕無邊表之大。往而窮之，無有盡處。故云大曰逝。向下又釋逝字。逝者遠而無所至極也。故云逝曰遠。遠則不可聞見，無聲無色，非耳目之所到。故云遠曰反。反，謂反一絕跡。道之極處，名亦不立，此道之所以為大也。然此大道，能生天生地，神鬼神王。是則不獨道大，而天地亦大。不獨天地大，而王亦大。故域中所稱大者有四，而王居其一焉。世人但知王大，而不知聖人取法於天地。此則天地又大於王。世人但知天地大，而不知天地自道中生，取法於道。此則道又大於天地也。雖然，道固為大，而猶有稱謂名字。至若離名絕字，方為至妙，合乎自然。故曰道法自然。且而大道之妙，如此廣大精微。而世人豈可以一曲之見，自見自是以為得哉。此其所以自見者不明，自是者不彰耳。",
    26: "此誡君人者，當知輕重動靜，欲其保身重命之意也。然重字指身。輕字指身外之物，即功名富貴。靜字指性命。躁字指嗜慾之情。意謂身為生本，固當重者。彼功名利祿，聲色貨利，乃身外之物，固當輕者。且彼外物必因身而後有，故重為輕之根。性為形本，固至靜者。彼馳騁狂躁，甘心物慾，出於好尚之情者，彼必由性而發，故靜為躁之君。世人不知輕重，故忘身徇物，戕生於名利之間。不達動靜，故傷性失真，馳情於嗜慾之境。惟聖人不然，雖終日行而不離輜重。輜重，兵車所載糧食者也。兵行而糧食在後，乃大軍之司命。雖千里遠行，深入敵國，戒其擄掠，三軍不致鼓譟以取敗者，賴其所保輜重也。聖人遊行生死畏途，不因貪位慕祿，馳情物慾，而取戕生傷性之害者，以其所保身心性命為重也。故曰不離輜重。縱使貴為天子，富有四海之榮觀，但恬澹燕處，超然物慾之表。此其堯舜有天下而不與也。奈何後之人主，沈暝荒淫於聲色貨利之間，戕生傷性而不悟。是以物為重而身為輕也。故曰身輕天下。奈何者，怪歎之詞。物重則損生，故曰輕則失根。慾極則傷性，故曰躁則失君。君，謂性也。莊子養生讓王，蓋釋此篇之意。子由本云，輕則失臣。然臣字蓋亦指身而言。齊物以身為臣妾，以性為真君，源出於此。",
    27: "此言聖人善入塵勞，過化存神之妙也。轍跡，猶言痕跡。世人皆以人我對待，動與物競，彼此不忘，故有痕跡。聖人虛己遊世，不與物忤，任物之自然，所謂忘於物者物亦忘之。彼此兼忘，此行之善者。故無轍跡。瑕謫，謂是非辨別，指瑕謫疵之意。聖人無意必固我。因人之言。然，然。不然，不然。可，可。不可，不可。未嘗堅白同異，此言之善者，故無瑕謫。籌策，謂揣摩進退，算計得失利害之意。聖人無心御世，迫不得已而後應，曾無得失之心。然死生無變於己，而況利害之端乎。此計之善者，故不用籌策。關鍵，閉門之具。猶言機關也。世人以巧設機關，籠羅一世，將謂機密而不可破。殊不知能設之，亦有能破之者。歷觀古之機詐相尚之士，造為勝負者，皆可破者也。唯聖人忘機待物，在宥群生。然以道為密，不設網羅，而物無所逃。此閉之善者，所謂天下莫能破。故無關鍵而不可開。繩約，謂繫屬之意。世人有心施恩，要以結屬人心。殊不知有可屬，亦有可解。然有心之德，使人雖感而易忘，所謂賊莫大於德有心。聖人大仁不仁，利澤施乎一世，而不為己功，且無望報之心，故使人終古懷之而不忘。此結之善者，故無繩約而不可解。是以聖人處世，無不可化之人，有教無類，故無棄人。無不可為之事，物各有理，故無棄物。物，猶事也。如此應用，初無難者，不過承其本明，因之以通其蔽耳。故曰襲明。襲，承也。猶因也。莊子庖丁游刃解牛，因其固然，動刀甚微，劃然已解。意出於此。觀留侯躡足附耳，因偶語而乞封，借四皓而定漢，以得老氏之用。故其因事處事，如此之妙，可謂善救者也。其他孰能與之。故世之善人，不善人之師。不善人，善人之資。由其飾智矜愚，修身明汙，故皆知師之可貴。擇類而教，樂得而育，故皆知資之可愛。若夫聖人為舉世師保，而不知其師之可貴。化育億兆，而不知其資之可愛。所謂兼忘天下易。使天下忘己難。此雖在智者，猶太迷而不知，況淺識乎。斯所過者化，所存者神，是謂要妙。",
    28: "此承上章行道之妙，而言聖人不以知道為難，而以守道為要妙也。古德云，學道，悟之為難。既悟，守之為難。然行道之妙，實出於守道之要耳。蓋此中知字，即悟也。知雄守雌者，物無與敵謂之雄，柔伏處下謂之雌。谿，乃窊下之地。眾水所歸之處也。嬰兒者，柔和之至也。前云專氣致柔，能如嬰兒乎。然氣雖勝物，物有以敵之。而道超萬物，物無與敵者。故謂之雄。聖人氣與道合，心超物表，無物與敵，而能順物委蛇，與時俱化，不與物競，故曰知其雄，守其雌。由守其雌，故眾德交歸，如水之就下，故為天下谿也。由乎處下如谿，故但受而不拒，應而不藏，流潤而不竭，故曰常德不離。以入物而物不知，如嬰兒終日號而嗌不嗄，和之至也。以能勝物而不傷，故曰復歸於嬰兒。知白守黑者。白，謂昭然明白。智無不知之意。黑，昏悶無知之貌。式，謂法則。忒，差謬也。謂聖人智包天地，明並日月，而不自用其知。所謂明白四達，能無知乎。故曰知其白，守其黑。由其真知而不用其知，故無強知之過謬，故可為天下式。然強知則有謬，謬則有所不知。既有所不知，則知不極矣。今知既無謬，則知無不極，故曰復歸於無極。知榮守辱者。榮，乃光榮貴高。辱，乃汙辱賤下。谷，乃虛而能應者也。樸，謂樸素。乃木之未雕斲也。謂聖人自知道光一世，德貴人臣，而不自有其德。乃以汙辱賤下，蒙恥含垢以守之。所謂光而不耀，仁常而不居者，虛之至也。故為天下谷。由其虛，故常德乃足。德自足於中，則不緣飾於外，故復歸於樸素也。以虛而能應物，故樸散則為器。聖人以此應運出世，則可以官天地府萬物。故能範圍天地而不過。曲成萬物而不遺。化行於世而無棄人棄物。故曰大制不割。割，截斷也。不割者，不分彼此界限之意。",
    29: "此言聖人道全德備，應運出世，為官為長。當任無為無事，而不可有為太過也。由上章云，樸散則為器。聖人用之則為官長。故老子因而誡之曰，將欲取天下者，當任自然，不可有心為之。而有心為之者，吾見其必不可得已。何也，且天下者大器，有神主之。豈可以人力私智取而奪之耶。故曰不可為也。而為之者，必反敗之。縱為而得之，亦不可執為己有。而執之者，必反失之。故如強秦力能併吞六國，混一天下，是為之也。且誓云一世以至萬世，是執之也。故不旋踵而敗，二世而亡，豈非為者敗之，執者失之之驗歟。然而所以敗之失之者，以其所處過甚，而奢泰之極也。凡物極則反，此亦自然之勢耳。故物或行或在。或呴或吹。或強或羸。或載或隳。是以聖人去甚，去奢，去泰。",
    30: "此承上言聖人不為已甚，故誡之不可以兵強天下也。凡以兵強者，過甚之事也。勢極則反，故其事好還。師之所處，必蹂踐民物，無不殘掠，故荊棘生。大軍之後，殺傷和氣，故五穀疵癘而年歲凶，此必然之勢也。然於濟弱扶傾，除暴救民，蓋有不得不用之者，惟在善用。善用者，果而已。已者，休也，此也。果，猶言結果。俗云了事便休。謂但可了事令其平服便休，不敢以此常取強焉。縱能了事，而亦不可自矜其能。亦不可自伐其功。亦不可驕恃其氣。到底若出不得已。此所謂果而不可以取強也。取強者，速敗之道。且物壯甚則易老，況兵強乎。凡物恃其強壯而過動者，必易傷。如世人恃強而用力過者，必夭死於力。恃壯而過於酒色者，必夭死於酒色。蓋傷元氣也。元氣傷，則死之速。兵強亦然。故曰是謂不道。不道早已。已者，絕也。又已者，止也。言既知其為不道，則當速止而不可再為也，亦通。孟子言威天下不以兵革之利，其有聞於此乎。",
    31: "此承上言不以兵強天下，故此甚言兵之不可尚也。佳兵，乃用兵之最精巧者，謂之佳兵。凡善用兵者，必甘心於殺人。兵益佳而禍益深，故為不祥之器。歷觀古今善用兵者，不但不得其死，而多無後。此蓋殺機自絕，而造物或惡之者。以其詐變不正，好殺不仁，故有道者不處。不但有道者不處，而苟有仁心者，亦不處也。何以知其然耶。觀夫君子所居則以左為貴，用兵則以右為貴，然右乃凶地，由是而知兵者，乃不祥之器，非君子之器也。萬一不得已而用之者。老子誡曰，當以恬淡為上。恬淡者，言其心和平，不以功利為美，而厭飽之意。既無貪功欲利之心，則雖勝而不以為美。縱不貪功利，而若以勝為美者，亦是甘心樂於殺人。夫樂於殺人者，必不可使其得志於天下矣。且世之吉事必尚左。凶事則尚右。凶事，謂喪事也。所以用兵則貴右，言其可哀也。故兵家以偏將軍居左，以上將軍居右者，蓋上將軍司殺之重者。言居上勢者，則當以喪禮處之也。故殺人眾多，則當以悲哀泣之。即戰勝，亦當以喪禮處之。甚言其不得已而用之，即不得已而處之也。上二章，通言人臣不能以道佐人主，而返以兵為強者，故切誡之。",
    32: "此承上章不以兵強天下，因言人主當守道無為，則萬物賓而四海服，天地合而人民和，自然利濟無窮也。常者，終古不變之義。凡有名者，必遷變。道之所以不變者，以其無名也。故曰道常無名。樸，乃無名之譬。木之未制成器者，謂之樸。若制而成器，則有名矣。小，猶眇小。謂不足視也。且如合抱之材，智者所不顧。若取徑寸以為冠，則愚者亦尊焉。是以名為大，而以無名為小。甚言世人貴名，概以樸為不足視。故以道曰樸曰小也。然道雖樸小，而為天地萬物之本。即愚夫愚婦，而亦知所尊。故曰天下不敢臣。但侯王不能守耳。藉使侯王若能守，則萬物自然賓服矣，奚假兵力哉。然兵者凶器，未必賓服一國。且上干和氣，必有凶年。若以道服之，不但萬物來賓。抑且和氣致祥，天地相合以降甘露。兵來未必盡和民人，若以道宥之，則民莫之令而自然均調，各遂其生。無名之樸，利濟如此，惜乎侯王不能守之善用耳。若散樸為器，始制則有名矣。始，猶方纔也。謂樸本無名，方纔制作，則有名生焉。且從無名而有名。既有名，而名又有名，將不知其所止矣。莊子所謂從有適有，巧歷不能得，故曰名亦既有。而殉名者愈流愈下，逐末忘本，不知其返矣。故老子戒之曰，夫名者，不可馳騖而不返。亦將知止而自足。苟不知止足，則危殆而不安。知止所以不殆也。由是而知道在天下，為萬物之宗，流潤無窮，猶川谷之於江海也。然江海所以流潤於川谷，川谷無不歸宗於江海。以譬道散於萬物，萬物莫不賓服於大道。此自然之勢也。意明侯王若能守，其效神速於此。",
    33: "此因上言侯王當守道無為，故此教以守之之要也。知人者，謂能察賢愚，辨是非，司黜陟，明賞罰，指瑕摘疵，皆謂之智。但明於責人者，必昧於責己。然雖明於知人為智，不若自知者明也。老子謂孔子曰，聰明深察而近於死者，好議者也。博辯宏大而危其身者，好發人之惡也。去子之恭驕與智能，則近之矣。謂是故也。莊子云，所謂見見者，非謂見彼也，自見而已矣。所謂聞聞者，非謂聞彼也，自聞而已矣。能自見自聞，是所謂自知者明也。世之力足以勝人者，雖云有力。但強梁者必遇其敵，不若自勝者強。然欲之伐性，殆非敵國可比也。力能克而自勝之，可謂真強。如傳所云，和而不流，中立而不倚者，所謂自強不息者也。凡貪得無厭者，必心不足。苟不知足，雖尊為天子，必務厚斂以殃民。雖貴為侯王，必務強兵而富國。即縱適其欲，亦將憂而不足，故雖富不富。苟自知足，則鷦鷯偃鼠，藜藿不糝，抑將樂而有餘，此知足者富也。強志，好過於人者，未為有志。惟強行於道德者，為有志也。所者，如北辰居其所之所。又故有之義，蓋言其性也。孟子曰，性者故而已矣。世人貪欲勞形，冀立久長之業。殊不知戕生傷性，旋踵而滅亡，誰能久哉。惟抱道凝神，而復於性真者，德光終古，澤流無窮，此所謂不失其所者久也。世人嗜味養生，以希壽考，殊不知厚味腐腸，氣憊速死，誰見其壽哉。惟養性復真，形化而性常存，入於不死不生，此所謂死而不亡者壽也。老子意謂道大無垠，人欲守之，莫知其向往。苟能知斯數者，去彼取此，可以入道矣。侯王知此，果能自知自勝，知足強行。適足以全性復真，將與天地終窮。不止賓萬物，調人民而已。又豈肯以蝸角相爭，以至戕生傷性者哉。",
    34: "此言道為天地萬物之本，欲人體道虛懷，而造乎至德也。謂道本無名，強名之一。故曰道生一。然天地人物，皆從此生。故曰一生二，二生三，三生萬物。是則萬物莫不負陰而抱陽也。所以得遂其生，不致夭折者，以物各含一沖虛之體也。和氣積中，英華昭著，秀實生成，皆道力也。故云沖氣以為和。是則物物皆以沖虛為本也。且沖虛柔弱，與物不類，似乎無用，人皆惡之而不取。殊不知無用之用為大用也。即如世人之所惡者，唯孤寡不穀，以為不美。而王公返以此為稱者，豈不以柔弱為天下之利器耶。且孤寡不穀，皆自損之辭也。然而侯王不自損，則天下不歸。故堯舜有天下而不與，至今稱之，澤流無窮，此自損而人益之。故曰或損之而益。若夫桀紂以天下奉一己，暴戾恣睢，但知有己，而不知有人。故雖有天下，而天下叛之，此自益者而人損之。故曰或益之而損。以人人皆具此道，但日用不知，須待教而後能。且人之所教者，我亦未嘗不教之也。惟人不善教人，祇知增益知見，使之矯矜恃氣，好為強梁。殊不知強梁者，不得其死。我唯教人以日損其欲，謙虛自守，以全沖和之德。是故吾將以為教父。而風天下以謙虛之德也。教父，猶木鐸意。",
    35: "此承上言無為之益，以明不言之教也。然天下之至堅，非至柔不足以馳騁之。如水之穿山透地，浸潤金石是已。若以有入有，即相觸而有間。若以空入有，則細無不入。如虛空偏入一切有形，即纖塵芒芴，無所不入，以其虛也。若知虛無之有用，足知無為之有益矣。前云人不善教人者，以其有言也。有言則有跡，有跡則恃智，恃智則自多。自多者則矜能而好為。凡好為者必易敗。此蓋有言之教，有為之無益也，如此。則知不言之教，無為之益，天下希及之矣。",
    36: "此言名利損生，誡人當知止足也。謂世人祇知名之可貴，故忘身以殉名。殊不知名乃身外之虛聲耳。與身較之，身親而名疏。故曰孰親。貨，利也。謂世人祇知利之可貪，故忘身以殉利。殊不知利乃身之長物耳。與身較之，身在則有餘。故曰孰多。世人不察，每役役於名利之間，貪得而無厭，戕生傷性。與夫貪得而身亡，不若身存而遠害。故曰得與亡孰病。故凡愛之甚者，費必大。藏之多者，亡必厚。如以隋侯之珠，彈千仞之雀，雀未得而珠已失。此愛之甚，而不知所費者大矣。如斂天下之財，以縱鹿臺之欲，天下叛而臺已空。此藏之多，而不知所亡者厚矣。不唯愛者費而藏者亡。抑且身死名滅，國危而不安。斯皆不知止足之過也。故知足則不辱，知止則不殆，即斯可以長久矣。噫，老氏此言，可謂破千古之重昏，啟膏肓之妙藥，昭然如揭日月於中天也。而人不察乎此，惜哉。",
    37: "此言聖人法天制用，與道為一，故能勝物而物不能勝。以申明前章不言之教，無為之益也。大成若缺，其用不敝者。若天地生物曲成萬物而不遺，可謂成之大矣。然必春生而夏方長之，秋殺而冬方成之。以此觀之，似若有所缺。苟不如此，若一徑生長而無秋冬之肅殺。不但物不能成，而造物者亦將用之而敝矣。由其若缺，故所成者大，而其用不敝也。大盈若沖，其用不窮者。若陽和之氣，充塞天地，無處不至，無物不足，可謂盈矣。其體沖虛而不可見。若塊然可見，亦將用之有盡矣。由其若沖，故既已為人己愈有，既已與人己愈多，故其用不窮也。大直若屈者。若一氣浩然，至大至剛，可謂直矣。然潛伏隱微，委曲周匝，細入無間，故若屈。由若屈，故能伸其生意也。大巧若拙者。若天之生物，刻雕眾形而不見其巧。故云若拙。若恃其巧者，巧於此而拙於彼，則巧非大矣。大辯若訥者。上云若缺，則天地無全功，故人猶有所憾。然天何言哉，四時行焉，百物生焉。是則生物之功，不辯而自白矣。故曰若訥。是以天地不言而萬物成，聖人不言而教化行。以聖人法天制用，故以不言之教，無為之化，似乎不勝，而物卒莫能勝之也。且躁能勝寒而不能勝熱，靜能勝熱而不能勝寒。斯皆有所勝，則有所不勝。是故聖人貴乎清淨為天下正。此其不言之教，無為之益，天下希及之矣。",
    38: "此承上清淨無為之益，甚言多欲有為之害，以誡人君當以知足自守也。謂上古之世，有道之君，清淨無欲，無為而化。故民安其生，樂其業，棄卻走馬而糞田疇。所以家給人足，而無不足者。及世衰道微，聖人不作，諸侯暴亂。各務富國強兵，嗜欲無厭，爭利不已，互相殺伐。故戎馬生於郊。以致民不聊生，奸欺並作。此無他，是皆貪欲務得，不知止足之過也。故天下罪之大者，莫大於可欲。以其戕生傷性，敗亂彝倫。以至君臣父子，皆失其分者，皆見可欲之罪也。以致敗國亡家，覆宗滅族之禍者，皆不知止足所致也。由不知足，故凡見他人之所有，而必欲得之。然欲得之心，為眾罪大禍之本。故咎之大者，莫大於欲得。欲得者，心不足也。古人云，若厭於心，何日而足。以貪得不止，終無足時。惟知足之足，無不足矣，故常足。",
    39: "此承上言聖人所以無為而成者，以其自足於己也。謂聖人性真自足，則智周萬物，無幽不鑒。故天下雖，可不出戶而知。天道雖微，可不窺牖而見。以其私欲淨盡，而無一毫障蔽，故也。若夫人者，沉瞑利欲，向外馳求，以利令智昏，故去性日遠，情塵日厚，塵厚而心益暗。故其出彌遠，其知彌少。是以聖人淡然無欲，不事於物。故寂然不動，感而遂通天下之故。故曰不行而知。如此，則尸居而龍見，淵默而雷聲。故曰不見而名。道備於己，德被群生，可不言而化。故曰不為而成。是皆自足於性也。",
    40: "此承上言無為之德，由日損之功而至也。為學者，增長知見，故日益。為道者，克去情欲，窮形泯智，故日損。初以智去情，可謂損矣。情忘則智亦泯，故又損。如此則心境兩忘，私欲淨盡，可至於無為。所謂我無為而民自化。民果化，則無不可為之事矣。此由無為而後可以大有為，故無不為。是故取天下者，貴乎常以無事也。無事，則無欲。我無欲，而民自正。民自正，而天下之心得。天下之心得，則治國如視諸掌，此所以無事足以取天下也。若夫有事則有欲，有欲則民擾，民擾則人心失。人心既失，則眾叛親離，此所以有事不足以取天下也。無為之益，天下希及之者，此耳。舊注取字訓為，攝化之意。應如春秋取國之取，言得之易也。",
    41: "此言聖人不言之教，無心成化，故無不可教之人也。常者，一定不移之意。謂聖人之心，至虛無我。以至誠待物，曾無一定之心。但無百姓之心為心耳。以聖人復乎性善，而見人性皆善。故善者固已善之，即不善者亦以善遇之。彼雖不善，因我以善遇之。彼將因我之德所感，亦化之而為善矣。故曰德善。以聖人至誠待物，而見人性皆誠。故信者固已信之，即不信者亦以信待之。彼雖不信，因我以信遇之。彼將因我之德所感，亦化之而為信矣。故曰德信。以天下人心不古，日趨於澆薄。聖人處其厚而不處其薄，汲汲為天下渾厚其心。惵惵，猶汲汲也。百姓皆注其耳目者，謂注目而視，傾耳而聽，司其是非之昭昭。聖人示之以不識不知，無是無非，渾然不見有善惡之跡，一皆以淳厚之德而遇之，若嬰孩而已。故曰皆孩之。若以嬰孩待天下之人，則無一人可責其過者。聖人之心如此，所以不言而信，無為而化，則天下無不可教之人矣。",
    42: "此因上言侯王當守道無為，故此教以守之之要也。嗇，有而不用之意。老子所言人天，莊子解之甚明。如曰，不以人害天，不以物傷性。蓋人，指物欲。天，指性德也。言治人事天莫若嗇者。然嗇，即復性工夫也。謂聖人在位，貴為天子，富有四海。其子女玉帛，聲色貨利，充盈於前。而聖人以道自守，視之若無，澹然無欲，雖有而不用。所謂堯舜有天下而不與，此以嗇治人也。聖人并包四海，智周萬物。不以私智勞慮，而傷其性真。所謂毋搖爾精，毋勞爾形，毋使汝思慮營營。蓋有智而不用其智，此以嗇事天也。復性工夫，莫速於此。故曰是謂之早復。此復字，是復卦不遠復之意。言其速也。又如一日克己復禮，天下歸仁之意。莊子曰，賊莫大於德有心。然有心之德施於外，故輕而不厚。復性之功，天德日全，不期復而自復，所謂復見天地之心。故曰早復謂之重積德。能重積德，則無不克矣。此克字，乃克敵之克。即顏子克己之克。以性德日厚，則物欲消融。而所過者化，無物與敵。則其德高明廣大，民無得而稱焉。故曰無不克，則莫知其極。極，至極，猶涯量也。此內聖之德既全，雖無心於天下，乃可以託於天下。故曰莫知其極，可以有國。此內聖之道，真以治身，其緒餘以為天下國家。故曰可以有國。此道先天地不為老，後天地不為終。故曰可以長久。古人所言深根固蒂長生久視之道者，如此而已。結句蓋古語。老子引證，以結其意耳。",
    43: "此言無為之益，福利於民，反顯有為之害也。凡治大國，以安靜無擾為主，行其所無事，則民自安居樂業，而蒙其福利矣。故曰若烹小鮮。烹小鮮，則不可撓。撓，則靡爛而不全矣。治民亦然。夫虐政害民，災害並至，民受其殃。不知為政之道，乃以鬼神為厲而傷人，反以祭祀以要其福。其實君人者不道所致也。若以道德君臨天下，則和氣致祥，雖有鬼而亦不神矣。不神，謂不能為禍福也。且鬼神非無，然洋洋乎如在其上，如在其左右，豈不昭格於上下耶。第雖靈爽赫然，但只為民之福，不為民害。故曰非其鬼不神，但其神不傷人耳。然非其神不傷人，實由聖人含哺百姓，如保赤子。與天地合其德，鬼神合其吉凶，而絕無傷民之意，故鬼神協和而致福也。故曰非其神不傷人，聖人亦不傷之。如湯之時，七年大旱。湯以身代犧牲，藉茅以禱，致雨三尺。故民皆以湯王克誠感格所致，斯蓋由夫兩不相傷，故其德交歸焉。此無為之德，福民如此。",
    44: "此言君天下者，當以靜勝為主，不可以力相尚也。夫流之在下者，如江海，眾水歸之。故大國之在天下，眾望歸之。故如流之在下，以為天下之交。納汙含垢，無所不容。又虛而能受，如天下之牝也。凡物之雌曰牝，雄曰牡，牡動而牝靜。動則不育，靜能有生，是牝以靜勝牡也。以此譬喻聖人之德。然聖人為天下牝者。以天下之人，衣食皆賴之以生，爵祿皆賴之以榮，萬幾並集於一人。故君道無為，而皆任其所欲，各遂其所生。所謂萬物皆往資焉而不匱，此似牝以靜勝牡也。是則靜為群動之歸趨，故以靜為下。大字小，如母育子。小事大，如子奉母。精神相孚，相得最易，故如掇之也。然大字小，必有所容。故曰或下以取。以，猶左右之也。小事大，必有所忍。故曰或下而取。而，因而取之也。皆無妄動之過，故交歸焉。且大國之欲，不過兼畜人，非容無以成其大。小國之欲，不過入事人，非忍無以濟其事。兩者既各得其所欲，而大者更宜下。何也。以大國素尊，難於下耳，故特勉之。此老子見當時諸侯，專於征伐，以力不以德，知動不知靜，徒見相服之難，而不知下之一字，為至簡之術。蓋傷時之論也。",
    45: "此言道之為貴，誡人當勉力求之也。道者，萬物之奧。奧者，室之西南隅。有室必有奧。但人雖居其室，而不知奧之深邃。以譬道在萬物，施之日用尋常之間，人日用而不知，故如奧也。然道既在萬物，足知人性皆同。雖有善惡之差，而性未嘗異，以其俗習之偏耳。故善人得之以為寶。惡人雖失，亦賴此道保之以有生。故曰所保。苟非其道以保之，則同無情瓦石矣。足見理本同也，所謂堯舜與人同耳。由此觀之，天下豈有可棄之人耶。且一言之美，則可以市。市，利也。一行之尊，則可以加於人之上。況大道之貴，豈止一言之美，一行之尊。且人之全具而不欠缺一毫者，斯則不善之人，又何棄之有耶。故立天子，置三公，雖有拱璧以先駟馬，不如坐進此道，此古語也。老子解之曰，然天子三公，不足為尊貴。拱璧駟馬，不足為榮觀。總不如坐進此道。所以貴此道者，何耶。豈不曰，求道以得之，縱有罪亦可以免之耶。是知桀紂，天子也，不免其誅。四凶，三公也，不免其戮。非無拱璧駟馬，而竟不能免其罪。故夷齊諫武王而不兵，巢許傲天子而不譴，豈非求以得有罪以免耶。況夫一念復真，諸罪頓滅。苟求而得，立地超凡。故為天下貴也。",
    46: "此言聖人入道之要妙，示人以真切工夫也。凡有為，謂智巧。有事，謂功業。有味，謂功名利欲。此三者，皆世人之所尚。然道本至虛而無為。至靜而無事。至淡而無味。獨聖人以道為懷，去彼取此。故所為者無為。所事者無事。所味者無味。故世人皆以名位為大，以利祿為多而取之。然道至虛微淡泊無物，皆以為小少，故棄而不取。聖人去功與名，釋智遺形，而獨與道游。是去其大多，而取其小少。故至小為至大，至少為至多。故大其小，而多其少也。試觀世人報怨以德，則可知矣。何也。且世之人，無論貴賤，事最大而難解者，怨也。然怨之始也，偶因一言之失，一事之差。遂相搆結，以至殺身滅名，亡國敗家之禍。甚至有積怨深憤，父子子孫，累世相報而未已者。此舉世古今之恆情也。豈非其事極大且多哉。惟聖人則不然。察其怨之未結也，本不有。始結也，事甚小。既結也，以為無與於己。故無固執不化之心，亦無有我以與物為匹敵。其既往也，事已消之，求其朕而不可得。以此觀之，則任彼之怨，在我了無報之之心矣。然彼且以為有怨，在我全無報復之心，彼必以我為德矣。是所謂報怨以德，非謂曲意將德以報怨也。孔子以直報怨，正謂此耳。斯則怨乃事之至大而多，人人必有難釋者。殊不知有至易者存焉。是所謂為無為，事無事，大其小，而多其少也。天下之事，何獨於怨，而事事皆然。故天下之事至難者，有至易存焉。至大者，有至細存焉。人不見其易與細，而於難處圖之，大處為之，必終無成。苟能圖之於易，而為之於細，鮮不濟者。以天下難事必作於易。天下大事必作於細，故也。作者，始起也。是以聖人虛心體道，退藏於密。跡愈隱而道愈光，澤流終古而與天地參。此所謂終不為大，故能成其大也。老子言及至此，抑恐世人把易字當作容易輕易字看。故誡之曰，夫輕諾必寡信，多易必多難。謂世人不可將事作容易看也。且容易許人，謂之輕諾。凡輕許者，必食言而寡信。見事之容易而輕為者，必有始而無終。是故易字，非容易也。世人之所難，而聖人之所易。世人之所易，而聖人之所難。故曰聖人猶難之，故終無難。猶，應作尤。古字通用。更也。謂世人之所甚易者，而聖人更難之，故終不難耳。觀夫文王兢兢，周公業業，戒慎恐懼乎不睹不聞，皆聖人之所難也。余少誦圖難於易為大於細二語，只把作事看。及余入山學道，初為極難，苦心不可言。及得用心之訣，則見其甚易。然初之難，即今之易。今之易，即初之難。然治心如此，推之以及天下之事皆然。此聖人示人入道之真切工夫也。志道者勉之。",
    47: "此釋上章圖難於易為大於細之意，以示聖人之要妙，只在為人之所不為，以為學道之捷徑也。治人事天工夫，全在於此。安與未兆。蓋一念不生。喜怒未形。寂然不動之時。吉凶未見之地。乃禍福之先。所謂幾先也。持字，全是用心力量。謂聖人尋常心心念念，朗然照於一念未生之前，持之不失。此中但有一念動作，當下就見就知。是善則容，是惡則止，所謂早復。孔子所謂知幾其神乎，此中下手甚易，用力少而收功多。故曰其安易持。兆，是念之初起。未兆，即未起。此中喜怒未形，而言謀者。此謀，非機謀之謀，乃戒慎恐懼之意。於此著力，圖其早復。蓋第一念為之於未有也。若脆與微，乃一念始萌，乃第二念耳。然一念雖動，善惡未著，甚脆且微。於此著力，所謂治之於未亂也。合抱之木以下，三句皆譬喻。毫末，喻最初一念。累土足下，喻最初一步工夫也。上言用心於內，下言作事於外。為執二句，言常人不知著力於未然之前，卻在既發之後用心。為之則反敗，執之則反失矣。聖人見在幾先，安然於無事之時，故無所為，而亦無所敗。虛心鑑照，故無所執，而亦無所失。以其聖人因理以達事耳。常民不知在心上做，卻從事上做，費盡許多力氣，且每至於幾成而敗之。此特機巧智謀，有心做來，不但不成，縱成亦不能久，以不知聽其自然耳。慎終如始。始，乃事之初。終，乃事之成。天下之事，縱然盈乎天地之間。聖人之見，察其始也本來不有。以本不有，故將有也，任其自然，而無作為之心。及其終也，事雖已成，觀之亦似未成之始，亦無固執不化之念，此所謂慎終如始，故無敗事也。是以聖人欲不欲，不貴難得之貨。學不學，復眾人之所過。以輔萬物之自然。而不敢為。莊子內聖外王學問，全出於此。吾人日用明此，可以坐進此道。以此用世，則功大名顯。伊周事業，特緒餘耳。豈不至易哉。",
    48: "此言聖人治國之要，當以樸實為本，不可以智誇民也。明者，昭然揭示之意。愚者，民可使由之，不可使知之意。夫民之所趨，皆觀望於上也，所謂百姓皆注其耳目。凡民之欲蔽，皆上有以啟之。故上有好者，下必有甚焉者也。故聖人在上，善能以斯道覺斯民，當先身以教之。上先不用智巧，離欲清淨，一無所好，若無所知者。則民自各安其日用之常，絕無一念好尚之心。而黠滑之智自消，奸盜之行自絕矣。所謂我好靜而民自正，我無為而民自化。故曰非以明民，將以愚之。此重在以字。前云眾人皆有以。以，如春秋以某師之以。謂左右之也。此其上不用智，故民易治耳。然民之難治者，皆用智之過也。足知以智治國者，反為害也，乃國之賊。不用智而民自安，則為國之福矣。人能知此兩者，可為治國之楷式也。楷式，好規模也。苟能知此楷式，是謂之玄德矣。玄德，謂德之玄妙，而人不測識也。故歎之曰，玄德深矣遠矣。非淺識者所可知也。民之欲，火馳而不返。唯以此化民，則民自然日與物相反，而大順於妙道之域矣。語曰，齊一變至於魯，魯一變至於道，猶有智也。況玄德乎。",
    49: "此教君天下者，以無我之德，故天下歸之如水之就下也。百川之水，不拘淨穢，總歸於江海。江海而能容納之，以其善下也。此喻聖人在上，天下歸之，以其無我也。欲上民，必以言下之。言者，心之聲也。故君天下者，尊為天子。聖人虛心應物，而不見其尊，故凡出言必謙下。如日孤寡不穀，不以尊陵天下也。欲先人，必以身後之者，身者，心之表也。君天下者，貴為天子，天下推之以為先。聖人忘己與人，而不自見有其貴。故凡於物欲，澹然無所嗜好，不以一己之養害天下也。重者，猶不堪也。是則聖人之心，有天下而不與。故雖處上，而民自堪命，不以為重。雖處前，而民自遂生，不以為害。此所以天下樂推而不厭。蓋無我之至，乃不爭之德也。此爭非爭鬥之謂，蓋言心不馳競於物也。以其不爭，故天下莫能與之爭。莊子所謂兼忘天下易，使天下忘己難。此則能使天下忘己，故莫能與之爭耳。",
    50: "此章老子自言所得之道至大，世人不知，其實所守者至約也。道大，如巍巍乎惟天為大，蕩蕩乎民無稱焉，言其廣大難以名狀也。不肖，如孔子云不器。大史公謂孟子迂遠而不切於事情之意。即莊子所謂大有徑庭，不近人情也。此蓋當時人見老子其道廣大，皆如下文所云，以勇廣器長稱之，且不得而名，故又為不肖，即若孔子稱之猶龍也。故老子因時人之言，乃自解之曰，天下人皆謂我之道大，似乎不肖，無所可用。惟其大，所以似不肖耳。肖者，與物相似。如俗云一樣也。若肖，作一句。久矣其細，作一句。倒文法耳。謂我若是與世人一樣，則成細人久矣，又安得以道大稱之哉。下文釋其大之所以。謂世人皆見其物莫能勝我，遂以我為勇。見我寬裕有餘，遂以我為廣。見其人皆推我為第一等人，遂以我為器長。器者，人物之通稱也。以此故，皆謂我道大，其實似無所肖。殊不知我所守者至約。乃慈，儉，不敢為天下先，三法而已。慈者，并包萬物，覆育不遺，如慈母之育嬰兒。儉者，嗇也，有而不敢盡用。不敢為天下先者，虛懷遊世，無我而不與物對。然以慈育物，物物皆己。且無己與物敵，物自莫能勝矣。故曰慈故能勇。心常自足，雖有餘而不用，所處無不裕然寬大矣。故曰儉故能廣。物我兩忘，超然獨立，而不見有己以處人前。故人皆以我為畸人，推為人中之最上者矣。故曰不敢為天下先，故能成器長。以此故，皆以我為道大似不肖耳。以我所守者如此，即前所云我獨異於人，而貴求食於母也。以此三者，乃大道之要妙耳。且今世人，捨慈而言勇，捨儉而言廣，捨後而言先，死矣。此死字，非生死之死，如禪家所云死在句下。蓋死活之死，言其無生意也。以世人不知大道之妙，但以血氣誇侈爭勝做工夫。故一毫沒用頭，皆死法，非活法也。且此三者之中，又以慈為主。不但學道，即治天下國家莫不皆然。若以戰則勝，以守則固，故王師無敵，民效死而勿去，皆仁慈素有所孚，故為戰勝守固之道。此所謂道之真以治身，其緒餘以為天下國家。以天地之大德曰生。故天將救斯民，而純以慈衛之。故聖人法天利用，而以慈為第一也，世俗惡足以知之。故知治世能用老氏之術，坐觀三代之化。所以漢之文景，得糟粕之餘，施於治道，迴超百代耳。此老子言言皆真實工夫，切於人事，故云甚易知易行。學人視太高，類以虛玄談之，不能身體而力行，故不得其受用耳。惜哉。",
    51: "此重明前章不爭之德，以釋上三寶之意也。一章主意，只在善用人者為之下一句。乃假兵家戰勝之事，以形容其慈，乃不爭之至耳。士者，介胄之士。武者，武勇。然士以武為主。戰以怒為主。勝敵以爭為主。三者又以氣為主。況善於為士者不用武。善於戰者不在怒。善勝敵者不必爭。即前所云以慈用兵也。意謂武怒爭三者，獨兵事所必用。若用之而必死，故善者皆不用。何況常人，豈可恃之以為用耶。乃驕矜恃氣，不肯下人，故人不樂其用，乃不善用人耳。故古之善用人者，必為之下，即此是謂不爭之德也。若以力驅人，能驅幾何。若以下驅人，則天下歸之。是以下用人，最有力也。所謂上善若水，水善利萬物而不爭，以其有力也。是謂配天古之極者。乾天，坤地。若天地正位，則為否，而萬物不生。若乾下坤上，則為泰。是知天在上而用在下也。聖人處民上而心在下，可謂配天之德。此古皇維極之道，置百姓於熙皞至樂之中。斯豈不爭之德以治天下，而為力之大者與。此章主意，全在不用氣上做工夫。即前云專氣致柔，能如嬰兒。純和之至，則形化而心忘。不見物為對，則不期下而自下矣。殆非有心要下，而為用人之術也。然學人有志於謙德，則必尊而光，況聖人無我之至乎。",
    52: "此重明前章不爭之德，以釋上三寶以慈為本之意也。然用兵有言，吾不敢為主而為客，不敢進寸而退尺。以此觀之，足可知也。古之用兵，如涿鹿孟津之師是也。兵主，如春秋征伐之盟主。蓋專征伐，主於兵者，言以必爭必殺為主也。客，如諸侯應援之師。本意絕無好殺之心。今雖迫不得已而應之，然亦聽之待之，若可已則已。以無心於功利，故絕無爭心，所以進之難而退之易。故曰不敢進寸而退尺。言身進而心不進，是以退心進也。以無爭心，故雖行而如不在行陣，雖攘而若無臂之人。仍，相仍，猶就也。言彼以我為敵，而我以彼為敵也。雖就，亦似無敵可對。雖執，猶若無兵可揮。戒懼之至，而不敢輕於敵。由不敢輕敵，所以能保全民命，不傷好生之仁。然禍之大者莫大於輕敵。以輕敵則多殺，多殺則傷慈，故幾喪吾寶矣。抗兵，乃兩敵相當，不相上下，難於決勝。但有慈心哀之者，則自勝矣。何則，以天道好生，助勝於慈者也。由是觀之，兵者對敵，必爭必殺以取勝。今乃以不爭不殺而勝之，蓋以慈為本故也。足見慈乃不爭之德，施於必爭地，而以不爭勝之，豈非大有力乎。用之於敵尚如此，況乎聖人無物為敵，而以平等大慈，并包萬物，又何物而可勝之耶。故前云不爭之德，是謂用人之力，是謂配天古之極。此章舊解多在用兵上說，全不得老子主意。今觀初一句，乃借用兵之言。至輕敵喪寶，則了然明白。是釋上慈字，以明不爭之德耳。",
    53: "此章示人立言之指，使知而行之，欲其深造而自得也。老子自謂我所言者，皆人人日用中最省力一著工夫。明明白白，甚容易知，容易行。只是人不能知，不能行耳。以我言言事事，皆以大道為主，非是漫衍荒唐之說。故曰言有宗，事有君。宗，君，皆主也。且如一往所說，絕聖棄智，虛心無我，謙下不爭，忘形釋智，件件都是最省力工夫，放下便是，全不用你多知多解。只在休心二字，豈不最易知最易行耶。然人之所以不能知者，因從來人人都在知見上用心。除卻知字，便無下落。以我無知無識一著，極難湊泊，所以人不知我耳。故曰夫惟無知，是以不我知。然無知一著，不獨老子法門宗旨，即孔子亦同。如曰吾有知乎哉，無知也，有鄙夫問於我空空如也，此豈不是孔聖亦以無知為心宗耶。此夫子見老子後，方得妙悟如此。故稱猶龍，正謂此耳。然以無知契無知，如以空合空。若以有知求無知，如以水投石。所以孔老心法，千古罕明。故曰知我者希。若能當下頓悟此心，則立地便是聖人，故曰則我者貴。則，謂法則。言取法也。聖人懷此虛心妙道以遊世。則終日與人周旋，對面不識。故如披褐懷王。永嘉云，貧則身常披縷褐，道則心藏無價珍。此一章書，當在末後結束。蓋老子向上一往所言天人之蘊，至此已發露太盡，故著此語。後章只是要人在日用著力做工夫，以至妙悟而後已。",
    54: "此承上言惟無知，是以不我知。恐人錯認無知，故重指出無知之地也。然世人之知，乃敵物分別之知，有所知也。聖人之知，乃離物絕待，照體獨立之知，無所知也。故聖人之無知，非斷滅無知，乃無世人之所知耳。無所知，乃世人所不知也。世人所不知，乃聖人之獨知。人能知其所不知之地，則為上矣。故曰知不知上。若夫臆度妄見，本所不知，而強自以為知。或錯認無知為斷滅，同於木石之無知。此二者皆非真知，適足為知之病耳。故曰不知知病。若苟知此二者為知之病，則知見頓亡，可造無知之地，而無強妄妄之病矣。故曰夫惟病病，是以不病。聖人但無強妄之知，故稱無知，非是絕然斷滅無知也。故曰聖人不病。此段工夫，更無別樣玄妙。唯病其妄知強知是病而不用。是以不墮知病之中，而名無知。此無知，乃真知。苦如此真知，則終日知而無所知。斯實聖人自知之明，常人豈易知哉。此所以易知易行，而世人不能知不能行也。古云，知之一字，眾妙之門。知之一字，眾禍之門。然聖人無知之地，必假知以入。若悟無知，則妄知自泯。此乃知之一字，眾妙之門也。若執有知以求無知，則反增知障，此乃眾禍之門。正是此中知之病也。知不知上，最初知字，正是入道之要。永嘉云，所謂知者，但知而已，此句最易而難明。學者日用工夫，當從此入。",
    55: "此章教人遺形去欲，為入道之工夫，以造聖人無知之地也。凜然赫然而可畏者，謂之威。如云寒威，炎威，是也。是則凡可畏者，皆謂威。唯國之大罰，與天地之肅殺，乃大威也。此借以為戕生傷性者之喻。世人以為小惡不足戒，而不知畏，必致殺身而後已。此民不畏威，大威至矣。喻世人祇知嗜欲養生，而不知養生者，皆足以害生而可畏也。且若嗜酒色，必死於酒色。嗜利欲，必死於利欲。嗜飲食，必死於飲食。是則但有所嗜，而不知畏，必至於戕生傷性而後已。此不畏威，故大威至矣。然人但知嗜而不知畏者，以其止知有身之可愛，有生之可貴，以此為足。而不知大有過於此者，性也。且吾性之廣大，與太虛同體，乃吾之真宅也。苟以性視身，則若大海之一涵，太虛之一塵耳，至微小而不足貴者。人不知此，而但以蕞爾之身。以為所居之地。將為至足，而貴愛之，則狹陋甚矣。故戒之曰，無狹其所居。狹其居者，將以此身此生為至足也。故又戒之曰，無厭其所生。厭，足也。若知此身此生之不足貴，則彼物欲固能傷生，亦不足以害我矣，以其無死地也。故曰夫惟不厭，是以不厭。厭，棄也。故聖人自知尊性，而不見生之可養。自愛遺形，而不見身之可貴。此聖人之所獨知，世人之所不知也。故去彼眾人之所知，取彼所不知，以為道之要妙耳。以此足見世人之所知者，皆病也。聖人病之而不取，故不病也。後三章互相發明此章之旨。",
    56: "此言天命可畏，報應昭然，教人不可輕忽也。勇者，決定之志也。敢者，不計利害而決於為也。殺活，死生也。謂凡世人作事，不顧利害，不怕死生，而敢為之。然敢乃必死之地。故曰勇於敢則殺。若用志於不敢為，是足以保身全生。故曰勇於不敢則活。此天道必然之理也。且此二者，亦有敢而生，不敢而死者，至若顏子夭，而盜蹤壽，此乃當害而利，當利而反害者，何耶。況天道好謙而惡盈，與善而惡惡。是則為惡者，當惡而不惡，斯豈報應差舛耶。世皆疑之。故解之曰，天之所惡，孰能知其故。故，所以然也。孔子曰，無求生以害仁，有殺身以成仁。由此觀之，生存而仁害，雖生亦死。身滅而仁成，雖死亦生。斯則蹠非壽，顏非夭矣。此乃天道所以然之妙，而非世人所易知。是以聖人於此猶難之，不敢輕忽，而敬畏之。所謂畏天之威，於時保之也。故下文歷示天道之所以。逆天者亡，故不爭而善勝。感應冥符，故不言而善應。吉凶禍福如影響，故不召而自來。然報愈遲，而惡愈深，禍愈慘，故繟然而善謀。以報速者有所警，報緩則不及悔，必至盡絕而後已。此所謂善謀也。是則天道昭昭在上，如網之四張，雖恢恢廣大，似乎疏闊。其實善惡感應，毫髮不遺。此所謂疏而不失也。世人不知天命之如此，乃以敢以強以爭競於名利之場。將謂一身之謀，不顧利害死生而為之，自謂智力以致之。蓋不知命之過，皆取死之道也。可不畏哉。",
    57: "此承上章天道無言，而賞罰不遺，以明治天下者當敬天保民，不可有心尚殺以傷慈也。治天下者，不知天道，動尚刑威，是以死懼民也。老子因而欺之曰，民不畏死，奈何以死懼之耶。以愚民無知，但為養生口體之故。或因利而行劫奪，或貪欲而嗜酒色。明知曰蹈死亡，而安心為之，是不畏死也。如此者眾，豈得人人而盡殺之耶。若民果有畏死之心，但凡有為奇詭之行者，吾執一人而殺之，則足以禁天下之暴矣。如此，誰又敢為不法耶。民既不畏死，殺之無益，適足以傷慈耳。夫天之生民，必有以養之。而人不知天，不安命，橫肆貪欲以養生。甚至不顧利害，而無忌憚以作惡，是乃不畏天威。天道昭昭，必將有以殺之矣。是居常自有司殺者殺，無庸有心以殺之也。所謂天生天殺，道之理也。今夫人主，操生殺之權，乃代天之威以保民者。若民惡貫盈，天必殺之。人主代天以行殺，故云代司殺者殺，如代大匠斲也。且天鑑昭明，毫髮不爽。其於殺也，運無心以合度，揮神斤以巧裁。不疾不徐，故如大匠之斲，運斤成風而不傷鋒犯手。至若代大匠斲者，希有不傷手矣。何也，夫有心之殺，乃嗜殺也。嗜殺傷慈。且天之司殺，實為好生。然天好生，而人好殺，是不畏天而悖之，反取其殃。此所以為自傷其手也。孟子曰，不嗜殺人者能一之，此語深得老子之餘意。故軻力排楊墨，而不及老莊，良有以焉。至哉仁人之言也。",
    58: "此釋上章民不畏死之所以，教治天下者當以淡泊無欲為本也。凡厥有生，以食為命。故無君子莫治野人，無野人莫養君子，是則上下同一命根也。然在上之食，必取稅下民。一夫之耕，不足以養父母妻子。若取之有制，猶可免於飢寒。若取之太多，則奪民之食以自奉，使民不免於死亡。凡賊盜起於飢寒也。民既飢矣，求生不得，而必至於奸盜詐偽，無敢為者。雖有大威，亦不畏之矣。是則民之為盜，由上有以驅之也。既驅民以致盜，然後用智術法以治之。故法令茲彰，盜賊多有，此民所以愈難治。雖有斧銳之誅，民將輕死而犯之矣。由是推之，民之輕死，良由在上求生之厚以致之，非別故也。厚，重也。此句影前當有一上字，方盡其妙。然重於求生，以但知生之可貴，而以養生為事，不知有生之主。苟知養生之主，則自不見有身之可愛，有生之可貴。欲自消而心自靜，天下治矣。所謂我無為而民自化，我好靜而民自正，我無事而民自富，我無欲而民自樸。故曰夫惟無以生為者，是賢於貴生。賢，猶勝也。此中妙處，難盡形容。當熟讀莊子養生主，馬蹄胠篋諸篇，便是注解。又當通前四章反復參玩，方見老子喫緊處。若能知養生之主，則自不見有身之可愛，有生之可貴。欲自消而心自靜，天下治矣。所謂我無為而民自化，我好靜而民自正，我無事而民自富，我無欲而民自樸。故曰夫惟無以生為者，是賢於貴生。賢，猶勝也。此中妙處，難盡形容。當熟讀莊子養生主，馬蹄胠篋諸篇，便是注解。又當通前四章反復參玩，方見老子喫緊處。",
    59: "此章傷世人之難化，欲在上者當先自化，而後可以化民也。結句乃本意，上文皆借喻以明之耳。經曰，此土眾生，其性剛強，難調難化。故老子專以虛心無為不敢，為立教之本。全篇上下，專尚柔弱而斥剛強。故此云，堅強者死之徒，柔弱者生之徒，乃借人物草木為喻。是以兵喻戒懼，言兵若臨事而懼，不敢輕敵，故能全師以自勝。是以全生為上，而多死為下也。木之枝條，以沖氣為和。故欣欣向榮，而生意自見。是以虛心柔弱在上。若成拱把，則麤幹堅強者在下矣。以此足知戒懼虛心，柔弱翕受者，方可處於民上也。若夫堅強自用，敢於好為，則終無有生意矣。此語大可畏哉。",
    60: "此言天道之妙，以明聖人法天以制用也。弓之為物，本弣高而有餘，弰下而不足，乃弛而不用也。及張而用之，則抑高舉下，損弣有餘之力，以補弰之不足。上下均停，然後巧於中的。否則由基逢蒙，無所施其巧矣。天之道亦猶是也。以其但施而不受，皆損一氣之有餘，以補萬物之不足，均調適可，故各遂其生。人道但受而不施，故人主以天下奉一己。皆損百姓之不足，以補一人之有餘，裒寡益多，故民不堪其命。誰能損有餘以奉天下哉。唯有道者，達性分之至足，一身之外皆餘物也。故堯舜有天下而不與，即以所養而養民，乃能以有餘奉不足也。是以聖人與道為一，與天為徒。故法天制用，雖為而不恃其能，雖成而不居其功，此損之至也。損之至，故天下樂推而不厭。雖不欲見賢，不可得也。其不欲見賢耶一句，謂我心本不欲見賢，而人自以我為賢矣。此益也，由損而至。故唯天為大，唯堯則之，此之謂也。",
    61: "此言無為之益，福利於民，反顯有為之害也。凡治大國，以安靜無擾為主，行其所無事，則民自安居樂業，而蒙其福利矣。故曰若烹小鮮。烹小鮮，則不可撓。撓，則靡爛而不全矣。治民亦然。夫虐政害民，災害並至，民受其殃。不知為政之道，乃以鬼神為厲而傷人，反以祭祀以要其福。其實君人者不道所致也。若以道德君臨天下，則和氣致祥，雖有鬼而亦不神矣。不神，謂不能為禍福也。且鬼神非無，然洋洋乎如在其上，如在其左右，豈不昭格於上下耶。第雖靈爽赫然，但只為民之福，不為民害。故曰非其鬼不神，但其神不傷人耳。然非其神不傷人，實由聖人含哺百姓，如保赤子。與天地合其德，鬼神合其吉凶，而絕無傷民之意，故鬼神協和而致福也。故曰非其神不傷人，聖人亦不傷之。如湯之時，七年大旱。湯以身代犧牲，藉茅以禱，致雨三尺。故民皆以湯王克誠感格所致，斯蓋由夫兩不相傷，故其德交歸焉。此無為之德，福民如此。",
    62: "此言君天下者，當以靜勝為主，不可以力相尚也。夫流之在下者，如江海，眾水歸之。故大國之在天下，眾望歸之。故如流之在下，以為天下之交。納汙含垢，無所不容。又虛而能受，如天下之牝也。凡物之雌曰牝，雄曰牡，牡動而牝靜。動則不育，靜能有生，是牝以靜勝牡也。以此譬喻聖人之德。然聖人為天下牝者。以天下之人，衣食皆賴之以生，爵祿皆賴之以榮，萬幾並集於一人。故君道無為，而皆任其所欲，各遂其所生。所謂萬物皆往資焉而不匱，此似牝以靜勝牡也。是則靜為群動之歸趨，故以靜為下。大字小，如母育子。小事大，如子奉母。精神相孚，相得最易，故如掇之也。然大字小，必有所容。故曰或下以取。以，猶左右之也。小事大，必有所忍。故曰或下而取。而，因而取之也。皆無妄動之過，故交歸焉。且大國之欲，不過兼畜人，非容無以成其大。小國之欲，不過入事人，非忍無以濟其事。兩者既各得其所欲，而大者更宜下。何也。以大國素尊，難於下耳，故特勉之。此老子見當時諸侯，專於征伐，以力不以德，知動不知靜，徒見相服之難，而不知下之一字，為至簡之術。蓋傷時之論也。",
    63: "此言道之為貴，誡人當勉力求之也。道者，萬物之奧。奧者，室之西南隅。有室必有奧。但人雖居其室，而不知奧之深邃。以譬道在萬物，施之日用尋常之間，人日用而不知，故如奧也。然道既在萬物，足知人性皆同。雖有善惡之差，而性未嘗異，以其俗習之偏耳。故善人得之以為寶。惡人雖失，亦賴此道保之以有生。故曰所保。苟非其道以保之，則同無情瓦石矣。足見理本同也，所謂堯舜與人同耳。由此觀之，天下豈有可棄之人耶。且一言之美，則可以市。市，利也。一行之尊，則可以加於人之上。況大道之貴，豈止一言之美，一行之尊。且人之全具而不欠缺一毫者，斯則不善之人，又何棄之有耶。故立天子，置三公，雖有拱璧以先駟馬，不如坐進此道，此古語也。老子解之曰，然天子三公，不足為尊貴。拱璧駟馬，不足為榮觀。總不如坐進此道。所以貴此道者，何耶。豈不曰，求道以得之，縱有罪亦可以免之耶。是知桀紂，天子也，不免其誅。四凶，三公也，不免其戮。非無拱璧駟馬，而竟不能免其罪。故夷齊諫武王而不兵，巢許傲天子而不譴，豈非求以得有罪以免耶。況夫一念復真，諸罪頓滅。苟求而得，立地超凡。故為天下貴也。",
    64: "此言聖人入道之要妙，示人以真切工夫也。凡有為，謂智巧。有事，謂功業。有味，謂功名利欲。此三者，皆世人之所尚。然道本至虛而無為。至靜而無事。至淡而無味。獨聖人以道為懷，去彼取此。故所為者無為。所事者無事。所味者無味。故世人皆以名位為大，以利祿為多而取之。然道至虛微淡泊無物，皆以為小少，故棄而不取。聖人去功與名，釋智遺形，而獨與道游。是去其大多，而取其小少。故至小為至大，至少為至多。故大其小，而多其少也。試觀世人報怨以德，則可知矣。何也。且世之人，無論貴賤，事最大而難解者，怨也。然怨之始也，偶因一言之失，一事之差。遂相搆結，以至殺身滅名，亡國敗家之禍。甚至有積怨深憤，父子子孫，累世相報而未已者。此舉世古今之恆情也。豈非其事極大且多哉。惟聖人則不然。察其怨之未結也，本不有。始結也，事甚小。既結也，以為無與於己。故無固執不化之心，亦無有我以與物為匹敵。其既往也，事已消之，求其朕而不可得。以此觀之，則任彼之怨，在我了無報之之心矣。然彼且以為有怨，在我全無報復之心，彼必以我為德矣。是所謂報怨以德，非謂曲意將德以報怨也。孔子以直報怨，正謂此耳。斯則怨乃事之至大而多，人人必有難釋者。殊不知有至易者存焉。是所謂為無為，事無事，大其小，而多其少也。天下之事，何獨於怨，而事事皆然。故天下之事至難者，有至易存焉。至大者，有至細存焉。人不見其易與細，而於難處圖之，大處為之，必終無成。苟能圖之於易，而為之於細，鮮不濟者。以天下難事必作於易。天下大事必作於細，故也。作者，始起也。是以聖人虛心體道，退藏於密。跡愈隱而道愈光，澤流終古而與天地參。此所謂終不為大，故能成其大也。老子言及至此，抑恐世人把易字當作容易輕易字看。故誡之曰，夫輕諾必寡信，多易必多難。謂世人不可將事作容易看也。且容易許人，謂之輕諾。凡輕許者，必食言而寡信。見事之容易而輕為者，必有始而無終。是故易字，非容易也。世人之所難，而聖人之所易。世人之所易，而聖人之所難。故曰聖人猶難之，故終無難。猶，應作尤。古字通用。更也。謂世人之所甚易者，而聖人更難之，故終不難耳。觀夫文王兢兢，周公業業，戒慎恐懼乎不睹不聞，皆聖人之所難也。余少誦圖難於易為大於細二語，只把作事看。及余入山學道，初為極難，苦心不可言。及得用心之訣，則見其甚易。然初之難，即今之易。今之易，即初之難。然治心如此，推之以及天下之事皆然。此聖人示人入道之真切工夫也。志道者勉之。",
    65: "此釋上章圖難於易為大於細之意，以示聖人之要妙，只在為人之所不為，以為學道之捷徑也。治人事天工夫，全在於此。安與未兆。蓋一念不生。喜怒未形。寂然不動之時。吉凶未見之地。乃禍福之先。所謂幾先也。持字，全是用心力量。謂聖人尋常心心念念，朗然照於一念未生之前，持之不失。此中但有一念動作，當下就見就知。是善則容，是惡則止，所謂早復。孔子所謂知幾其神乎。此中下手甚易，用力少而收功多。故曰其安易持。兆，是念之初起。未兆，即未起。此中喜怒未形，而言謀者。此謀，非機謀之謀，乃戒慎恐懼之意。於此著力，圖其早復。蓋第一念為之於未有也。若脆與微，乃一念始萌，乃第二念耳。然一念雖動，善惡未著，甚脆且微。於此著力，所謂治之於未亂也。合抱之木以下，三句皆譬喻。毫末，喻最初一念。累土足下，喻最初一步工夫也。上言用心於內，下言作事於外。為執二句，言常人不知著力於未然之前，卻在既發之後用心。為之則反敗，執之則反失矣。聖人見在幾先，安然於無事之時，故無所為，而亦無所敗。虛心鑒照，故無所執，而亦無所失。以其聖人因理以達事耳。常民不知在心上做，卻從事上做，費盡許多力氣，且每至於幾成而敗之。此特機巧智謀，有心做來，不但不成，縱成亦不能久，以不知聽其自然耳。慎終如始。始，乃事之初。終，乃事之成。天下之事，縱然盈乎天地之間。聖人之見，察其始也本來不有。以本不有，故將有也，任其自然，而無作為之心。及其終也，事雖已成，觀之亦似未成之始，亦無固執不化之念，此所謂慎終如始，故無敗事也。是以聖人欲不欲，不貴難得之貨。學不學，復眾人之所過。以輔萬物之自然。而不敢為。莊子內聖外王學問，全出於此。吾人日用明此，可以坐進此道。以此用世，則功大名顯。伊周事業，特緒餘耳。豈不至易哉。",
    66: "此言聖人治國之要，當以樸實為本，不可以智誇民也。明者，昭然揭示之意。愚者，民可使由之，不可使知之之意。夫民之所趨，皆觀望於上也，所謂百姓皆注其耳目。凡民之欲蔽，皆上有以啟之。故上有好者，下必有甚焉者也。故聖人在上，善能以斯道覺斯民，當先身以教之。上先不用智巧，離欲清淨，一無所好，若無所知者。則民自各安其日用之常，絕無一念好尚之心。而黠滑之智自消，奸盜之行自絕矣。所謂我好靜而民自正，我無為而民自化。故曰非以明民，將以愚之。此重在以字。前云眾人皆有以。以，如春秋以某師之以。謂左右之也。此其上不用智，故民易治耳。然民之難治者，皆用智之過也。足知以智治國者，反為害也，乃國之賊。不用智而民自安，則為國之福矣。人能知此兩者，可為治國之楷式也。楷式，好規模也。苟能知此楷式，是謂之玄德矣。玄德，謂德之玄妙，而人不測識也。故歎之曰，玄德深矣遠矣。非淺識者所可知也。民之欲，火馳而不返。唯以此化民，則民自然日與物相反，而大順於妙道之域矣。語曰，齊一變至於魯，魯一變至於道，猶有智也。況玄德乎。",
    67: "此教君天下者，以無我之德，故天下歸之如水之就下也。百川之水，不拘淨穢，總歸於江海。江海而能容納之，以其善下也。此喻聖人在上，天下歸之，以其無我也。欲上民，必以言下之。言者，心之聲也。故君天下者，尊為天子。聖人虛心應物，而不見其尊，故凡出言必謙下。如日孤寡不穀，不以尊陵天下也。欲先人，必以身後之。身者，心之表也。君天下者，貴為天子，天下推之以為先。聖人忘己與人，而不自見有其貴。故凡於物欲，澹然無所嗜好，不以一己之養害天下也。重者，猶不堪也。是則聖人之心，有天下而不與。故雖處上，而民自堪命，不以為重。雖處前，而民自遂生，不以為害。此所以天下樂推而不厭。蓋無我之至，乃不爭之德也。此爭非爭鬥之謂，蓋言心不馳競於物也。以其不爭，故天下莫能與之爭。莊子所謂兼忘天下易，使天下忘己難。此則能使天下忘己，故莫能與之爭耳。",
    68: "此章老子自言所得之道至大，世人不知，其實所守者至約也。道大，如巍巍乎惟天為大，蕩蕩乎民無稱焉，言其廣大難以名狀也。不肖，如孔子云不器。大史公謂孟子迂遠而不切於事情之意。即莊子所謂大有徑庭，不近人情也。此蓋當時人見老子其道廣大，皆如下文所云，以勇廣器長稱之，且不得而名，故又為不肖，即若孔子稱之猶龍也。故老子因時人之言，乃自解之曰，天下人皆謂我之道大，似乎不肖，無所可用。惟其大，所以似不肖耳。肖者，與物相似。如俗云一樣也。若肖，作一句。久矣其細，作一句。倒文法耳。謂我若是與世人一樣，則成細人久矣，又安得以道大稱之哉。下文釋其大之所以。謂世人皆見其物莫能勝我，遂以我為勇。見我寬裕有餘，遂以我為廣。見其人皆推我為第一等人，遂以我為器長。器者，人物之通稱也。以此故，皆謂我道大，其實似無所肖。殊不知我所守者至約。乃慈，儉，不敢為天下先，三法而已。慈者，并包萬物，覆育不遺，如慈母之育嬰兒。儉者，嗇也，有而不敢盡用。不敢為天下先者，虛懷游世，無我而不與物對。然以慈育物，物物皆己。且無己與物敵，物自莫能勝矣。故曰慈故能勇。心常自足，雖有餘而不用，所處無不裕然寬大矣。故曰儉故能廣。物我兩忘，超然獨立，而不見有己以處人前。故人皆以我為畸人，推為人中之最上者矣。故曰不敢為天下先，故能成器長。以此故，皆以我為道大似不肖耳。以我所守者如此，即前所云我獨異於人，而貴求食於母也。以此三者，乃大道之要妙耳。且今世人，捨慈而言勇，捨儉而言廣，捨後而言先，死矣。此死字，非生死之死，如禪家所云死在句下。蓋死活之死，言其無生意也。以世人不知大道之妙，但以血氣誇侈爭勝做工夫。故一毫沒用頭，皆死法，非活法也。且此三者之中，又以慈為主。不但學道，即治天下國家莫不皆然。若以戰則勝，以守則固，故王師無敵，民效死而勿去，皆仁慈素有所孚，故為戰勝守固之道。此所謂道之真以治身，其緒餘以為天下國家。以天地之大德曰生。故天將救斯民，而純以慈衛之。故聖人法天利用，而以慈為第一也，世俗惡足以知之。故知治世能用老氏之術，坐觀三代之化。所以漢之文景，得糟粕之餘，施於治道，迴超百代耳。此老子言言皆真實工夫，切於人事，故云甚易知易行。學人視太高，類以虛玄談之，不能身體而力行，故不得其受用耳。惜哉。",
    69: "此言聖人善於下人，以明不爭之德，釋上三寶之意也。一章主意，只在善用人者為之下一句。乃假兵家戰勝之事，以形容其慈，乃不爭之至耳。士者，介胄之士。武者，武勇。然士以武為主。戰以怒為主。勝敵以爭為主。三者又以氣為主。況善於為士者不用武。善於戰者不在怒。善勝敵者不必爭。即前所云以慈用兵也。意謂武怒爭三者，獨兵事所必用。若用之而必死，故善者皆不用。何況常人，豈可恃之以為用耶。乃驕矜恃氣，不肯下人，故人不樂其用，乃不善用人耳。故古之善用人者，必為之下，即此是謂不爭之德也。若以力驅人，能驅幾何。若以下驅人，則天下歸之。是以下用人，最有力也。所謂上善若水，水善利萬物而不爭，以其有力也。是謂配天古之極者。乾天，坤地。若天地正位，則為否，而萬物不生。若乾下坤上，則為泰。是知天在上而用在下也。聖人處民上而心在下，可謂配天之德。此古皇維極之道，置百姓於熙皞至樂之中。斯豈不爭之德以治天下，而為力之大者與。此章主意，全在不用氣上做工夫。即前云專氣致柔，能如嬰兒。純和之至，則形化而心忘。不見物為對，則不期下而自下矣。殆非有心要下，而為用人之術也。然學人有志於謙德，則必尊而光，況聖人無我之至乎。",
    70: "此重明前章不爭之德，以釋上三寶以慈為本之意也。然慈，乃至仁之全德也。所謂大仁不仁。以其物我兼忘，內不見有施仁之心，外不見有受施之地。故凡應物而動，皆非出於有心好為，蓋迫不得已而後應。故借用兵以明慈德之至也。何以知之。且如古之用兵者有言曰，吾不敢為主而為客，不敢進寸而退尺。以此觀之，足可知也。古之用兵，如涿鹿孟津之師是也。兵主，如春秋征伐之盟主。蓋專征伐，主於兵者，言以必爭必殺為主也。客，如諸侯應援之師。本意絕無好殺之心。今雖迫不得已而應之，然亦聽之待之，若可已則已。以無心於功利，故絕無爭心，所以進之難而退之易。故曰不敢進寸而退尺。言身進而心不進，是以退心進也。以無爭心，故雖行而如不在行陣，雖攘而若無臂之人。仍，相仍，猶就也。言彼以我為敵，而我以彼為敵也。雖就，亦似無敵可對。雖執，猶若無兵可揮。戒懼之至，而不敢輕於敵。由不敢輕敵，所以能保全民命，不傷好生之仁。然禍之大者莫大於輕敵。以輕敵則多殺，多殺則傷慈，故幾喪吾寶矣。抗兵，乃兩敵相當，不相上下，難於決勝。但有慈心哀之者，則自勝矣。何則，以天道好生，助勝於慈者也。由是觀之，兵者對敵，必爭必殺以取勝。今乃以不爭不殺而勝之，蓋以慈為本故也。足見慈乃不爭之德，施於必爭地，而以不爭勝之，豈非大有力乎。用之於敵尚如此。況乎聖人無物為敵，而以平等大慈，并包萬物，又何物而可勝之耶。故前云不爭之德，是謂用人之力，是謂配天古之極。此章舊解多在用兵上說，全不得老子主意。今觀初一句，乃借用兵之言。至輕敵喪寶，則了然明白。是釋上慈字，以明不爭之德耳。",
    71: "此章示人立言之指，使知而行之，欲其深造而自得也。老子自謂我所言者，皆人人日用中最省力一著工夫。明明白白，甚容易知，容易行。只是人不能知，不能行耳。以我言言事事，皆以大道為主，非是漫衍荒唐之說。故曰言有宗，事有君。宗，君，皆主也。且如一往所說，絕聖棄智，虛心無我，謙下不爭，忘形釋智，件件都是最省力工夫，放下便是，全不用你多知多解。只在休心二字，豈不最易知最易行耶。然人之所以不能知者，因從來人人都在知見上用心。除卻知字，便無下落。以我無知無識一著，極難湊泊，所以人不知我耳。故曰夫惟無知，是以不我知。然無知一著，不獨老子法門宗旨，即孔子亦同。如曰吾有知乎哉，無知也，有鄙夫問於我空空如也，此豈不是孔聖亦以無知為心宗耶。此夫子見老子後，方得妙悟如此。故稱猶龍，正謂此耳。然以無知契無知，如以空合空。若以有知求無知，如以水投石。所以孔老心法，千古罕明。故曰知我者希。若能當下頓悟此心，則立地便是聖人，故曰則我者貴。則，謂法則。言取法也。聖人懷此虛心妙道以遊世。則終日與人周旋，對面不識。故如披褐懷王。永嘉云，貧則身常披縷褐，道則心藏無價珍。此一章書，當在末後結束。蓋老子向上一往所言天人之蘊，至此已發露太盡，故著此語。後章只是要人在日用著力做工夫，以至妙悟而後已。",
    72: "此承上言惟無知，是以不我知。恐人錯認無知，故重指出無知之地也。然世人之知，乃敵物分別之知，有所知也。聖人之知，乃離物絕待，照體獨立之知，無所知也。故聖人之無知，非斷滅無知，乃無世人之所知耳。無所知，乃世人所不知也。世人所不知，乃聖人之獨知。人能知其所不知之地，則為上矣。故曰知不知上。若夫臆度妄見，本所不知，而強自以為知。或錯認無知為斷滅，同於木石之無知。此二者皆非真知，適足為知之病耳。故曰不知知病。若苟知此二者為知之病，則知見頓亡，可造無知之地，而無強知妄知之病矣。故曰夫惟病病，是以不病。聖人但無強妄之知，故稱無知，非是絕然斷滅無知也。故曰聖人不病。此段工夫，更無別樣玄妙。唯病其妄知強知是病而不用。是以不墮知病之中，而名無知。此無知，乃真知。苦如此真知，則終日知而無所知。斯實聖人自知之明，常人豈易知哉。此所以易知易行，而世人不能知不能行也。古云，知之一字，眾妙之門。知之一字，眾禍之門。然聖人無知之地，必假知以入。若悟無知，則妄知自泯。此乃知之一字，眾妙之門也。若執有知以求無知，則反增知障，此乃眾禍之門。正是此中知之病也。知不知上，最初知字，正是入道之要。永嘉云，所謂知者，但知而已，此句最易而難明。學者日用工夫，當從此入。",
    73: "此章教人遺形去欲，為入道之工夫，以造聖人無知之地也。凜然赫然而可畏者，謂之威。如云寒威，炎威，是也。是則凡可畏者，皆謂之威。唯國之大罰，與天地之肅殺，乃大威也。此借以為戕生傷性者之喻。世人以為小惡不足戒，而不知畏，必致殺身而後已。此民不畏威，大威至矣。喻世人祇知嗜欲養生，而不知養生者，皆足以害生而可畏也。且若嗜酒色，必死於酒色。嗜利欲，必死於利欲。嗜飲食，必死於飲食。是則但有所嗜，而不知畏，必至於戕生傷性而後已。此不畏威，故大威至矣。然人但知嗜而不知畏者，以其止知有身之可愛，有生之可貴，以此為足。而不知大有過於此者，性也。且吾性之廣大，與太虛同體，乃吾之真宅也。苟以性視身，則若大海之一涵，太虛之一塵耳，至微小而不足貴者。人不知此，而但以蕞爾之身。以為所居之地。將為至足，而貴愛之，則狹陋甚矣。故戒之曰，無狹其所居。狹其居者，將以此身此生為至足也。故又戒之曰，無厭其所生。厭，足也。若知此身此生之不足貴，則彼物欲固能傷生，亦不足以害我矣，以其無死地也。故曰夫惟不厭，是以不厭。厭，棄也。故聖人自知尊性，而不見生之可養。自愛遺形，而不見身之可貴。此聖人之所獨知，世人之所不知也。故去彼眾人之所知，取彼所不知，以為道之要妙耳。以此足見世人之所知者，皆病也。聖人病之而不取，故不病也。後三章互相發明此章之旨。",
    74: "此言天命可畏，報應昭然，教人不可輕忽也。勇者，決定之志也。敢者，不計利害而決於為也。殺活，死生也。謂凡世人作事，不顧利害，不怕死生，而敢為之。然敢乃必死之地。故曰勇於敢則殺。若用志於不敢為，是足以保身全生。故曰勇於不敢則活。此天道必然之理也。且此二者，亦有敢而生，不敢而死者。至若顏子夭，而盜蹤壽，此乃當害而利，當利而反害者，何耶。況天道好謙而惡盈，與善而惡惡。是則為惡者，當惡而不惡，斯豈報應差舛耶。世皆疑之。故解之曰，天之所惡，孰能知其故。故，所以然也。孔子曰，無求生以害仁，有殺身以成仁。由此觀之，生存而仁害，雖生亦死。身滅而仁成，雖死亦生。斯則蹠非壽，顏非夭矣。此乃天道所以然之妙，而非世人所易知。是以聖人於此猶難之，不敢輕忽，而敬畏之。所謂畏天之威，於時保之也。故下文歷示天道之所以。逆天者亡，故不爭而善勝。感應冥符，故不言而善應。吉凶禍福如影響，故不召而自來。然報愈遲，而惡愈深，禍愈慘，故繟然而善謀。以報速者有所警，報緩則不及悔，必至盡絕而後已。此所謂善謀也。是則天道昭昭在上，如網之四張，雖恢恢廣大，似乎疏闊。其實善惡感應，毫髮不遺。此所謂疏而不失也。世人不知天命之如此，乃以敢以強以爭競於名利之場。將謂一身之謀，不顧利害死生而為之，自謂智力以致之。蓋不知命之過，皆取死之道也。可不畏哉。",
    75: "此承上章天道無言，而賞罰不遺，以明治天下者當敬天保民，不可有心尚殺以傷慈也。治天下者，不知天道，動尚刑威，是以死懼民也。老子因而欺之曰，民不畏死，奈何以死懼之耶。以愚民無知，但為養生口體之故。或因利而行劫奪，或貪欲而嗜酒色。明知曰蹈死亡，而安心為之，是不畏死也。如此者眾，豈得人人而盡殺之耶。若民果有畏死之心，但凡有為奇詭之行者，吾執一人而殺之，則足以禁天下之暴矣。如此，誰又敢為不法耶。民既不畏死，殺之無益，適足以傷慈耳。夫天之生民，必有以養之。而人不知天，不安命，橫肆貪欲以養生。甚至不顧利害，而無忌憚以作惡，是乃不畏天威。天道昭昭，必將有以殺之矣。是居常自有司殺者殺，無庸有心以殺之也。所謂天生天殺，道之理也。今夫人主，操生殺之權，乃代天之威以保民者。若民惡貫盈，天必殺之。人主代天以行殺，故云代司殺者殺，如代大匠斲也。且天鑑昭明，毫髮不爽。其於殺也，運無心以合度，揮神斤以巧裁。不疾不徐，故如大匠之斲，運斤成風而不傷鋒犯手。至若代大匠斲者，希有不傷手矣。何也，夫有心之殺，乃嗜殺也。嗜殺傷慈。且天之司殺，實為好生。然天好生，而人好殺，是不畏天而悖之，反取其殃。此所以為自傷其手也。孟子曰，不嗜殺人者能一之，此語深得老子之餘意。故軻力排楊墨，而不及老莊，良有以焉。至哉仁人之言也。",
    76: "此釋上章民不畏死之所以，教治天下者當以淡泊無欲為本也。凡厥有生，以食為命。故無君子莫治野人，無野人莫養君子，是則上下同一命根也。然在上之食，必取稅下民。一夫之耕，不足以養父母妻子。若取之有制，猶可免於飢寒。若取之太多，則奪民之食以自奉，使民不免於死亡。凡賊盜起於飢寒也。民既飢矣，求生不得，而必至於奸盜詐偽，無敢為之者。雖有大威，亦不畏之矣。是則民之為盜，由上有以驅之也。既驅民以致盜，然後用智術法以治之。故法令茲彰，盜賊多有，此民所以愈難治。雖有斧銳之誅，民將輕死而犯之矣。由是推之，民之輕死，良由在上求生之厚以致之，非別故也。厚，重也。此句影前當有一上字，方盡其妙。然重於求生，以但知生之可貴，而以養生為事，不知有生之主。苟知養生之主，則自不見有身之可愛，有生之可貴。欲自消而心自靜，天下治矣。所謂我無為而民自化，我好靜而民自正，我無事而民自富，我無欲而民自樸。故曰夫惟無以生為者，是賢於貴生。賢，猶勝也。此中妙處，難盡形容。當熟讀莊子養生主，馬蹄胠篋諸篇，便是注解。又當通前四章反復參玩，方見老子喫緊處。",
    77: "此章傷世人之難化，欲在上者當先自化，而後可以化民也。結句乃本意，上文皆借喻以明之耳。經曰，此土眾生，其性剛強，難調難化。故老子專以虛心無為不敢，為立教之本。全篇上下，專尚柔弱而斥剛強。故此云，堅強者死之徒，柔弱者生之徒，乃借人物草木為喻。是以兵喻戒懼，言兵若臨事而懼，不敢輕敵，故能全師以自勝。是以全生為上，而多死為下也。木之枝條，以沖氣為和。故欣欣向榮，而生意自見。是以虛心柔弱在上。若成拱把，則麤幹堅強者在下矣。以此足知戒懼虛心，柔弱翕受者，方可處於民上也。若夫堅強自用，敢於好為，則終無有生意矣。此語大可畏哉。",
    78: "此言天道之妙，以明聖人法天以制用也。弓之為物，本弣高而有餘，弰下而不足，乃弛而不用也。及張而用之，則抑高舉下，損弣有餘之力，以補弰之不足。上下均停，然後巧於中的。否則由基逢蒙，無所施其巧矣。天之道亦猶是也。以其但施而不受，皆損一氣之有餘，以補萬物之不足，均調適可，故各遂其生。人道但受而不施，故人主以天下奉一己。皆損百姓之不足，以補一人之有餘，裒寡益多，故民不堪其命。誰能損有餘以奉天下哉。唯有道者，達性分之至足，一身之外皆餘物也。故堯舜有天下而不與，即以所養而養民，乃能以有餘奉不足也。是以聖人與道為一，與天為徒。故法天制用，雖為而不恃其能，雖成而不居其功，此損之至也。損之至，故天下樂推而不厭。雖不欲見賢，不可得也。其不欲見賢耶一句，謂我心本不欲見賢，而人自以我為賢矣。此益也，由損而至。故唯天為大，唯堯則之，此之謂也。",
    79: "此結通篇柔弱之意，欲人知而能行也。無以易之。易，輕易也。即左傳訓師無易敵之易。謂師之柔弱，則敵人有以料而易之以取勝。至若水之柔弱，則人莫能料。莫能料，故無以易之，而卒莫能以取勝。此所以攻堅強者莫之能先。莫能先，謂無有過於此也。世人皆以柔弱為不足取，率輕易之。故天下皆知之而莫能行，以柔弱為垢辱不美之稱故也。祥，猶嘉美也。是以凡稱人君，則曰乾剛能斷有為，遂以為明君。若夫無為，則國人皆以柔弱為恥辱而不美矣。故聖人云，果能以柔弱處上，恬澹無為，能受一國之恥垢者，則為社稷真主。能受一國不美之名者，則為天下明王矣。如堯之垂拱無為，則野老謳曰，帝力何有於我哉。此受國之垢也。然柔弱無為，乃合道之正言，但世俗以為反耳。",
    80: "此言聖人無心之恩，但施而不責報，此為當時計利者發也。然恩生於怨，怨生於恩。當時諸侯兩相搆怨，霸者主盟而為和之。大怨既和，而必責報。報之不至，而怨亦隨之，是有餘怨也。莊子云，賊莫大於德有心。故曰安可以為善。是以聖人無心之德，但施而不責報。故如貸之執左契，雖有而若無也。契，貸物之符券也。合同剖之，而有左右。貸者執右，物主執左，所以責其報也。有德司契，但與而不取，徒存虛契。無德司徹，不計彼之有無，必征其餘，如賦徹耳。徹，周之賦法。謂時至必取於民，而無一毫假借之意。然上責報而下計利，將謂與而不取，為失利也。殊不知失於人，而得於天。故曰天道無親，常與善人。且施而不取，我既善矣。人不與而天必與之，所謂自天佑之，吉無不利。豈常人所易知哉。",
    81: "此結通篇無為之益，施於治道，可復太古之化也。什伯之器，並十曰什，兼百曰伯。器，材也。老子自謂以我無為之治，試於小國。縱使有兼十夫百夫之材者，亦無所用之，以民淳而無事故也。若國多事，煩擾於民。或窮兵致亂，重賦致饑。民不安其居，則輕死而去之。今一切無之，故使民重死，而不遠徙。舟輿，水陸之具。不遠徙，故雖有舟車無所用。不尚爭，故雖有甲兵無所陳。陳，列也。不用智，故可使結繩而用之如太古矣。民各自足其足，絕無外慕之心。不事口體，故以尋常衣食為甘美，以平居里俗為安樂，曰與鄰國雞狗相聞。至近之地，民至老死而不相往來。如此，則淳樸之至，乃太古之化也。老子所言，疾當時之弊，皆有為用智剛強，好爭尚利，自私奉己，而不恤於民。故國亂民貧，而愈難治。所以治推上古，道合無為，全篇所論，不出乎此，蓋立言之本旨也。故終篇以此，請試而行之，可以頓見太古鴻荒之化。言取效之速如此也。所謂一日克己復禮，天下歸仁，深有味乎此言也。老氏之學，豈矯世絕俗之謂哉。",
}


def create_remaining_chapters():
    """生成第11-81章的基础数据结构"""
    remaining_chapters = []

    # 第11-37章完整原文
    chapters_full_text = [
        (11, "三十辐共一毂，当其无，有车之用。埏埴以为器，当其无，有器之用。凿户牖以为室，当其无，有室之用。故有之以为利，无之以为用。",
         "三十根辐条汇集到一个毂中，正是因为有了毂中的空虚，车才能发挥作用。揉和陶土做成器具，正是因为有了器具中间的空虚，器具才能发挥作用。开凿门窗建造房屋，正是因为有了门窗四壁中间的空虚，房屋才能发挥作用。所以，有给人以便利，无发挥了它的作用。"),

        (12, "五色令人目盲，五音令人耳聋，五味令人口爽，驰骋畋猎令人心发狂，难得之货令人行妨。是以圣人为腹不为目，故去彼取此。",
         "缤纷的色彩使人眼花缭乱；嘈杂的音乐使人耳朵失聪；丰美的食物使人口舌麻木；纵情骑马打猎使人心情放荡发狂；稀有的物品使人行为不轨。因此，圣人只求饱腹而不求声色娱目，所以摒弃物欲的诱惑，保持内心的安宁。"),

        (13, "宠辱若惊，贵大患若身。何谓宠辱若惊？宠为下，得之若惊，失之若惊，是谓宠辱若惊。何谓贵大患若身？吾所以有大患者，为吾有身，及吾无身，吾有何患？故贵以身为天下，若可寄天下；爱以身为天下，若可托天下。",
         "受到宠爱和受到侮辱好像都感到惊恐，把宠辱看得像生命一样重要。什么叫宠辱若惊？得宠是卑下的，得到宠爱感到惊恐，失去宠爱也感到惊恐，这就叫宠辱若惊。什么叫贵大患若身？我所以有大的祸患，是因为我有身体；如果我没有身体，我有什么祸患呢？所以珍贵自己的身体是为了治理天下，天下就可以托付他；爱惜自己的身体是为了治理天下，天下就可以依靠他。"),

        (14, "视之不见，名曰夷；听之不闻，名曰希；搏之不得，名曰微。此三者不可致诘，故混而为一。其上不皦，其下不昧。绳绳兮不可名，复归于无物。是谓无状之状，无物之象，是谓惚恍。迎之不见其首，随之不见其后。执古之道，以御今之有。能知古始，是谓道纪。",
         "看它看不见，叫作夷；听它听不到，叫作希；摸它摸不着，叫作微。这三者的形状无从追究，它们原本就浑然而为一。它的上面既不显得明亮，它的下面也不显得昏暗。它绵延不绝而又不可名状，又总要回到看不见物体的虚无状态。这是没有形状的形状，没有物体的形象，叫作惚恍。迎着它，看不见它的头；跟着它，看不见它的尾。运用自古以来的道，来驾驭现在的具体事物。能了解远古开始的事物，这就叫作道的规律。"),

        (15, "古之善为士者，微妙玄通，深不可识。夫唯不可识，故强为之容：豫兮若冬涉川，犹兮若畏四邻，俨兮其若客，涣兮其若冰之将释，敦兮其若朴，旷兮其若谷，混兮其若浊。孰能浊以静之徐清？孰能安以动之徐生？保此道者，不欲盈。夫唯不盈，故能蔽不新成。",
         "古代善于为士的人，微妙玄妙，深奥通达，深刻得无法认识。正因为无法认识，所以只能勉强地形容他：小心谨慎啊，像冬天踩冰过河；警惕疑虑啊，像提防四邻围攻；恭敬庄重啊，像在做客；融化和顺啊，像冰块将要融化；淳厚朴实啊，像未经雕琢的素材；空旷开阔啊，像深山幽谷；浑厚宽容啊，像浑浊的流水。谁能够使浑浊安静下来慢慢澄清？谁能够使安静变动起来慢慢显出生机？保持这个道的人，不要求圆满。正因为不要求圆满，所以虽破旧却不会败坏，不需要更新。"),

        (16, "致虚极，守静笃。万物并作，吾以观复。夫物芸芸，各复归其根。归根曰静，静曰复命。复命曰常，知常曰明。不知常，妄作凶。知常容，容乃公，公乃王，王乃天，天乃道，道乃久，没身不殆。",
         "努力使心灵虚空到极点，坚守清静到极致。万物都在蓬勃生长，我由此观察到了循环往复的道理。万物纷繁茂盛，最终各自返回到它们的本根。返回本根叫作静，静叫作复命。复命叫作常，认识了常叫作明。不认识常，轻举妄动就会遇到凶险。认识了常才能包容，包容才能公正，公正才能称王，称王才能顺应天，顺应天才能符合道，符合道才能长久，终身没有危险。"),

        (17, "太上，不知有之；其次，亲而誉之；其次，畏之；其次，侮之。信不足焉，有不信焉。悠兮其贵言。功成事遂，百姓皆谓我自然。",
         "最好的统治者，人民并不知道他的存在；其次的统治者，人民亲近他并且称赞他；再次的统治者，人民畏惧他；更次的统治者，人民轻蔑他。统治者的诚信不足，人民才不相信他。最好的统治者是多么悠闲，他很少发号施令。功业成就了，百姓都说：我们本来就是这样的。"),

        (18, "大道废，有仁义；智慧出，有大伪；六亲不和，有孝慈；国家昏乱，有忠臣。",
         "大道被废弃了，才有仁义；智慧出现了，才有大的虚伪；家庭不和了，才显出孝慈；国家昏乱了，才有忠臣。"),

        (19, "绝圣弃智，民利百倍；绝仁弃义，民复孝慈；绝巧弃利，盗贼无有。此三者以为文，不足。故令有所属：见素抱朴，少私寡欲，绝学无忧。",
         "抛弃聪明智巧，人民可以得到百倍的好处；抛弃仁义，人民可以恢复孝慈的天性；抛弃巧诈和私利，盗贼也就没有了。圣智、仁义、巧利这三者全是巧饰，作为治理社会的法则是不够的。所以要使人们的认识有所归属：表现单纯，持守朴素，减少私欲，抛弃学问，没有忧愁。"),

        (20, "唯之与阿，相去几何？善之与恶，相去若何？人之所畏，不可不畏。荒兮，其未央哉！众人熙熙，如享太牢，如春登台。我独泊兮，其未兆；沌兮，如婴儿之未孩；儽儽兮，若无所归。众人皆有余，而我独若遗。我愚人之心也哉！俗人昭昭，我独昏昏；俗人察察，我独闷闷。澹兮其若海，飂兮若无止。众人皆有以，而我独顽似鄙。我独异于人，而贵食母。",
         "应诺和呵斥，相差有多远？美好和丑恶，相差有多远？别人所畏惧的，我也不能不畏惧。这风气从远古以来就是如此，好像没有尽头的样子！众人都兴高采烈，好像去参加盛大的宴席，好像春天登台眺望美景。而我却独自淡泊宁静，无动于衷；混混沌沌，好像还不会笑的婴儿；疲惫懒散，好像无家可归。众人都有余裕，而我却好像不足。我真是只有一颗愚人的心啊！众人都光辉自炫，唯独我昏昏糊糊；众人都严厉苛刻，唯独我淳朴宽宏。恍惚啊，像大海汹涌；飘逸啊，像无处停留。众人都精明灵巧，唯独我愚昧笨拙。我唯独与人不同，而重视用道来滋养自己。"),

        (21, "孔德之容，惟道是从。道之为物，惟恍惟惚。惚兮恍兮，其中有象；恍兮惚兮，其中有物。窈兮冥兮，其中有精；其精甚真，其中有信。自今及古，其名不去，以阅众甫。吾何以知众甫之状哉？以此。",
         "大德的形态，是跟随道而变化的。道这个东西，是恍恍惚惚的。那样的惚啊恍啊，其中有形象；那样的恍啊惚啊，其中有实物。它是那样的深远幽暗啊，其中有精神；这精神是非常真实的，其中有信验。从今天上溯到古代，它的名字永远不消失，根据它才能观察万物的初始。我怎么知道万物开始的情况呢？就是根据这个道。"),

        (22, "曲则全，枉则直，洼则盈，敝则新，少则得，多则惑。是以圣人抱一为天下式。不自见，故明；不自是，故彰；不自伐，故有功；不自矜，故长。夫唯不争，故天下莫能与之争。古之所谓曲则全者，岂虚言哉！诚全而归之。",
         "委曲反而能保全，弯曲反而能伸直，低洼反而能充盈，破旧反而能更新，少取反而能多得，贪多反而能迷惑。所以，圣人坚守这一原则作为天下的范式。不自我表现，反而能显明；不自以为是，反而能彰显；不自我夸耀，反而能有功；不自我骄傲，反而能长久。正因为不与人争，所以天下没有人能和他争。古人所说的委曲能够保全等话，怎么会是空话呢？它确实能够保全并归向大道。"),

        (23, "希言自然。故飘风不终朝，骤雨不终日。孰为此者？天地。天地尚不能久，而况于人乎？故从事于道者，同于道；德者，同于德；失者，同于失。同于道者，道亦乐得之；同于德者，德亦乐得之；同于失者，失亦乐得之。信不足焉，有不信焉。",
         "少说话是合乎自然的。所以狂风刮不了一早晨，暴雨下不了一整天。谁使它这样的呢？天地。天地都不能长久，何况人呢？所以从事于道的人，就与道相同；从事于德的人，就与德相同；从事于失道失德的人，就与失道失德相同。与道相同的人，道也乐于得到他；与德相同的人，德也乐于得到他；与失道失德相同的人，失道失德也乐于得到他。诚信不足，就有不相信。"),

        (24, "跂者不立，跨者不行。自见者不明，自是者不彰，自伐者无功，自矜者不长。其在道也，曰余食赘行。物或恶之，故有道者不处。",
         "踮起脚尖想要站得高的人反而站不稳；迈着大步想要走得快的人反而走不远。自我表现的人反而不能显明；自以为是的人反而不能彰显；自我夸耀的人反而不能建立功勋；自高自大的人反而不能长久。从道的角度看，这些叫作剩饭赘瘤。人们厌恶它们，所以有道的人不这样做。"),

        (25, "有物混成，先天地生。寂兮寥兮，独立而不改，周行而不殆，可以为天地母。吾不知其名，字之曰道，强为之名曰大。大曰逝，逝曰远，远曰反。故道大，天大，地大，人亦大。域中有四大，而人居其一焉。人法地，地法天，天法道，道法自然。",
         "有一个东西混然而成，在天地形成之前就已经产生。它寂静啊空虚啊，独立存在而不改变，循环运行而不停止，可以作为天地的母亲。我不知道它的名字，给它取字叫道，勉强给它取名叫大。大叫做离去，离去叫做遥远，遥远叫做返回。所以道大，天大，地大，人也大。宇宙中有四大，而人占据其中之一。人效法地，地效法天，天效法道，道效法自然。"),

        (26, "重为轻根，静为躁君。是以圣人终日行不离辎重。虽有荣观，燕处超然。奈何万乘之主，而以身轻天下？轻则失根，躁则失君。",
         "稳重是轻率的根本，静定是躁动的主宰。所以圣人整天行走不离载着物资的车辆。虽然有华丽的生活，但他安居泰然，超然物外。为什么身为大国的君主，却以轻率的态度治理天下呢？轻率就会失去根本，躁动就会失去主宰。"),

        (27, "善行无辙迹，善言无瑕谪，善数不用筹策，善闭无关楗而不可开，善结无绳约而不可解。是以圣人常善救人，故无弃人；常善救物，故无弃物。是谓袭明。故善人者，不善人之师；不善人者，善人之资。不贵其师，不爱其资，虽智大迷，是谓要妙。",
         "善于行走的人不会留下痕迹，善于说话的人没有过失可以指责，善于计算的人不需要筹码，善于关闭的人不用栓锁却使人无法打开，善于打结的人不用绳索却使人无法解开。因此，圣人总是善于挽救人，所以没有被遗弃的人；总是善于挽救物，所以没有被遗弃的物。这就叫作承袭光明的智慧。所以善人是不善人的老师，不善人是善人的借鉴。不尊重他的老师，不爱惜他的借鉴对象，即使自以为聪明，也是极大的糊涂，这就叫作精深奥妙的道理。"),

        (28, "知其雄，守其雌，为天下溪。为天下溪，常德不离，复归于婴儿。知其白，守其黑，为天下式。为天下式，常德不忒，复归于无极。知其荣，守其辱，为天下谷。为天下谷，常德乃足，复归于朴。朴散则为器，圣人用之，则为官长，故大制不割。",
         "知道什么是雄强，却安守雌柔，做天下的溪涧。做天下的溪涧，永恒的德性就不会离散，回复到婴儿的状态。知道什么是光明，却安守暗昧，做天下的范式。做天下的范式，永恒的德性就不会有差错，回复到不可穷极的真理。知道什么是荣耀，却安守屈辱，做天下的川谷。做天下的川谷，永恒的德性才能够充足，回复到朴的状态。朴一旦分散就成为器具，圣人使用它，就成为掌管器具的官长，所以完善的政治制度是不割裂的。"),

        (29, "将欲取天下而为之，吾见其不得已。天下神器，不可为也，不可执也。为者败之，执者失之。故物或行或随，或嘘或吹，或强或羸，或载或隳。是以圣人去甚，去奢，去泰。",
         "想要治理天下却要用强制的办法，我看他是达不到目的的。天下是神圣的器物，是不可以有所作为的，是不可以强行控制的。有所作为就会失败，强行控制就会失去。所以万物有的前行，有的后随；有的呼气，有的吹气；有的强壮，有的瘦弱；有的安稳，有的坠落。因此，圣人要摒弃极端的、奢侈的、过度的措施。"),

        (30, "以道佐人主者，不以兵强天下。其事好还。师之所处，荆棘生焉。大军之后，必有凶年。善有果而已，不以取强。果而勿矜，果而勿伐，果而勿骄，果而不得已，果而勿强。物壮则老，是谓不道，不道早已。",
         "用道辅佐君主的人，不靠兵力在天下逞强。动用兵革这种事情一定会得到报应。军队驻扎过的地方，荆棘就会生长。大战之后，必定有荒年。善于用兵的人只要达到救济危难的目的就是了，不用来夺取强权。达到了目的不要自我夸耀，达到了目的不要自我吹嘘，达到了目的不要骄傲，达到了目的是出于不得已，达到了目的不要逞强。事物强壮了就会衰老，这叫作不合乎道，不合乎道就会很快灭亡。"),

        (31, "夫佳兵者，不祥之器，物或恶之，故有道者不处。君子居则贵左，用兵则贵右。兵者不祥之器，非君子之器，不得已而用之，恬淡为上。胜而不美，而美之者，是乐杀人。夫乐杀人者，则不可得志于天下矣。吉事尚左，凶事尚右。偏将军居左，上将军居右，言以丧礼处之。杀人之众，以悲哀泣之，战胜以丧礼处之。",
         "精良的兵器，是不祥的器物，人们都厌恶它，所以有道的人不使用它。君子平时以左边为贵，打仗时以右边为贵。兵器是不祥的器物，不是君子使用的器物，万不得已才使用它，最好淡然处之。胜利了也不要得意洋洋，如果得意洋洋，就是以杀人为乐。以杀人为乐的人，是不能在天下得志的。吉庆的事情以左边为上，凶丧的事情以右边为上。偏将军站在左边，上将军站在右边，这是说用丧礼的仪式来对待战争。杀人众多，要用悲哀的心情对待，打了胜仗要用丧礼的仪式来处理。"),

        (32, "道常无名。朴虽小，天下莫能臣。侯王若能守之，万物将自宾。天地相合，以降甘露，民莫之令而自均。始制有名，名亦既有，夫亦将知止，知止可以不殆。譬道之在天下，犹川谷之于江海。",
         "道永远是没有名称的。朴虽然微小，天下没有谁能使它服从。侯王如果能守住它，万物将会自然地服从他。天地之间阴阳之气相合，就降下甘露，百姓没有谁命令它，它自然均匀。管理万物开始有了名称，名称既然有了，就要知道适可而止，知道适可而止就可以没有危险。比如道存在于天下，就像江河溪流归于大海一样。"),

        (33, "知人者智，自知者明。胜人者有力，自胜者强。知足者富。强行者有志。不失其所者久。死而不亡者寿。",
         "了解别人的人聪明，了解自己的人明智。战胜别人的人有力量，战胜自己的人坚强。知足的人富有。坚持不懈的人有志向。不丧失根基的人能够长久。身死而精神不亡的人才是长寿。"),

        (34, "大道泛兮，其可左右。万物恃之以生而不辞，功成不名有。衣养万物而不为主，常无欲，可名于小；万物归焉而不为主，可名为大。以其终不自为大，故能成其大。",
         "大道广泛啊，它可以左右一切。万物依靠它生存而它不推辞，功业成就了它也不占有名誉。它养育万物而不做万物的主宰，经常没有欲望，可以叫它渺小；万物归附于它而不做万物的主宰，可以叫它伟大。正因为它始终不自以为伟大，所以才能成就它的伟大。"),

        (35, "执大象，天下往。往而不害，安平太。乐与饵，过客止。道之出口，淡乎其无味，视之不足见，听之不足闻，用之不足既。",
         "坚守大道的形象，天下的人们都会来归往。归往而不互相伤害，于是平和安泰。音乐和美食，能使过路的人停下脚步。道如果用言语表述出来，是平淡而无味的，看它看不见，听它听不到，但用它却是用不完的。"),

        (36, "将欲歙之，必固张之；将欲弱之，必固强之；将欲废之，必固兴之；将欲取之，必固与之。是谓微明。柔弱胜刚强。鱼不可脱于渊，国之利器不可以示人。",
         "想要收缩它，必先扩张它；想要削弱它，必先增强它；想要废除它，必先兴盛它；想要夺取它，必先给予它。这就叫作微妙而明智的道理。柔弱能战胜刚强。鱼不能离开深水，国家的有效武器不能轻易展示给人看。"),

        (37, "道常无为而无不为。侯王若能守之，万物将自化。化而欲作，吾将镇之以无名之朴。无名之朴，夫亦将不欲。不欲以静，天下将自定。",
         "道永远是顺其自然而无不为的。侯王如果能守住它，万物将会自然化育。化育过程中如果有欲望产生，我将用无名的朴来镇住它。无名的朴，也就是没有欲望。没有欲望就能安静，天下将会自然安定。")
    ]

    for num, original, modern in chapters_full_text:
        # 获取王弼《老子注》完整注解
        wangbi_note = WANGBI_NOTES.get(num, f"王弼注（第{num}章）：待补充")
        # 获取河上公《老子章句》完整注解
        heshanggong_note = HESHANGGONG_NOTES.get(num, f"河上公注（第{num}章）：待补充")
        # 获取王夫之《老子衍》完整注解
        wangfuzhi_note = WANGFUZHI_NOTES.get(num, f"王夫之注（第{num}章）：待补充")
        # 获取憨山德清《老子道德经解》完整注解
        hanshandeqing_note = HANSHANDEQING_NOTES.get(num, f"憨山德清注（第{num}章）：待补充")
        # 获取帛书异文文本
        postsilk_text = POSTSILK_TEXT.get(num)
        # 获取帛书异文注解
        postsilk_diff = POSTSILK_NOTES.get(num, f"帛书异文（第{num}章）：待补充")
        # 获取郭店异文文本
        guodian_text = GUODIAN_TEXT.get(num)
        # 获取郭店异文注解
        guodian_diff = GUODIAN_NOTES.get(num, f"郭店异文（第{num}章）：待补充")
        remaining_chapters.append({
            "chapter": num,
            "original": original,
            "wangbi_note": wangbi_note,
            "heshanggong_note": heshanggong_note,
            "wangfuzhi_note": wangfuzhi_note,
            "hanshandeqing_note": hanshandeqing_note,
            "postsilk_text": postsilk_text,
            "postsilk_diff": postsilk_diff,
            "guodian_text": guodian_text,
            "guodian_diff": guodian_diff,
            "english_lau": ENGLISH_LAU.get(num, f"[D.C. Lau translation - Chapter {num} to be added]"),
            "english_henricks": ENGLISH_HENRICKS.get(num, f"[Henricks translation - Chapter {num} to be added]"),
            "english_addiss": ENGLISH_ADDISS.get(num, f"[Addiss & Lombardo translation - Chapter {num} to be added]"),
            "modern_chinese": modern
        })

    # 第38-81章完整原文和译文
    chapters_38_81_full_text = [
        (38, "上德不德，是以有德；下德不失德，是以无德。上德无为而无以为；下德无为而有以为。上仁为之而无以为；上义为之而有以为。上礼为之而莫之应，则攘臂而扔之。故失道而后德，失德而后仁，失仁而后义，失义而后礼。夫礼者，忠信之薄，而乱之首。前识者，道之华，而愚之始。是以大丈夫处其厚，不居其薄；处其实，不居其华。故去彼取此。",
         "具备上等德行的人不自以为有德，所以实际上有德；具备下等德行的人自以为不丧失德，所以实际上没有德。具备上等德行的人顺应自然而无心作为；具备下等德行的人顺应自然而有心作为。上等的仁者有所作为而无心作为；上等的义者有所作为而有心作为。上等的礼者有所作为而得不到回应，就挽起袖子强引别人。所以失去了道然后才有德，失去了德然后才有仁，失去了仁然后才有义，失去了义然后才有礼。礼是忠信不足的产物，是祸乱的开端。所谓的先知，是道的虚华，是愚昧的开始。因此大丈夫立身敦厚，不居于浅薄；存心朴实，不居于虚华。所以要舍弃浅薄虚华，采取敦厚朴实。"),

        (39, "昔之得一者：天得一以清；地得一以宁；神得一以灵；谷得一以生；侯王得一以为天下正。其致之也，谓天无以清，将恐裂；地无以宁，将恐发；神无以灵，将恐歇；谷无以生，将恐竭；侯王无以正，将恐蹶。故贵以贱为本，高以下为基。是以侯王自谓孤、寡、不谷。此非以贱为本邪？非乎？故至誉无誉。是故不欲琭琭如玉，珞珞如石。",
         "自古以来得到道于一体的：天得到道而清明；地得到道而宁静；神得到道而灵妙；山谷得到道而充盈；侯王得到道而成为天下的首领。推而言之，天若不保持清明，恐怕要崩裂；地若不保持宁静，恐怕要震溃；神若不保持灵妙，恐怕要消失；山谷若不保持充盈，恐怕要枯竭；侯王若不保持高贵，恐怕要跌倒。所以贵以贱为根本，高以下为基础。因此侯王自称孤、寡、不谷，这不就是以贱为根本吗？不是吗？所以最高的荣誉是无须赞誉的。不希望像宝玉那样华丽，而要像顽石那样坚硬质朴。"),

        (40, "反者道之动，弱者道之用。天下万物生于有，有生于无。",
         "循环往复是道的运动方式，柔弱胜刚强是道的应用特性。天下万物产生于有形之物，而有形之物又产生于无形之道。"),

        (41, "上士闻道，勤而行之；中士闻道，若存若亡；下士闻道，大笑之。不笑不足以为道。故建言有之：明道若昧；进道若退；夷道若颣；上德若谷；广德若不足；建德若偷；质真若渝；大白若辱；大方无隅；大器晚成；大音希声；大象无形；道隐无名。夫唯道，善贷且成。",
         "上士听了道，努力去实行；中士听了道，半信半疑；下士听了道，大笑之。不被嘲笑，就不足以成为道。所以古人有言说：光明的道好像暗昧；前进的道好像后退；平坦的道好像崎岖；崇高的德好像峡谷；广大的德好像不足；刚健的德好像怠惰；质朴的真好像变幻；最洁白的好像污黑；最大的方形没有棱角；最大的器皿最后完成；最大的声音听不到；最大的形象看不见；大道隐微无名。只有道，善于施予万物并且成就万物。"),

        (42, "道生一，一生二，二生三，三生万物。万物负阴而抱阳，冲气以为和。人之所恶，唯孤、寡、不谷，而王公以为称。故物或损之而益，或益之而损。人之所教，我亦教之。强梁者不得其死，吾将以为教父。",
         "道产生一，一产生二，二产生三，三产生万物。万物背阴而向阳，阴阳二气互相激荡而形成和谐。人们所厌恶的，就是孤、寡、不谷，但王公却用这些词来称呼自己。所以万物有的减损它反而增益，有的增益它反而减损。别人教导我的，我也用来教导人。强横的人不得善终，我把这话当作施教的宗旨。"),

        (43, "天下之至柔，驰骋天下之至坚。无有入无间，吾是以知无为之有益。不言之教，无为之益，天下希及之。",
         "天下最柔弱的东西，能穿透天下最坚硬的东西。空虚无形之物能进入没有缝隙的东西中，我因此知道无为的好处。不言的教化，无为的好处，天下很少能赶上它的。"),

        (44, "名与身孰亲？身与货孰多？得与亡孰病？甚爱必大费，多藏必厚亡。故知足不辱，知止不殆，可以长久。",
         "名声与生命相比哪个亲切？生命与货利相比哪个贵重？得到与失去相比哪个有害？过分爱惜必招致巨大的破费，过多的贮藏必招致惨重的损失。所以知道满足就不会受屈辱，知道适可而止就不会有危险，这样可以长久。"),

        (45, "大成若缺，其用不弊。大盈若冲，其用不穷。大直若屈，大巧若拙，大辩若讷。躁胜寒，静胜热。清静为天下正。",
         "最完满的东西好像有残缺，但它的作用不会衰竭。最充盈的东西好像空虚，但它的作用无穷无尽。最直的东西好像弯曲，最灵巧的东西好像笨拙，最雄辩的人好像口吃。运动能战胜寒冷，安静能战胜炎热。只有清静无为才能做天下的典范。"),

        (46, "天下有道，却走马以粪。天下无道，戎马生于郊。祸莫大于不知足；咎莫大于欲得。故知足之足，常足矣。",
         "天下有道时，战马退还给农田去耕种。天下无道时，怀胎的母马也要上战场。最大的祸患是不知足，最大的过失是贪得无厌。所以知道满足的这种满足，永远是满足的。"),

        (47, "不出户，知天下；不窥牖，见天道。其出弥远，其知弥少。是以圣人不行而知，不见而名，不为而成。",
         "不出门户，能够推知天下的事理；不望窗外，能够认识自然的规律。他向外走得越远，他所知道的越少。所以圣人不出行却能知晓，不看却能明白，无为却能成功。"),

        (48, "为学日益，为道日损。损之又损，以至于无为。无为而无不为。取天下常以无事，及其有事，不足以取天下。",
         "求学是每天增加知识，修道是每天减少欲望。减少又减少，直到无为的境界。无为却没有什么做不成的。治理天下常常靠无为而治，至于有为去治理，就不足以治理天下了。"),

        (49, "圣人无常心，以百姓心为心。善者，吾善之；不善者，吾亦善之，德善。信者，吾信之；不信者，吾亦信之，德信。圣人在天下，歙歙焉，为天下浑其心，百姓皆注其耳目，圣人皆孩之。",
         "圣人没有固定的意志，以百姓的意志为意志。善良的人，我善待他；不善良的人，我也善待他，这样可使人人向善。守信的人，我信任他；不守信的人，我也信任他，这样可使人人守信。圣人在天下，总是收敛自己的欲望，使天下的心思归于浑朴，百姓都专注视听于圣人，圣人使他们都像婴孩一样纯真。"),

        (50, "出生入死。生之徒，十有三；死之徒，十有三；人之生，动之于死地，亦十有三。夫何故？以其生生之厚。盖闻善摄生者，路行不遇兕虎，入军不被甲兵；兕无所投其角，虎无所用其爪，兵无所容其刃。夫何故？以其无死地。",
         "人出世为生，入地为死。属于长寿的，占十分之三；属于短命的，占十分之三；本来可以活得长久，却自己走向死路的，也占十分之三。为什么呢？因为他追求生活享受太丰厚了。听说善于养护生命的人，在陆地上行走不会遇到犀牛和老虎，在战争中不会受到武器的伤害；犀牛无处投它的角，老虎无处用它的爪，武器无处用它的锋刃。为什么呢？因为他没有进入死地。"),

        (51, "道生之，德畜之，物形之，势成之。是以万物莫不尊道而贵德。道之尊，德之贵，夫莫之命而常自然。故道生之，德畜之；长之育之；亭之毒之；养之覆之。生而不有，为而不恃，长而不宰，是谓玄德。",
         "道生长万物，德养育万物，使万物呈现各种形态，环境使万物成长。因此万物没有不尊崇道而贵重德的。道之所以被尊崇，德之所以被贵重，它不需要谁来下令，而是常自然的。所以道生长万物，德养育万物；使万物生长发育，使万物成熟结果；使万物得到爱护和保护。生长万物而不占有，养育万物而不自恃有功，统领万物而不任意主宰，这就是最深远的德。"),

        (52, "天下有始，以为天下母。既得其母，以知其子；既知其子，复守其母，没身不殆。塞其兑，闭其门，终身不勤。开其兑，济其事，终身不救。见小曰明，守柔曰强。用其光，复归其明，无遗身殃，是为袭常。",
         "天下万物都有个开端，以此作为天下的根源。既然知道了根源，就能认识万物；既然认识了万物，再坚守着根源，终身不会有危险。堵塞嗜欲的孔窍，关闭嗜欲的门径，终身不会有劳苦。打开嗜欲的孔窍，成就世俗的事务，终身不可救药。能察见细微叫作明，能坚守柔弱叫作强。运用智慧的光芒，复归内在的明智，不给自己留下祸殃，这就是承袭永恒不变的道。"),

        (53, "使我介然有知，行于大道，唯施是畏。大道甚夷，而人好径。朝甚除，田甚芜，仓甚虚；服文采，带利剑，厌饮食，财货有馀；是为盗夸。非道也哉！",
         "假如我稍微有些知识，就在大道上行走，唯恐走入了邪路。大道很平坦，但人君却喜欢走小路。朝政非常腐败，农田非常荒芜，仓库非常空虚；穿着华丽的衣服，佩戴锋利的宝剑，吃腻精美的饮食，占有过多的财货；这叫作强盗头子。这是无道啊！"),

        (54, "善建者不拔，善抱者不脱，子孙以祭祀不辍。修之于身，其德乃真；修之于家，其德乃余；修之于乡，其德乃长；修之于邦，其德乃丰；修之于天下，其德乃普。故以身观身，以家观家，以乡观乡，以邦观邦，以天下观天下。吾何以知天下之然哉？以此。",
         "善于建树的人不可拔除，善于抱持的人不会脱落，子孙后代会以此来祭祀不绝。用道修身，他的德就真实；用道治家，他的德就有余；用道治乡，他的德就久长；用道治国，他的德就丰盛；用道治天下，他的德就普及。所以用自身的修身之道来观察别身，以自家的治家之道来观察别家，以自乡的治乡之道来观察别乡，以自国的治国之道来观察别国，以平天下的之道来观察天下。我凭什么知道天下的情况呢？就是用这个方法。"),

        (55, "含德之厚，比于赤子。毒虫不螫，猛兽不据，攫鸟不搏。骨弱筋柔而握固。未知牝牡之合而朘作，精之至也。终日号而不嗄，和之至也。知和曰常，知常曰明。益生曰祥。心使气曰强。物壮则老，谓之不道，不道早已。",
         "含德深厚的人，就像初生的婴儿。毒虫不刺他，猛兽不伤害他，凶鸟不搏击他。筋骨柔弱而拳头握得牢固。不懂男女交合而生殖器勃起，这是精气充沛的极致。整天啼哭而嗓子不哑，这是元气和谐的极致。懂得和谐叫作常，懂得常叫作明。贪生纵欲就叫作妖祥。欲望支配精气叫作逞强。事物过于强壮就会走向衰老，这叫作不合乎道，不合乎道就会很快灭亡。"),

        (56, "知者不言，言者不知。塞其兑，闭其门，挫其锐，解其纷，和其光，同其尘，是谓玄同。故不可得而亲，不可得而疏；不可得而利，不可得而害；不可得而贵，不可得而贱。故为天下贵。",
         "真正了解的人不说话，说话的人不了解。堵塞嗜欲的孔窍，关闭嗜欲的门径，磨掉锋芒，消解纷扰，含敛光耀，混同尘世，这就叫作玄妙的同化。所以对他既不能亲近，也不能疏远；既不能使他得利，也不能使他受害；既不能使他尊贵，也不能使他卑贱。所以被天下所尊贵。"),

        (57, "以正治国，以奇用兵，以无事取天下。吾何以知其然哉？以此：天下多忌讳，而民弥贫；人多利器，国家滋昏；人多伎巧，奇物滋起；法令滋彰，盗贼多有。故圣人云：我无为，而民自化；我好静，而民自正；我无事，而民自富；我无欲，而民自朴。",
         "用清正无为的方法治理国家，用诡奇的方法用兵，用无为的方法来夺取天下。我怎么知道是这样的呢？根据下面这些情况：天下的禁忌越多，百姓越贫穷；民间的利器越多，国家越昏乱；人们的技巧越多，邪恶的事情就越发生；法令越森严，盗贼反而越多。所以圣人说：我无为，百姓自然感化；我好静，百姓自然端正；我无事，百姓自然富足；我无欲，百姓自然淳朴。"),

        (58, "其政闷闷，其民淳淳；其政察察，其民缺缺。祸兮福之所倚，福兮祸之所伏。孰知其极？其无正也。正复为奇，善复为妖。人之迷，其日固久。是以圣人方而不割，廉而不刿，直而不肆，光而不耀。",
         "政治宽厚，百姓就淳朴；政治严苛，百姓就狡诈。灾祸中倚伏着幸福，幸福中潜伏着灾祸。谁知道它们的终极？它们并没有定准。正可以转变为邪，善可以转变为恶。人们的迷惑，已经很久了。因此圣人方正而不割人，锐利而不伤人，直率而不放肆，光亮而不刺眼。"),

        (59, "治人事天，莫若啬。夫唯啬，是谓早服；早服谓之重积德；重积德则无不克；无不克则莫知其极；莫知其极，可以有国；有国之母，可以长久；是谓深根固蒂，长生久视之道。",
         "治理百姓和侍奉上天，没有比爱惜精力更重要的了。正因为爱惜精力，就是早做准备；早做准备就是不断积累德；不断积累德就能无往不胜；无往不胜就没有人知道他的极限；没有人知道他的极限就可以担负治理国家的重任；有了治理国家的根本就可以长久保持；这就是根深蒂固、长生久视的道理。"),

        (60, "治大国，若烹小鲜。以道莅天下，其鬼不神；非其鬼不神，其神不伤人；非其神不伤人，圣人亦不伤人。夫两不相伤，故德交归焉。",
         "治理大国，好像煎烹小鱼一样。用道治理天下，鬼怪不起作用；不是鬼怪不起作用，而是它的作用不伤人；不是它的作用不伤人，而是圣人也不伤人。鬼怪和圣人都不伤人，所以德归于他们，交相会合。"),

        (61, "大邦者下流，天下之牝，天下之交也。牝常以静胜牡，以静为下。故大邦以下小邦，则取小邦；小邦以下大邦，则取大邦。故或下以取，或下而取。大邦不过欲兼畜人，小邦不过欲入事人。夫两者各得所欲，大者宜为下。",
         "大国要像居于江河下游那样，使天下百川汇集，处在天下雌柔的位置。雌柔常以静定战胜雄强，因为静定而又居于下位。所以大国对小国谦下，就能取得小国的信任；小国对大国谦下，就能取得大国的信任。所以有的因为谦下而取得，有的因为谦下而被取得。大国不过是要兼并小国，小国不过是要见容于大国。如果双方都能达到目的，大国尤其应该谦下。"),

        (62, "道者万物之奥。善人之宝，不善人之所保。美言可以市，尊行可以加人。人之不善，何弃之有？故立天子，置三公，虽有拱璧以先驷马，不如坐进此道。古之所以贵此道者何？不曰：求以得，有罪以免邪？故为天下贵。",
         "道是万物的庇荫所。善人珍视它，不善的人也保持它。美好的言语可以换取别人的尊重，高尚的行为可以见重于人。那些不善的人，怎么可以舍弃道呢？所以天子即位、设置三公的时候，虽然先献上璧玉后献上车马，不如献上这个道。古人之所以重视这个道为什么呢？不是说有求的就能得到，有罪的就能免除吗？所以被天下所尊贵。"),

        (63, "为无为，事无事，味无味。大小多少，报怨以德。图难于其易，为大于其细；天下难事，必作于易；天下大事，必作于细。是以圣人终不为大，故能成其大。夫轻诺必寡信，多易必多难。是以圣人犹难之，故终无难。",
         "以无为的态度去作为，以不生事的态度去处事，以淡泊无味当作味。不管大怨小怨，都以德来报答。谋划困难的事情要从容易的地方入手，做大事要从细微的地方入手；天下的难事一定从容易的地方做起，天下的大事一定从细微的地方做起。所以圣人始终不自以为大，所以能成就大事。轻易许诺必然信用不足，把事情看得太容易必然困难重重。所以圣人总是把事情看得困难，所以始终没有困难。"),

        (64, "其安易持，其未兆易谋。其脆易泮，其微易散。为之于未有，治之于未乱。合抱之木，生于毫末；九层之台，起于累土；千里之行，始于足下。为者败之，执者失之。是以圣人无为故无败，无执故无失。民之从事，常于几成而败之。慎终如始，则无败事。是以圣人欲不欲，不贵难得之货；学不学，复众人之所过。以辅万物之自然而不敢为。",
         "事物安稳时容易持守，问题没显露时容易谋划。事物脆弱时容易消解，事物微小时容易散除。要在事情没有发生时就处理，要在祸乱没有产生时就治理。合抱的大树，是从幼芽开始生长的；九层的高台，是由一筐筐泥土堆积起来的；千里的远行，是从脚下一步步走出来的。妄为必然失败，强行把持必然失去。所以圣人无为所以不会失败，不强求所以不会失去。人们做事情，总是在快要成功时失败。如果在结束时仍像开始时那样谨慎，就不会有失败的事情。所以圣人追求人所不追求的，不稀罕难得的财物；学习别人所不学习的，补救众人所犯的过错。以此辅助万物自然发展而不敢妄为。"),

        (65, "古之善为道者，非以明民，将以愚之。民之难治，以其智多。故以智治国，国之贼；不以智治国，国之福。知此两者亦稽式。常知稽式，是谓玄德。玄德深矣，远矣，与物反矣，然后乃至大顺。",
         "古代善于为道的人，不是教人民精巧，而是使人民淳朴。人民所以难治理，是因为他们有太多的智巧心机。所以用智巧治理国家，是国家的灾害；不用智巧治理国家，是国家的福气。要知道这两种方式也是法则。常守这个法则，就叫作玄德。玄德深啊，远啊，与万物返璞归真，然后达到极大的和顺。"),

        (66, "江海所以能为百谷王者，以其善下之，故能为百谷王。是以圣人欲上民，必以言下之；欲先民，必以身後之。是以圣人处上而民不重，处前而民不害。是以天下乐推而不厌。以其不争，故天下莫能与之争。",
         "江海所以能成为百川河流的王者，是因为它善于处在下游，所以能成为百川的王。因此圣人想要在人民之上，必须用言语对人民谦下；想要在人民之前，必须把自己放在人民之后。所以圣人处在上面而人民不感到沉重，处在前面而人民不感到受害。因此天下人民乐意推崇他而不厌恶。因为他不与人争，所以天下没有人能和他争。"),

        (67, "天下皆谓我道大，似不肖。夫唯大，故似不肖。若肖，久矣其细也夫！我有三宝，持而保之。一曰慈，二曰俭，三曰不敢为天下先。夫慈，故能勇；俭，故能广；不敢为天下先，故能成器长。今舍慈且勇；舍俭且广；舍后且先；死矣！夫慈，以战则胜，以守则固。天将救之，以慈卫之。",
         "天下人都说我的道大，好像什么都不像。正因为大，所以什么都不像。如果像什么，早就渺小了！我有三件宝贝，持守而保全它们：第一叫作慈爱，第二叫作俭啬，第三叫作不敢居于天下人的前面。因为有慈爱，所以能勇武；因为俭啬，所以能宽广；因为不敢居于天下人的前面，所以能成为万物的首长。现在舍弃慈爱而追求勇武，舍弃俭啬而追求宽广，舍弃退让而追求争先，就是死路！慈爱，用来作战就能胜利，用来守卫就能坚固。天要救助谁，就用慈爱来保卫谁。"),

        (68, "善为士者，不武；善战者，不怒；善胜敌者，不与；善用人者，为之下。是谓不争之德，是谓用人之力，是谓配天古之极。",
         "善于做将帅的人不逞勇武，善于作战的人不逞愤怒，善于战胜敌人的人不与敌人对斗，善于用人的人对人谦下。这叫作不争的品德，这叫作用人的能力，这叫作符合天道的准则。"),

        (69, "用兵有言：吾不敢为主，而为客；不敢进寸，而退尺。是谓行无行；攘无臂；扔无敌；执无兵。祸莫大于轻敌，轻敌几丧吾宝。故抗兵相若，哀者胜矣。",
         "用兵的人曾说：我不敢主动进攻，而采取防守；不敢前进一寸，而要后退一尺。这就是说：虽然有阵势，却像没有阵势可摆；虽然要奋臂，却像没有手臂可举；虽然要对抗，却像没有敌人可对；虽然要拿着兵器，却像没有兵器可拿。灾祸没有比轻敌更大的了，轻敌几乎丧失了我的三宝。所以两军对垒力量相当时，悲愤的一方会获胜。"),

        (70, "吾言甚易知，甚易行。天下莫能知，莫能行。言有宗，事有君。夫唯无知，是以不我知。知我者希，则我者贵。是以圣人被褐而怀玉。",
         "我的话很容易理解，很容易实行。天下却没有人能够理解，没有人能够实行。说话要有宗旨，做事要有主见。正是由于人们无知，所以不理解我。理解我的人很少，效法我的人就很难得了。因此圣人外表穿着粗布衣服，怀里却揣着美玉。"),

        (71, "知不知，尚矣；不知知，病也。夫唯病病，是以不病。圣人不病，以其病病，是以不病。",
         "知道自己不知道，是高明的；不知道却自以为知道，是弊病。只有把弊病当作弊病，所以才没有弊病。圣人没有弊病，是因为他把弊病当作弊病，所以才没有弊病。"),

        (72, "民不畏威，则大威至矣。无狎其所居，无厌其所生。夫唯不厌，是以不厌。是以圣人自知不自见；自爱不自贵。故去彼取此。",
         "当人民不畏惧统治者的威压时，那么可怕的祸乱就要到来了。不要逼迫人民的居处，不要压榨人民的生活。只有不压榨人民，人民才不厌恶统治者。因此圣人有自知之明而不自我表现，有自爱之心而不自显高贵。所以舍弃后者而采取前者。"),

        (73, "勇于敢则杀，勇于不敢则活。此两者，或利或害。天之所恶，孰知其故？天之道，不争而善胜，不言而善应，不召而自来，繟然而善谋。天网恢恢，疏而不失。",
         "勇于敢做就会杀身，勇于不敢做就会活命。这两种勇气，一个有利，一个有害。天所厌恶的，谁知道是什么缘故？天的道，不争斗而善于获胜，不说话而善于应答，不召唤而自动到来，宽缓而善于谋划。天网广大无边，虽然稀疏却不会有一点漏失。"),

        (74, "民不畏死，奈何以死惧之？若使民常畏死，而为奇者，吾将得而杀之，孰敢？常有司杀者杀。夫代司杀者杀，是谓代大匠斫。夫代大匠斫者，希有不伤其手矣。",
         "人民不畏惧死亡，为什么用死亡来恐吓他们呢？如果使人民真的畏惧死亡，对于为非作歹的人，我就可以抓来杀掉，谁还敢为非作歹呢？常有专管杀人的去执行杀戮。如果代替专管杀人的去执行杀戮，这就好比代替高明的木匠去砍木头。代替高明的木匠去砍木头，很少有不砍伤自己手的。"),

        (75, "民之饥，以其上食税之多，是以饥。民之难治，以其上之有为，是以难治。民之轻死，以其上求生之厚，是以轻死。夫唯无以生为者，是贤于贵生。",
         "人民所以遭受饥荒，是因为统治者吞食的赋税太多，所以遭受饥荒。人民所以难治理，是因为统治者妄作为政，所以难治理。人民所以轻视死亡，是因为统治者追求奉养的过分丰厚，所以轻视死亡。只有不把奉养生命看得太重的人，比过分看重生命的人高明。"),

        (76, "人之生也柔弱，其死也坚强。草木之生也柔脆，其死也枯槁。故坚强者死之徒，柔弱者生之徒。是以兵强则灭，木强则折。强大处下，柔弱处上。",
         "人活着的时候身体是柔软的，死后就变得僵硬。草木活着的时候是柔软脆弱的，死后就变得干枯坚硬。所以坚强的东西属于死亡的一类，柔弱的东西属于生存的一类。因此军队逞强就会被消灭，树木逞强就会被折断。强大的处于下位，柔弱的处于上位。"),

        (77, "天之道，其犹张弓与？高者抑之，下者举之；有余者损之，不足者补之。天之道，损有余而补不足。人之道，则不然，损不足以奉有余。孰能有余以奉天下？唯有道者。是以圣人为而不恃，功成而不居，其不欲见贤。",
         "天的道，不就像张弓射箭一样吗？高了就压低一些，低了就抬高一些；有余的就减少一些，不足的就补充一些。天的道，是减少有余的来补充不足的。人的道却不是这样，是减少不足的来供奉有余的。谁能把有余的拿来供奉给天下呢？只有有道的人。因此圣人有所作为而不自恃，功成而不居功，他不愿意表现自己的贤能。"),

        (78, "天下莫柔弱于水，而攻坚强者莫之能胜，以其无以易之。弱之胜强，柔之胜刚，天下莫不知，莫能行。故圣人云：受国之垢，是谓社稷主；受国不祥，是为天下王。正言若反。",
         "天下没有什么比水更柔弱的，但攻坚克强却没有什么能胜过它，因为没有什么能改变它。弱胜过强，柔胜过刚，天下没有人不知道，但没有人能实行。所以圣人说：承担国家的屈辱，这就叫作国家的君主；承担国家的灾祸，这就叫作天下的君王。正面的话好像反话一样。"),

        (79, "和大怨，必有余怨；报怨以德，安可以为善？是以圣人执左契，而不责于人。有德司契，无德司彻。天道无亲，常与善人。",
         "调解深重的怨恨，必然会有余留的怨恨；用德来报答怨恨，怎么可以算是妥善的呢？因此圣人拿着契约的存根，而不向人索取偿还。有德的人就像掌握契约的人一样宽容，无德的人就像掌管税收的人一样苛求。天道没有偏爱，永远帮助善人。"),

        (80, "小国寡民。使有什伯之器而不用；使民重死而不远徙。虽有舟舆，无所乘之；虽有甲兵，无所陈之。使民复结绳而用之。甘其食，美其服，安其居，乐其俗。邻国相望，鸡犬之声相闻，民至老死不相往来。",
         "使国家小，人民少。即使有各种器具也不使用；使人民重视死亡而不向远方迁徙。虽然有船只车辆，却没有乘坐的需要；虽然有武器装备，却没有陈列的机会。使人民回到结绳记事的状态。使人民饮食香甜，服饰美好，居住安适，习俗欢乐。邻国之间可以互相望见，鸡鸣狗叫的声音可以互相听到，但人民直到老死也不互相往来。"),

        (81, "信言不美，美言不信。善者不辩，辩者不善。知者不博，博者不知。圣人不积，既以为人己愈有，既以与人己愈多。天之道，利而不害；圣人之道，为而不争。",
         "真实的话不华美，华美的话不真实。善良的人不巧辩，巧辩的人不善良。真正了解的人不广博，广博的人不一定真正了解。圣人没有积蓄，尽力帮助别人，自己反而更充足；把一切给予别人，自己反而更丰富。天的道，有利于万物而不伤害万物；圣人的道，做什么都不和别人争。")
    ]

    for num, original, modern in chapters_38_81_full_text:
        # 获取王弼《老子注》完整注解
        wangbi_note = WANGBI_NOTES.get(num, f"王弼注（第{num}章）：待补充")
        # 获取河上公《老子章句》完整注解
        heshanggong_note = HESHANGGONG_NOTES.get(num, f"河上公注（第{num}章）：待补充")
        # 获取王夫之《老子衍》完整注解
        wangfuzhi_note = WANGFUZHI_NOTES.get(num, f"王夫之注（第{num}章）：待补充")
        # 获取憨山德清《老子道德经解》完整注解
        hanshandeqing_note = HANSHANDEQING_NOTES.get(num, f"憨山德清注（第{num}章）：待补充")
        # 获取帛书异文文本
        postsilk_text = POSTSILK_TEXT.get(num)
        # 获取帛书异文注解
        postsilk_diff = POSTSILK_NOTES.get(num, f"帛书异文（第{num}章）：待补充")
        # 获取郭店异文文本
        guodian_text = GUODIAN_TEXT.get(num)
        # 获取郭店异文注解
        guodian_diff = GUODIAN_NOTES.get(num, f"郭店异文（第{num}章）：待补充")
        remaining_chapters.append({
            "chapter": num,
            "original": original,
            "wangbi_note": wangbi_note,
            "heshanggong_note": heshanggong_note,
            "wangfuzhi_note": wangfuzhi_note,
            "hanshandeqing_note": hanshandeqing_note,
            "postsilk_text": postsilk_text,
            "postsilk_diff": postsilk_diff,
            "guodian_text": guodian_text,
            "guodian_diff": guodian_diff,
            "english_lau": ENGLISH_LAU.get(num, f"D.C. Lau translation (Chapter {num}): To be added."),
            "english_henricks": ENGLISH_HENRICKS.get(num, f"Robert Henricks translation (Chapter {num}): To be added."),
            "english_addiss": ENGLISH_ADDISS.get(num, f"Addiss & Lombardo translation (Chapter {num}): To be added."),
            "modern_chinese": modern
        })

    return remaining_chapters


def generate_full_data():
    """生成完整的81章数据"""
    # 已有的1-10章完整数据
    full_data = CHAPTERS_DATA.copy()

    # 添加11-81章
    full_data.extend(create_remaining_chapters())

    return full_data


def main():
    """主函数：生成并保存JSON数据"""
    # 确保data目录存在
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = script_dir
    os.makedirs(data_dir, exist_ok=True)

    # 生成完整数据
    daodejing_data = {
        "title": "道德经",
        "subtitle": "多版本对照研究平台",
        "chapters": generate_full_data()
    }

    # 保存到JSON文件
    output_path = os.path.join(data_dir, "daodejing.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(daodejing_data, f, ensure_ascii=False, indent=2)

    print(f"数据文件已生成: {output_path}")
    print(f"共包含 {len(daodejing_data['chapters'])} 章")
    print(f"前10章为完整数据（含原文、四家注、异文、三英译）")
    print(f"第11-37章含完整原文和译文")
    print(f"第38-81章为框架结构（待后续补充）")
    print("\n后续可继续补充以下内容：")
    print("- 第38-81章的完整原文")
    print("- 所有章节的完整注解（王弼、河上公、王夫之、憨山德清）")
    print("- 所有章节的完整异文说明（帛书、郭店）")
    print("- 所有章节的完整英文译本（Lau、Henricks、Addiss）")


if __name__ == "__main__":
    main()
