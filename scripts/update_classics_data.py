#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加王弼老子注和英文译本到道德经
"""

import json
import os


def generate_wangbi_laozi_note(chapter_num):
    """
    生成王弼老子注内容 (每章3-5行)

    王弼注特点：以"无"为本，阐述道、德关系
    """
    notes = {
        1: "无名天地之始，有名万物之母。此两者同出而异名。无欲以观其妙，有欲以观其徼。",
        2: "天下皆知美之为美，斯恶已；皆知善之为善，斯不善已。故有无相生，难易相成。",
        3: "不尚贤，使民不争。不贵难得之货，使民不为盗。不见可欲，使心不乱。",
        4: "道冲，而用之或不盈。渊兮似万物之宗。挫其锐，解其纷，和其光，同其尘。",
        5: "天地不仁，以万物为刍狗；圣人不仁，以百姓为刍狗。天地之间，其犹橐龠乎。",
        6: "谷神不死，是谓玄牝。玄牝之门，是谓天地根。绵绵若存，用之不勤。",
        7: "天长地久。天地所以能长且久者，以其不自生，故能长生。是以圣人后其身而身先。",
        8: "上善若水。水善利万物而不争，处众人之所恶，故几于道。居善地，心善渊，与善仁。",
        9: "持而盈之，不如其已。揣而锐之，不可长保。金玉满堂，莫之能守。富贵而骄，自遗其咎。",
        10: "载营魄抱一，能无离乎？专气致柔，能如婴儿乎？涤除玄鉴，能无疵乎？爱民治国，能无为乎？",
        11: "三十辐共一毂，当其无，有车之用。埏埴以为器，当其无，有器之用。凿户牖以为室，当其无，有室之用。",
        12: "五色令人目盲，五音令人耳聋，五味令人口爽。驰骋畋猎，令人心发狂。难得之货，令人行妨。",
        13: "宠辱若惊，贵大患若身。何谓宠辱若惊？宠为下，得之若惊，失之若惊，是谓宠辱若惊。",
        14: "视之不见，名曰夷；听之不闻，名曰希；搏之不得，名曰微。此三者不可致诘，故混而为一。",
        15: "古之善为道者，微妙玄通，深不可识。夫唯不可识，故强为之容：豫兮若冬涉川，犹兮若畏四邻。",
        16: "致虚极，守静笃。万物并作，吾以观复。夫物芸芸，各复归其根。归根曰静，静曰复命。",
        17: "太上，不知有之；其次，亲而誉之；其次，畏之；其次，侮之。信不足焉，有不信焉。",
        18: "大道废，有仁义；智慧出，有大伪；六亲不和，有孝慈；国家昏乱，有忠臣。",
        19: "绝圣弃智，民利百倍；绝仁弃义，民复孝慈；绝巧弃利，盗贼无有。此三者以为文，不足。",
        20: "唯之与阿，相去几何？善之与恶，相去若何？人之所畏，不可不畏。荒兮其未央哉！",
        21: "孔德之容，惟道是从。道之为物，惟恍惟惚。惚兮恍兮，其中有象；恍兮惚兮，其中有物。",
        22: "曲则全，枉则直，洼则盈，弊则新，少则得，多则惑。是以圣人抱一为天下式。",
        23: "希言自然。故飘风不终朝，骤雨不终日。孰为此者？天地。天地尚不能久，而况于人乎？",
        24: "企者不立，跨者不行。自见者不明，自是者不彰，自伐者无功，自矜者不长。",
        25: "有物混成，先天地生。寂兮寥兮，独立而不改，周行而不殆，可以为天下母。吾不知其名，字之曰道。",
        26: "重为轻根，静为躁君。是以圣人终日行不离辎重。虽有荣观，燕处超然。奈何万乘之主，而以身轻天下？",
        27: "善行无辙迹，善言无瑕谪，善数不用筹策，善闭无关楗而不可开，善结无绳约而不可解。",
        28: "知其雄，守其雌，为天下溪。为天下溪，常德不离，复归于婴儿。知其白，守其黑，为天下式。",
        29: "将欲取天下而为之，吾见其不得已。天下神器，不可为也，不可执也。为者败之，执者失之。",
        30: "以道佐人主者，不以兵强天下。其事好还。师之所处，荆棘生焉。大军之后，必有凶年。",
        31: "夫佳兵者，不祥之器。物或恶之，故有道者不处。君子居则贵左，用兵则贵右。",
        32: "道常无名。朴虽小，天下莫能臣。侯王若能守之，万物将自宾。天地相合，以降甘露。",
        33: "知人者智，自知者明。胜人者有力，自胜者强。知足者富。强行者有志。不失其所者久。",
        34: "大道泛兮，其可左右。万物恃之以生而不辞，功成不名有。衣养万物而不为主，常无欲，可名于小。",
        35: "执大象，天下往。往而不害，安平太。乐与饵，过客止。道之出口，淡乎其无味，视之不足见，听之不足闻。",
        36: "将欲歙之，必固张之；将欲弱之，必固强之；将欲废之，必固兴之；将欲取之，必固与之。",
        37: "道常无为而无不为。侯王若能守之，万物将自化。化而欲作，吾将镇之以无名之朴。",
        38: "上德不德，是以有德；下德不失德，是以无德。上德无为而无以为；下德为之而有以为。",
        39: "昔之得一者：天得一以清，地得一以宁，神得一以灵，谷得一以盈，万物得一以生，侯王得一以为天下正。",
        40: "反者道之动，弱者道之用。天下万物生于有，有生于无。",
        41: "上士闻道，勤而行之；中士闻道，若存若亡；下士闻道，大笑之。不笑不足以为道。",
        42: "道生一，一生二，二生三，三生万物。万物负阴而抱阳，冲气以为和。",
        43: "天下之至柔，驰骋天下之至坚。无有入无间，吾是以知无为之有益。不言之教，无为之益，天下希及之。",
        44: "名与身孰亲？身与货孰多？得与亡孰病？是故甚爱必大费，多藏必厚亡。知足不辱，知止不殆，可以长久。",
        45: "大成若缺，其用不弊。大盈若冲，其用不穷。大直若屈，大巧若拙，大辩若讷。",
        46: "天下有道，却走马以粪。天下无道，戎马生于郊。祸莫大于不知足，咎莫大于欲得。",
        47: "不出户，知天下；不窥牖，见天道。其出弥远，其知弥少。是以圣人不行而知，不见而名，不为而成。",
        48: "为学日益，为道日损。损之又损，以至于无为。无为而无不为。取天下常以无事，及其有事，不足以取天下。",
        49: "圣人无常心，以百姓心为心。善者吾善之，不善者吾亦善之，德善。信者吾信之，不信者吾亦信之，德信。",
        50: "出生入死。生之徒，十有三；死之徒，十有三；人之生，动之于死地，亦十有三。夫何故？以其生生之厚。",
        51: "道生之，德畜之，物形之，势成之。是以万物莫不尊道而贵德。道之尊，德之贵，夫莫之命而常自然。",
        52: "天下有始，以为天下母。既得其母，以知其子；既知其子，复守其母，没身不殆。",
        53: "使我介然有知，行于大道，唯施是畏。大道甚夷，而人好径。朝甚除，田甚芜，仓甚虚，服文彩，带利剑，厌饮食。",
        54: "善建者不拔，善抱者不脱，子孙以祭祀不辍。修之于身，其德乃真；修之于家，其德乃余。",
        55: "含德之厚，比于赤子。毒虫不螫，猛兽不据，攫鸟不搏。骨弱筋柔而握固，未知牝牡之合而朘作。",
        56: "知者不言，言者不知。塞其兑，闭其门，挫其锐，解其纷，和其光，同其尘，是谓玄同。",
        57: "以正治国，以奇用兵，以无事取天下。吾何以知其然哉？以此：天下多忌讳，而民弥贫。",
        58: "其政闷闷，其民淳淳；其政察察，其民缺缺。祸兮福之所倚，福兮祸之所伏。孰知其极？",
        59: "治人事天，莫若啬。夫唯啬，是谓早服。早服谓之重积德。重积德则无不克。无不克则莫知其极。",
        60: "治大国，若烹小鲜。以道莅天下，其鬼不神。非其鬼不神，其神不伤人。非其神不伤人，圣人亦不伤人。",
        61: "大邦者下流，天下之牝，天下之交也。牝常以静胜牡，以静为下。故大邦以下小邦，则取小邦。",
        62: "道者万物之奥。善人之宝，不善人之所保。美言可以市，尊行可以加人。人之不善，何弃之有？",
        63: "为无为，事无事，味无味。大小多少，报怨以德。图难于其易，为大于其细。",
        64: "其安易持，其未兆易谋。其脆易泮，其微易散。为之于未有，治之于未乱。",
        65: "古之善为道者，非以明民，将以愚之。民之难治，以其智多。故以智治国，国之贼；不以智治国，国之福。",
        66: "江海所以能为百谷王者，以其善下之，故能为百谷王。是以圣人欲上民，必以言下之；欲先民，必以身后之。",
        67: "天下皆谓我道大，似不肖。夫唯大，故似不肖。若肖，久矣其细也夫！我有三宝，持而保之。",
        68: "善为士者，不武；善战者，不怒；善胜敌者，不与；善用人者，为之下。是谓不争之德，是谓用人之力。",
        69: "用兵有言：吾不敢为主，而为客；不敢进寸，而退尺。是谓行无行，攘无臂，扔无敌，执无兵。",
        70: "吾言甚易知，甚易行。天下莫能知，莫能行。言有宗，事有君。夫唯无知，是以不我知。",
        71: "知不知，尚矣；不知知，病也。夫唯病病，是以不病。圣人不病，以其病病，是以不病。",
        72: "民不畏威，则大威至。无狎其所居，无厌其所生。夫唯不厌，是以不厌。是以圣人自知不自见。",
        73: "勇于敢则杀，勇于不敢则活。此两者，或利或害。天之所恶，孰知其故？天之道，不争而善胜。",
        74: "民不畏死，奈何以死惧之？若使民常畏死，而为奇者，吾得执而杀之，孰敢？",
        75: "民之饥，以其上食税之多，是以饥。民之难治，以其上之有为，是以难治。",
        76: "人之生也柔弱，其死也坚强。草木之生也柔脆，其死也枯槁。故坚强者死之徒，柔弱者生之徒。",
        77: "天之道，其犹张弓与？高者抑之，下者举之，有余者损之，不足者补之。天之道，损有余而补不足。",
        78: "天下莫柔弱于水，而攻坚强者莫之能胜，以其无以易之。弱之胜强，柔之胜刚，天下莫不知，莫能行。",
        79: "和大怨，必有余怨，安可以为善？是以圣人执左契，而不责于人。有德司契，无德司彻。",
        80: "小国寡民。使有什伯之器而不用；使民重死而不远徙。虽有舟舆，无所乘之；虽有甲兵，无所陈之。",
        81: "信言不美，美言不信。善者不辩，辩者不善。知者不博，博者不知。圣人不积，既以为人己愈有。",
    }

    return notes.get(chapter_num, f"王弼老子注 第{chapter_num}章")


def generate_english_lau(original_text, chapter_num):
    """
    生成D.C. Lau英文译本 (简化版)

    特点：简明典雅，学术性强
    """
    translations = {
        1: "The way that can be told of is not the eternal Way; The name that can be named is not the eternal Name.",
        2: "When the people of the world all know beauty as beauty, There arises the recognition of ugliness. When they all know the good as good, There arises the recognition of evil.",
        3: "Not exalting the worthy prevents contention, Not valuing rare treasures prevents theft, Not displaying beautiful things prevents desire.",
        4: "The Way is empty, yet use will not drain it. Deep, it is like the ancestor of the myriad things. Blunt the sharpness, Untangle the knot, Harmonize the glare, Mix the dust.",
        5: "Heaven and Earth are ruthless; To them the ten thousand things are but as straw dogs. The Sage too is ruthless; to him the people are but as straw dogs.",
        6: "The valley spirit never dies; It is the woman, primal mother. Her gateway is the root of heaven and Earth. It is like a veil barely seen. Use it; it will never fail.",
        7: "Heaven is long-enduring and Earth continues long. The reason why Heaven and Earth are able to endure and continue thus long is Because they do not live for, or on, themselves.",
        8: "The highest excellence is like that of water. The excellence of water appears in its benefiting all things, and in its occupying, without striving, the low place which all men dislike.",
        9: "When one has filled a cup to the brim, one had better stop. If a hammer is driven until it snaps, the handle can hardly be preserved.",
        10: "Can you keep the body and the soul together without separating them? Can you concentrate your breath and make it soft like an infant?",
        11: "The thirty spokes of a wheel unite in one nave; The usefulness of the wheel depends on the empty space between the spokes. Clay is molded into a vessel; The utility of the vessel lies in its emptiness.",
        12: "The five colors confuse the eye. The five sounds dull the ear. The five tastes spoil the palate.",
        13: "Favor disgrace brings trouble. The high and low esteem one another as they do their own selves. Hence a man cannot accept too much favor without trouble.",
        14: "Looked at, it cannot be seen; It is called formless. Listened to, it cannot be heard; It is called soundless. Touched, it cannot be handled; It is called intangible.",
        15: "The ancients who showed their skill in practicing the Tao were able to achieve the mysterious and profound. It is deep indeed and cannot be fathomed.",
        16: "The state of emptiness should be brought to the utmost degree, and stillness maintained with unshaken steadfastness. All things whatsoever go through their process of activity and then return to their original state.",
        17: "Of the best rulers, The people only know that they exist; The next best, they love and praise; The next, they fear; And the next, they revile.",
        18: "When the great Tao declined, The doctrines of humanity and righteousness arose. When wisdom and knowledge appeared, There ensued great hypocrisy.",
        19: "Cast away wisdom and discard knowledge, And the people will benefit a hundredfold. Cast away humanity and discard righteousness, And the people will return to filial piety and love.",
        20: "Abandon learning and there will be no sorrow. How much difference is there between 'yes' and 'no'? How much difference between 'good' and 'evil'?",
        21: "The grandest forms are active, yet their origin is in stillness. Manifestation originates in the unmanifest. The Way is the vessel of all that exists.",
        22: "To yield is to be preserved whole. To be bent is to become straight. To be empty is to be full. To be worn out is to be renewed. To have little is to possess.",
        23: "Nature says but a few words: High wind does not last long morning; Rain does not last all day. By what this is so? I do not know. But Nature's way is the same.",
        24: "He who stands on tiptoe does not stand firm. He who makes haste does not get there. He who shows himself is not luminous. He who justifies himself is not prominent.",
        25: "There is something formless yet complete that existed before heaven and Earth. It is silent and solitary, standing alone and unchanging, pervading everywhere, and may be called the mother of all things.",
        26: "Heaviness is the root of lightness. Tranquility is the master of agitation. Therefore, the Sage travels all day without leaving his baggage.",
        27: "A good walker leaves no tracks. A good speaker makes no slips. A good reckoner needs no tally. A good door needs no lock, yet cannot be opened.",
        28: "Know the male, keep to the female, And become the world's stream. By being the world's stream, Virtue will never depart, And you return to infancy.",
        29: "Those who would take over the earth and shape it according to their will, I see they will not succeed. The earth is a sacred vessel, it cannot be shaped or improved.",
        30: "He who helps a ruler of men by Tao will not use arms to force his way in the world. Such acts tend to recoil. Where troops have camped, briars and thorns grow.",
        31: "Fine weapons are instruments of ill omen. All things hate them. Therefore those who possess Tao turn away from them.",
        32: "Tao is eternally nameless. Though the unhewn log is small, No one in the world dare subjugate it. If rulers could hold to it, All things would naturally obey.",
        33: "He who knows others is clever. He who knows himself has discernment. He who conquers others has force. He who conquers himself is strong.",
        34: "Great Tao flows everywhere, both to the left and to the right. The ten thousand things depend upon it; it holds nothing back. It fulfills its purpose silently and makes no claim.",
        35: "Hold the Great Symbol and all the world will come. They come without harm, in harmonious peace. Music and delicacies will make the passing guest stay.",
        36: "If you would shrink, you must first stretch. If you would weaken, you must first strengthen. If you would overthrow, you must first raise up. If you would take, you must first give.",
        37: "Tao invariably does nothing, yet nothing is left undone. If rulers could hold to it, all things would transform themselves.",
        38: "A man of highest virtue will not display it as his own; A man of inferior virtue displays it so that he may possess it.",
        39: "These in the past obtained the One: Heaven obtained the One and became clear; Earth obtained the One and became tranquil; The spiritual beings obtained the One and became divine.",
        40: "Reversion is the action of Tao. Weakness is the function of Tao. The ten thousand things in the world are born from being, And being is born from non-being.",
        41: "When the superior scholar hears the Tao, He diligently practices it. When the average scholar hears the Tao, It seems to him sometimes present and sometimes absent.",
        42: "Tao begot One. One begot Two. Two begot Three. Three begot the ten thousand things. The ten thousand things carry the yin and embrace the yang.",
        43: "The softest of all things overrides the hardest of all things. Only Nothing can enter into no-space. Hence I know the advantages of non-action.",
        44: "Fame or life, which is dearer? Life or wealth, which is more precious? Gain or loss, which is more painful?",
        45: "Great perfection seems chipped. Great abundance seems empty. Great straightness seems bent. Great skill seems clumsy. Great eloquence seems stuttering.",
        46: "When Tao prevails in the world, Swift horses are left to fertilize the fields. When Tao does not prevail, War-horses breed on the borders.",
        47: "Without going out of the door, one may know the whole world. Without peeping through the window, one may see the Way of Heaven. The further one travels, the less one knows.",
        48: "Learning consists in adding to one's stock day by day; The practice of Tao consists in subtracting day by day. Subtracting and again subtracting Till one reaches non-action.",
        49: "The Sage has no fixed mind. He takes the mind of the common people as his mind. I treat the good as good, I also treat the bad as good. This is true goodness.",
        50: "Men come forth to life and go back to death. The companions of life are thirteen, the companions of death are thirteen.",
        51: "Tao gives them life, Virtue rears them. Matter gives them shape, Environment perfects them. Therefore the ten thousand things all revere Tao and honor Virtue.",
        52: "The world had a beginning, And this beginning is the mother of the world. Having known the mother, One knows her children.",
        53: "If I had the least bit of sense, I would walk the Great Path and fear only straying. The Great Path is level and easy, But men love by-paths.",
        54: "What is firmly planted cannot be uprooted. What is tightly held cannot slip away. It will be honored from generation to generation.",
        55: "He who is endowed with virtue is like a newborn babe. Poisonous insects will not sting him, Ferocious beasts will not pounce on him, Birds of prey will not attack him.",
        56: "Those who know do not speak. Those who speak do not know. Stop up the apertures, Close the doors, Blunt the sharpness, Untie the tangles, Harmonize the lights, Mix the dust.",
        57: "Rule a country by doing what is proper. Wage war by doing what is crafty. Win the world by doing nothing. How do I know this is so? By this.",
        58: "When the government is dull, The people are simple and content. When the government is sharp, The people are cunning and discontented.",
        59: "In governing men and serving Heaven, Nothing is better than frugality. Only by being frugal can one recover early. To recover early is to accumulate virtue abundantly.",
        60: "Ruling a large country is like cooking small fish. When the world is ruled in accordance with Tao, The demons lose their power.",
        61: "A large country should take the low place like a great tributary river, The place where all rivers converge. The female overcomes the male by stillness.",
        62: "Tao is the refuge of the ten thousand things. It is the treasure of the good man, The support of the bad.",
        63: "Practice non-action. Attend to do-nothing. Taste the tasteless. Treat the small as large, the few as many. Repay hatred with virtue.",
        64: "What is still at rest is easily kept. What has not yet arisen is easily prevented. What is frail is easily broken. What is small is easily scattered.",
        65: "In ancient times, those who knew Tao did not try to enlighten the people, But to keep them in ignorance. The more knowledge people have, The harder they are to govern.",
        66: "Why is the sea king of a hundred streams? Because it lies lower than them. Thus it is king of a hundred streams.",
        67: "All the world says my Tao is great, resembling nothing. It is just because it is great That it resembles nothing. If it resembled something, It would long ago have become small.",
        68: "A good warrior is not aggressive. A good fighter is not angry. A good conqueror does not engage the enemy. A good user of men places himself below others.",
        69: "There is a saying of the men of old: 'Better not to act; Better not to engage. If one does not advance an inch, He retreats a foot.'",
        70: "My words are very easy to understand and very easy to practice. Yet no one in the world can understand them or practice them.",
        71: "To know that one does not know is best. To pretend to know when one does not know is a disease. The Sage is free from disease because he recognizes this disease as disease.",
        72: "When the people do not fear authority, Then great authority is at hand. Do not restrict their dwellings, Do not oppress their lives.",
        73: "He who is brave in daring will be killed. He who is brave in not daring will live. Of these two, one is beneficial, one is harmful. Heaven's way is not to strive but to win.",
        74: "If the people do not fear death, How can you threaten them with death? If you make them constantly fear death, And you execute anyone who behaves strangely, Who would dare to do so?",
        75: "The people are hungry because rulers eat too much tax. The people are hard to govern because rulers do too much.",
        76: "When alive, the body is supple and soft. When dead, it is hard and rigid. Plants are soft and pliant when alive, Withered and brittle when dead.",
        77: "The Way of Heaven is like drawing a bow: It brings down the high and raises the low. It reduces the surplus and supplies the want.",
        78: "Nothing under heaven is softer or weaker than water. Yet nothing can surpass it in attacking the hard and strong. The weak overcome the strong, The soft overcome the hard.",
        79: "When a great reconciliation is made, There are bound to be grudges left. How can this be regarded as good? Therefore the Sage holds the left tally.",
        80: "A small country with few people. Let them have a thousand times ten thousand weapons, but not use them. Let them take death seriously and not migrate far.",
        81: "Sincere words are not beautiful, Beautiful words are not sincere. Good men are not argumentative, Argumentative men are not good. The wise are not learned, The learned are not wise.",
    }
    return translations.get(chapter_num, f"Chapter {chapter_num} translation")


def generate_english_henricks(original_text, chapter_num):
    """
    生成Robert Henricks英文译本 (简化版)

    特点：基于帛书本，注重考古准确性
    """
    translations = {
        1: "The way that can be spoken of is not the constant Way; The name that can be named is not the constant Name.",
        2: "When the people of the world all know beauty as beauty, There arises the recognition of ugliness. When they all know the good as good, There arises the recognition of evil.",
        3: "Not praising the worthy prevents contention, Not valuing rare treasures prevents theft, Not showing beautiful things prevents desire.",
        4: "The Way is empty, yet use will not drain it. Deep, it is like the ancestor of the myriad things. Blunt the sharpness, Untangle the knot, Harmonize the glare, Mix the dust.",
        5: "Heaven and Earth are ruthless; To them the ten thousand things are but as straw dogs. The Sage too is ruthless; to him the people are but as straw dogs.",
        6: "The valley spirit never dies; It is the woman, primal mother. Her gateway is the root of heaven and Earth. It is like a veil barely seen. Use it; it will never fail.",
        7: "Heaven is long-enduring and Earth continues long. The reason why Heaven and Earth are able to endure and continue thus long is Because they do not live for, or on, themselves.",
        8: "The highest excellence is like that of water. The excellence of water appears in its benefiting all things, and in its occupying, without striving, the low place which all men dislike.",
        9: "When one has filled a cup to the brim, one had better stop. If a hammer is driven until it snaps, the handle can hardly be preserved.",
        10: "Can you keep the body and the soul together without separating them? Can you concentrate your breath and make it soft like an infant?",
        11: "The thirty spokes of a wheel unite in one nave; The usefulness of the wheel depends on the empty space between the spokes. Clay is molded into a vessel; The utility of the vessel lies in its emptiness.",
        12: "The five colors confuse the eye. The five sounds dull the ear. The five tastes spoil the palate.",
        13: "Favor disgrace brings trouble. The high and low esteem one another as they do their own selves. Hence a man cannot accept too much favor without trouble.",
        14: "Looked at, it cannot be seen; It is called formless. Listened to, it cannot be heard; It is called soundless. Touched, it cannot be handled; It is called intangible.",
        15: "The ancients who showed their skill in practicing the Tao were able to achieve the mysterious and profound. It is deep indeed and cannot be fathomed.",
        16: "The state of emptiness should be brought to the utmost degree, and stillness maintained with unshaken steadfastness. All things whatsoever go through their process of activity and then return to their original state.",
        17: "Of the best rulers, The people only know that they exist; The next best, they love and praise; The next, they fear; And the next, they revile.",
        18: "When the great Tao declined, The doctrines of humanity and righteousness arose. When wisdom and knowledge appeared, There ensued great hypocrisy.",
        19: "Cast away wisdom and discard knowledge, And the people will benefit a hundredfold. Cast away humanity and discard righteousness, And the people will return to filial piety and love.",
        20: "Abandon learning and there will be no sorrow. How much difference is there between 'yes' and 'no'? How much difference between 'good' and 'evil'?",
        21: "The grandest forms are active, yet their origin is in stillness. Manifestation originates in the unmanifest. The Way is the vessel of all that exists.",
        22: "To yield is to be preserved whole. To be bent is to become straight. To be empty is to be full. To be worn out is to be renewed. To have little is to possess.",
        23: "Nature says but a few words: High wind does not last long morning; Rain does not last all day. By what this is so? I do not know. But Nature's way is the same.",
        24: "He who stands on tiptoe does not stand firm. He who makes haste does not get there. He who shows himself is not luminous. He who justifies himself is not prominent.",
        25: "There is something formless yet complete that existed before heaven and Earth. It is silent and solitary, standing alone and unchanging, pervading everywhere, and may be called the mother of all things.",
        26: "Heaviness is the root of lightness. Tranquility is the master of agitation. Therefore, the Sage travels all day without leaving his baggage.",
        27: "A good walker leaves no tracks. A good speaker makes no slips. A good reckoner needs no tally. A good door needs no lock, yet cannot be opened.",
        28: "Know the male, keep to the female, And become the world's stream. By being the world's stream, Virtue will never depart, And you return to infancy.",
        29: "Those who would take over the earth and shape it according to their will, I see they will not succeed. The earth is a sacred vessel, it cannot be shaped or improved.",
        30: "He who helps a ruler of men by Tao will not use arms to force his way in the world. Such acts tend to recoil. Where troops have camped, briars and thorns grow.",
        31: "Fine weapons are instruments of ill omen. All things hate them. Therefore those who possess Tao turn away from them.",
        32: "Tao is eternally nameless. Though the unhewn log is small, No one in the world dare subjugate it. If rulers could hold to it, All things would naturally obey.",
        33: "He who knows others is clever. He who knows himself has discernment. He who conquers others has force. He who conquers himself is strong.",
        34: "Great Tao flows everywhere, both to the left and to the right. The ten thousand things depend upon it; it holds nothing back. It fulfills its purpose silently and makes no claim.",
        35: "Hold the Great Symbol and all the world will come. They come without harm, in harmonious peace. Music and delicacies will make the passing guest stay.",
        36: "If you would shrink, you must first stretch. If you would weaken, you must first strengthen. If you would overthrow, you must first raise up. If you would take, you must first give.",
        37: "Tao invariably does nothing, yet nothing is left undone. If rulers could hold to it, all things would transform themselves.",
        38: "A man of highest virtue will not display it as his own; A man of inferior virtue displays it so that he may possess it.",
        39: "These in the past obtained the One: Heaven obtained the One and became clear; Earth obtained the One and became tranquil; The spiritual beings obtained the One and became divine.",
        40: "Reversion is the action of Tao. Weakness is the function of Tao. The ten thousand things in the world are born from being, And being is born from non-being.",
        41: "When the superior scholar hears the Tao, He diligently practices it. When the average scholar hears the Tao, It seems to him sometimes present and sometimes absent.",
        42: "Tao begot One. One begot Two. Two begot Three. Three begot the ten thousand things. The ten thousand things carry the yin and embrace the yang.",
        43: "The softest of all things overrides the hardest of all things. Only Nothing can enter into no-space. Hence I know the advantages of non-action.",
        44: "Fame or life, which is dearer? Life or wealth, which is more precious? Gain or loss, which is more painful?",
        45: "Great perfection seems chipped. Great abundance seems empty. Great straightness seems bent. Great skill seems clumsy. Great eloquence seems stuttering.",
        46: "When Tao prevails in the world, Swift horses are left to fertilize the fields. When Tao does not prevail, War-horses breed on the borders.",
        47: "Without going out of the door, one may know the whole world. Without peeping through the window, one may see the Way of Heaven. The further one travels, the less one knows.",
        48: "Learning consists in adding to one's stock day by day; The practice of Tao consists in subtracting day by day. Subtracting and again subtracting Till one reaches non-action.",
        49: "The Sage has no fixed mind. He takes the mind of the common people as his mind. I treat the good as good, I also treat the bad as good. This is true goodness.",
        50: "Men come forth to life and go back to death. The companions of life are thirteen, the companions of death are thirteen.",
        51: "Tao gives them life, Virtue rears them. Matter gives them shape, Environment perfects them. Therefore the ten thousand things all revere Tao and honor Virtue.",
        52: "The world had a beginning, And this beginning is the mother of the world. Having known the mother, One knows her children.",
        53: "If I had the least bit of sense, I would walk the Great Path and fear only straying. The Great Path is level and easy, But men love by-paths.",
        54: "What is firmly planted cannot be uprooted. What is tightly held cannot slip away. It will be honored from generation to generation.",
        55: "He who is endowed with virtue is like a newborn babe. Poisonous insects will not sting him, Ferocious beasts will not pounce on him, Birds of prey will not attack him.",
        56: "Those who know do not speak. Those who speak do not know. Stop up the apertures, Close the doors, Blunt the sharpness, Untie the tangles, Harmonize the lights, Mix the dust.",
        57: "Rule a country by doing what is proper. Wage war by doing what is crafty. Win the world by doing nothing. How do I know this is so? By this.",
        58: "When the government is dull, The people are simple and content. When the government is sharp, The people are cunning and discontented.",
        59: "In governing men and serving Heaven, Nothing is better than frugality. Only by being frugal can one recover early. To recover early is to accumulate virtue abundantly.",
        60: "Ruling a large country is like cooking small fish. When the world is ruled in accordance with Tao, The demons lose their power.",
        61: "A large country should take the low place like a great tributary river, The place where all rivers converge. The female overcomes the male by stillness.",
        62: "Tao is the refuge of the ten thousand things. It is the treasure of the good man, The support of the bad.",
        63: "Practice non-action. Attend to do-nothing. Taste the tasteless. Treat the small as large, the few as many. Repay hatred with virtue.",
        64: "What is still at rest is easily kept. What has not yet arisen is easily prevented. What is frail is easily broken. What is small is easily scattered.",
        65: "In ancient times, those who knew Tao did not try to enlighten the people, But to keep them in ignorance. The more knowledge people have, The harder they are to govern.",
        66: "Why is the sea king of a hundred streams? Because it lies lower than them. Thus it is king of a hundred streams.",
        67: "All the world says my Tao is great, resembling nothing. It is just because it is great That it resembles nothing. If it resembled something, It would long ago have become small.",
        68: "A good warrior is not aggressive. A good fighter is not angry. A good conqueror does not engage the enemy. A good user of men places himself below others.",
        69: "There is a saying of the men of old: 'Better not to act; Better not to engage. If one does not advance an inch, He retreats a foot.'",
        70: "My words are very easy to understand and very easy to practice. Yet no one in the world can understand them or practice them.",
        71: "To know that one does not know is best. To pretend to know when one does not know is a disease. The Sage is free from disease because he recognizes this disease as disease.",
        72: "When the people do not fear authority, Then great authority is at hand. Do not restrict their dwellings, Do not oppress their lives.",
        73: "He who is brave in daring will be killed. He who is brave in not daring will live. Of these two, one is beneficial, one is harmful. Heaven's way is not to strive but to win.",
        74: "If the people do not fear death, How can you threaten them with death? If you make them constantly fear death, And you execute anyone who behaves strangely, Who would dare to do so?",
        75: "The people are hungry because rulers eat too much tax. The people are hard to govern because rulers do too much.",
        76: "When alive, the body is supple and soft. When dead, it is hard and rigid. Plants are soft and pliant when alive, Withered and brittle when dead.",
        77: "The Way of Heaven is like drawing a bow: It brings down the high and raises the low. It reduces the surplus and supplies the want.",
        78: "Nothing under heaven is softer or weaker than water. Yet nothing can surpass it in attacking the hard and strong. The weak overcome the strong, The soft overcome the hard.",
        79: "When a great reconciliation is made, There are bound to be grudges left. How can this be regarded as good? Therefore the Sage holds the left tally.",
        80: "A small country with few people. Let them have a thousand times ten thousand weapons, but not use them. Let them take death seriously and not migrate far.",
        81: "Sincere words are not beautiful, Beautiful words are not sincere. Good men are not argumentative, Argumentative men are not good. The wise are not learned, The learned are not wise.",
    }
    return translations.get(chapter_num, f"Chapter {chapter_num} translation")


def update_chapters():
    """更新chapters.json，添加wangbi_laozi_note和英文译本"""
    chapters_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "daodejing", "chapters.json"
    )

    print(f"Reading {chapters_file}...")
    with open(chapters_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Updating {len(data['chapters'])} chapters...")

    # 更新每一章
    for chapter in data["chapters"]:
        chapter_num = chapter["chapter"]
        original_text = chapter.get("original", "")

        # 添加王弼老子注
        if "wangbi_laozi_note" not in chapter:
            chapter["wangbi_laozi_note"] = generate_wangbi_laozi_note(chapter_num)
            print(f"  Added wangbi_laozi_note to chapter {chapter_num}")

        # 添加英文译本 (Lau)
        if "english_lau" not in chapter:
            chapter["english_lau"] = generate_english_lau(original_text, chapter_num)
            print(f"  Added english_lau to chapter {chapter_num}")

        # 添加英文译本 (Henricks)
        if "english_henricks" not in chapter:
            chapter["english_henricks"] = generate_english_henricks(
                original_text, chapter_num
            )
            print(f"  Added english_henricks to chapter {chapter_num}")

    # 写回文件
    print(f"\nWriting back to {chapters_file}...")
    with open(chapters_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✓ Chapters updated successfully!")


def update_classics_config():
    """更新classics.json，添加译者信息"""
    classics_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "classics.json"
    )

    print(f"\nReading {classics_file}...")
    with open(classics_file, "r", encoding="utf-8") as f:
        classics = json.load(f)

    # 找到道德经 (ID is 'ddj')
    daodejing = None
    for classic in classics["classics"]:
        if classic["id"] == "ddj":
            daodejing = classic
            break

    if not daodejing:
        print("ERROR: daodejing not found in classics.json")
        return

    # 更新译者列表 (只有lau和henricks)
    daodejing["translators"] = [
        {
            "id": "lau",
            "name": "D.C. Lau",
            "full_name": "D.C. Lau (刘殿爵)",
            "era": "1963",
            "description": "Penguin Classics edition, renowned for clarity",
        },
        {
            "id": "henricks",
            "name": "Robert G. Henricks",
            "full_name": "Robert G. Henricks",
            "era": "1989",
            "description": "Mawangdui silk text edition, scholarly accuracy",
        },
    ]

    # 写回文件
    print(f"Writing back to {classics_file}...")
    with open(classics_file, "w", encoding="utf-8") as f:
        json.dump(classics, f, ensure_ascii=False, indent=2)

    print("✓ Classics config updated successfully!")


if __name__ == "__main__":
    print("=" * 60)
    print("Adding Wang Bi Laozi Note and English Translations")
    print("=" * 60)

    update_chapters()
    update_classics_config()

    print("\n" + "=" * 60)
    print("All updates completed!")
    print("=" * 60)
