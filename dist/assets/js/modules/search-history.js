/**
 * 搜索历史管理器
 * 管理用户的搜索历史记录（使用 localStorage）
 */
const SearchHistoryManager = {
    STORAGE_KEY: 'daodejing_search_history',
    MAX_HISTORY: 50,

    /**
     * 获取搜索历史
     * @returns {Array} 搜索历史数组
     */
    getHistory() {
        try {
            const history = localStorage.getItem(this.STORAGE_KEY);
            return history ? JSON.parse(history) : [];
        } catch (e) {
            console.error('[SearchHistory] 获取搜索历史失败:', e);
            return [];
        }
    },

    /**
     * 保存搜索记录
     * @param {string} query - 搜索查询词
     * @param {Object} filters - 搜索过滤器
     */
    addSearch(query, filters = {}) {
        if (!query || !query.trim()) return;

        try {
            let history = this.getHistory();

            // 移除重复项（相同查询词和过滤器）
            history = history.filter(item => {
                const sameQuery = item.query === query;
                const sameFilters = JSON.stringify(item.filters) === JSON.stringify(filters);
                return !(sameQuery && sameFilters);
            });

            // 添加到开头
            history.unshift({
                query: query.trim(),
                filters: filters,
                timestamp: Date.now()
            });

            // 限制数量
            if (history.length > this.MAX_HISTORY) {
                history = history.slice(0, this.MAX_HISTORY);
            }

            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(history));
            console.log('[SearchHistory] 搜索历史已保存:', query);
        } catch (e) {
            console.error('[SearchHistory] 保存搜索历史失败:', e);
        }
    },

    /**
     * 清空搜索历史
     */
    clearHistory() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            console.log('[SearchHistory] 搜索历史已清空');
            return true;
        } catch (e) {
            console.error('[SearchHistory] 清空搜索历史失败:', e);
            return false;
        }
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
    module.exports = SearchHistoryManager;
}

if (typeof window !== 'undefined') {
    window.SearchHistoryManager = SearchHistoryManager;
}
