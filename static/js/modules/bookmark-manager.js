/**
 * 书签、笔记、收藏管理模块
 * 支持 localStorage 持久化存储
 */
const BookmarkManager = {
    // 存储键
    STORAGE_KEY: {
        BOOKMARKS: 'daodejing_bookmarks',
        NOTES: 'daodejing_notes',
        FAVORITES: 'daodejing_favorites'
    },

    // 数据
    bookmarks: {
        chapters: [],  // 章节书签
        passages: []   // 段落书签
    },
    notes: [],         // 笔记
    favorites: [],      // 收藏

    // 当前经典ID
    currentClassicId: 'ddj',

    /**
     * 初始化
     */
    init() {
        this.currentClassicId = this.getCurrentClassicId();
        this.loadFromStorage();
        this.setupUI();
        console.log('[BookmarkManager] 初始化完成', {
            classic: this.currentClassicId,
            bookmarks: this.bookmarks.chapters.length,
            notes: this.notes.length,
            favorites: this.favorites.length
        });
    },

    /**
     * 获取当前经典ID
     */
    getCurrentClassicId() {
        const path = window.location.pathname;
        const match = path.match(/\/([a-z]+)\//);
        if (match) return match[1];
        return 'ddj'; // 默认道德经
    },

    /**
     * 获取当前章节ID
     */
    getCurrentChapterId() {
        const path = window.location.pathname;
        const match = path.match(/\/chapter\/(\d+)/);
        if (match) return parseInt(match[1]);
        return null;
    },

    /**
     * 从 localStorage 加载数据
     */
    loadFromStorage() {
        try {
            // 加载书签
            const bookmarksData = localStorage.getItem(this.STORAGE_KEY.BOOKMARKS);
            this.bookmarks = bookmarksData ? JSON.parse(bookmarksData) : {
                chapters: [],
                passages: []
            };

            // 加载笔记
            const notesData = localStorage.getItem(this.STORAGE_KEY.NOTES);
            this.notes = notesData ? JSON.parse(notesData) : [];

            // 加载收藏
            const favoritesData = localStorage.getItem(this.STORAGE_KEY.FAVORITES);
            this.favorites = favoritesData ? JSON.parse(favoritesData) : [];
        } catch (error) {
            console.error('[BookmarkManager] 加载数据失败:', error);
        }
    },

    /**
     * 保存数据到 localStorage
     */
    saveToStorage() {
        try {
            localStorage.setItem(this.STORAGE_KEY.BOOKMARKS, JSON.stringify(this.bookmarks));
            localStorage.setItem(this.STORAGE_KEY.NOTES, JSON.stringify(this.notes));
            localStorage.setItem(this.STORAGE_KEY.FAVORITES, JSON.stringify(this.favorites));
        } catch (error) {
            console.error('[BookmarkManager] 保存数据失败:', error);
        }
    },

    /**
     * 设置UI
     */
    setupUI() {
        this.setupBookmarkButtons();
        this.setupNoteButtons();
        this.setupFavoriteButtons();
        this.setupModals();
    },

    /**
     * 设置书签按钮
     */
    setupBookmarkButtons() {
        const chapterId = this.getCurrentChapterId();
        if (!chapterId) return;

        const isBookmarked = this.bookmarks.chapters.includes(chapterId);

        // 创建或获取书签按钮
        let bookmarkBtn = document.getElementById('bookmarkBtn');
        if (!bookmarkBtn) {
            const cardHeader = document.querySelector('.card-header');
            if (!cardHeader) return;

            const btnGroup = cardHeader.querySelector('.btn-group');
            if (!btnGroup) return;

            bookmarkBtn = document.createElement('button');
            bookmarkBtn.id = 'bookmarkBtn';
            bookmarkBtn.className = 'btn btn-outline-secondary btn-sm';
            bookmarkBtn.type = 'button';
            bookmarkBtn.title = isBookmarked ? '取消书签' : '添加书签';
            bookmarkBtn.innerHTML = isBookmarked ? '★ 已收藏' : '☆ 收藏';
            btnGroup.appendChild(bookmarkBtn);
        } else {
            bookmarkBtn.innerHTML = isBookmarked ? '★ 已收藏' : '☆ 收藏';
            bookmarkBtn.className = isBookmarked ? 'btn btn-warning btn-sm' : 'btn btn-outline-secondary btn-sm';
        }

        // 绑定点击事件
        bookmarkBtn.onclick = () => this.toggleChapterBookmark(chapterId);
    },

    /**
     * 切换章节书签
     */
    toggleChapterBookmark(chapterId) {
        const index = this.bookmarks.chapters.indexOf(chapterId);
        if (index > -1) {
            this.bookmarks.chapters.splice(index, 1);
            this.showToast('已取消书签');
        } else {
            this.bookmarks.chapters.push(chapterId);
            this.showToast('已添加书签');
        }
        this.saveToStorage();
        this.setupBookmarkButtons();
        this.updateBookmarkCounts();
    },

    /**
     * 设置笔记按钮
     */
    setupNoteButtons() {
        const chapterId = this.getCurrentChapterId();
        if (!chapterId) return;

        const hasNote = this.notes.some(n => n.chapter === chapterId);

        // 创建或获取笔记按钮
        let noteBtn = document.getElementById('noteBtn');
        if (!noteBtn) {
            const cardHeader = document.querySelector('.card-header');
            if (!cardHeader) return;

            const btnGroup = cardHeader.querySelector('.btn-group');
            if (!btnGroup) return;

            noteBtn = document.createElement('button');
            noteBtn.id = 'noteBtn';
            noteBtn.className = 'btn btn-outline-secondary btn-sm';
            noteBtn.type = 'button';
            noteBtn.title = '添加笔记';
            noteBtn.innerHTML = '📝 笔记';
            btnGroup.appendChild(noteBtn);
        } else {
            noteBtn.innerHTML = hasNote ? '📝 已有笔记' : '📝 笔记';
            noteBtn.className = hasNote ? 'btn btn-info btn-sm' : 'btn btn-outline-secondary btn-sm';
        }

        // 绑定点击事件
        noteBtn.onclick = () => this.openNoteModal(chapterId);
    },

    /**
     * 设置收藏按钮
     */
    setupFavoriteButtons() {
        const chapterId = this.getCurrentChapterId();
        if (!chapterId) return;

        const isFavorite = this.favorites.some(f => f.chapter === chapterId);

        // 创建或获取收藏按钮
        let favoriteBtn = document.getElementById('favoriteBtn');
        if (!favoriteBtn) {
            const cardHeader = document.querySelector('.card-header');
            if (!cardHeader) return;

            const btnGroup = cardHeader.querySelector('.btn-group');
            if (!btnGroup) return;

            favoriteBtn = document.createElement('button');
            favoriteBtn.id = 'favoriteBtn';
            favoriteBtn.className = 'btn btn-outline-secondary btn-sm';
            favoriteBtn.type = 'button';
            favoriteBtn.title = isFavorite ? '取消收藏' : '添加收藏';
            favoriteBtn.innerHTML = isFavorite ? '❤️ 已收藏' : '🤍 收藏';
            btnGroup.appendChild(favoriteBtn);
        } else {
            favoriteBtn.innerHTML = isFavorite ? '❤️ 已收藏' : '🤍 收藏';
            favoriteBtn.className = isFavorite ? 'btn btn-danger btn-sm' : 'btn btn-outline-secondary btn-sm';
        }

        // 绑定点击事件
        favoriteBtn.onclick = () => this.toggleFavorite(chapterId);
    },

    /**
     * 切换收藏
     */
    toggleFavorite(chapterId) {
        const index = this.favorites.findIndex(f => f.chapter === chapterId);
        if (index > -1) {
            this.favorites.splice(index, 1);
            this.showToast('已取消收藏');
        } else {
            const chapterTitle = document.querySelector('.card-header h1')?.textContent || `第${chapterId}章`;
            this.favorites.push({
                chapter: chapterId,
                title: chapterTitle,
                classicId: this.currentClassicId,
                timestamp: Date.now()
            });
            this.showToast('已添加到收藏');
        }
        this.saveToStorage();
        this.setupFavoriteButtons();
        this.updateBookmarkCounts();
    },

    /**
     * 设置模态框
     */
    setupModals() {
        // 书签列表模态框
        let modal = document.getElementById('bookmarksModal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'bookmarksModal';
            modal.className = 'modal fade';
            modal.innerHTML = `
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">书签 & 收藏</h5>
                            <button type="button" class="btn-close" data-dismiss="modal">&times;</button>
                        </div>
                        <div class="modal-body">
                            <ul class="nav nav-tabs" id="bookmarkTabs">
                                <li class="nav-item">
                                    <a class="nav-link active" data-tab="bookmarks">章节书签</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" data-tab="favorites">收藏</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" data-tab="notes">笔记</a>
                                </li>
                            </ul>
                            <div id="bookmarkContent" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        // 笔记编辑模态框
        let noteModal = document.getElementById('noteModal');
        if (!noteModal) {
            noteModal = document.createElement('div');
            noteModal.id = 'noteModal';
            noteModal.className = 'modal fade';
            noteModal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">编辑笔记</h5>
                            <button type="button" class="btn-close" data-dismiss="noteModal">&times;</button>
                        </div>
                        <div class="modal-body">
                            <textarea id="noteContent" class="form-control" rows="8" placeholder="输入笔记内容..."></textarea>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="noteModal">取消</button>
                            <button type="button" class="btn btn-primary" id="saveNoteBtn">保存</button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(noteModal);
        }

        // 添加书签按钮到导航
        this.addBookmarksNavItem();

        // 绑定事件
        this.bindModalEvents(modal, noteModal);
    },

    /**
     * 添加书签菜单项到导航
     */
    addBookmarksNavItem() {
        const nav = document.querySelector('.navbar-nav');
        if (!nav) return;

        const existingItem = document.getElementById('bookmarksNavItem');
        if (existingItem) return;

        const li = document.createElement('li');
        li.className = 'nav-item';
        li.id = 'bookmarksNavItem';

        const count = this.bookmarks.chapters.length + this.favorites.length + this.notes.length;

        li.innerHTML = `
            <a class="nav-link" href="#" id="bookmarksTrigger">
                <span>📚 书签</span>
                <span class="badge bg-primary ms-1" id="bookmarksCount">${count}</span>
            </a>
        `;

        nav.appendChild(li);

        document.getElementById('bookmarksTrigger').addEventListener('click', (e) => {
            e.preventDefault();
            this.openBookmarksModal();
        });

        this.updateBookmarkCounts();
    },

    /**
     * 绑定模态框事件
     */
    bindModalEvents(modal, noteModal) {
        // 标签页切换
        modal.querySelectorAll('[data-tab]').forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                modal.querySelectorAll('[data-tab]').forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                this.renderTabContent(e.target.dataset.tab);
            });
        });

        // 关闭按钮
        modal.querySelectorAll('[data-dismiss="modal"]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeModals();
            });
        });

        // 笔记保存
        const saveNoteBtn = document.getElementById('saveNoteBtn');
        if (saveNoteBtn) {
            saveNoteBtn.addEventListener('click', () => {
                this.saveNote();
            });
        }

        // 笔记取消
        noteModal.querySelectorAll('[data-dismiss="noteModal"]').forEach(btn => {
            btn.addEventListener('click', () => {
                noteModal.classList.remove('show');
            });
        });
    },

    /**
     * 打开书签模态框
     */
    openBookmarksModal() {
        const modal = document.getElementById('bookmarksModal');
        if (modal) {
            this.renderTabContent('bookmarks');
            modal.classList.add('show');
            modal.style.display = 'block';
        }
    },

    /**
     * 关闭模态框
     */
    closeModals() {
        document.getElementById('bookmarksModal').classList.remove('show');
        document.getElementById('bookmarksModal').style.display = 'none';
        document.getElementById('noteModal').classList.remove('show');
    },

    /**
     * 渲染标签页内容
     */
    renderTabContent(tab) {
        const content = document.getElementById('bookmarkContent');
        if (!content) return;

        if (tab === 'bookmarks') {
            this.renderBookmarksList(content);
        } else if (tab === 'favorites') {
            this.renderFavoritesList(content);
        } else if (tab === 'notes') {
            this.renderNotesList(content);
        }
    },

    /**
     * 渲染书签列表
     */
    renderBookmarksList(container) {
        if (this.bookmarks.chapters.length === 0) {
            container.innerHTML = '<p class="text-center text-muted py-4">暂无书签</p>';
            return;
        }

        let html = '<div class="bookmarks-list">';
        this.bookmarks.chapters.forEach(chapter => {
            html += `
                <div class="bookmark-item d-flex justify-content-between align-items-center py-2 border-bottom">
                    <div>
                        <a href="/${this.currentClassicId}/chapter/${chapter}" class="text-decoration-none fw-bold">
                            第${chapter}章
                        </a>
                        <small class="text-muted d-block">书签章节</small>
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="BookmarkManager.removeBookmark(${chapter}, 'chapter')">
                        &times;
                    </button>
                </div>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
    },

    /**
     * 渲染收藏列表
     */
    renderFavoritesList(container) {
        if (this.favorites.length === 0) {
            container.innerHTML = '<p class="text-center text-muted py-4">暂无收藏</p>';
            return;
        }

        let html = '<div class="favorites-list">';
        this.favorites.forEach((fav, index) => {
            const date = new Date(fav.timestamp).toLocaleDateString('zh-CN');
            html += `
                <div class="favorite-item d-flex justify-content-between align-items-center py-2 border-bottom">
                    <div>
                        <a href="/${fav.classicId}/chapter/${fav.chapter}" class="text-decoration-none fw-bold">
                            ${fav.title || `第${fav.chapter}章`}
                        </a>
                        <small class="text-muted d-block">
                            ${fav.classicId} · ${date}
                        </small>
                    </div>
                    <button class="btn btn-sm btn-outline-danger" onclick="BookmarkManager.removeFavorite(${index})">
                        &times;
                    </button>
                </div>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
    },

    /**
     * 渲染笔记列表
     */
    renderNotesList(container) {
        if (this.notes.length === 0) {
            container.innerHTML = '<p class="text-center text-muted py-4">暂无笔记</p>';
            return;
        }

        let html = '<div class="notes-list">';
        this.notes.forEach((note, index) => {
            const date = new Date(note.timestamp).toLocaleString('zh-CN');
            html += `
                <div class="note-item py-3 border-bottom">
                    <div class="d-flex justify-content-between">
                        <div>
                            <a href="/${note.classicId}/chapter/${note.chapter}" class="text-decoration-none fw-bold">
                                第${note.chapter}章
                            </a>
                            <small class="text-muted d-block">${date}</small>
                        </div>
                        <button class="btn btn-sm btn-outline-danger" onclick="BookmarkManager.removeNote(${index})">
                            &times;
                        </button>
                    </div>
                    <p class="mt-2 small">${this.escapeHtml(note.content)}</p>
                </div>
            `;
        });
        html += '</div>';
        container.innerHTML = html;
    },

    /**
     * 移除书签
     */
    removeBookmark(id, type) {
        if (type === 'chapter') {
            const index = this.bookmarks.chapters.indexOf(id);
            if (index > -1) {
                this.bookmarks.chapters.splice(index, 1);
                this.saveToStorage();
                this.showToast('已删除书签');
                this.renderTabContent('bookmarks');
                this.updateBookmarkCounts();
            }
        }
    },

    /**
     * 移除收藏
     */
    removeFavorite(index) {
        this.favorites.splice(index, 1);
        this.saveToStorage();
        this.showToast('已删除收藏');
        this.renderTabContent('favorites');
        this.updateBookmarkCounts();
    },

    /**
     * 移除笔记
     */
    removeNote(index) {
        this.notes.splice(index, 1);
        this.saveToStorage();
        this.showToast('已删除笔记');
        this.renderTabContent('notes');
        this.updateBookmarkCounts();
    },

    /**
     * 打开笔记编辑模态框
     */
    openNoteModal(chapterId) {
        const existingNote = this.notes.find(n => n.chapter === chapterId);
        const modal = document.getElementById('noteModal');
        const textarea = document.getElementById('noteContent');

        if (modal && textarea) {
            textarea.value = existingNote ? existingNote.content : '';
            textarea.dataset.chapter = chapterId;
            modal.classList.add('show');
            modal.style.display = 'block';
        }
    },

    /**
     * 保存笔记
     */
    saveNote() {
        const textarea = document.getElementById('noteContent');
        if (!textarea) return;

        const chapterId = parseInt(textarea.dataset.chapter);
        const content = textarea.value.trim();

        if (!content) {
            this.showToast('笔记内容不能为空');
            return;
        }

        // 查找或创建笔记
        const existingIndex = this.notes.findIndex(n => n.chapter === chapterId);
        const chapterTitle = document.querySelector('.card-header h1')?.textContent || `第${chapterId}章`;

        if (existingIndex > -1) {
            // 更新现有笔记
            this.notes[existingIndex] = {
                chapter: chapterId,
                classicId: this.currentClassicId,
                title: chapterTitle,
                content: content,
                timestamp: Date.now()
            };
        } else {
            // 创建新笔记
            this.notes.push({
                chapter: chapterId,
                classicId: this.currentClassicId,
                title: chapterTitle,
                content: content,
                timestamp: Date.now()
            });
        }

        this.saveToStorage();
        this.showToast('笔记已保存');
        this.closeModals();
        this.setupNoteButtons();
        this.updateBookmarkCounts();
    },

    /**
     * 更新书签计数
     */
    updateBookmarkCounts() {
        const count = this.bookmarks.chapters.length + this.favorites.length + this.notes.length;
        const badge = document.getElementById('bookmarksCount');
        if (badge) {
            badge.textContent = count;
        }
    },

    /**
     * HTML转义
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    /**
     * 显示提示
     */
    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast show';
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 12px 24px;
            border-radius: 4px;
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 2000);
    },

    /**
     * 获取数据统计
     */
    getStats() {
        return {
            bookmarks: this.bookmarks.chapters.length,
            favorites: this.favorites.length,
            notes: this.notes.length
        };
    }
};

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    .modal {
        display: none;
        background: rgba(0, 0, 0, 0.5);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 1050;
        overflow-y: auto;
    }
    .modal.show {
        display: block !important;
    }
    .modal-dialog {
        background: white;
        margin: 50px auto;
        border-radius: 8px;
        max-width: 600px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .bookmark-item, .favorite-item, .note-item {
        transition: background 0.2s;
    }
    .bookmark-item:hover, .favorite-item:hover, .note-item:hover {
        background: #f8f9fa;
    }
    .nav-link[data-tab] {
        cursor: pointer;
    }
    .nav-link[data-tab].active {
        background: var(--accent-color) !important;
        color: white !important;
    }
`;
document.head.appendChild(style);

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BookmarkManager;
}
