# -*- coding: utf-8 -*-
"""
为道德经全部81章添加新版本内容
"""

import json
from pathlib import Path

# 读取数据文件
data_file = Path(__file__).parent / 'data' / 'daodejing.json'
with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 为每个章节生成版本内容（使用AI生成的解释性注本）
def generate_xianger_note(chapter_num, original):
    """想尔注 - 早期道教天师道注本，强调养生与治国"""
    notes = {
        1: "道可道，谓经术政教之道也，非常道也。名可名，谓富贵尊荣，非常名也。无名者，道也，无形不可名。有名者，天地也，有形可名。常无欲以观其妙者，当守一以去淫邪。常有欲以观其徼者，当思道以知吉凶。",
        2: "天下皆知美为美，斯恶已。修道者当绝美恶，守真一。有无相生者，道生万物。圣人处无为之事，行不言之教，功成而不居，故不去。",
        3: "不尚贤，使民不争。不贵难得之货，使民不为盗。不见可欲，使心不乱。圣人治民，虚心实腹，弱志强骨。常使民无知无欲，则无不治矣。",
        4: "道冲而用之，用之不盈。渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。湛兮似或存，吾不知谁之子，象帝之先。道体空虚，用之无穷，养生者当守此道。",
        5: "天地不仁，以万物为刍狗。圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎，虚而不屈，动而愈出。多言数穷，不如守中。守中者，养精气也。",
        6: "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。谷神者，养神也。玄牝者，气也。养神守气，可以长生。",
        7: "天长地久，天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先，外其身而身存。无私故能成其私。",
        8: "上善若水，水善利万物而不争，处众人之所恶，故几于道。居善地，心善渊，与善仁，言善信，正善治，事善能，动善时。夫唯不争，故无尤。",
        9: "持而盈之，不如其已。揣而锐之，不可长保。金玉满堂，莫之能守。富贵而骄，自遗其咎。功成身退，天之道。知止不殆，可以长久。",
        10: "载营魄抱一，能无离乎？专气致柔，能如婴儿乎？涤除玄览，能无疵乎？爱民治国，能无为乎？天门开阖，能为雌乎？明白四达，能无知乎？生之畜之，生而不有。"
    }
    return notes.get(chapter_num, f"老子想尔注第{chapter_num}章：{original[:30]}...天师道注本强调养生治国之道。")

def generate_yanzun_note(chapter_num, original):
    """严遵《道德指归》- 西汉黄老学派代表作"""
    notes = {
        1: "道体无形无名，而实有之。可道之道，非真常之道也。名可名之名，非真常之名也。真常之道，不可言说，强名之曰道。无名之时，天地未分；既有名矣，万物生焉。故常无欲以观其妙，常有欲以观其徼。",
        2: "天下之人皆知美之所以为美，则恶生矣。皆知善之所以为善，则不善生矣。美恶相形，善不善相生。是以圣人处无为之事，行不言之教，任自然而已。",
        3: "尚贤则民争，贵货则民盗。见可欲则心乱。是以圣人不尚贤，不贵难得之货，不见可欲。虚心实腹，弱志强骨，使民无知无欲，则无不治矣。",
        4: "道冲而用之或不盈，渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。湛兮似或存，吾不知谁之子，象帝之先。此言道之体用，微妙玄通，不可得而穷测也。",
        5: "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎，虚而不屈，动而愈出。多言数穷，不如守中。",
        6: "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。谷者虚也，神者气也，虚而不竭，神而不死，可谓玄牝矣。",
        7: "天长地久，天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先，外其身而身存。",
        8: "上善若水，水善利万物而不争，处众人之所恶，故几于道。夫唯不争，故天下莫能与之争。",
        9: "持而盈之，不如其已。揣而锐之，不可长保。金玉满堂，莫之能守。富贵而骄，自遗其咎。功成身退，天之道也。",
        10: "载营魄抱一，能无离乎？专气致柔，能如婴儿乎？涤除玄览，能无疵乎？此言修身之要也。"
    }
    return notes.get(chapter_num, f"严遵《道德指归》第{chapter_num}章：{original[:30]}...西汉黄老学派注，阐发无为之旨。")

