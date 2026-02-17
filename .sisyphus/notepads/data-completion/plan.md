# 数据补全计划

**目标**: 按照道德经的数据标准，补全其他经典缺失的数据字段

---

## 一、道德经数据标准（参考模型）

### 1.1 数据结构
```json
{
  "chapter": 1,
  "original": "道可道，非常道...",
  "modern_chinese": "可以用语言表述的道...",
  // === 注释家 (11个) ===
  "wangbi_note": "王弼注",
  "heshanggong_note": "河上公注",
  "wangfuzhi_note": "王夫之注",
  "hanshandeqing_note": "憨山德清注",
  "suzhe_note": "苏辙注",
  "lihanxu_note": "李涵虚注",
  "huangyuanji_note": "黄元吉注",
  "weiyuan_note": "魏源注",
  "xianger_note": "想尔注",
  "yanzun_note": "严遵注",
  "wanganshi_note": "王安石注",
  // === 英译本 (6个) ===
  "english_lau": "D.C. Lau 译本",
  "english_henricks": "Robert Henricks 译本",
  "english_addiss": "Addiss & Lombardo 译本",
  "english_waley": "Arthur Waley 译本",
  "english_mitchell": "Stephen Mitchell 译本",
  "english_lin": "林语堂 译本",
  // === 古籍版本 (2个) ===
  "postsilk_text": "马王堆帛书文本",
  "postsilk_diff": "差异说明",
  "guodian_text": "郭店楚简文本",
  "guodian_diff": "郭店差异说明"
}
```

### 1.2 数据字段统计

| 字段类型 | 道德经数量 |
|---------|-----------|
| 注释家 | 11个 |
| 英译本 | 6个 |
| 古籍版本 | 2个（马王堆、郭店） |

---

## 二、其他经典数据缺失分析

### 2.1 庄子（zzj）

#### 当前状态
- ✓ 注释家：3个（郭象、成玄英、王夫之）
- ✓ 英译本：2个（Watson、Ziporyn）
- ✗ 古籍版本：0个
- ✗ diff说明：0个

#### 缺失字段
```json
// 古籍版本（庄子可能没有马王堆、郭店出土）
"guodian_text": "",
"guodian_diff": "",

// 更多注释家（建议达到5-7个）
// 可添加：林希逸、司马彪、张湛、陆德明、吕吉甫、褚伯秀等
"linxiyi_note": "",
"simaobiao_note": "",
"zhangzhan_note": "",
"ludeming_note": "",
"lvjifu_note": "",
"chuboxiu_note": "",

// 更多英译本
"english_feng": "冯友兰译",
"english_culver": "冯承钧译",
"english_mair": "Victor Mair译",
"english_graham": "A.C. Graham译",

// 差异说明
"guodian_diff": "",
```

#### 建议补全数量
- 古籍版本：至少1个（如郭店楚简或其他出土文献）
- 注释家：补全至5-7个
- 英译本：补全至5个
- diff说明：至少1个

---

### 2.2 黄帝内经（hdnj）

#### 当前状态
- ✓ 注释家：3个（王冰、张志聪、高士宗）
- ✓ 英译本：2个（Wiluson、Unschuld）
- ✗ 古籍版本：0个

#### 缺失字段
```json
// 古籍版本
"postsilk_text": "马王堆帛书版本（如有）",
"postsilk_diff": "",
"guodian_text": "",
"guodian_diff": "",

// 更多注释家
"wangbing_note": "王冰已添加",
"zhangzhicong_note": "张志聪已添加",
"gaoshizong_note": "高士宗已添加",
// 可添加：杨上善、吴崑等
"yangshangshan_note": "",
"wuqikun_note": "",

// 更多英译本
"english_li": "李约瑟译",
"english_pearson": "倪豪士译",
"english_sivin": "Veith译",

// diff说明
"postsilk_diff": "",
"guodian_diff": "",
```

