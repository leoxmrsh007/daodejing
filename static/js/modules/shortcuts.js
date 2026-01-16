/**
 * 键盘快捷键模块
 * 提供便捷的键盘操作
 */

const KeyboardShortcuts = {
    shortcuts: {
        // 导航
        'ArrowLeft': { action: 'prevChapter', description: '上一章' },
        'ArrowRight': { action: 'nextChapter', description: '下一章' },
        'ArrowUp': { action: 'scrollUp', description: '向上滚动' },
        'ArrowDown': { action: 'scrollDown', description: '向下滚动' },
        'Home': { action: 'firstChapter', description: '第一章' },
        'End': { action: 'lastChapter', description: '第八十一章' },

        // 功能
        'k': { action: 'focusSearch', description: '聚焦搜索' },
        'n': { action: 'toggleTheme', description: '切换主题' },
        'm': { action: 'toggleMusic', description: '播放/暂停音乐' },
        's': { action: 'toggleSpeech', description: '开始/停止朗读' },
        'b': { action: 'toggleBookmark', description: '添加/取消书签' },
        'f': { action: 'toggleFullscreen', description: '全屏' },
        '?': { action: 'showHelp', description: '显示快捷键帮助' },

        // 退出
        'Escape': { action: 'closePanels', description: '关闭面板' }
    },

    init() {
        this.bindEvents();
        this.setupHelpModal();
    },

    bindEvents() {
        document.addEventListener('keydown', (e) => {
            // 忽略在输入框中的按键
            if (e.target.tagName === 'INPUT' ||
                e.target.tagName === 'TEXTAREA' ||
                e.target.contentEditable === 'true') {
                // 只响应 Escape 键
                if (e.key === 'Escape') {
                    this.executeAction('closePanels');
                }
                return;
            }

            const shortcut = this.shortcuts[e.key];
            if (shortcut) {
                e.preventDefault();
                this.executeAction(shortcut.action);
            }
        });
    },

    executeAction(action) {
        switch (action) {
            case 'prevChapter':
                this.navigateToChapter(-1);
                break;
            case 'nextChapter':
                this.navigateToChapter(1);
                break;
            case 'scrollUp':
                window.scrollBy({ top: -300, behavior: 'smooth' });
                break;
            case 'scrollDown':
                window.scrollBy({ top: 300, behavior: 'smooth' });
                break;
            case 'firstChapter':
                window.location.href = '/daodejing/chapter/1';
                break;
            case 'lastChapter':
                window.location.href = '/daodejing/chapter/81';
                break;
            case 'focusSearch':
                const searchInput = document.getElementById('searchInput');
                if (searchInput) {
                    searchInput.focus();
                }
                break;
            case 'toggleTheme':
                if (typeof ThemeManager !== 'undefined') {
                    ThemeManager.toggle();
                }
                break;
            case 'toggleMusic':
                if (typeof MusicManager !== 'undefined') {
                    MusicManager.toggle();
                }
                break;
            case 'toggleSpeech':
                if (typeof SpeechManager !== 'undefined') {
                    SpeechManager.toggle();
                }
                break;
            case 'toggleBookmark':
                if (typeof BookmarkManager !== 'undefined') {
                    BookmarkManager.setupBookmarkButtons();
                    const btn = document.getElementById('bookmarkBtn');
                    if (btn) btn.click();
                }
                break;
            case 'toggleFullscreen':
                this.toggleFullscreen();
                break;
            case 'showHelp':
                this.showHelpModal();
                break;
            case 'closePanels':
                this.closeAllPanels();
                break;
        }
    },

    navigateToChapter(direction) {
        const currentChapter = this.getCurrentChapter();
        if (!currentChapter) return;

        const newChapter = currentChapter + direction;
        if (newChapter >= 1 && newChapter <= 81) {
            window.location.href = `/daodejing/chapter/${newChapter}`;
        }
    },

    getCurrentChapter() {
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            if (match) return parseInt(match[1]);
        }
        return null;
    },

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('全屏模式不可用');
            });
        } else {
            document.exitFullscreen();
        }
    },

    closeAllPanels() {
        // 关闭所有面板
        const panels = document.querySelectorAll('.settings-panel.show, .speech-panel.show, .volume-panel.show, .ai-sidebar.show');
        panels.forEach(panel => panel.classList.remove('show'));

        // 关闭模态框
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) modalInstance.hide();
        });
    },

    setupHelpModal() {
        // 如果帮助面板不存在，创建一个
        if (!document.getElementById('shortcutsHelp')) {
            const helpHtml = `
                <div class="modal fade" id="shortcutsHelp" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">⌨️ 键盘快捷键</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <table class="table table-sm">
                                    <thead>
                                        <tr><th>快捷键</th><th>功能</th></tr>
                                    </thead>
                                    <tbody>
                                        <tr><td><kbd>←</kbd> <kbd>→</kbd></td><td>上一章 / 下一章</td></tr>
                                        <tr><td><kbd>Home</kbd> / <kbd>End</kbd></td><td>第一章 / 第八十一章</td></tr>
                                        <tr><td><kbd>K</kbd></td><td>聚焦搜索</td></tr>
                                        <tr><td><kbd>N</kbd></td><td>切换主题</td></tr>
                                        <tr><td><kbd>M</kbd></td><td>播放/暂停音乐</td></tr>
                                        <tr><td><kbd>S</kbd></td><td>开始/停止朗读</td></tr>
                                        <tr><td><kbd>B</kbd></td><td>添加/取消书签</td></tr>
                                        <tr><td><kbd>F</kbd></td><td>全屏模式</td></tr>
                                        <tr><td><kbd>Esc</kbd></td><td>关闭面板</td></tr>
                                        <tr><td><kbd>?</kbd></td><td>显示此帮助</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', helpHtml);
        }
    },

    showHelpModal() {
        const helpModal = document.getElementById('shortcutsHelp');
        if (helpModal) {
            const modal = new bootstrap.Modal(helpModal);
            modal.show();
        }
    },

    getShortcutsList() {
        return this.shortcuts;
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = KeyboardShortcuts;
}