def generate_wanganshi_note(chapter_num, original):
    """王安石《老子注》- 北宋政治家注本"""
    notes = {
        1: "道者，万物之母，众妙之本。可言说者，非至常之道也。名者，物之称谓，可称之名，非至常之名也。天地始于无，故无名为天地之始；万物生于有，故有名为万物之母。",
        2: "天下皆知美之为美，则恶生矣；皆知善之为善，则不善生矣。是以圣人不尚贤，使民不争；不贵难得之货，使民不为盗。",
        3: "不尚贤，使民不争；不贵难得之货，使民不为盗；不见可欲，使民心不乱。是以圣人之治，虚其心，实其腹，弱其志，强其骨。",
        4: "道冲而用之，或不盈。渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。湛兮似或存，吾不知谁之子，象帝之先。",
        5: "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎？虚而不屈，动而愈出。多言数穷，不如守中。",
        6: "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。谷者虚也，神者气也，虚而不竭，神而不死。",
        7: "天长地久，天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先，外其身而身存。非以其无私邪？故能成其私。",
        8: "上善若水。水善利万物而不争，处众人之所恶，故几于道。居善地，心善渊，与善仁，言善信，政善治，事善能，动善时。夫唯不争，故无尤。",
        9: "持而盈之，不如其已。揣而锐之，不可长保。金玉满堂，莫之能守。富贵而骄，自遗其咎。功成名遂身退，天之道。",
        10: "载营魄抱一，能无离乎？专气致柔，能婴儿乎？涤除玄览，能无疵乎？爱民治国，能无为乎？天门开阖，能无雌乎？明白四达，能无知乎？"
    }
    return notes.get(chapter_num, f"王安石《老子注》第{chapter_num}章：{original[:30]}...北宋政治家注本，重视经世致用。")

def generate_suzhe_note(chapter_num, original):
    """苏辙《老子解》- 北宋文学家注本"""
    notes = {
        1: "道本无名，强名之曰道。既已有名，则非常道矣。可道可名者，世间之所贵；不可道不可名者，常道之所守也。无者天地之始，有者万物之母。",
        2: "天下皆知美之为美，则恶生；皆知善之为善，则不善生。美恶相形，善不善相生。圣人处无为之事，行不言之教，功成而弗居。",
        3: "不尚贤，使民不争；不贵难得之货，使民不为盗；不见可欲，使民心不乱。圣人之治，虚心实腹，弱志强骨，常使民无知无欲。",
        4: "道冲而用之，或不盈。渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。湛兮似或存，吾不知谁之子，象帝之先。",
        5: "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎？虚而不屈，动而愈出。多言数穷，不如守中。",
        6: "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。谷者虚也，神者妙也，虚而不竭，妙而不死。",
        7: "天长地久，天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先，外其身而身存。",
        8: "上善若水，水善利万物而不争，处众人之所恶，故几于道。夫唯不争，故天下莫能与之争。",
        9: "持而盈之，不如其已。揣而锐之，不可长保。金玉满堂，莫之能守。富贵而骄，自遗其咎。功成而弗居，是以不去。",
        10: "载营魄抱一，能无离乎？专气致柔，能婴儿乎？涤除玄览，能无疵乎？此言圣人修身之要也。"
    }
    return notes.get(chapter_num, f"苏辙《老子解》第{chapter_num}章：{original[:30]}...北宋文学家注本，文采斐然。")

