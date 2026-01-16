/**
 * 书签管理模块
 * 标记重要段落、章节
 */

const BookmarkManager = {
    STORAGE_KEY: 'daodejing_bookmarks',

    init() {
        this.bookmarks = this.loadBookmarks();
        this.setupBookmarkButtons();
    },

    loadBookmarks() {
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                return { chapters: [], passages: [] };
            }
        }
        return { chapters: [], passages: [] };
    },

    saveBookmarks() {
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.bookmarks));
    },

    setupBookmarkButtons() {
        // 为每章添加书签按钮
        const chapterNum = this.getCurrentChapter();
        if (!chapterNum) return;

        // 检查当前章节是否已加书签
        const isBookmarked = this.bookmarks.chapters.includes(chapterNum);

        // 创建或更新书签按钮
        let bookmarkBtn = document.getElementById('bookmarkBtn');
        if (!bookmarkBtn) {
            // 在页面头部添加书签按钮
            const cardHeader = document.querySelector('.card-header');
            if (cardHeader) {
                const btnGroup = cardHeader.querySelector('.btn-group');
                if (btnGroup) {
                    bookmarkBtn = document.createElement('button');
                    bookmarkBtn.id = 'bookmarkBtn';
                    bookmarkBtn.className = 'btn btn-outline-secondary btn-sm';
                    bookmarkBtn.type = 'button';
                    bookmarkBtn.title = isBookmarked ? '取消书签' : '添加书签';
                    bookmarkBtn.innerHTML = isBookmarked ? '★ 已收藏' : '☆ 收藏';
                    btnGroup.appendChild(bookmarkBtn);
                }
            }
        }

        if (bookmarkBtn) {
            bookmarkBtn.innerHTML = isBookmarked ? '★ 已收藏' : '☆ 收藏';
            bookmarkBtn.className = isBookmarked
                ? 'btn btn-warning btn-sm'
                : 'btn btn-outline-secondary btn-sm';

            bookmarkBtn.onclick = () => this.toggleChapterBookmark(chapterNum);
        }

        // 显示所有书签
        this.displayBookmarksList();
    },

    getCurrentChapter() {
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            if (match) return parseInt(match[1]);
        }
        return null;
    },

    toggleChapterBookmark(chapter) {
        const index = this.bookmarks.chapters.indexOf(chapter);
        if (index > -1) {
            // 移除书签
            this.bookmarks.chapters.splice(index, 1);
        } else {
            // 添加书签
            this.bookmarks.chapters.push(chapter);
        }
        this.saveBookmarks();
        this.setupBookmarkButtons();
    },

    addPassageBookmark(chapter, text, position) {
        const passage = {
            chapter,
            text: text.substring(0, 50) + '...',
            position,
            timestamp: Date.now()
        };
        this.bookmarks.passages.push(passage);
        this.saveBookmarks();
    },

    removePassageBookmark(index) {
        this.bookmarks.passages.splice(index, 1);
        this.saveBookmarks();
        this.displayBookmarksList();
    },

    displayBookmarksList() {
        let container = document.getElementById('bookmarksList');
        if (!container) return;

        if (this.bookmarks.chapters.length === 0 && this.bookmarks.passages.length === 0) {
            container.innerHTML = '<p class="text-muted">暂无书签</p>';
            return;
        }

        let html = '<div class="bookmarks-chapters mb-3">';
        html += '<h6>书签章节</h6>';
        html += '<div class="d-flex flex-wrap gap-2">';

        this.bookmarks.chapters.forEach(ch => {
            html += `<a href="/daodejing/chapter/${ch}" class="badge bg-primary">第${ch}章</a>`;
        });

        html += '</div></div>';

        if (this.bookmarks.passages.length > 0) {
            html += '<div class="bookmarks-passages">';
            html += '<h6>书签段落</h6>';
            html += '<ul class="list-group">';

            this.bookmarks.passages.forEach((passage, index) => {
                html += `<li class="list-group-item">
                    <a href="/daodejing/chapter/${passage.chapter}" class="text-decoration-none">
                        第${passage.chapter}章
                    </a>
                    <small class="d-block text-muted">${passage.text}</small>
                    <button class="btn btn-sm btn-link text-danger p-0" onclick="BookmarkManager.removePassageBookmark(${index})">
                        删除
                    </button>
                </li>`;
            });

            html += '</ul></div>';
        }

        container.innerHTML = html;
    },

    getBookmarks() {
        return this.bookmarks;
    },

    clearAll() {
        if (confirm('确定要清空所有书签吗？')) {
            this.bookmarks = { chapters: [], passages: [] };
            this.saveBookmarks();
            this.setupBookmarkButtons();
        }
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = BookmarkManager;
}
