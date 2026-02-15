# -*- coding: utf-8 -*-
"""
古籍经典静态网站生成器
生成纯静态HTML文件，可部署到任何静态托管平台
支持多经典：道德经、庄子等
"""

import json
import shutil

# 从服务层导入共享逻辑
from config import BASE_DIR, DATA_DIR
from services.annotation_service import annotate_difficult_chars
from services.classic_service import load_classics_metadata

# 静态生成器专用配置
OUTPUT_DIR = BASE_DIR / "dist"
CLASSICS_FILE = DATA_DIR / "classics.json"
IDIOMS_FILE = DATA_DIR / "idioms.json"


def load_classic_data(classic_id):
    """加载指定经典的数据"""
    metadata = load_classics_metadata()
    for classic in metadata.get("classics", []):
        if classic["id"] == classic_id:
            data_file = BASE_DIR / classic["data_file"]
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f), classic
    return None, None


def load_idioms():
    """加载成语数据"""
    try:
        with open(IDIOMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("idioms", [])
    except FileNotFoundError:
        return []


# 加载所有经典元数据（全局缓存）
_ALL_CLASSICS = None


def get_all_classics():
    """获取所有经典元数据（带缓存）"""
    global _ALL_CLASSICS
    if _ALL_CLASSICS is None:
        _ALL_CLASSICS = load_classics_metadata()
    return _ALL_CLASSICS


def generate_classic_switcher_html(current_classic_id):
    """生成经典切换导航HTML"""
    classics = get_all_classics().get("classics", [])
    if not classics:
        return ""

    items = []
    for c in classics:
        is_active = c["id"] == current_classic_id
        active_class = "active" if is_active else ""
        # 计算相对路径
        path_prefix = "../" + c["id"] + "/" if current_classic_id else "./"
        items.append(
            f"""
        <li>
            <a class="dropdown-item {active_class}" href="{path_prefix}index.html">
                <span class="classic-icon">{c.get("icon", "☯")}</span>
                <span class="classic-name">{c["short_name"]}</span>
                <span class="classic-info">{c.get("chapters", 0)}章 · {c.get("author", "")}</span>
            </a>
        </li>"""
        )

    current_classic = next((c for c in classics if c["id"] == current_classic_id), None)
    current_icon = current_classic.get("icon", "☯") if current_classic else "☯"
    current_name = (
        current_classic.get("short_name", "经典") if current_classic else "经典"
    )

    return f"""
    <!-- 经典切换器 - 下拉菜单 -->
    <div class="classic-nav ms-2 me-auto">
        <div class="dropdown">
            <button class="btn btn-sm btn-outline-light dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                <span class="me-1">{current_icon}</span>
                <span class="d-none d-sm-inline">{current_name}</span>
            </button>
            <ul class="dropdown-menu dropdown-menu-dark classic-dropdown">
                <li><h6 class="dropdown-header">📚 选择经典</h6></li>
                {"".join(items)}
            </ul>
        </div>
    </div>
    """


# ==================== HTML 模板 ====================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="auto">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{classic_name}多版本对照平台 - {classic_desc}">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>{classic_icon}</text></svg>">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/assets/css/style.css" rel="stylesheet">
    <style>
/* 经典切换下拉菜单样式 */
.classic-dropdown {{
    min-width: 280px;
    max-height: 400px;
    overflow-y: auto;
    background: #2c3e50;
    border: 1px solid rgba(255,255,255,0.1);
}}
.classic-dropdown .dropdown-item {{
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    color: #fff;
}}
.classic-dropdown .dropdown-item:hover,
.classic-dropdown .dropdown-item.active {{
    background: rgba(255,255,255,0.1);
}}
.classic-icon {{
    width: 24px;
    text-align: center;
    margin-right: 8px;
}}
.classic-name {{
    flex: 1;
}}
.classic-info {{
    font-size: 0.75rem;
    color: rgba(255,255,255,0.6);
    margin-left: 8px;
}}
/* 设置按钮与功能栏并置 */
.navbar-nav {{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.5rem;
}}
.navbar-nav .btn {{
    white-space: nowrap;
}}

/* 侧边栏目录滚动样式 */
.sidebar-content {{
    display: flex;
    flex-direction: column;
    height: calc(100vh - 70px);
    padding: 1rem 0.5rem;
}}
.sidebar-title {{
    flex-shrink: 0;
    padding: 0 0.5rem 0.75rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-color, #e0d5c9);
    font-weight: 600;
    color: var(--accent-color, #d4a574);
}}
.chapter-list-scrollable {{
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: 4px;
}}
.chapter-list-scrollable::-webkit-scrollbar {{
    width: 4px;
}}
.chapter-list-scrollable::-webkit-scrollbar-track {{
    background: transparent;
}}
.chapter-list-scrollable::-webkit-scrollbar-thumb {{
    background: var(--accent-color, #d4a574);
    border-radius: 2px;
}}
.chapter-list-scrollable .nav-link {{
    padding: 0.5rem 0.75rem;
    border-radius: 6px;
    margin-bottom: 2px;
    transition: all 0.2s ease;
}}
.chapter-list-scrollable .nav-link:hover {{
    background: rgba(212, 165, 116, 0.1);
}}
.chapter-list-scrollable .nav-link.active {{
    background: var(--accent-color, #d4a574);
    color: #fff;
}}


{extra_css}
    </style>
</head>
<body>
    <!-- 顶部导航栏 - 悬浮置顶 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top" style="z-index: 1040;">
        <div class="container-fluid">
            <button class="navbar-toggler d-lg-none me-2" type="button" id="sidebarToggle">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="./index.html">
                <span class="brand-icon">{classic_icon}</span>
                <span class="brand-text">{classic_short_name}</span>
            </a>

            <!-- 经典切换器 -->
            {classic_switcher}

            <span class="navbar-text ms-2 d-none d-md-block">{page_title}</span>

            <!-- 设置栏和功能栏并置 -->
            <div class="ms-auto d-flex align-items-center gap-2 navbar-nav">
                <!-- 音乐控制 -->
                <div class="music-controls d-flex align-items-center">
                    <button class="btn btn-sm btn-outline-light media-btn" id="musicToggle" title="背景音乐">
                        <span class="music-icon">🎵</span>
                    </button>
                    <button class="btn btn-sm btn-outline-light media-btn d-none" id="musicLoop" title="循环播放">
                        <span class="loop-icon">🔁</span>
                    </button>
                </div>

                <div class="media-divider"></div>

                <!-- 朗读控制 -->
                <div class="speech-controls d-flex align-items-center">
                    <button class="btn btn-sm btn-outline-light media-btn" id="speechToggle" title="朗读原文">
                        <span class="speech-icon">🔊</span>
                    </button>
                    <button class="btn btn-sm btn-outline-light media-btn d-none" id="speechStop" title="停止朗读">
                        ⏹
                    </button>
                </div>

                <!-- AI解读按钮 -->
                <button class="btn btn-sm btn-outline-light ai-btn" id="aiToggle" title="AI解读">
                    <span>🤖</span>
                </button>

                <!-- AI创新功能下拉菜单 -->
                <div class="dropdown">
                    <button class="btn btn-sm btn-outline-warning dropdown-toggle" type="button" data-bs-toggle="dropdown" title="AI创新功能">
                        <span>✨</span>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><h6 class="dropdown-header">AI创新功能</h6></li>
                        <li>
                            <button class="dropdown-item" id="knowledgeGraphBtn">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2">
                                    <circle cx="12" cy="12" r="3"></circle>
                                    <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
                                </svg>
                                概念关系图谱
                            </button>
                        </li>
                        <li>
                            <button class="dropdown-item" id="commentaryChatBtn">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2">
                                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                                </svg>
                                与注释家对话
                            </button>
                        </li>
                        <li>
                            <button class="dropdown-item" id="philosophyDialogueBtn">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                                    <line x1="9" y1="9" x2="9.01" y2="9"></line>
                                    <line x1="15" y1="9" x2="15.01" y2="9"></line>
                                </svg>
                                跨文明哲学对话
                            </button>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li><h6 class="dropdown-header">实用工具</h6></li>
                        <li>
                            <button class="dropdown-item" id="noteBtn">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                                </svg>
                                阅读笔记
                            </button>
                        </li>
                        <li>
                            <button class="dropdown-item" id="quoteBtn">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2">
                                    <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>
                                    <polyline points="16 6 12 2 8 6"></polyline>
                                    <line x1="12" y1="2" x2="12" y2="15"></line>
                                </svg>
                                生成引用卡片
                            </button>
                        </li>
                    </ul>
                </div>

                <!-- 设置按钮 -->
                <button class="btn btn-sm btn-outline-light" id="settingsToggle" title="设置">
                    <span>⚙️</span>
                </button>

                <!-- 暗黑模式切换 -->
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
                    <h6 class="sidebar-title">📑 章节目录</h6>
                    <div class="chapter-list-scrollable" id="chapterList">
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

    <!-- 背景音乐 -->
    <audio id="bgMusic" loop preload="auto">
        <source src="/assets/audio/gaoshanliushui.mp3" type="audio/mpeg">
    </audio>

    <!-- 音乐音量控制面板 -->
    <div class="volume-panel" id="volumePanel">
        <div class="volume-panel-header">
            <span>音量控制</span>
            <button type="button" class="btn-close btn-close-white" id="closeVolumePanel"></button>
        </div>
        <div class="volume-panel-body">
            <input type="range" class="form-range" id="volumeSlider" min="0" max="100" value="30">
            <div class="volume-level">
                <span id="volumeValue">30</span>%
            </div>
        </div>
    </div>

    <!-- 朗读控制面板 -->
    <div class="speech-panel" id="speechPanel">
        <div class="speech-panel-header">
            <span>朗读设置</span>
            <button type="button" class="btn-close btn-close-white" id="closeSpeechPanel"></button>
        </div>
        <div class="speech-panel-body">
            <div class="speech-option mb-3">
                <label class="form-label">朗读模式</label>
                <div class="btn-group w-100" role="group">
                    <input type="radio" class="btn-check" name="speechMode" id="speechModeCurrent" value="current" checked>
                    <label class="btn btn-outline-light" for="speechModeCurrent">当前章节</label>

                    <input type="radio" class="btn-check" name="speechMode" id="speechModeAll" value="all">
                    <label class="btn btn-outline-light" for="speechModeAll">连续朗读</label>
                </div>
            </div>
            <div class="speech-option">
                <label class="form-label">语速</label>
                <input type="range" class="form-range" id="speechRate" min="50" max="150" value="80">
                <div class="rate-level">
                    <span id="rateValue">0.8</span>x
                </div>
            </div>
            <div class="speech-status mt-3" id="speechStatus">
                准备就绪
            </div>
        </div>
    </div>

    <!-- AI解读侧边栏 -->
    <aside class="ai-sidebar" id="aiSidebar">
        <div class="ai-sidebar-header">
            <h6 class="ai-title">🤖 AI解读</h6>
            <div class="ai-actions">
                <button class="btn btn-sm btn-outline-light" id="aiNewChat" title="新对话">
                    <span>➕</span>
                </button>
                <button class="btn btn-sm btn-outline-light" id="aiCloseSidebar" title="关闭">
                    <span>✕</span>
                </button>
            </div>
        </div>
        <div class="ai-messages" id="aiMessages">
            <div class="ai-welcome">
                <div class="ai-welcome-icon">🤖</div>
                <h6>AI助手</h6>
                <p>您可以：</p>
                <ul>
                    <li>点击下方快捷问题开始</li>
                    <li>或直接输入您的问题</li>
                </ul>
            </div>
        </div>
        <div class="ai-suggestions">
            <button class="ai-suggestion-btn">解释这一章的核心思想</button>
            <button class="ai-suggestion-btn">这段话的哲学含义</button>
            <button class="ai-suggestion-btn">如何在生活中应用</button>
        </div>
        <div class="ai-input-area">
            <div class="ai-input-wrapper">
                <textarea class="ai-input" id="aiInput" placeholder="输入您的问题..." rows="2"></textarea>
                <button class="ai-send-btn" id="aiSendBtn">
                    <span>📤</span>
                </button>
            </div>
            <small class="ai-model-info">
                模型: <span id="aiModelDisplay">自动检测</span>
            </small>
        </div>
    </aside>

    <!-- 设置面板 -->
    <div class="settings-panel" id="settingsPanel">
        <div class="settings-panel-header">
            <span>⚙️ 阅读设置</span>
            <button type="button" class="btn-close btn-close-white" id="closeSettingsPanel"></button>
        </div>
        <div class="settings-panel-body">
            <!-- 阅读模式 -->
            <div class="setting-section">
                <label class="setting-label">阅读模式</label>
                <div class="setting-options">
                    <button class="mode-btn active" data-mode="reading">
                        <span class="mode-icon">📖</span>
                        <span class="mode-text">阅读</span>
                    </button>
                    <button class="mode-btn" data-mode="zen">
                        <span class="mode-icon">🧘</span>
                        <span class="mode-text">禅读</span>
                    </button>
                    <button class="mode-btn" data-mode="recite">
                        <span class="mode-icon">📝</span>
                        <span class="mode-text">背诵</span>
                    </button>
                </div>
            </div>

            <!-- 字体选择 -->
            <div class="setting-section">
                <label class="setting-label">字体选择</label>
                <select class="form-select form-select-sm" id="fontSelect">
                    <option value="default">系统默认</option>
                    <option value="kaiti">楷体</option>
                    <option value="songti">宋体</option>
                    <option value="fangsong">仿宋</option>
                    <option value="mingliu">明体</option>
                    <option value="xkai">华文行楷</option>
                </select>
            </div>

            <!-- 字体大小 -->
            <div class="setting-section">
                <label class="setting-label">字体大小</label>
                <div class="font-size-control">
                    <button class="size-btn" data-size="small">小</button>
                    <button class="size-btn active" data-size="medium">中</button>
                    <button class="size-btn" data-size="large">大</button>
                </div>
            </div>

            <!-- 文字布局 -->
            <div class="setting-section">
                <label class="setting-label">文字布局</label>
                <div class="setting-options">
                    <button class="layout-btn active" data-layout="center">
                        <span class="layout-icon">📍</span>
                        <span class="layout-text">居中</span>
                    </button>
                    <button class="layout-btn" data-layout="left">
                        <span class="layout-icon">⬅️</span>
                        <span class="layout-text">靠左</span>
                    </button>
                </div>
            </div>

            <!-- 背景音乐 -->
            <div class="setting-section">
                <label class="setting-label">背景音乐</label>
                <select class="form-select form-select-sm mb-2" id="musicSelect">
                    <option value="none">关闭</option>
                    <option value="chinese">中国古典（古琴/琵琶）</option>
                    <option value="western">西方古典（钢琴/小提琴）</option>
                </select>
                <div class="volume-control-inline">
                    <span class="volume-label">音量</span>
                    <input type="range" class="form-range form-range-sm" id="musicVolumeSlider" min="0" max="100" value="30">
                    <span class="volume-value" id="musicVolumeValue">30%</span>
                </div>
            </div>

            <!-- 显示选项 -->
            <div class="setting-section">
                <label class="setting-label">显示选项</label>
                <div class="setting-toggles">
                    <label class="toggle-item">
                        <input type="checkbox" id="showPinyin" checked>
                        <span>显示拼音</span>
                    </label>
                    <label class="toggle-item">
                        <input type="checkbox" id="showAnnotation" checked>
                        <span>显示释义</span>
                    </label>
                </div>
            </div>

            <!-- 版本选择 -->
            <div class="setting-section">
                <label class="setting-label">显示版本</label>
                <div class="version-toggles">
                    <label class="toggle-item">
                        <input type="checkbox" id="showModern" checked>
                        <span>白话译文</span>
                    </label>
                    <label class="toggle-item">
                        <input type="checkbox" id="showNotes" checked>
                        <span>注解版本</span>
                    </label>
                    <label class="toggle-item">
                        <input type="checkbox" id="showEnglish">
                        <span>英文译本</span>
                    </label>
                </div>
            </div>

            <!-- AI设置 -->
            <div class="setting-section">
                <label class="setting-label">AI API配置</label>
                <input type="password" class="form-control form-control-sm mb-2" id="deepseekKey" placeholder="DeepSeek API Key (可选)">
                <input type="password" class="form-control form-control-sm" id="openaiKey" placeholder="OpenAI API Key (可选)">
                <small class="text-muted d-block mt-1">
                    API Key仅存储在本地，不会上传服务器
                </small>
            </div>

            <!-- 语音朗读设置 -->
            <div class="setting-section">
                <label class="setting-label">🎙️ 语音朗读设置</label>
                <div class="mb-2">
                    <label class="small text-muted">选择语音：</label>
                    <select class="form-select form-select-sm" id="browserVoice">
                        <option value="">正在加载可用语音...</option>
                    </select>
                    <small class="text-muted d-block">
                        提示：Microsoft语音质量最佳，搜索"Microsoft"或"Chinese"
                    </small>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/assets/js/modules/theme.js"></script>
    <script src="/assets/js/modules/sidebar.js"></script>
    <script src="/assets/js/modules/music.js"></script>
    <script src="/assets/js/modules/shortcuts.js"></script>
    <script src="/assets/js/modules/pwa.js"></script>
    <script src="/assets/js/modules/local-search.js"></script>
    <script src="/assets/js/modules/notes.js"></script>
    <script src="/assets/js/modules/quote-card.js"></script>
    <script src="/assets/js/modules/knowledge-graph.js"></script>
    <script src="/assets/js/modules/commentary-chat.js"></script>
    <script src="/assets/js/modules/philosophy-dialogue.js"></script>
    <script src="/assets/js/modules/settings.js"></script>
    <script src="/assets/js/main.js"></script>
    <script>
{extra_js}
    </script>
</body>
</html>
"""

INDEX_EXTRA_CSS = """
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
"""

CHAPTER_EXTRA_CSS = """
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
"""

CHAPTER_EXTRA_JS = """
// 复制原文
document.getElementById('copyOriginal')?.addEventListener('click', function() {
    const text = document.getElementById('originalText').innerText;
    navigator.clipboard.writeText(text).then(() => {
        this.textContent = '已复制';
        setTimeout(() => this.textContent = '复制', 2000);
    });
});

// 成语标签悬停效果
document.querySelectorAll('.idiom-tag').forEach(tag => {
    tag.addEventListener('click', function() {
        // 点击成语时显示详细信息（可选功能）
        const meaning = this.getAttribute('title');
        if (meaning) {
            alert(meaning.replace(/&#10;/g, '\\n'));
        }
    });
});
"""


def generate_chapter_list_html(chapters, _classic_id, active_id=None):  # noqa: U101
    """生成章节目录HTML"""
    items = []
    for ch in chapters:
        active_class = "active" if ch["chapter"] == active_id else ""
        items.append(
            f'<a class="nav-link chapter-item {active_class}" href="./chapter{ch["chapter"]}.html">'
        )
        items.append(f'    <span class="chapter-num">第{ch["chapter"]}章</span>')
        items.append("</a>")
    return "\n".join(items)


def generate_index_page(data, classic_meta):
    """生成经典首页"""
    classic_id = classic_meta["id"]
    short_name = classic_meta["short_name"]
    icon = classic_meta.get("icon", "☯")
    color = classic_meta.get("color", "#d4a574")
    chapter_unit = "篇" if classic_id == "zzj" else "章"
    total_chapters = classic_meta.get("chapters", len(data["chapters"]))

    chapter_list = generate_chapter_list_html(data["chapters"], classic_id)

    # 生成章节卡片
    cards = []
    for ch in data["chapters"][:20]:  # 首页显示前20章
        preview = ch.get("modern_chinese", "")[:30]
        ch_title = ch.get("title", f"第{ch['chapter']}{chapter_unit}")
        cards.append(f'<a href="./chapter{ch["chapter"]}.html" class="chapter-card">')
        cards.append(f'    <div class="chapter-num">{ch_title}</div>')
        cards.append(f'    <div class="chapter-preview">{preview}...</div>')
        cards.append("</a>")

    # 生成版本标签
    version_badges = ""
    if classic_id == "ddj":
        version_badges = """
            <span class="badge bg-secondary me-1">王弼注</span>
            <span class="badge bg-secondary me-1">河上公注</span>
            <span class="badge bg-secondary me-1">王夫之</span>
            <span class="badge bg-secondary me-1">憨山德清</span>
            <span class="badge bg-info me-1">帛书</span>
            <span class="badge bg-info">郭店简</span>
        """
    elif classic_id == "zzj":
        version_badges = """
            <span class="badge bg-secondary me-1">成玄英疏</span>
            <span class="badge bg-secondary me-1">郭象注</span>
            <span class="badge bg-secondary">王夫之</span>
        """

    content = f"""
    <div class="intro-section">
        <h1 class="text-center mb-4">{icon} {short_name}</h1>
        <p class="text-center text-muted mb-4">多版本对照研究平台</p>
        <p class="text-center">
            {version_badges}
        </p>
    </div>

    <h4 class="mb-3">章节目录</h4>
    <div class="chapters-grid index-page">
{"".join(cards)}
    </div>

    <div class="text-center mt-4">
        <a href="./all-chapters.html" class="btn btn-outline-primary">查看全部{total_chapters}{chapter_unit} →</a>
    </div>
"""

    extra_css = INDEX_EXTRA_CSS.replace("#d4a574", color)

    # 生成经典切换器
    classic_switcher = generate_classic_switcher_html(classic_id)

    # 构建经典描述
    classic_desc_parts = []
    if classic_id == "ddj":
        classic_desc = "王弼本 · 河上公本 · 王夫之 · 憨山德清 | 帛书 · 郭店简"
    elif classic_id == "zzj":
        classic_desc = "成玄英疏 · 郭象注 · 王夫之"
    else:
        classic_desc = f"{classic_meta.get('author', '')}著 · {short_name}"

    html = HTML_TEMPLATE.format(
        title=f"{short_name} - 多版本对照平台",
        page_title="首页",
        classic_name=short_name,
        classic_icon=icon,
        classic_short_name=short_name,
        classic_desc=classic_desc,
        classic_switcher=classic_switcher,
        extra_css=extra_css,
        chapter_list=chapter_list,
        content=content,
        extra_js="",
    )

    return html


def generate_all_chapters_page(data, classic_meta):
    """生成全部章节页面"""
    classic_id = classic_meta["id"]
    short_name = classic_meta["short_name"]
    total_chapters = classic_meta.get("chapters", len(data["chapters"]))
    chapter_unit = "篇" if classic_id == "zzj" else "章"

    chapter_list = generate_chapter_list_html(data["chapters"], classic_id)

    cards = []
    for ch in data["chapters"]:
        preview = ch.get("modern_chinese", "")[:30]
        ch_title = ch.get("title", f"第{ch['chapter']}{chapter_unit}")
        cards.append(f'<a href="./chapter{ch["chapter"]}.html" class="chapter-card">')
        cards.append(f'    <div class="chapter-num">{ch_title}</div>')
        cards.append(f'    <div class="chapter-preview">{preview}...</div>')
        cards.append("</a>")

    content = f"""
    <h4 class="mb-3">全部{total_chapters}{chapter_unit}</h4>
    <div class="chapters-grid index-page">
{"".join(cards)}
    </div>
"""

    # 生成经典切换器
    classic_switcher = generate_classic_switcher_html(classic_id)

    # 构建经典描述
    if classic_id == "ddj":
        classic_desc = "王弼本 · 河上公本 · 王夫之 · 憨山德清 | 帛书 · 郭店简"
    elif classic_id == "zzj":
        classic_desc = "成玄英疏 · 郭象注 · 王夫之"
    else:
        classic_desc = f"{classic_meta.get('author', '')}著 · {short_name}"

    html = HTML_TEMPLATE.format(
        title=f"全部章节 - {short_name}",
        page_title="全部章节",
        classic_name=short_name,
        classic_icon=classic_meta.get("icon", "☯"),
        classic_short_name=short_name,
        classic_desc=classic_desc,
        classic_switcher=classic_switcher,
        extra_css=INDEX_EXTRA_CSS,
        chapter_list=chapter_list,
        content=content,
        extra_js="",
    )

    return html


def generate_chapter_page(data, chapter_id, classic_meta, idioms=None):
    """生成单章页面"""
    classic_id = classic_meta["id"]
    short_name = classic_meta["short_name"]
    color = classic_meta.get("color", "#d4a574")
    chapter_unit = "篇" if classic_id == "zzj" else "章"
    total_chapters = classic_meta.get("chapters", len(data["chapters"]))

    chapter = next((c for c in data["chapters"] if c["chapter"] == chapter_id), None)
    if not chapter:
        return None

    # 获取相邻章节
    idx = data["chapters"].index(chapter)
    prev_chapter = data["chapters"][idx - 1] if idx > 0 else None
    next_chapter = (
        data["chapters"][idx + 1] if idx < len(data["chapters"]) - 1 else None
    )

    # 使用服务层的标注函数
    original_annotated = annotate_difficult_chars(chapter.get("original", ""))

    chapter_list = generate_chapter_list_html(data["chapters"], classic_id, chapter_id)

    # 筛选当前章节相关的成语
    related_idioms = []
    if idioms:
        related_idioms = [
            idiom for idiom in idioms if idiom.get("chapter") == chapter_id
        ]

    # 生成成语展示HTML
    idioms_html = ""
    if related_idioms:
        idioms_html = '<div class="idioms-container d-flex flex-wrap gap-2">'
        for idiom in related_idioms:
            safe_meaning = idiom.get("meaning", "").replace('"', "&quot;")
            safe_source = idiom.get("source", "").replace('"', "&quot;")
            idioms_html += f"""
            <span class="idiom-tag" title="{safe_meaning}&#10;原文：{safe_source}">
                <span class="idiom-word">{idiom.get("word", "")}</span>
                <span class="idiom-chapter">📖</span>
            </span>"""
        idioms_html += "</div>"
    else:
        idioms_html = '<span class="text-muted">本章暂无收录相关成语</span>'

    ch_title = chapter.get("title", f"第{chapter_id}{chapter_unit}")

    # 构建内容
    content = f"""
    <nav aria-label="章节导航" class="chapter-nav mb-3">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="./index.html">目录</a></li>
            <li class="breadcrumb-item active">{ch_title}</li>
        </ol>
    </nav>

    <section class="idioms-section mb-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">📖 相关成语</h5>
            </div>
            <div class="card-body">
                <div id="idiomsContainer">
                    {idioms_html}
                </div>
            </div>
        </div>
    </section>

    <section class="original-section mb-4">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">{ch_title} · 原文</h5>
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
                <p class="modern-text mb-0">{chapter.get("modern_chinese", "")}</p>
            </div>
        </div>
    </section>
"""

    # 根据经典类型添加不同的注释版本
    if classic_id == "ddj":
        content += f"""
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
                </ul>
                <div class="tab-content p-3">
                    <div class="tab-pane fade show active" id="wangbi">
                        <h6 class="text-muted mb-2">王弼注（魏晋）</h6>
                        <p class="note-text mb-0">{chapter.get("wangbi_note", "")}</p>
                    </div>
                    <div class="tab-pane fade" id="heshanggong">
                        <h6 class="text-muted mb-2">河上公注（汉）</h6>
                        <p class="note-text mb-0">{chapter.get("heshanggong_note", "")}</p>
                    </div>
                    <div class="tab-pane fade" id="wangfuzhi">
                        <h6 class="text-muted mb-2">王夫之《老子衍》（明末清初）</h6>
                        <p class="note-text mb-0">{chapter.get("wangfuzhi_note", "")}</p>
                    </div>
                    <div class="tab-pane fade" id="hanshan">
                        <h6 class="text-muted mb-2">憨山德清《老子道德经解》（明）</h6>
                        <p class="note-text mb-0">{chapter.get("hanshandeqing_note", "")}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

    # 添加英文译本
    content += f"""
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
                </ul>
                <div class="tab-content p-3">
                    <div class="tab-pane fade show active" id="lau">
                        <p class="english-text mb-0 fst-italic">{chapter.get("english_lau", "")}</p>
                    </div>
                    <div class="tab-pane fade" id="henricks">
                        <p class="english-text mb-0 fst-italic">{chapter.get("english_henricks", "")}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

    # 添加导航
    content += f"""
    <nav class="chapter-navigation" aria-label="章节翻页">
        <ul class="pagination justify-content-center">
            {f'<li class="page-item"><a class="page-link" href="./chapter{prev_chapter["chapter"]}.html">← 第{prev_chapter["chapter"]}{chapter_unit}</a></li>' if prev_chapter else '<li class="page-item disabled"><span class="page-link">← 上一篇</span></li>'}
            <li class="page-item disabled">
                <span class="page-link">{chapter_id} / {total_chapters}</span>
            </li>
            {f'<li class="page-item"><a class="page-link" href="./chapter{next_chapter["chapter"]}.html">第{next_chapter["chapter"]}{chapter_unit} →</a></li>' if next_chapter else '<li class="page-item disabled"><span class="page-link">下一篇 →</span></li>'}
        </ul>
    </nav>
"""

    extra_css = CHAPTER_EXTRA_CSS.replace("#d4a574", color)

    # 生成经典切换器
    classic_switcher = generate_classic_switcher_html(classic_id)

    # 构建经典描述
    if classic_id == "ddj":
        classic_desc = "王弼本 · 河上公本 · 王夫之 · 憨山德清 | 帛书 · 郭店简"
    elif classic_id == "zzj":
        classic_desc = "成玄英疏 · 郭象注 · 王夫之"
    else:
        classic_desc = f"{classic_meta.get('author', '')}著 · {short_name}"

    html = HTML_TEMPLATE.format(
        title=f"{ch_title} - {short_name}",
        page_title=ch_title,
        classic_name=short_name,
        classic_icon=classic_meta.get("icon", "☯"),
        classic_short_name=short_name,
        classic_desc=classic_desc,
        classic_switcher=classic_switcher,
        extra_css=extra_css,
        chapter_list=chapter_list,
        content=content,
        extra_js=CHAPTER_EXTRA_JS,
    )

    return html


def copy_assets():
    """复制静态资源文件"""
    # 创建assets目录
    assets_css_dir = OUTPUT_DIR / "assets" / "css"
    assets_js_dir = OUTPUT_DIR / "assets" / "js"
    assets_js_modules_dir = assets_js_dir / "modules"
    assets_audio_dir = OUTPUT_DIR / "assets" / "audio"
    assets_css_dir.mkdir(parents=True, exist_ok=True)
    assets_js_dir.mkdir(parents=True, exist_ok=True)
    assets_js_modules_dir.mkdir(parents=True, exist_ok=True)
    assets_audio_dir.mkdir(parents=True, exist_ok=True)

    # 复制CSS
    shutil.copy(BASE_DIR / "static" / "css" / "style.css", assets_css_dir / "style.css")

    # 复制JS模块
    modules_dir = BASE_DIR / "static" / "js" / "modules"
    if modules_dir.exists():
        for module_file in modules_dir.glob("*.js"):
            shutil.copy(module_file, assets_js_modules_dir / module_file.name)

    # 复制Service Worker和Manifest
    sw_src = BASE_DIR / "static" / "js" / "sw.js"
    if sw_src.exists():
        shutil.copy(sw_src, assets_js_dir / "sw.js")

    manifest_src = BASE_DIR / "static" / "manifest.json"
    if manifest_src.exists():
        shutil.copy(manifest_src, OUTPUT_DIR / "manifest.json")

    # 复制并修改main.js (移除API搜索功能)  # noqa: E800
    js_content = (BASE_DIR / "static" / "js" / "main.js").read_text(encoding="utf-8")
    # 静态版本不需要搜索功能，注释掉
    static_js = js_content.replace(
        "SearchManager.init();", "// SearchManager.init();  // 静态版本禁用搜索"
    ).replace(
        "API_ENDPOINT: '/api/daodejing/search',",
        "// API_ENDPOINT: '/api/daodejing/search',  // 静态版本",
    )
    (assets_js_dir / "main.js").write_text(static_js, encoding="utf-8")

    # 复制音频文件
    audio_dir = BASE_DIR / "static" / "audio"
    if audio_dir.exists():
        for audio_file in audio_dir.glob("*.mp3"):
            shutil.copy(audio_file, assets_audio_dir / audio_file.name)
        print(f"      复制了 {len(list(assets_audio_dir.glob('*.mp3')))} 个音频文件")


def generate_site():
    """生成静态网站"""
    print("=" * 50)
    print("古籍经典静态网站生成器")
    print("=" * 50)

    # 清理并创建输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 获取所有经典
    print("\n[1/6] 加载经典元数据...")
    metadata = load_classics_metadata()
    classics = metadata.get("classics", [])
    default_classic = metadata.get("default_classic", "ddj")
    print(f"      发现 {len(classics)} 部经典")

    # 加载成语数据
    print("\n[2/6] 加载成语数据...")
    idioms = load_idioms()
    print(f"      加载了 {len(idioms)} 个成语")

    # 复制静态资源
    print("\n[3/6] 复制静态资源...")
    copy_assets()
    print("      CSS 和 JS 文件已复制")

    # 为每部经典生成页面
    print("\n[4/6] 生成经典页面...")
    total_html_files = 0

    for classic in classics:
        classic_id = classic["id"]
        print(f"\n      正在处理 {classic['name']} ({classic_id})...")

        data, classic_meta = load_classic_data(classic_id)
        if not data:
            print(f"        跳过 {classic_id}：数据文件未找到")
            continue

        # 创建经典子目录
        classic_dir = OUTPUT_DIR / classic_id
        classic_dir.mkdir(parents=True, exist_ok=True)

        # 生成经典首页
        index_html = generate_index_page(data, classic_meta)
        (classic_dir / "index.html").write_text(index_html, encoding="utf-8")

        # 生成全部章节页
        all_html = generate_all_chapters_page(data, classic_meta)
        (classic_dir / "all-chapters.html").write_text(all_html, encoding="utf-8")

        # 生成章节页面
        for ch in data["chapters"]:
            html = generate_chapter_page(data, ch["chapter"], classic_meta, idioms)
            if html:
                (classic_dir / f"chapter{ch['chapter']}.html").write_text(
                    html, encoding="utf-8"
                )

        total_html_files += len(data["chapters"]) + 2  # +2 for index and all-chapters
        print(f"        生成完成：{len(data['chapters'])} 个章节 + 2 个导航页")

    # 生成总首页（重定向到默认经典）
    print("\n[5/6] 生成总首页...")
    index_html = generate_main_index_page(classics, default_classic)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    total_html_files += 1

    print("\n[6/6] 完成！")
    print("\n" + "=" * 50)
    print("✓ 静态网站生成完成！")
    print(f"  输出目录: {OUTPUT_DIR}")
    print(f"  总文件数: {total_html_files} 个HTML文件")
    print(f"  包含经典: {', '.join([c['short_name'] for c in classics])}")
    print("=" * 50)

    # 统计信息
    total_size = sum(f.stat().st_size for f in OUTPUT_DIR.rglob("*"))
    print(f"\n总大小: {total_size / 1024:.1f} KB")


def generate_main_index_page(classics, default_classic):
    """生成总首页（多经典目录）"""

    # 生成经典卡片
    classic_cards = []
    for classic in classics:
        card_html = f"""
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 classic-card">
                <div class="card-body text-center">
                    <div class="classic-icon mb-3" style="font-size: 4rem;">{classic.get("icon", "📖")}</div>
                    <h3 class="card-title">{classic.get("name", "")}</h3>
                    <p class="card-text text-muted">{classic.get("description", "")}</p>
                    <div class="classic-meta mb-3">
                        <span class="badge bg-secondary">{classic.get("author", "")}</span>
                        <span class="badge bg-light text-dark">{classic.get("era", "")}</span>
                        <span class="badge bg-info">{classic.get("chapters", 0)}章</span>
                    </div>
                    <a href="./{classic.get("id", "")}/index.html" class="btn btn-primary w-100">
                        开始阅读
                    </a>
                </div>
                <div class="card-footer bg-transparent">
                    <small class="text-muted">
                        注释: {len(classic.get("commentators", []))}家
                        译本: {len(classic.get("translators", []))}种
                    </small>
                </div>
            </div>
        </div>
        """
        classic_cards.append(card_html)

    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-theme="auto">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>古籍经典平台 - 道德经 · 庄子</title>
    <meta name="description" content="多版本对照学习平台 - 支持多种注释版本、英文翻译、古籍版本对比">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>☯</text></svg>">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #8B4513;
            --secondary-color: #D2691E;
            --bg-color: #f5f5dc;
            --card-bg: #fff;
        }}
        [data-theme="dark"] {{
            --bg-color: #1a1a1a;
            --card-bg: #2d2d2d;
            color: #e0e0e0;
        }}
        body {{
            background: var(--bg-color);
            min-height: 100vh;
        }}
        .hero-section {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4rem 0;
            margin-bottom: 3rem;
        }}
        .classic-card {{
            background: var(--card-bg);
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .classic-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        }}
        .classic-icon {{
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
        }}
        .features-section {{
            padding: 3rem 0;
        }}
        .feature-item {{
            text-align: center;
            padding: 1.5rem;
        }}
        .feature-icon {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        .footer {{
            background: rgba(0,0,0,0.05);
            padding: 2rem 0;
            margin-top: 4rem;
        }}
    </style>
</head>
<body>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">
                <span style="font-size: 1.5rem;">☯</span>
                <span class="ms-2">古籍经典平台</span>
            </a>
            <div class="navbar-nav ms-auto">
                <button class="btn btn-outline-light btn-sm" id="themeToggle" title="切换主题">
                    🌓
                </button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container text-center">
            <h1 class="display-4 mb-3">古籍经典学习平台</h1>
            <p class="lead mb-4">多版本对照 · 深度注释 · AI辅助理解</p>
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <p class="mb-0 opacity-75">
                        支持王弼注、河上公注、王夫之、憨山德清等历代名家注释<br>
                        提供D.C. Lau、Henricks、Addiss & Lombardo等权威英译对照
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- 经典目录 -->
    <section class="container mb-5">
        <h2 class="text-center mb-5">📚 经典目录</h2>
        <div class="row">
            {"".join(classic_cards)}
        </div>
    </section>

    <!-- 功能特性 -->
    <section class="features-section bg-light">
        <div class="container">
            <h2 class="text-center mb-5">✨ 平台特色</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="feature-item">
                        <div class="feature-icon">📖</div>
                        <h4>多版本对照</h4>
                        <p class="text-muted">原文、注释、英译并列展示，便于比较研究</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <div class="feature-icon">🔍</div>
                        <h4>智能搜索</h4>
                        <p class="text-muted">支持全文检索，快速定位相关内容</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <div class="feature-icon">📝</div>
                        <h4>阅读笔记</h4>
                        <p class="text-muted">添加个人笔记，书签收藏，支持数据导出</p>
                    </div>
                </div>
            </div>
            <div class="row mt-4">
                <div class="col-md-4">
                    <div class="feature-item">
                        <div class="feature-icon">🤖</div>
                        <h4>AI解读</h4>
                        <p class="text-muted">知识图谱、语义考古、跨文明对话</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <div class="feature-icon">🔊</div>
                        <h4>语音朗读</h4>
                        <p class="text-muted">TTS语音合成，支持原文朗读</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="feature-item">
                        <div class="feature-icon">🌙</div>
                        <h4>暗黑模式</h4>
                        <p class="text-muted">护眼的深色主题，夜间阅读更舒适</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
        <div class="container text-center">
            <p class="text-muted mb-2">古籍经典学习平台 © 2026</p>
            <p class="text-muted small">
                Made with ❤️ and ☯️ |
                <a href="https://github.com/yourusername/daodejing" target="_blank">GitHub</a>
            </p>
        </div>
    </footer>

    <!-- 主题切换脚本 -->
    <script>
        const themeToggle = document.getElementById('themeToggle');
        const html = document.documentElement;

        // 加载保存的主题
        const savedTheme = localStorage.getItem('theme') || 'auto';
        html.setAttribute('data-theme', savedTheme);

        themeToggle.addEventListener('click', () => {{
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        }});
    </script>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""


if __name__ == "__main__":
    generate_site()