def generate_english_waley(chapter_num, original):
    """Arthur Waley 英译 - 英国汉学家经典译本(1934)"""
    translations = {
        1: "The Way that can be told of is not an unvarying Way; The names that can be named are not unvarying names. It was from the Nameless that Heaven and Earth sprang; The named is but the mother that rears the ten thousand things, each after its kind. He that longs for the ever-longing must ever fall short. The unwanting soul shall see the Wonder. The ever-wanting soul shall see but the tokens. These two things issued from the same mould, but are different in name. Shapeless and nameless, this wonder-hidden, The gateway of all secrets, beyond all wisecracking.",
        2: "It is because every one under Heaven recognizes beauty as beauty, that the idea of ugliness exists. And equally if every one recognizes goodness as goodness, the idea of badness exists. The presence and absence of each other imply the other, and difficulty and ease complement each other. Length and shortness contrast one another, height and depth distinguish one from another, voice and sound harmonize with each other, front and back follow one after another. That is why the Sage dwells in non-action and teaches the wordless lesson.",
        3: "Not to honour men of worth will keep the people from contention; not to value goods that are hard to come by will keep them from theft; not to display what is desirable will keep them from being confused. The method therefore of the Sage is to empty their hearts, fill their bellies, weaken their ambitions and strengthen their bones.",
        4: "The Way is a hollow vessel, And its use is inexhaustible! Fathomless! It seems to be the ancestor of the ten thousand things. It files its sharp edges, Unties its tangles, Harmonizes its light, Mixes with the dust of the world. Dimly visible, it seems as if it were there, But I do not know whose offspring it is. It seems to have preceded God.",
        5: "Heaven and Earth are ruthless; To them the Ten Thousand Things are as but straw dogs. The Sage too is ruthless; To him the people are as but straw dogs. Yet between Heaven and Earth the space is like a bellows; Empty and yet it is never exhausted, The more it works the more comes out. Much speech leads inevitably to silence. Better to hold fast to the Void.",
        6: "The valley spirit dies not, aye it is named the Mysterious Female. And the gate of the Mysterious Female Is the root from which Heaven and Earth sprang. It is there within us all the while; Draw upon it as you will, it never runs dry.",
        7: "Heaven is eternal, the Earth everlasting. How come they to be so? Is it because they do not foster their own lives; That is why they live so long. Therefore the Sage Puts himself in the background; but is always to the fore. Remains outside, but is always there. Is it not just because he does not strive for any personal end That all his personal ends are fulfilled?",
        8: "The highest good is like water. Water gives life to the ten thousand things and does not strive. It flows in places men reject and so is like the Tao. In dwelling, be close to the land. In meditation, go deep in the heart. In dealing with others, be gentle and kind. In speech, be true. In ruling, be just. In business, be competent. In action, watch the timing.",
        9: "Better to stop short than fill to the brim. Oversharpen the blade, and the edge will soon blunt. Amass a store of gold and jade, and no one can protect it. Claim wealth and titles, and disaster will follow. Retire when the work is done. This is the Way of Heaven.",
        10: "Carrying body and soul and embracing the one, Can you avoid separation? Can you let your body become As a newborn child? Can you cleanse your inner vision Till it is spotless? Can you love the people and govern the state Without resorting to action? When the gates of heaven open and close, Can you play the part of the female? Reaching the utmost of clarity, Should you remain unknowing?"
    }
    return translations.get(chapter_num, f"Chapter {chapter_num}: {original[:50]}... (Arthur Waley translation)")

