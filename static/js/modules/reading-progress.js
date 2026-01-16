/**
 * 阅读进度管理模块
 * 保存阅读位置、自动恢复
 */

const ReadingProgress = {
    STORAGE_KEY: 'daodejing_reading_progress',
    SAVE_INTERVAL: 5000, // 5秒保存一次

    init() {
        this.currentChapter = null;
        this.scrollPosition = 0;
        this.saveTimer = null;

        // 获取当前章节号
        this.detectChapter();

        // 恢复上次阅读位置
        this.restoreProgress();

        // 监听滚动事件（带节流）
        this.setupScrollTracking();

        // 监听页面离开事件
        window.addEventListener('beforeunload', () => this.saveProgress());
    },

    detectChapter() {
        // 从URL或面包屑获取章节号
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            if (match) {
                this.currentChapter = parseInt(match[1]);
            }
        }

        // 从URL路径获取
        if (!this.currentChapter) {
            const pathMatch = window.location.pathname.match(/\/chapter\/?(\d+)/);
            if (pathMatch) {
                this.currentChapter = parseInt(pathMatch[1]);
            }
        }
    },

    setupScrollTracking() {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    this.updateScrollPosition();
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    },

    updateScrollPosition() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        this.scrollPosition = scrollTop / docHeight; // 0-1 之间

        // 定期保存
        if (!this.saveTimer) {
            this.saveTimer = setTimeout(() => {
                this.saveProgress();
                this.saveTimer = null;
            }, this.SAVE_INTERVAL);
        }
    },

    saveProgress() {
        if (!this.currentChapter) return;

        const progress = {
            chapter: this.currentChapter,
            scrollPosition: this.scrollPosition,
            timestamp: Date.now()
        };

        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(progress));
    },

    restoreProgress() {
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (!saved) return;

        try {
            const progress = JSON.parse(saved);

            // 如果是在同一章节，恢复滚动位置
            if (progress.chapter === this.currentChapter) {
                if (progress.scrollPosition > 0 && progress.scrollPosition < 0.95) {
                    // 延迟恢复，等待页面完全加载
                    setTimeout(() => {
                        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                        const scrollTop = progress.scrollPosition * docHeight;
                        window.scrollTo({
                            top: scrollTop,
                            behavior: 'smooth'
                        });
                    }, 500);
                }
            }
        } catch (e) {
            console.error('恢复阅读进度失败:', e);
        }
    },

    getProgress() {
        const saved = localStorage.getItem(this.STORAGE_KEY);
        if (!saved) return null;

        try {
            return JSON.parse(saved);
        } catch (e) {
            return null;
        }
    },

    clearProgress() {
        localStorage.removeItem(this.STORAGE_KEY);
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReadingProgress;
}
