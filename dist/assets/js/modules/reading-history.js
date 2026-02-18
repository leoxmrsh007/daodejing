/**
 * 阅读历史管理器
 * 管理用户的阅读历史，用于个性化推荐
 */
const ReadingHistoryManager = {
    STORAGE_KEY: 'daodejing_reading_history',
    MAX_HISTORY: 100,

    /**
     * 获取阅读历史
     * @returns {Array} 阅读历史数组
     */
    getHistory() {
        try {
            const history = localStorage.getItem(this.STORAGE_KEY);
            return history ? JSON.parse(history) : [];
        } catch (e) {
            console.error('[ReadingHistory] 获取阅读历史失败:', e);
            return [];
        }
    },

    /**
     * 记录章节阅读
     * @param {string} classicId - 经典ID
     * @param {number} chapterId - 章节ID
     * @param {string} chapterTitle - 章节标题
     */
    recordChapter(classicId, chapterId, chapterTitle) {
        if (!classicId || !chapterId) return;

        try {
            let history = this.getHistory();

            // 移除重复项（同一经典和章节）
            history = history.filter(item => {
                return !(item.classic_id === classicId && item.chapter_id === chapterId);
            });

            // 添加到开头
            history.unshift({
                classic_id: classicId,
                chapter_id: chapterId,
                title: chapterTitle || `第${chapterId}章`,
                timestamp: Date.now()
            });

            // 限制数量
            if (history.length > this.MAX_HISTORY) {
                history = history.slice(0, this.MAX_HISTORY);
            }

            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(history));
            console.log('[ReadingHistory] 阅读历史已记录:', classicId, chapterId);
        } catch (e) {
            console.error('[ReadingHistory] 记录阅读历史失败:', e);
        }
    },

    /**
     * 清空阅读历史
     */
    clearHistory() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            console.log('[ReadingHistory] 阅读历史已清空');
            return true;
        } catch (e) {
            console.error('[ReadingHistory] 清空阅读历史失败:', e);
            return false;
        }
    },

    /**
     * 获取推荐参数（用于API请求）
     * @returns {Array} 推荐参数数组
     */
    getRecommendationParams() {
        const history = this.getHistory();
        return history.slice(0, 20).map(item => ({
            classic_id: item.classic_id,
            chapter_id: item.chapter_id
        }));
    },

    /**
     * 格式化时间戳为相对时间
     * @param {number} timestamp - Unix 时间戳
     * @returns {string} 格式化的时间字符串
     */
    formatTime(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;

        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (seconds < 60) return '刚刚';
        if (minutes < 60) return `${minutes}分钟前`;
        if (hours < 24) return `${hours}小时前`;
        if (days < 7) return `${days}天前`;
        if (days < 30) return `${Math.floor(days / 7)}周前`;
        if (days < 365) return `${Math.floor(days / 30)}个月前`;
        return `${Math.floor(days / 365)}年前`;
    }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ReadingHistoryManager;
}

if (typeof window !== 'undefined') {
    window.ReadingHistoryManager = ReadingHistoryManager;
}