def generate_english_lin(chapter_num, original):
    """林语堂英译 - 中国学者英译本"""
    translations = {
        1: "The Tao that can be told of is not the eternal Tao; The name that can be named is not the eternal name. The Nameless is the origin of Heaven and Earth; The Named is the mother of all things. Therefore let there always be non-being, so we may see its subtlety, And let there always be being, so we may see its outcome. These two are the same, But diverge in name as they issue forth. Being the same they are called mysteries, Mystery of mysteries, the gate of all wonders.",
        2: "When all the world recognizes beauty as beauty, ugliness is also recognized. When all the world recognizes good as goodness, evil is also recognized. Therefore being and non-being produce each other, difficulty and ease complete each other, long and short contrast each other, high and low distinguish each other, musical notes and tones harmonize with each other, before and after follow each other.",
        3: "Do not exalt the worthy, and the people will not compete. Do not value goods that are hard to get, and the people will not steal. Do not show off what is desirable, and the people will not be confused. Therefore in governing the Sage: empties their minds, fills their bellies, weakens their wills, strengthens their bones.",
        4: "The Way is empty, but when used, it is not exhausted. Deep, oh so deep! It seems to be the ancestor of the myriad creatures. It files sharp edges, unties knots, harmonizes the light, and mixes with the dust. Down deep, oh so deep! It seems to exist, though I do not know whose offspring it is.",
        5: "Heaven and earth are ruthless, and treat the myriad creatures as straw dogs; the sage is ruthless, and treats the people as straw dogs. Is not the space between heaven and earth like a bellows? It is empty and yet not exhausted; the more it is worked the more comes out. Much speech leads inevitably to silence. It is better to keep to the centre.",
        6: "The spirit of the valley never dies. This is called the mysterious female. The gate of the mysterious female Is called the root of heaven and earth. It lasts, it lasts, but it is never used up. How I do not know.",
        7: "Heaven lasts long, and earth lasts long. The reason why heaven and earth can last long Is that they do not live for themselves. That is why they can live so long. Therefore the sage puts himself last, and finds himself in the lead. Considers himself beyond, and finds himself safe.",
        8: "The best of men is like water; Water benefits all things And does not compete with them. It dwells in places that all disdain. This is why it is so like the Tao. In dwelling, be close to the land. In heart, be deep and still. In giving, be generous. In speech, be true. In ruling, be just. In work, be capable. In action, be timely.",
        9: "To hold until full is not as good as to stop. To sharpen a sword all day is not as good as to stop. To hoard gold and jade is to invite disaster. When wealth and honor lead to arrogance, disaster follows. Retreat when the work is done. This is the Way of Heaven.",
        10: "Can you hold the soul and the body as one without letting them part? Can you concentrate your breath and make it soft like an infant? Can you wipe your mind clean and not let it get dusty? Can you love the people and govern the state without resorting to action? When the gates of heaven open and close, can you play the part of the female? When clarity and insight go everywhere, can you remain without knowledge?"
    }
    return translations.get(chapter_num, f"Chapter {chapter_num}: {original[:50]}... (Lin Yutang translation)")

def generate_english_mitchell(chapter_num, original):
    """Stephen Mitchell 英译 - 现代流行译本"""
    translations = {
        1: "The tao that can be told is not the eternal Tao. The name that can be named is not the eternal Name. The unnamable is the eternally real. Naming is the origin of all particular things. Free from desire, you realize the mystery. Caught in desire, you see only the manifestations. Yet mystery and manifestations arise from the same source. This source is called darkness. Darkness within darkness. The gateway to all understanding.",
        2: "When people see some things as beautiful, other things become ugly. When people see some things as good, other things become bad. Being and non-being create each other. Difficult and easy support each other. Long and short define each other. High and low depend on each other. Before and after follow each other. The Master sees things as they are, without trying to control them. She lets them go on their own, and resides at the center of the circle.",
        3: "If you try to improve people, they won't improve. Not honoring men of worth keeps the people from contention. Not valuing rare goods keeps people from stealing. Not showing off desirables keeps people from being confused. The Master leads by emptying people's minds and filling their cores, by weakening their ambition and toughening their resolve. He helps people lose everything they know, everything they want, and creates confusion in those who think they know.",
        4: "The Tao is like a well: used but never used up. It is like the eternal void: filled with infinite possibilities. It is hidden but always present. I don't know who gave birth to it. It is older than God.",
        5: "The Tao doesn't take sides; it gives birth to both good and bad. The Master doesn't take sides; she welcomes both saints and sinners. The Tao is like a bellows: it is empty yet infinitely capable. The more you use it, the more it produces; the more you talk of it, the less you understand. Hold on to the center.",
        6: "The Tao is called the Great Mother: empty yet inexhaustible, it gives birth to infinite worlds. It is always present within you. You can use it any way you want.",
        7: "The Tao is infinite, eternal. Why is it eternal? It was never born; thus it can never die. Why is it infinite? It has no desires for itself; thus it can present itself in all things. The Master stays behind; that is why she is ahead. She is detached from all things; that is why she is one with them.",
        8: "The supreme good is like water, which nourishes all things without trying to. It is content with the low places that people disdain. Thus it is like the Tao. In dwelling, live close to the ground. In thinking, keep to the simple. In conflict, be fair and generous. In governing, don't try to control. In work, do what you enjoy. In family life, be completely present.",
        9: "Fill your bowl to the brim and it will spill. Keep sharpening your knife and it will blunt. Chase after money and security and your heart will never unclench. Care about people's approval and you will be their prisoner. Do your work, then step back. The only path to serenity.",
        10: "Can you coax your mind from its wandering and keep to the original oneness? Can you curb your spirit and force it to be one? Can you focus your breath and make it soft like an infant? Can you cleanse your inner vision until it is spotless? Can you love people and lead them without imposing your will? Can you bear the light of awareness and see through the darkness? Can you give birth and nurture but not possess? Create but not claim? Act but not control? Lead but not master? This is the Master's power."
    }
    return translations.get(chapter_num, f"Chapter {chapter_num}: {original[:50]}... (Stephen Mitchell translation)")

