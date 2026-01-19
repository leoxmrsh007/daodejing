#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
提取额外的道德经注释版本：
- 李涵虚注
- 黄元吉注
- 魏源注
"""

import re
import json

def read_file_with_encoding(file_path):
    """尝试多种编码读取文件"""
    encodings = ['gbk', 'gb2312', 'gb18030', 'utf-8']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc, errors='ignore') as f:
                return f.read()
        except:
            continue
    return None

def cn_to_arabic(cn):
    """将中文数字转换为阿拉伯数字"""
    mapping = {
        '一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,
        '十一':11,'十二':12,'十三':13,'十四':14,'十五':15,'十六':16,'十七':17,'十八':18,'十九':19,'二十':20,
        '二十一':21,'二十二':22,'二十三':23,'二十四':24,'二十五':25,'二十六':26,'二十七':27,'二十八':28,'二十九':29,'三十':30,
        '三十一':31,'三十二':32,'三十三':33,'三十四':34,'三十五':35,'三十六':36,'三十七':37,'三十八':38,'三十九':39,'四十':40,
        '四十一':41,'四十二':42,'四十三':43,'四十四':44,'四十五':45,'四十六':46,'四十七':47,'四十八':48,'四十九':49,'五十':50,
        '五十一':51,'五十二':52,'五十三':53,'五十四':54,'五十五':55,'五十六':56,'五十七':57,'五十八':58,'五十九':59,'六十':60,
        '六十一':61,'六十二':62,'六十三':63,'六十四':64,'六十五':65,'六十六':66,'六十七':67,'六十八':68,'六十九':69,'七十':70,
        '七十一':71,'七十二':72,'七十三':73,'七十四':74,'七十五':75,'七十六':76,'七十七':77,'七十八':78,'七十九':79,'八十':80,
        '八十一':81
    }
    return mapping.get(cn, 0)

def extract_lihanxu(content):
    """提取李涵虚注"""
    chapters = {}
    lines = content.split('\n')
    current_chapter = None
    current_content = []
    in_commentary = False

    for line in lines:
        line = line.strip()
        # 匹配章节标题: "第X章"
        match = re.match(r'第([一二三四五六七八九十百]+)章', line)
        if match:
            # 保存上一章内容
            if current_chapter and current_content:
                chapters[current_chapter] = '\n'.join(current_content).strip()

            cn_num = match.group(1)
            current_chapter = cn_to_arabic(cn_num)
            current_content = []
            in_commentary = True
            continue

        if in_commentary and current_chapter:
            # 收集注释内容
            if line and not line.startswith('序') and not line.startswith('纯阳'):
                current_content.append(line)

    # 保存最后一章
    if current_chapter and current_content:
        chapters[current_chapter] = '\n'.join(current_content).strip()

    return chapters

def extract_huangyuanji(content):
    """提取黄元吉注"""
    chapters = {}

    # 先找到每一章的起始位置
    chapter_patterns = []
    for i in range(1, 82):
        cn_num = arabic_to_cn(i)
        # 可能的格式: "第一章\nxxx"
        pattern = f'第{cn_num}章'
        chapter_patterns.append((i, pattern))

    lines = content.split('\n')
    current_chapter = None
    current_content = []

    for line in lines:
        line = line.strip()

        # 检查是否是章节标题
        for i, pattern in chapter_patterns:
            if pattern in line and len(line) < 20:
                # 保存上一章
                if current_chapter and current_content:
                    chapters[current_chapter] = '\n'.join(current_content).strip()

                current_chapter = i
                current_content = []
                break
        else:
            # 不是章节标题，收集内容
            if current_chapter and line:
                current_content.append(line)

    # 保存最后一章
    if current_chapter and current_content:
        chapters[current_chapter] = '\n'.join(current_content).strip()

    return chapters

def extract_weiyuan(content):
    """提取魏源注"""
    chapters = {}
    lines = content.split('\n')
    current_chapter = None
    current_content = []
    found_first = False

    for line in lines:
        line = line.strip()
        # 检查章节结束标记: "右第X章"
        match = re.match(r'右第([一二三四五六七八九十百]+)章', line)
        if match:
            if current_chapter and current_content:
                chapters[current_chapter] = '\n'.join(current_content).strip()

            cn_num = match.group(1)
            current_chapter = cn_to_arabic(cn_num)
            current_content = []
            found_first = True
            continue

        # 提取注释内容（在{{...}}中的内容）
        if found_first and line.startswith('{{'):
            # 去掉开头的{{
            content_line = line[2:].strip()
            if content_line:
                current_content.append(content_line)
        elif found_first and current_content and not line.startswith('右第'):
            # 继续收集注释内容
            if line and not line.startswith('{') and not line.startswith('}'):
                current_content.append(line)
            elif line.startswith('}}'):
                # 注释结束
                pass

    # 保存最后一章
    if current_chapter and current_content:
        chapters[current_chapter] = '\n'.join(current_content).strip()

    return chapters

def arabic_to_cn(n):
    """阿拉伯数字转中文"""
    mapping = {
        1:'一',2:'二',3:'三',4:'四',5:'五',6:'六',7:'七',8:'八',9:'九',10:'十',
        11:'十一',12:'十二',13:'十三',14:'十四',15:'十五',16:'十六',17:'十七',18:'十八',19:'十九',20:'二十',
        21:'二十一',22:'二十二',23:'二十三',24:'二十四',25:'二十五',26:'二十六',27:'二十七',28:'二十八',29:'二十九',30:'三十',
        31:'三十一',32:'三十二',33:'三十三',34:'三十四',35:'三十五',36:'三十六',37:'三十七',38:'三十八',39:'三十九',40:'四十',
        41:'四十一',42:'四十二',43:'四十三',44:'四十四',45:'四十五',46:'四十六',47:'四十七',48:'四十八',49:'四十九',50:'五十',
        51:'五十一',52:'五十二',53:'五十三',54:'五十四',55:'五十五',56:'五十六',57:'五十七',58:'五十八',59:'五十九',60:'六十',
        61:'六十一',62:'六十二',63:'六十三',64:'六十四',65:'六十五',66:'六十六',67:'六十七',68:'六十八',69:'六十九',70:'七十',
        71:'七十一',72:'七十二',73:'七十三',74:'七十四',75:'七十五',76:'七十六',77:'七十七',78:'七十八',79:'七十九',80:'八十',
        81:'八十一'
    }
    return mapping.get(n, '')

def main():
    # 读取数据文件
    with open(r'D:\项目文件\daodejing\data\daodejing.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取李涵虚注
    print("提取李涵虚注...")
    path = r'D:\数据集\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\09藏外-186种\09藏外-186种\道德经注释-清-李涵虚.txt'
    content = read_file_with_encoding(path)
    lihanxu = extract_lihanxu(content)
    print(f"  提取到 {len(lihanxu)} 章")

    # 提取黄元吉注
    print("提取黄元吉注...")
    path = r'D:\数据集\中华古籍文库\03.古代笔记学术类书\13仙学文库\05明清两代经典\黄元吉\道德经真义.txt'
    content = read_file_with_encoding(path)
    huangyuanji = extract_huangyuanji(content)
    print(f"  提取到 {len(huangyuanji)} 章")

    # 提取魏源注
    print("提取魏源注...")
    path = r'D:\数据集\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\09藏外-186种\09藏外-186种\老子本义-清-魏源.txt'
    content = read_file_with_encoding(path)
    weiyuan = extract_weiyuan(content)
    print(f"  提取到 {len(weiyuan)} 章")

    # 合并到数据中
    print("\n合并到daodejing.json...")
    for ch in data['chapters']:
        ch_num = ch['chapter']
        if ch_num in lihanxu:
            ch['lihanxu_note'] = lihanxu[ch_num]
        if ch_num in huangyuanji:
            ch['huangyuanji_note'] = huangyuanji[ch_num]
        if ch_num in weiyuan:
            ch['weiyuan_note'] = weiyuan[ch_num]

    # 保存更新后的数据
    with open(r'D:\项目文件\daodejing\data\daodejing.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n完成！已添加三个新注释版本。")

    # 统计结果
    print("\n统计结果:")
    for key, name in [('lihanxu_note', '李涵虚注'), ('huangyuanji_note', '黄元吉注'), ('weiyuan_note', '魏源注')]:
        count = sum(1 for ch in data['chapters'] if ch.get(key) and ch[key].strip())
        print(f"  {name}: {count} 章")

if __name__ == '__main__':
    main()
