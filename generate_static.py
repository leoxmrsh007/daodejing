# -*- coding: utf-8 -*-
"""
道德经静态网站生成器
生成纯静态HTML文件，可部署到任何静态托管平台
"""

import os
import json
import re
import shutil
from pathlib import Path

# ==================== 配置 ====================
BASE_DIR = Path(r'D:\项目文件\daodejing')
DATA_DIR = BASE_DIR / 'data'
OUTPUT_DIR = BASE_DIR / 'dist'
DATA_FILE = DATA_DIR / 'daodejing.json'

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


def load_data():
    """加载道德经数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def annotate_difficult_chars(text):
    """为疑难字添加拼音和释义标注"""
    result = text
    sorted_chars = sorted(DIFFICULT_CHARS.items(), key=lambda x: -len(x[0]))

    for char, info in sorted_chars:
        pinyin = info['pinyin']
        meaning = info['meaning']
        pattern = re.compile(re.escape(char))
        replacement = f'<span class="difficult" data-pinyin="{pinyin}" data-meaning="{meaning}">{char}</span>'
        result = pattern.sub(replacement, result)

    return result


# ==================== HTML 模板 ====================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN" data-theme="auto">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 道德经</title>
    <meta name="description" content="道德经多版本对照平台 - 王弼本 · 河上公本 · 王夫之 · 憨山德清 | 帛书 · 郭店简">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="./assets/css/style.css" rel="stylesheet">
    <style>
{extra_css}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
        <div class="container-fluid">
            <button class="navbar-toggler d-lg-none me-2" type="button" id="sidebarToggle">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="./index.html">
                <span class="brand-icon">☯</span>
                <span class="brand-text">道德经</span>
            </a>
            <span class="navbar-text ms-3 d-none d-md-block">{page_title}</span>
            <div class="ms-auto d-flex align-items-center gap-2">
                <button class="btn btn-sm btn-outline-light" id="themeToggle" title="切换模式">
                    <span class="theme-icon">🌙</span>
                </button>
            </div>
        </div>
    </nav>

    <div class="container-fluid">
        <div class="row">
            <aside class="col-lg-2 col-md-3 sidebar" id="sidebar">
                <div class="sidebar-content">
                    <h6 class="sidebar-title">目录</h6>
                    <div class="chapter-list" id="chapterList">
                        <nav class="nav flex-column">
{chapter_list}
                        </nav>
                    </div>
                </div>
            </aside>

            <main class="col-lg-10 col-md-9 main-content" id="mainContent">
{content}
            </main>
        </div>
    </div>

    <footer class="footer mt-auto py-3">
        <div class="container text-center text-muted">
            <small>道德经多版本对照平台 | 王弼本 · 河上公本 · 王夫之 · 憨山德清 | 帛书 · 郭店简</small>
        </div>
    </footer>

    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="./assets/js/main.js"></script>
    <script>
{extra_js}
    </script>
</body>
</html>
'''

INDEX_EXTRA_CSS = '''
.index-page .chapters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 0.75rem;
    padding: 1rem 0;
}
.index-page .chapter-card {
    text-align: center;
    padding: 1rem;
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    text-decoration: none;
    color: var(--text-primary);
    transition: all 0.2s ease;
}
.index-page .chapter-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow);
    border-color: var(--accent-color);
}
.index-page .chapter-num {
    font-family: 'KaiTi', '楷体', serif;
    font-size: 1.5rem;
    color: var(--accent-color);
}
.index-page .chapter-preview {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.intro-section {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
}
.intro-section h1 {
    font-family: 'KaiTi', '楷体', serif;
    color: var(--accent-color);
}
'''

CHAPTER_EXTRA_CSS = '''
.original-text {
    font-family: 'KaiTi', '楷体', serif;
    font-size: clamp(1.5rem, 2.8vw, 2.2rem);
    line-height: 2;
    text-align: center;
    padding: 1.5rem;
}
/* 疑难字标注 - 纯CSS方案 */
.difficult {
    border-bottom: 1px dashed var(--accent-color);
    cursor: help;
    position: relative;
    display: inline-block;
    transition: background-color 0.2s;
}
.difficult:hover {
    background-color: rgba(212, 165, 116, 0.15);
}
/* 悬停提示 - 显示在文字上方 */
.difficult:hover::after {
    content: attr(data-pinyin) ": " attr(data-meaning);
    position: absolute;
    bottom: 130%;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(44, 24, 16, 0.95);
    color: #fff;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 12px;
    white-space: nowrap;
    z-index: 9999;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    pointer-events: none;
}
/* 小箭头 */
.difficult:hover::before {
    content: "";
    position: absolute;
    bottom: 120%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: rgba(44, 24, 16, 0.95);
}
[data-theme="dark"] .difficult:hover::after {
    background-color: rgba(232, 224, 216, 0.95);
    color: #2c1810;
}
[data-theme="dark"] .difficult:hover::before {
    border-top-color: rgba(232, 224, 216, 0.95);
}
.modern-text {
    line-height: 1.8;
    font-size: 1.05rem;
}
.note-text {
    line-height: 1.8;
}
.english-text {
    line-height: 1.6;
    font-family: Georgia, serif;
}
.chapter-navigation .page-link {
    border-color: var(--border-color);
}
#versionTabs .nav-link {
    color: var(--text-primary);
    border-color: transparent;
}
#versionTabs .nav-link:hover {
    background-color: rgba(212, 165, 116, 0.1);
}
#versionTabs .nav-link.active {
    color: var(--accent-color);
    border-color: var(--accent-color);
}
#englishTabs .nav-link {
    color: var(--text-primary);
}
#englishTabs .nav-link.active {
    background-color: var(--accent-color);
}
.version-content {
    line-height: 1.8;
}
.version-original-text {
    padding: 0.75rem;
    background-color: var(--bg-secondary);
    border-left: 3px solid var(--accent-color);
    border-radius: 4px;
}
'''

CHAPTER_EXTRA_JS = '''
// 复制原文
document.getElementById('copyOriginal')?.addEventListener('click', function() {
    const text = document.getElementById('originalText').innerText;
    navigator.clipboard.writeText(text).then(() => {
        this.textContent = '已复制';
        setTimeout(() => this.textContent = '复制', 2000);
    });
});
'''


def generate_chapter_list_html(chapters, active_id=None):
    """生成章节目录HTML"""
    items = []
    for ch in chapters:
        active_class = 'active' if ch['chapter'] == active_id else ''
        items.append(f'<a class="nav-link chapter-item {active_class}" href="./chapter{ch["chapter"]}.html">')
        items.append(f'    <span class="chapter-num">第{ch["chapter"]}章</span>')
        items.append('</a>')
    return '\n'.join(items)


def generate_index_page(data):
    """生成首页"""
    chapter_list = generate_chapter_list_html(data['chapters'])

    # 生成章节卡片
    cards = []
    for ch in data['chapters'][:20]:  # 首页显示前20章
        preview = ch.get('modern_chinese', '')[:30]
        cards.append(f'<a href="./chapter{ch["chapter"]}.html" class="chapter-card">')
        cards.append(f'    <div class="chapter-num">第{ch["chapter"]}章</div>')
        cards.append(f'    <div class="chapter-preview">{preview}...</div>')
        cards.append('</a>')

    content = f'''
    <div class="intro-section">
        <h1 class="text-center mb-4">☯ 道德经</h1>
        <p class="text-center text-muted mb-4">多版本对照研究平台</p>
        <p class="text-center">
            <span class="badge bg-secondary me-1">王弼注</span>
            <span class="badge bg-secondary me-1">河上公注</span>
            <span class="badge bg-secondary me-1">王夫之</span>
            <span class="badge bg-secondary me-1">憨山德清</span>
            <span class="badge bg-info me-1">帛书</span>
            <span class="badge bg-info">郭店简</span>
        </p>
    </div>

    <h4 class="mb-3">章节目录</h4>
    <div class="chapters-grid index-page">
{''.join(cards)}
    </div>

    <div class="text-center mt-4">
        <a href="./all-chapters.html" class="btn btn-outline-primary">查看全部81章 →</a>
    </div>
'''

    html = HTML_TEMPLATE.format(
        title='道德经 - 多版本对照平台',
        page_title='首页',
        extra_css=INDEX_EXTRA_CSS,
        chapter_list=chapter_list,
        content=content,
        extra_js=''
    )

    return html


def generate_all_chapters_page(data):
    """生成全部章节页面"""
    chapter_list = generate_chapter_list_html(data['chapters'])

    cards = []
    for ch in data['chapters']:
        preview = ch.get('modern_chinese', '')[:30]
        cards.append(f'<a href="./chapter{ch["chapter"]}.html" class="chapter-card">')
        cards.append(f'    <div class="chapter-num">第{ch["chapter"]}章</div>')
        cards.append(f'    <div class="chapter-preview">{preview}...</div>')
        cards.append('</a>')

    content = f'''
    <h4 class="mb-3">全部81章</h4>
    <div class="chapters-grid index-page">
{''.join(cards)}
    </div>
'''

    html = HTML_TEMPLATE.format(
        title='全部章节 - 道德经',
        page_title='全部章节',
        extra_css=INDEX_EXTRA_CSS,
        chapter_list=chapter_list,
        content=content,
        extra_js=''
    )

    return html


def generate_chapter_page(data, chapter_id):
    """生成单章页面"""
    chapter = next((c for c in data['chapters'] if c['chapter'] == chapter_id), None)
    if not chapter:
        return None

    # 获取相邻章节
    idx = data['chapters'].index(chapter)
    prev_chapter = data['chapters'][idx - 1] if idx > 0 else None
    next_chapter = data['chapters'][idx + 1] if idx < len(data['chapters']) - 1 else None

    # 为原文添加疑难字标注
    original_annotated = annotate_difficult_chars(chapter.get('original', ''))

    chapter_list = generate_chapter_list_html(data['chapters'], chapter_id)

    # 构建内容
    content = f'''
    <nav aria-label="章节导航" class="chapter-nav mb-3">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="./index.html">目录</a></li>
            <li class="breadcrumb-item active">第{chapter['chapter']}章</li>
        </ol>
    </nav>

    <section class="original-section mb-4">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">第{chapter['chapter']}章 · 原文</h5>
                <div class="btn-group btn-group-sm">
                    <button type="button" class="btn btn-outline-secondary" id="copyOriginal" title="复制原文">复制</button>
                </div>
            </div>
            <div class="card-body">
                <div class="original-text" id="originalText">
                    {original_annotated}
                </div>
            </div>
        </div>
    </section>

    <section class="modern-section mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">现代白话译文</h5>
            </div>
            <div class="card-body">
                <p class="modern-text mb-0">{chapter.get('modern_chinese', '')}</p>
            </div>
        </div>
    </section>

    <section class="versions-section mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">多版本对照</h5>
            </div>
            <div class="card-body p-0">
                <ul class="nav nav-tabs" id="versionTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#wangbi" type="button">王弼注</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#heshanggong" type="button">河上公注</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#wangfuzhi" type="button">王夫之注</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#hanshan" type="button">憨山德清注</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#postsilk" type="button">帛书异文</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="tab" data-bs-target="#guodian" type="button">郭店异文</button>
                    </li>
                </ul>
                <div class="tab-content p-3">
                    <div class="tab-pane fade show active" id="wangbi">
                        <h6 class="text-muted mb-2">王弼注（魏晋）</h6>
                        <p class="note-text mb-0">{chapter.get('wangbi_note', '')}</p>
                    </div>
                    <div class="tab-pane fade" id="heshanggong">
                        <h6 class="text-muted mb-2">河上公注（汉）</h6>
                        <p class="note-text mb-0">{chapter.get('heshanggong_note', '')}</p>
                    </div>
                    <div class="tab-pane fade" id="wangfuzhi">
                        <h6 class="text-muted mb-2">王夫之《老子衍》（明末清初）</h6>
                        <p class="note-text mb-0">{chapter.get('wangfuzhi_note', '')}</p>
                    </div>
                    <div class="tab-pane fade" id="hanshan">
                        <h6 class="text-muted mb-2">憨山德清《老子道德经解》（明）</h6>
                        <p class="note-text mb-0">{chapter.get('hanshandeqing_note', '')}</p>
                    </div>
                    <div class="tab-pane fade" id="postsilk">
                        <h6 class="text-muted mb-2">马王堆帛书异文（西汉）</h6>
                        <div class="version-content mb-0">
                            {f'<p class="note-text mb-0 fst-italic">{chapter.get("postsilk_text", "")}</p>' if chapter.get('postsilk_text') else ''}
                            <div class="version-explanation">
                                <small class="text-muted">{chapter.get('postsilk_diff', '')}</small>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="guodian">
                        <h6 class="text-muted mb-2">郭店楚简异文（战国）</h6>
                        <div class="version-content mb-0">
                            {f'<p class="note-text mb-0 fst-italic">{chapter.get("guodian_text", "")}</p>' if chapter.get('guodian_text') and chapter.get('guodian_text') != '此章缺' else '<p class="text-muted">此章缺</p>'}
                            <div class="version-explanation">
                                <small class="text-muted">{chapter.get('guodian_diff', '')}</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="english-section mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">English Translations / 英文译本</h5>
            </div>
            <div class="card-body p-0">
                <ul class="nav nav-pills mb-0 p-2" id="englishTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" data-bs-toggle="pill" data-bs-target="#lau" type="button">D.C. Lau</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="pill" data-bs-target="#henricks" type="button">Henricks</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" data-bs-toggle="pill" data-bs-target="#addiss" type="button">Addiss & Lombardo</button>
                    </li>
                </ul>
                <div class="tab-content p-3">
                    <div class="tab-pane fade show active" id="lau">
                        <p class="english-text mb-0 fst-italic">{chapter.get('english_lau', '')}</p>
                    </div>
                    <div class="tab-pane fade" id="henricks">
                        <p class="english-text mb-0 fst-italic">{chapter.get('english_henricks', '')}</p>
                    </div>
                    <div class="tab-pane fade" id="addiss">
                        <p class="english-text mb-0 fst-italic">{chapter.get('english_addiss', '')}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <nav class="chapter-navigation" aria-label="章节翻页">
        <ul class="pagination justify-content-center">
            {f'<li class="page-item"><a class="page-link" href="./chapter{prev_chapter["chapter"]}.html">← 第{prev_chapter["chapter"]}章</a></li>' if prev_chapter else '<li class="page-item disabled"><span class="page-link">← 上一章</span></li>'}
            <li class="page-item disabled">
                <span class="page-link">{chapter["chapter"]} / 81</span>
            </li>
            {f'<li class="page-item"><a class="page-link" href="./chapter{next_chapter["chapter"]}.html">第{next_chapter["chapter"]}章 →</a></li>' if next_chapter else '<li class="page-item disabled"><span class="page-link">下一章 →</span></li>'}
        </ul>
    </nav>
'''

    html = HTML_TEMPLATE.format(
        title=f'第{chapter_id}章 - 道德经',
        page_title=f'第{chapter_id}章',
        extra_css=CHAPTER_EXTRA_CSS,
        chapter_list=chapter_list,
        content=content,
        extra_js=CHAPTER_EXTRA_JS
    )

    return html


def copy_assets():
    """复制静态资源文件"""
    # 创建assets目录
    assets_css_dir = OUTPUT_DIR / 'assets' / 'css'
    assets_js_dir = OUTPUT_DIR / 'assets' / 'js'
    assets_css_dir.mkdir(parents=True, exist_ok=True)
    assets_js_dir.mkdir(parents=True, exist_ok=True)

    # 复制CSS
    shutil.copy(BASE_DIR / 'static' / 'css' / 'style.css', assets_css_dir / 'style.css')

    # 复制并修改JS (移除API搜索功能)
    js_content = (BASE_DIR / 'static' / 'js' / 'main.js').read_text(encoding='utf-8')
    # 静态版本不需要搜索功能，注释掉
    static_js = js_content.replace(
        'SearchManager.init();',
        '// SearchManager.init();  // 静态版本禁用搜索'
    ).replace(
        "API_ENDPOINT: '/api/daodejing/search',",
        "// API_ENDPOINT: '/api/daodejing/search',  // 静态版本"
    )
    (assets_js_dir / 'main.js').write_text(static_js, encoding='utf-8')


def generate_site():
    """生成静态网站"""
    print("=" * 50)
    print("道德经静态网站生成器")
    print("=" * 50)

    # 清理并创建输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 加载数据
    print("\n[1/4] 加载数据...")
    data = load_data()
    print(f"      加载了 {len(data['chapters'])} 章内容")

    # 复制静态资源
    print("\n[2/4] 复制静态资源...")
    copy_assets()
    print("      CSS 和 JS 文件已复制")

    # 生成首页
    print("\n[3/4] 生成首页...")
    index_html = generate_index_page(data)
    (OUTPUT_DIR / 'index.html').write_text(index_html, encoding='utf-8')
    print("      index.html 已生成")

    # 生成全部章节页
    print("\n[3/4] 生成全部章节页...")
    all_html = generate_all_chapters_page(data)
    (OUTPUT_DIR / 'all-chapters.html').write_text(all_html, encoding='utf-8')
    print("      all-chapters.html 已生成")

    # 生成章节页面
    print("\n[4/4] 生成章节页面...")
    for ch in data['chapters']:
        html = generate_chapter_page(data, ch['chapter'])
        if html:
            (OUTPUT_DIR / f'chapter{ch["chapter"]}.html').write_text(html, encoding='utf-8')
    print(f"      生成了 {len(data['chapters'])} 个章节页面")

    print("\n" + "=" * 50)
    print(f"✓ 静态网站生成完成！")
    print(f"  输出目录: {OUTPUT_DIR}")
    print(f"  总文件数: {len(list(OUTPUT_DIR.glob('*.html')))} 个HTML文件")
    print("=" * 50)

    # 统计信息
    total_size = sum(f.stat().st_size for f in OUTPUT_DIR.rglob('*'))
    print(f"\n总大小: {total_size / 1024:.1f} KB")


if __name__ == '__main__':
    generate_site()