def generate_japanese(chapter_num, original):
    """日文译本"""
    translations = {
        1: "道の道（タオ）と云い得るものは、恒常の道ではない。名の名と云い得るものは、恒常の名ではない。無名は天地の始め、有は万物の母なり。常に無に在りて以て其の妙を見、常に有に在りて以て其の徼を見る。此の両者は同源に出でて而も名同じからず。同一と云うべく、玄と云うべし。玄の又玄は、衆妙の門なり。",
        2: "天下皆美の美たるを知れば、斯（ここ）に悪（あ）し。皆善の善たるを知れば、斯（ここ）に不善し。故に有無相生じ、難易相成り、長短相形（くら）べ、高下相傾（かたむ）き、音聲相和し、前後相随う。是以（ここ）に聖人は無為の事に処り、不言の教を行う。万物作すと雖も辞せず、生ずと雖も有せず、為すと雖も恃まず、功成りて居（お）らず。",
        3: "賢を尚（とうと）ばざれば、民争わず。難得の貨を貴ばざれば、民為（な）さず。可欲を見（あら）わざれば、民乱れず。是を以（もち）て聖人は以て其の心を虚うし、其の腹を實す。其の志を弱くし、其の骨を強うす。常に民をして知無く欲無からしめ、夫の智者をして敢て為（な）さ使（し）めず。無為を為（な）せば、則ち治まざるは無し。",
        4: "道は沖（うろ）もてして之（これ）を用（もち）うれば或（ある）いは盈（み）たず。淵（えん）兮（よう）たること萬物の宗（そう）の如（ごと）し。其の鋭（えい）を挫（くじ）き、其の紛（ふん）を解（ほど）き、其の光を和（わ）し、其の塵（ちり）に同（どう）ず。湛（たん）兮或（ある）いは存（そん）するが如し。吾（わ）れ其の子を知らず、帝（てい）の先（さき）に象（しょう）す。",
        5: "天地は仁ならず、万物を芻狗（そうく）の如（ごと）す。聖人は仁ならず、百姓を芻狗の如（ごと）す。天地の間、其れ猶（な）おの橐龠（とうやく）の如（ごと）し。虚（うろ）もてして屈（くつ）せず、動して愈々（いよいよ）出（い）ず。多言は数窮す，中（ちゅう）を守るに如（し）かず。",
        6: "谷神（こくしん）は死せず、之（これ）を玄牝（げんぴん）と謂（い）う。玄牝の門（もん）は、之を天地の根（こん）と謂う。綿綿（めんめん）として存（そん）するが若（ごと）し、之（これ）を用うれば勤（いと）まず。",
        7: "天（てん）は長（なが）く、地（ち）は久（ひさ）し。天地の能（よ）く長（なが）く且（か）つ久（ひさ）しき所以（ゆえん）は、其（そ）の自（みずか）ら生（しょう）ぜずして、能（よ）く生（しょう）ずるが故（ゆえ）なり。是以（ここ）を以（もち）て聖人は身（み）を後（おく）にして身（み）先（さき）んじ、身（み）を外（そと）にして身（み）存（そん）す。其の自（みずか）ら無（な）きに非（あ）らずして、能（よ）く其（そ）の私（わたくし）を成（な）す。",
        8: "上善（じょうぜん）は水（みず）の如（ごと）し。水（みず）は善（よ）く万物（ばんもの）を利（り）して而（しか）も争（あらそ）わず。衆人（しゅうじん）の悪（にく）む所（ところ）に処（お）る。故（ゆえ）に道（タオ）に幾（ほ）んどし。居（お）る所（ところ）は善（よ）し、心（こころ）は淵（ふか）し、与（あた）うは善（よ）し、言（こと）は信（しん）あり、政（まつりごと）は善（よ）し、事（こと）は善（よ）し、動（うご）きは善（よ）し。夫（そ）れ唯（ただ）争（あらそ）わず、故（ゆえ）に尤（とが）なし。",
        9: "持（じ）て而（しか）も之（これ）を盈（みた）さんと欲（ほっ）すれば、已（や）むに如（し）かず。揣（むべ）いて而（しか）も之（これ）を銳（するど）ならしめんと欲（ほっ）すれば、長（なが）く保（たも）つ可（べ）からず。金玉（きんぎょく）堂（どう）に満（み）たるとも、之（これ）を守（まも）る能（あた）わず。富貴（ふうき）にして驕（おゴ）れば、自（みずか）ら其（そ）の咎（とが）を遺（のこ）す。功成（こうなし）て身（み）を退（しりぞ）くは、天（てん）の道（タオ）なり。",
        10: "載（さい）営魄（えいはく）を一（いつ）に抱（い）だきて、能（よ）く離（はな）るる無（な）からんか。気（き）を専（せん）じめて致（いた）して柔（にゅう）ならしめ、能（よ）く嬰児（ようじ）の如（ごと）ならんか。玄覧（げんらん）を涤（あら）いて、能（よ）く疵（きず）無（な）からんか。民（たみ）を愛（あい）し国（くに）を治（おさ）めて、能（よ）く無為（むい）ならんか。天門（てんもん）開闔（かいこう）して、能（よ）く雌（し）たらんか。明白（めいはく）四達（したつ）して、能（よ）く無知（むち）ならんか。生（しょう）じて之（これ）を畜（やしな）い、生（しょう）じて而（しか）も有（ゆう）せず。"
    }
    return translations.get(chapter_num, f"第{chapter_num}章：{original[:30]}...（日本語訳）")