#### 建议补全数量
- 古籍版本：至少1个
- 注释家：补全至5个
- 英译本：补全至5个
- diff说明：至少1个

---

### 2.3 金刚经（jgj）

#### 当前状态
- ✓ 注释家：2个（孔子、传大士颂）
- ✓ 译本：3个（鸠摩罗什、玄奘、Red Pine - 中英混合）
- ✗ 现代白话译文：部分章节有，但缺失英译本的规范

#### 缺失字段
```json
// 补全现代白话译文（统一格式）
"modern_chinese": "完整现代白话译文",

// 更多注释家
"kongzi_note": "孔子注已添加",
"zhuanshi_note": "传大士颂已添加",
// 可添加：吉藏、宗密、憨山等
"jizang_note": "",
"hanshan_note": "",

// 英译本（按道德经标准配置在classics.json）
"english_davis": "A.J. Davis译",
"english_conze": "Edward Conze译",
"english_watts": "Alan Watts译",
```

#### 建议补全数量
- 现代白话译文：补全所有章节
- 注释家：补全至5个
- 英译本：补全至5个

---

### 2.4 六祖坛经（lztyj）

#### 当前状态
- ✓ 注释家：2个（慧能、法海）
- ✓ 英译本：1个（Red Pine）
- ✗ 更多英译本：缺失
- ✗ 古籍版本：0个

#### 缺失字段
```json
// 古籍版本
"postsilk_text": "",
"postsilk_diff": "",
"guodian_text": "",
"guodian_diff": "",

// 更多注释家
"huineng_note": "慧能已添加",
"fahai_note": "法海已添加",
// 可添加：憨山德清、德清、元来等
"hanshan_note": "",
"deqing_note": "",

// 更多英译本
"english_dumoulin": "D.T. Suzuki译",
"english_yampolsky": "Philip Yampolsky译",
"english_pine": "John Pine译",
"english_mcleod": "Thomas Cleary译",
```

#### 建议补全数量
- 注释家：补全至5个
- 英译本：补全至5个
- 古籍版本：至少1个

---

### 2.5 唯识三十颂（ws30）

#### 当前状态
- ✓ 现代白话译文
- ✗ 注释家：0个
- ✗ 英译本：仅每个颂有english字段，未在classics.json配置

#### 缺失字段
```json
// classics.json需要添加translators配置
// 英译本（按道德经标准）
"english_shen": "Shen-hsiu译",
"english_kochumutt": "Kochumutt译",
"english_powers": "John Powers译",
"english_tola": "Federico Tola译",

// 注释家
"dharmakirti_note": "法称注",
"yasomitra_note": "世亲注",
"sthiramati_note": "安慧注",
"jnanagarjuna_note": "月称注",

// 古籍版本（如可能）
"postsilk_text": "",
"guodian_text": "",
```

#### 建议补全数量
- 注释家：补全至5个
- 英译本：补全至5个
- 梵文（sanskrit）字段：补全为非空值

---

### 2.6 周易（zy）

#### 当前状态
- ✓ 注释家：2个（王弼、程颐、朱熹）
- ✓ 英译本：1个（James Legge）
- ✗ 更多英译本
- ✗ 古籍版本

#### 缺失字段
```json
// 更多注释家
"kongyingda_note": "孔颖达注",
"maixi_shan_note": "马融注",
"juyi_note": "虞翻注",

// 更多英译本
"english_wilhelm": "Richard Wilhelm译",
"english_blofeld": "Richard Blofeld译",
"english_huang": "Archibald Huang译",
"english_shchults": "Léon Shchuts译",

// 古籍版本
"postsilk_text": "",
"guodian_text": "",
```

#### 建议补全数量
- 注释家：补全至5个
- 英译本：补全至5个
- 古籍版本：至少1个

---

### 2.7 四书（ss）

#### 当前状态
- ✗ 注释家：0个
- ✗ 英译本：0个
- ✗ 古籍版本：0个

