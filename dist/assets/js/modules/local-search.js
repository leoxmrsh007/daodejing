/**
 * 本地搜索模块
 * 支持静态版本的客户端搜索
 */

const LocalSearchManager = {
    searchData: null,
    searchIndex: null,

    init() {
        this.searchInput = document.getElementById('searchInput');
        this.searchModal = document.getElementById('searchModal');
        this.searchResults = document.getElementById('searchResults');

        if (!this.searchInput) return;

        // 加载搜索数据
        this.loadSearchData();

        // 绑定事件
        this.bindEvents();
    },

    loadSearchData() {
        // 检查是否有嵌入的搜索数据
        if (typeof WINDOW_SEARCH_DATA !== 'undefined') {
            this.searchData = WINDOW_SEARCH_DATA;
            this.buildSearchIndex();
            console.log('[LocalSearch] 加载了嵌入的搜索数据');
            return;
        }

        // 尝试从页面中提取章节数据
        this.extractChapterData();
    },

    extractChapterData() {
        // 从当前页面的章节列表中提取数据
        const chapterLinks = document.querySelectorAll('.chapter-item');
        if (chapterLinks.length > 0) {
            this.searchData = {
                chapters: Array.from(chapterLinks).map((link, index) => ({
                    id: index + 1,
                    title: link.querySelector('.chapter-num')?.textContent || `第${index + 1}章`,
                    url: link.getAttribute('href')
                }))
            };
            console.log('[LocalSearch] 从页面提取了章节数据');
        }
    },

    buildSearchIndex() {
        if (!this.searchData || !this.searchData.chapters) return;

        this.searchIndex = this.searchData.chapters.map(ch => ({
            id: ch.id,
            title: ch.title,
            url: ch.url,
            content: (ch.content || '').toLowerCase(),
            original: (ch.original || '').toLowerCase(),
            translation: (ch.translation || '').toLowerCase()
        }));
    },

    bindEvents() {
        let searchTimeout;

        // 搜索输入
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();

            if (query.length < 2) {
                this.hideResults();
                return;
            }

            searchTimeout = setTimeout(() => {
                this.performSearch(query);
            }, 300);
        });

        // 回车键
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const query = this.searchInput.value.trim();
                if (query.length >= 2) {
                    this.performSearch(query);
                }
            }
            if (e.key === 'Escape') {
                this.hideResults();
                this.searchInput.blur();
            }
        });

        // 点击外部关闭
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-box') && !e.target.closest('#searchModal')) {
                this.hideResults();
            }
        });
    },

    performSearch(query) {
        if (!this.searchIndex) {
            this.showNoDataMessage();
            return;
        }

        const queryLower = query.toLowerCase();
        const results = [];

        for (const chapter of this.searchIndex) {
            // 搜索章节号
            if (queryLower.includes(chapter.id.toString())) {
                results.push({
                    ...chapter,
                    matchType: 'chapter',
                    score: 100
                });
                continue;
            }

            // 搜索原文
            if (chapter.original && chapter.original.includes(queryLower)) {
                results.push({
                    ...chapter,
                    matchType: 'original',
                    score: this.calculateScore(chapter.original, queryLower)
                });
                continue;
            }

            // 搜索译文
            if (chapter.translation && chapter.translation.includes(queryLower)) {
                results.push({
                    ...chapter,
                    matchType: 'translation',
                    score: this.calculateScore(chapter.translation, queryLower)
                });
                continue;
            }
        }

        // 按相关度排序
        results.sort((a, b) => b.score - a.score);

        // 限制结果数量
        const limitedResults = results.slice(0, 20);

        this.displayResults(limitedResults, query);
    },

    calculateScore(text, query) {
        let score = 0;
        const words = query.split(/\s+/);

        for (const word of words) {
            // 精确匹配得分更高
            if (text === word) {
                score += 50;
            } else if (text.includes(word)) {
                // 计算出现次数
                const count = (text.match(new RegExp(word, 'g')) || []).length;
                score += count * 10;

                // 词首匹配加分
                if (text.startsWith(word)) {
                    score += 5;
                }
            }
        }

        return score;
    },

    displayResults(results, query) {
        if (!this.searchResults) {
            // 创建搜索结果容器
            this.createResultsContainer();
        }

        if (results.length === 0) {
            this.searchResults.innerHTML = `
                <div class="text-center text-muted py-4">
                    <p>未找到与"<strong>${this.escapeHtml(query)}</strong>"相关的内容</p>
                    <small>请尝试其他关键词</small>
                </div>
            `;
        } else {
            this.searchResults.innerHTML = `
                <div class="search-results-count mb-2">
                    找到 <strong>${results.length}</strong> 个结果
                </div>
                <div class="list-group list-group-flush">
                    ${results.map(result => this.renderResultItem(result, query)).join('')}
                </div>
            `;
        }

        this.showResults();
    },

    renderResultItem(result, query) {
        const matchLabel = {
            'chapter': '章节匹配',
            'original': '原文匹配',
            'translation': '译文匹配'
        }[result.matchType] || '匹配';

        return `
            <a href="${result.url}" class="list-group-item list-group-item-action search-result-item">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1">${this.highlightText(result.title, query)}</h6>
                        ${result.excerpt ? `<p class="mb-1 text-muted small">${this.highlightText(result.excerpt, query)}</p>` : ''}
                    </div>
                    <span class="badge bg-secondary">${matchLabel}</span>
                </div>
            </a>
        `;
    },

    highlightText(text, query) {
        const words = query.split(/\s+/).filter(w => w.length > 0);
        let highlighted = this.escapeHtml(text);

        for (const word of words) {
            const regex = new RegExp(`(${this.escapeRegex(word)})`, 'gi');
            highlighted = highlighted.replace(regex, '<mark>$1</mark>');
        }

        return highlighted;
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    },

    createResultsContainer() {
        if (!this.searchResults) {
            // 创建模态框用于显示搜索结果
            const modalHtml = `
                <div class="modal fade" id="searchModal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-scrollable modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">搜索结果</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body" id="searchResults">
                                搜索结果将在这里显示
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            this.searchModal = document.getElementById('searchModal');
            this.searchResults = document.getElementById('searchResults');
        }
    },

    showResults() {
        if (this.searchModal) {
            const modal = new bootstrap.Modal(this.searchModal);
            modal.show();
        }
    },

    hideResults() {
        if (this.searchModal) {
            const modal = bootstrap.Modal.getInstance(this.searchModal);
            if (modal) {
                modal.hide();
            }
        }
    },

    showNoDataMessage() {
        if (!this.searchResults) {
            this.createResultsContainer();
        }
        this.searchResults.innerHTML = `
            <div class="text-center text-muted py-4">
                <p>搜索数据未加载</p>
                <small>请刷新页面重试</small>
            </div>
        `;
        this.showResults();
    }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LocalSearchManager;
}

// 自动初始化
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => LocalSearchManager.init());
    } else {
        LocalSearchManager.init();
    }
    window.LocalSearchManager = LocalSearchManager;
}
