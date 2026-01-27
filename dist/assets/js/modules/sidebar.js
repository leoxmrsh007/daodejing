/**
 * 侧边栏管理模块
 * 移动端侧边栏切换
 */

const SidebarManager = {
    init() {
        this.sidebar = document.getElementById('sidebar');
        this.toggleBtn = document.getElementById('sidebarToggle');
        this.overlay = document.getElementById('sidebarOverlay');

        if (!this.sidebar || !this.toggleBtn) return;

        // 如果没有overlay，创建一个
        if (!this.overlay) {
            this.createOverlay();
        }

        this.bindEvents();
    },

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'sidebar-overlay';
        this.overlay.id = 'sidebarOverlay';
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
    },

    open() {
        this.sidebar.classList.add('show');
        this.overlay.classList.add('show');
    }
};

// 导出模块（兼容多种模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SidebarManager;
}

// 自动初始化
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => SidebarManager.init());
    } else {
        SidebarManager.init();
    }
    window.SidebarManager = SidebarManager;
}
