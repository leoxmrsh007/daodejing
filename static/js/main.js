/**
 * 道德经多版本对照平台 - 主脚本文件
 * 功能：暗黑模式切换、侧边栏、搜索、键盘导航
 */

(function() {
    'use strict';

    // ==================== 暗黑模式管理 ====================
    const ThemeManager = {
        STORAGE_KEY: 'daodejing_theme',
        ICONS: {
            light: '☀️',
            dark: '🌙'
        },

        init() {
            this.themeToggle = document.getElementById('themeToggle');
            if (!this.themeToggle) return;

            // 加载保存的主题
            const savedTheme = localStorage.getItem(this.STORAGE_KEY);
            if (savedTheme) {
                this.setTheme(savedTheme);
            } else {
                // 自动检测系统偏好
                this.detectSystemTheme();
            }

            // 绑定切换事件
            this.themeToggle.addEventListener('click', () => this.toggle());

            // 监听系统主题变化
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
                if (!localStorage.getItem(this.STORAGE_KEY)) {
                    this.detectSystemTheme();
                }
            });
        },

        detectSystemTheme() {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.setTheme(prefersDark ? 'dark' : 'light');
        },

        toggle() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            this.setTheme(newTheme);
        },

        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem(this.STORAGE_KEY, theme);
            this.updateIcon();
        },

        updateIcon() {
            const icon = this.themeToggle.querySelector('.theme-icon');
            const currentTheme = document.documentElement.getAttribute('data-theme');
            icon.textContent = currentTheme === 'dark' ? this.ICONS.dark : this.ICONS.light;
        }
    };

    // ==================== 侧边栏管理 ====================
    const SidebarManager = {
        init() {
            this.sidebar = document.getElementById('sidebar');
            this.toggleBtn = document.getElementById('sidebarToggle');
            this.overlay = null;

            if (!this.sidebar || !this.toggleBtn) return;

            this.createOverlay();
            this.bindEvents();
        },

        createOverlay() {
            this.overlay = document.createElement('div');
            this.overlay.className = 'sidebar-overlay';
            document.body.appendChild(this.overlay);
        },

        bindEvents() {
            // 打开/关闭侧边栏
            this.toggleBtn.addEventListener('click', () => this.toggle());

            // 点击遮罩关闭
            this.overlay.addEventListener('click', () => this.close());

            // 选择章节后自动关闭（移动端）
            const chapterLinks = this.sidebar.querySelectorAll('.chapter-item');
            chapterLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth < 992) {
                        this.close();
                    }
                });
            });

            // 窗口大小改变时重置
            window.addEventListener('resize', () => {
                if (window.innerWidth >= 992) {
                    this.sidebar.classList.remove('show');
                    this.overlay.classList.remove('show');
                }
            });
        },

        toggle() {
            this.sidebar.classList.toggle('show');
            this.overlay.classList.toggle('show');
        },

        close() {
            this.sidebar.classList.remove('show');
            this.overlay.classList.remove('show');
        }
    };

    // ==================== 搜索功能 ====================
    const SearchManager = {
        API_ENDPOINT: '/api/daodejing/search',
        DEBOUNCE_DELAY: 300,

        init() {
            this.searchInput = document.getElementById('searchInput');
            this.searchModal = document.getElementById('searchModal');
            this.searchResults = document.getElementById('searchResults');
            this.debounceTimer = null;

            if (!this.searchInput) return;

            this.bindEvents();
        },

        bindEvents() {
            // 输入事件（带防抖）
            this.searchInput.addEventListener('input', (e) => {
                clearTimeout(this.debounceTimer);
                this.debounceTimer = setTimeout(() => {
                    this.search(e.target.value);
                }, this.DEBOUNCE_DELAY);
            });

            // 回车键直接搜索
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    clearTimeout(this.debounceTimer);
                    this.search(e.target.value);
                    this.showModal();
                }
            });

            // Escape 键清空
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.searchInput.value = '';
                    this.searchInput.blur();
                }
            });
        },

        async search(query) {
            if (!query || query.trim().length < 1) {
                return;
            }

            try {
                const response = await fetch(`${this.API_ENDPOINT}?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                this.displayResults(data.results);
                if (data.results.length > 0) {
                    this.showModal();
                }
            } catch (error) {
                console.error('搜索失败:', error);
            }
        },

        displayResults(results) {
            if (results.length === 0) {
                this.searchResults.innerHTML = '<p class="text-muted text-center">未找到相关内容</p>';
                return;
            }

            this.searchResults.innerHTML = results.map(result => `
                <div class="search-result-item" onclick="location.href='/daodejing/chapter/${result.id}'">
                    <h6 class="mb-1">${result.title}</h6>
                    <p class="small text-muted mb-0">${result.excerpt}</p>
                </div>
            `).join('');
        },

        showModal() {
            if (!this.searchModal) return;
            const modal = new bootstrap.Modal(this.searchModal);
            modal.show();
        }
    };

    // ==================== 滚动高亮目录 ====================
    const ScrollHighlight = {
        init() {
            this.sidebar = document.getElementById('sidebar');
            this.chapterItems = document.querySelectorAll('.chapter-item');

            if (this.chapterItems.length === 0) return;

            // 使用 Intersection Observer
            this.setupObserver();
        },

        setupObserver() {
            const options = {
                root: null,
                rootMargin: '-20% 0px -60% 0px',
                threshold: 0
            };

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.dataset.chapter;
                        this.highlightChapter(id);
                    }
                });
            }, options);

            // 观察所有章节内容
            document.querySelectorAll('.original-text, .original-section').forEach(el => {
                this.observer.observe(el);
            });
        },

        highlightChapter(chapterId) {
            this.chapterItems.forEach(item => {
                item.classList.remove('active');
                if (item.dataset.chapter == chapterId) {
                    item.classList.add('active');
                    // 滚动目录到可见区域
                    item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        }
    };

    // ==================== 初始化 ====================
    document.addEventListener('DOMContentLoaded', () => {
        ThemeManager.init();
        SidebarManager.init();
        SearchManager.init();
        ScrollHighlight.init();

        // 初始化疑难字 tooltip，增加偏移避免重叠
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                delay: { show: 300, hide: 150 },
                placement: 'top',
                offset: [0, 8],
                boundary: 'window',
                fallbackPlacements: ['top', 'bottom']
            });
        });
    });

})();