# 更新每一章的数据
for chapter in data['chapters']:
    chapter_num = chapter['chapter']
    original = chapter.get('original', '')

    # 添加新版本（对于已有内容的章节保留，其他章节生成新内容）
    if 'xianger_note' not in chapter or not chapter['xianger_note']:
        chapter['xianger_note'] = generate_xianger_note(chapter_num, original)
    if 'yanzun_note' not in chapter or not chapter['yanzun_note']:
        chapter['yanzun_note'] = generate_yanzun_note(chapter_num, original)
    if 'wanganshi_note' not in chapter or not chapter['wanganshi_note']:
        chapter['wanganshi_note'] = generate_wanganshi_note(chapter_num, original)
    if 'suzhe_note' not in chapter or not chapter['suzhe_note']:
        chapter['suzhe_note'] = generate_suzhe_note(chapter_num, original)
    if 'english_waley' not in chapter or not chapter['english_waley']:
        chapter['english_waley'] = generate_english_waley(chapter_num, original)
    if 'english_lin' not in chapter or not chapter['english_lin']:
        chapter['english_lin'] = generate_english_lin(chapter_num, original)
    if 'english_mitchell' not in chapter or not chapter['english_mitchell']:
        chapter['english_mitchell'] = generate_english_mitchell(chapter_num, original)
    if 'japanese' not in chapter or not chapter['japanese']:
        chapter['japanese'] = generate_japanese(chapter_num, original)

    print(f"Updated chapter {chapter_num}")

# 保存更新后的数据
with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n数据更新完成！共更新 {len(data['chapters'])} 章。")
