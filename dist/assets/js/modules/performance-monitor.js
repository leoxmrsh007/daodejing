/**
 * 性能监控工具
 * 用于监控和分析前端性能指标
 */

const PerformanceMonitor = {
    // 性能数据
    metrics: {
        startTime: 0,
        marks: {},
        measures: {},
        resources: []
    },

    // 配置
    config: {
        enabled: true,
        reportEndpoint: '/api/analytics/performance',
        reportInterval: 30000, // 30秒
        slowThreshold: 1000, // 1秒
        criticalThreshold: 3000 // 3秒
    },

    /**
     * 初始化性能监控
     */
    init() {
        if (!this.config.enabled) return;

        this.metrics.startTime = performance.now();

        // 监听页面加载事件
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.onDOMContentLoaded());
        } else {
            this.onDOMContentLoaded();
        }

        window.addEventListener('load', () => this.onLoad());

        // 定期上报数据
        setInterval(() => this.reportMetrics(), this.config.reportInterval);
    },

    /**
     * DOM 加载完成
     */
    onDOMContentLoaded() {
        this.mark('DOMContentLoaded');
        console.log('[Performance] DOMContentLoaded:', this.getMark('DOMContentLoaded'), 'ms');
    },

    /**
     * 页面完全加载
     */
    onLoad() {
        this.mark('load');
        this.measure('pageLoad', 'start', 'load');

        // 获取关键资源加载时间
        this.measureResources();

        // 获取 Web Vitals
        this.getWebVitals();

        console.log('[Performance] Page Load:', this.getMeasure('pageLoad'), 'ms');
        console.log('[Performance] Total Metrics:', this.getMetrics());
    },

    /**
     * 标记时间点
     */
    mark(name) {
        if (window.performance) {
            performance.mark(name);
            this.metrics.marks[name] = performance.now() - this.metrics.startTime;
        }
    },

    /**
     * 测量两个时间点之间的时间
     */
    measure(name, startMark, endMark) {
        if (window.performance) {
            try {
                performance.measure(name, startMark, endMark);
                const entry = performance.getEntriesByName(name)[0];
                if (entry) {
                    this.metrics.measures[name] = entry.duration;

                    // 慢操作警告
                    if (entry.duration > this.config.criticalThreshold) {
                        console.error(`[Performance] CRITICAL: ${name} took ${entry.duration.toFixed(2)}ms`);
                    } else if (entry.duration > this.config.slowThreshold) {
                        console.warn(`[Performance] SLOW: ${name} took ${entry.duration.toFixed(2)}ms`);
                    }
                }
            } catch (e) {
                console.warn('[Performance] Measure failed:', name, e.message);
            }
        }
    },

    /**
     * 测量资源加载时间
     */
    measureResources() {
        const resources = performance.getEntriesByType('resource');
        this.metrics.resources = resources.map(r => ({
            name: this.shortenUrl(r.name),
            duration: r.duration,
            size: r.transferSize,
            type: r.initiatorType
        }));

        // 找出慢资源
        const slowResources = resources
            .filter(r => r.duration > this.config.slowThreshold)
            .map(r => ({
                name: this.shortenUrl(r.name),
                duration: r.duration.toFixed(2)
            }));

        if (slowResources.length > 0) {
            console.warn('[Performance] Slow resources:', slowResources);
        }
    },

    /**
     * 获取 Web Vitals
     */
    getWebVitals() {
        // First Contentful Paint (FCP)
        const paintEntries = performance.getEntriesByType('paint');
        const fcp = paintEntries.find(e => e.name === 'first-contentful-paint');
        if (fcp) {
            this.metrics.fcp = fcp.startTime;
            console.log('[Performance] FCP:', fcp.startTime.toFixed(2), 'ms');
        }

        // Largest Contentful Paint (LCP)
        this.observeLCP();

        // First Input Delay (FID)
        this.observeFID();

        // Cumulative Layout Shift (CLS)
        this.observeCLS();
    },

    /**
     * 观察 LCP
     */
    observeLCP() {
        if (!('PerformanceObserver' in window)) return;

        try {
            const lcpObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.metrics.lcp = lastEntry.startTime;
                console.log('[Performance] LCP:', lastEntry.startTime.toFixed(2), 'ms');
            });

            lcpObserver.observe({ type: 'largest-contentful-paint', buffered: true });
        } catch (e) {
            console.warn('[Performance] LCP observation not supported');
        }
    },

    /**
     * 观察 FID
     */
    observeFID() {
        if (!('PerformanceObserver' in window)) return;

        try {
            const fidObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const fid = entries[0];
                this.metrics.fid = fid.processingStart - fid.startTime;
                console.log('[Performance] FID:', this.metrics.fid.toFixed(2), 'ms');
            });

            fidObserver.observe({ type: 'first-input', buffered: true });
        } catch (e) {
            console.warn('[Performance] FID observation not supported');
        }
    },

    /**
     * 观察 CLS
     */
    observeCLS() {
        if (!('PerformanceObserver' in window)) return;

        try {
            let clsScore = 0;
            const clsObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsScore += entry.value;
                    }
                }
                this.metrics.cls = clsScore;
                console.log('[Performance] CLS:', clsScore.toFixed(4));
            });

            clsObserver.observe({ type: 'layout-shift', buffered: true });
        } catch (e) {
            console.warn('[Performance] CLS observation not supported');
        }
    },

    /**
     * 获取标记时间
     */
    getMark(name) {
        return this.metrics.marks[name] || 0;
    },

    /**
     * 获取测量值
     */
    getMeasure(name) {
        return this.metrics.measures[name] || 0;
    },

    /**
     * 获取所有指标
     */
    getMetrics() {
        return {
            pageLoad: this.getMeasure('pageLoad'),
            fcp: this.metrics.fcp,
            lcp: this.metrics.lcp,
            fid: this.metrics.fid,
            cls: this.metrics.cls,
            resources: this.metrics.resources
        };
    },

    /**
     * 上报指标
     */
    reportMetrics() {
        if (!this.config.reportEndpoint) return;

        const metrics = this.getMetrics();

        fetch(this.config.reportEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                metrics,
                url: window.location.pathname,
                userAgent: navigator.userAgent,
                timestamp: Date.now()
            }),
            keepalive: true
        }).catch((error) => {
            // 上报失败时静默处理
            console.debug('[Performance] Report failed:', error.message);
        });
    },

    /**
     * 缩短URL显示
     */
    shortenUrl(url) {
        if (url.length > 50) {
            return url.substring(0, 25) + '...' + url.substring(url.length - 22);
        }
        return url;
    }
};

// 自动初始化
if (typeof window !== 'undefined') {
    window.PerformanceMonitor = PerformanceMonitor;

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => PerformanceMonitor.init());
    } else {
        PerformanceMonitor.init();
    }
}

// 导出给其他模块使用
export default PerformanceMonitor;
