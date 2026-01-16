/**
 * 道德经应用入口
 * 初始化所有功能模块
 */

(function() {
    'use strict';

    // 等待 DOM 加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        // 初始化各模块
        if (typeof ThemeManager !== 'undefined') ThemeManager.init();
        if (typeof SidebarManager !== 'undefined') SidebarManager.init();
        if (typeof MusicManager !== 'undefined') MusicManager.init();

        // 初始化其他功能（如果定义了的话）
        if (typeof SearchManager !== 'undefined') SearchManager.init();
        if (typeof SpeechManager !== 'undefined') SpeechManager.init();
        if (typeof SettingsManager !== 'undefined') SettingsManager.init();
        if (typeof KeyboardNavigation !== 'undefined') KeyboardNavigation.init();
        if (typeof ShareManager !== 'undefined') ShareManager.init();
        if (typeof AIManager !== 'undefined') AIManager.init();
    }

    // 导出到全局（用于模块化后的向后兼容）
    window.DaoDeJingApp = {
        init,
        ThemeManager,
        SidebarManager,
        MusicManager,
        // 添加其他模块...
    };
})();
