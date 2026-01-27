/**
 * 主题管理模块
 * 暗黑模式切换、系统主题检测
 */

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

// 导出模块（兼容多种模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}

// 自动初始化
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => ThemeManager.init());
    } else {
        ThemeManager.init();
    }
    window.ThemeManager = ThemeManager;
}
