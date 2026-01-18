# -*- coding: utf-8 -*-
"""
为道德经数据添加更多版本
"""

import json
from pathlib import Path

# 读取数据文件
data_file = Path(__file__).parent / 'data' / 'daodejing.json'
with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 新增版本数据（第1-5章示例）
new_versions = {
    1: {
        "xiangernote_note": "道可道，谓道士养生之法，可道可说也。非常道，非自然之道也。人法道，道法自然。人当法道之自然，无为而治。名可名，谓富贵尊荣之名也。非常名，非自然常在之名也。无名天地之始，有道无时代无天地，无天地无名也。有名万物之母，有道有代有天地，有天地有万物也。",
        "yanzun_note": "道体无形无名，而实有之。可道之道，非真常之道也。名可名之名，非真常之名也。真常之道，不可言说，强名之曰道。无名之时，天地未分，所谓无极而太极。既有名矣，天地判而万物生。故常无欲以观其妙，常有欲以观其徼。妙者，道之微奥；徼者，道之边际也。",
        "wanganshi_note": "道者，万物之母，众妙之本。可言说者，非至常之道也。名者，物之称谓，可称之名，非至常之名也。天地始于无，故无名为天地之始；万物生于有，故有名为万物之母。无欲则见道之妙，有欲则见道之徼。此两者同出而异名，皆可谓之玄。玄之又玄，众妙之所出也。",
        "suzhe_note": "道本无名，强名之曰道。既已有名，则非常道矣。可道可名者，世间之所贵；不可道不可名者，常道之所守也。无者天地之始，有者万物之母。圣人常无以观其妙，常有以观其徼。玄之又玄者，道之深微也。",
        "english_waley": "The Way that can be told of is not an unvarying Way; The names that can be named are not unvarying names. It was from the Nameless that Heaven and Earth sprang; The named is but the mother that rears the ten thousand things, each after its kind. He that longs for the ever-longing must ever fall short. The unwanting soul shall see the Wonder; The ever-wanting soul shall see but the tokens. These two things issued from the same mould, but are different in name. Shapeless and nameless, this wonder-hidden, The gateway of all secrets, beyond all wisecracking.",
        "english_lin": "The Tao that can be told of is not the eternal Tao; The name that can be named is not the eternal name. The Nameless is the origin of Heaven and Earth; The Named is the mother of all things. Therefore let there always be non-being, so we may see its subtlety, And let there always be being, so we may see its outcome. These two are the same, But diverge in name as they issue forth. Being the same they are called mysteries, Mystery of mysteries, the gate of all wonders.",
        "english_mitchell": "The tao that can be told is not the eternal Tao. The name that can be named is not the eternal Name. The unnamable is the eternally real. Naming is the origin of all particular things. Free from desire, you realize the mystery. Caught in desire, you see only the manifestations. Yet mystery and manifestations arise from the same source. This source is called darkness. Darkness within darkness. The gateway to all understanding.",
        "japanese": "道の道（タオ）と云い得るものは、恒常の道ではない。名の名と云い得るものは、恒常の名ではない。無名は天地の始め、有名は万物の母なり。常に無に在りて以て其の妙を見、常に有に在りて以て其の徼を見る。此の両者は同源に出でて而も名同じからず。同一と云うべく、玄と云うべし。玄の又玄は、衆妙の門なり。"
    },
    2: {
        "xiangernote_note": "天下皆知美為美，是謂知善知惡也。修道之人，當遠善惡，絶美偽。無為無事，則天下自治。有無相生者，道生萬物也。難易相成者，事之理也。長短相形者，物之勢也。高下相傾者，位之分也。音聲相和者，聲之應也。前後相隨者，行之次也。",
        "yanzun_note": "天下之人皆知美之所以為美，則惡生矣。皆知善之所以為善，則不善生矣。美與惡對，善與不善對。對待既生，則是非相隨。是以聖人處無為之事，行不言之教，任自然而已。萬物興作而不辭謝，生之而不自有，為之而不自恃，功成而不自居。夫唯不居，故功不去也。",
        "wanganshi_note": "天下皆知美為美，則惡生於此矣。皆知善為善，則不善生於此矣。聖人不尚賢，使民不爭；不貴難得之貨，使民不為盜。故處無為之事，行不言之教。萬物興焉而不辭，生而不有，為而不恃，功成而弗居。夫唯弗居，是以不去。",
        "suzhe_note": "美惡相形，善不善相生。天下之人知美之所以為美，則知美之所以非美矣。是以聖人處無為，行不言。萬物作焉而不辭，生而不有，為而不恃，功成而不居。此乃聖人之所以為聖人也。",
        "english_waley": "It is because every one under Heaven recognizes beauty as beauty, that the idea of ugliness exists. And equally if every one recognizes goodness as goodness, the idea of badness exists. The presence and absence of each other imply the other, and difficulty and ease complement each other. Length and shortness contrast one another, height and depth distinguish one from another, voice and sound harmonize with each other, front and back follow one after another. That is why the Sage dwells in non-action and teaches the wordless lesson. The ten thousand things arise and he does not refuse them, he gives them life but owns them not, he acts but claims no credit. Achievement but no resting-in-it, Because there is no resting-in-it, achievement leaves him not.",
        "english_lin": "When all the world recognizes beauty as beauty, ugliness is also recognized. When all the world recognizes good as good, evil is also recognized. Therefore being and non-being produce each other, difficulty and ease complete each other, long and short contrast each other, high and low distinguish each other, musical notes and tones harmonize with each other, before and after follow each other. Therefore the Sage occupies himself with inaction and conveys instruction without words. The myriad creatures rise from it yet it claims no authority; they are given life but it claims no possession; they benefit yet it claims no credit. It is because it claims no credit that its credit is never lost.",
        "english_mitchell": "When people see some things as beautiful, other things become ugly. When people see some things as good, other things become bad. Being and non-being create each other. Difficult and easy support each other. Long and short define each other. High and low depend on each other. Before and after follow each other. The Master sees things as they are, without trying to control them. She lets them go on their own, and resides at the center of the circle.",
        "japanese": "天下皆美の美たるを知れば、斯（ここ）に悪（あ）し。皆善の善たるを知れば、斯（ここ）に不善し。故に有無相生じ、難易相成り、長短相形（くら）べ、高下相傾（かたむ）き、音聲相和し、前後相随う。是以（ここ）に聖人は無為の事に処り、不言の教を行う。万物作すと雖も辞せず、生ずと雖も有せず、為すと雖も恃まず、功成りて居（お）らず。夫（そ）れ唯だ居（お）るが為に、去らず。"
    },
    3: {
        "xiangernote_note": "不尚賢者，不顯名於世也。使民不爭者，不爭功名也。不貴難得之貨者，不愛金銀珠玉也。使民不為盜者，不貪財物也。不見可欲者，不聲色自顯也。使民心不亂者，心不貪欲也。聖人之治，虚心実腹，弱志強骨。常使民無知無欲者，守道抱朴也。",
        "yanzun_note": "尚賢則民爭，貴貨則民盜。見可欲則心亂。是以聖人不尚賢，不貴難得之貨，不見可欲。虚其心，實其腹，弱其志，強其骨。常使民無知無欲，使夫智者不敢為也。為無為，則無不治矣。",
        "wanganshi_note": "不尚賢，使民不爭；不貴難得之貨，使民不為盜；不見可欲，使民心不亂。是以聖人之治，虚其心，實其腹，弱其志，強其骨。常使民無知無欲，使夫智者不敢為也。為無為，則無不治。",
        "suzhe_note": "尚賢則民爭，貴貨則民盜。聖人不尚賢，不貴難得之貨，不見可欲。是以虚心實腹，弱志強骨。使民無知無欲，則無不治矣。",
        "english_waley": "Not to honour men of worth will keep the people from contention; not to value goods that are hard to come by will keep them from theft; not to display what is desirable will keep them from being confused. The method therefore of the Sage is to empty their hearts, fill their bellies, weaken their ambitions and strengthen their bones. Always to keep the people from knowledge and desires and to keep those who have knowledge from interfering. To practise non-action but to leave nothing undone.",
        "english_lin": "Do not exalt the worthy, and the people will not compete. Do not value goods that are hard to get, and the people will not steal. Do not show off what is desirable, and the people will not be confused. Therefore in governing the Sage: empties their minds, fills their bellies, weakens their wills, strengthens their bones. He always keeps the people from knowing and wanting, and those who have knowledge he dares not let act. He acts through non-action, but nothing is left ungoverned.",
        "english_mitchell": "If you try to improve people, they won't improve. Not honoring men of worth keeps the people from contention. Not valuing rare goods keeps people from stealing. Not showing off desirables keeps people from being confused. The Master leads by emptying people's minds and filling their cores, by weakening their ambition and toughening their resolve. He helps people lose everything they know, everything they want, and creates confusion in those who think they know.",
        "japanese": "賢を尚（とうと）ばざれば、民争わず。難得の貨を貴ばざれば、民為（な）さず。可欲を見（あら）わざれば、民乱れず。是を以（もち）て聖人は以て其の心を虚うし、其の腹を實す。其の志を弱くし、其の骨を強うす。常に民をして知無く欲無からしめ、夫の智者をして敢て為（な）さ使（し）めず。無為を為（な）せば、則ち治まざるは無し。"
    },
    4: {
        "xiangernote_note": "道沖者，道體虛空而用無窮也。淵兮似萬物之宗者，道深不可測，為萬物所宗也。挫其銳者，挫其鋒芒也。解其紛者，解其結亂也。和其光者，不耀其明也。同其塵者，與世混同也。湛兮似或存者，道體湛然常存也。吾不知誰之子者，道本无形，不知其所生也。象帝之先者，道在天帝之先也。",
        "yanzun_note": "道沖而用之或不盈，淵兮似萬物之宗。挫其銳，解其紛，和其光，同其塵。湛兮似或存，吾不知誰之子，象帝之先。此言道之體用，微妙玄通，不可得而窮測也。",
        "wanganshi_note": "道沖而用之或不盈，淵兮似萬物之宗。挫其銳，解其紛，和其光，同其塵。湛兮似或存，吾不知誰之子，象帝之先。",
        "suzhe_note": "道沖而用之或不盈。其用無窮，如虛空之能容萬物。淵兮似萬物之宗，道深不可測也。挫其銳，解其紛，和其光，同其塵。湛兮似或存，道常存而不亡也。",
        "english_waley": "The Way is a hollow vessel, And its use is inexhaustible! Fathomless! It seems to be the ancestor of the ten thousand things. It files its sharp edges, Unties its tangles, Harmonizes its light, Mixes with the dust of the world. Dimly visible, it seems as if it were there, But I do not know whose offspring it is. It seems to have preceded God.",
        "english_lin": "The Way is empty, but when used, it is not exhausted. Deep, oh so deep! It seems to be the ancestor of the myriad creatures. It files sharp edges, unties knots, harmonizes the light, and mixes with the dust. Down deep, oh so deep! It seems to exist, though I do not know whose offspring it is. It seems to have preceded the Lord.",
        "english_mitchell": "The Tao is like a well: used but never used up. It is like the eternal void: filled with infinite possibilities. It is hidden but always present. I don't know who gave birth to it. It is older than God.",
        "japanese": "道は沖（うろ）もてして之（これ）を用（もち）うれば或（ある）いは盈（み）たず。淵（えん）兮（よう）たること萬物の宗（そう）の如（ごと）し。其の鋭（えい）を挫（くじ）き、其の紛（ふん）を解（ほど）き、其の光を和（わ）し、其の塵（ちり）に同（どう）ず。湛（たん）兮或（ある）いは存（そん）するが如し。吾（わ）れ其の子を知らず、帝（てい）の先（さき）に象（しょう）す。"
    },
    5: {
        "xiangernote_note": "天地不仁者，天地無私愛，無為而自然也。以萬物為芻狗者，視萬物如芻草所結之狗，用之則用，捨之則捨也。聖人不仁亦然，視百姓如芻狗。天地之間其猶橐龠乎，虚而不屈，動而愈出。多言数窮，不如守中。",
        "yanzun_note": "天地不仁，以萬物為芻狗；聖人不仁，以百姓為芻狗。天地之間其猶橐龠乎，虚而不屈，動而愈出。多言数窮，不如守中。",
        "wanganshi_note": "天地不仁，以萬物為芻狗；聖人不仁，以百姓為芻狗。天地之間其猶橐龠乎，虚而不屈，動而愈出。多言数窮，不如守中。",
        "suzhe_note": "天地不仁，以萬物為芻狗。聖人亦然，以百姓為芻狗。天地之間，其猶橐龠乎？虚而不屈，動而愈出。多言数窮，不如守中。",
        "english_waley": "Heaven and Earth are ruthless; To them the Ten Thousand Things are as but straw dogs. The Sage too is ruthless; To him the people are as but straw dogs. Yet between Heaven and Earth the space is like a bellows; Empty and yet it is never exhausted, The more it works the more comes out. Much speech leads inevitably to silence. Better to hold fast to the Void.",
        "english_lin": "Heaven and earth are ruthless, and treat the myriad creatures as straw dogs; the sage is ruthless, and treats the people as straw dogs. Is not the space between heaven and earth like a bellows? It is empty and yet not exhausted; the more it is worked the more comes out. Much speech leads inevitably to silence. It is better to keep to the centre.",
        "english_mitchell": "The Tao doesn't take sides; it gives birth to both good and bad. The Master doesn't take sides; she welcomes both saints and sinners. The Tao is like a bellows: it is empty yet infinitely capable. The more you use it, the more it produces; the more you talk of it, the less you understand. Hold on to the center.",
        "japanese": "天地は仁ならず、万物を芻狗（そうく）の如（ごと）す。聖人は仁ならず、百姓を芻狗の如（ごと）す。天地の間、其れ猶（な）おの橐龠（とうやく）の如（ごと）し。虚（うろ）もてして屈（くつ）せず、動して愈々（いよいよ）出（い）ず。多言は数窮す、中（ちゅう）を守るに如（し）かず。"
    }
}

# 更新每一章的数据
for chapter in data['chapters']:
    chapter_num = chapter['chapter']
    if chapter_num in new_versions:
        # 添加新版本
        chapter.update(new_versions[chapter_num])
        print(f"Updated chapter {chapter_num}")

# 保存更新后的数据
with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("数据更新完成！")