#### 缺失字段
```json
// 四书包含：大学、中庸、论语、孟子
// 每部书可以有自己的注释家
"great_learning_note": "朱熹《大学章句集注》",
"doctrine_mean_note": "朱熹《中庸章句集注》",
"analects_note": "朱熹《论语集注》",
"mencius_note": "朱熹《孟子集注》",

// 更多注释家
"zhu_xi_note": "朱熹注",
"wang_yangming_note": "王阳明注",

// 英译本
"english_legge": "James Legge译",
"english_lau": "D.C. Lau译",
"english_muller": "Max Müller译",

// 古籍版本
"postsilk_text": "",
"guodian_text": "",
```

#### 建议补全数量
- 注释家：至少5个
- 英译本：至少3个
- 古籍版本：至少1个

---

### 2.8 传习录（cxl）

#### 当前状态
- ✗ 注释家：0个
- ✗ 英译本：0个
- ✗ 古籍版本：0个

#### 缺失字段
```json
// 注释家
"chens_xu_note": "陈献章注",
"zhu_xi_note": "朱熹注",
"wang_yangming_note": "王阳明注",

// 英译本
"english_henkes": "David Hinkes译",
"english_wingtsit": "Wing-tsit Chan译",
"english_cleary": "Thomas Cleary译",

// 古籍版本
"postsilk_text": "",
"guodian_text": "",
```

#### 建议补全数量
- 注释家：至少3个
- 英译本：至少3个
- 古籍版本：至少1个

---

## 三、执行计划

### 阶段一：数据结构标准化（优先级P0）

1. 为所有经典添加`title`字段（章节标题）
2. 为所有经典统一`diff`说明字段格式
3. 为所有需要翻译的经典添加梵文/原文字段

### 阶段二：数据补全（优先级P1）

按经典优先级排序：
1. **庄子**：补充古籍版本、注释家、英译本
2. **黄帝内经**：补充古籍版本、注释家、英译本
3. **金刚经**：完善现代白话译文、补充英译本
4. **六祖坛经**：补充英译本
5. **唯识三十颂**：补充注释家、英译本
6. **周易**：补充注释家、英译本
7. **四书**：补充注释家、英译本
8. **传习录**：补充注释家、英译本

### 阶段三：配置更新（优先级P1）

1. 更新`data/classics.json`，添加所有缺失的注释家和译本配置
2. 确保字段命名规范统一

---

## 四、质量标准

### 4.1 数据质量要求

- 每个经典至少：5个注释家
- 每个经典至少：5个英译本（除唯识三十颂外）
- 古籍版本：至少1个（如有出土文献）
- modern_chinese：完整覆盖所有章节
- 字段命名：遵循`{字段类型}_note`、`{译者id}_text`格式

### 4.2 数据来源建议

- 使用权威版本和译本
- 注释家优先级：历史上重要注疏
- 英译本：知名学者译本
- 古籍：考古出土文献

---

## 五、执行检查清单

- [ ] 庄子：添加1个古籍版本
- [ ] 庄子：添加2-4个注释家
- [ ] 庄子：添加2-3个英译本
- [ ] 黄帝内经：添加1个古籍版本
- [ ] 黄帝内经：添加2个注释家
- [ ] 黄帝内经：添加2-3个英译本
- [ ] 金刚经：补全现代白话译文
- [ ] 金刚经：添加2个英译本
- [ ] 六祖坛经：添加3个英译本
- [ ] 唯识三十颂：添加5个注释家
- [ ] 唯识三十颂：添加5个英译本
- [ ] 周易：添加3个注释家
- [ ] 周易：添加4个英译本
- [ ] 四书：添加5个注释家
- [ ] 四书：添加3个英译本
- [ ] 传习录：添加3个注释家
- [ ] 传习录：添加3个英译本
- [ ] 更新classics.json配置

---

**创建日期**: 2026-02-17
**预计完成**: 根据数据源可用性
**状态**: 待开始执行
