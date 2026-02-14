# 性能优化基线

## 前端性能监控

### 当前状态评估

#### 资源清单

| 资源类型 | 文件 | 大小 (KB) | 优化建议 |
|---------|------|-----------|----------|
| CSS | bootstrap.min.css | ~160 | CDN + 压缩 |
| CSS | custom.css | ~15 | 已优化 |
| JS | bootstrap.bundle.min.js | ~80 | CDN + 压缩 |
| JS | main.js | ~25 | 按需加载 |
| 字体 | 自定义字体 | - | 子集化 |
| 图片 | logo.svg | <5 | 已优化 |

#### 性能指标基线

```javascript
// 在 main.js 中添加性能监控
const PerformanceMonitor = {
    init() {
        this.measurePageLoad();
        this.measureResourceTiming();
        this.measureUserInteraction();
    },
    
    measurePageLoad() {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const timing = performance.timing;
                const metrics = {
                    // DNS 查询时间
                    dns: timing.domainLookupEnd - timing.domainLookupStart,
                    // TCP 连接时间
                    tcp: timing.connectEnd - timing.connectStart,
                    // 首字节时间 (TTFB)
                    ttfb: timing.responseStart - timing.requestStart,
                    // DOM 解析时间
                    domParse: timing.domComplete - timing.domLoading,
                    // 页面完全加载时间
                    loadComplete: timing.loadEventEnd - timing.navigationStart,
                    // 首屏渲染时间 (FCP)
                    fcp: this.getFCP(),
                };
                
                console.log('[Performance] Page Load Metrics:', metrics);
                this.sendMetrics('page_load', metrics);
            }, 0);
        });
    },
    
    measureResourceTiming() {
        const resources = performance.getEntriesByType('resource');
        const slowResources = resources
            .filter(r => r.duration > 1000)
            .map(r => ({
                name: r.name,
                duration: r.duration,
                type: r.initiatorType
            }));
        
        if (slowResources.length > 0) {
            console.warn('[Performance] Slow Resources:', slowResources);
        }
    },
    
    measureUserInteraction() {
        // 测量关键交互的响应时间
        let lastClick = 0;
        document.addEventListener('click', () => {
            lastClick = performance.now();
        });
        
        // 测量章节切换时间
        const originalPushState = history.pushState;
        history.pushState = function(...args) {
            const start = performance.now();
            originalPushState.apply(this, args);
            
            requestAnimationFrame(() => {
                const duration = performance.now() - start;
                console.log(`[Performance] Navigation took ${duration.toFixed(2)}ms`);
            });
        };
    },
    
    getFCP() {
        const entries = performance.getEntriesByType('paint');
        const fcp = entries.find(e => e.name === 'first-contentful-paint');
        return fcp ? fcp.startTime : null;
    },
    
    sendMetrics(type, data) {
        // 发送到分析服务（如果配置）
        if (window.analyticsEnabled) {
            fetch('/api/analytics/performance', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type, data, timestamp: Date.now()}),
                keepalive: true
            }).catch(() => {});
        }
    }
};

// 初始化性能监控
if (window.performance && window.performance.timing) {
    PerformanceMonitor.init();
}
```

### 优化建议

#### 1. 资源优化

```javascript
// 懒加载非关键资源
const LazyLoader = {
    init() {
        this.lazyLoadImages();
        this.lazyLoadScripts();
    },
    
    lazyLoadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    },
    
    lazyLoadScripts() {
        // 延迟加载非关键JavaScript
        const deferredScripts = [
            // 'analytics.js',
            // 'extra-features.js'
        ];
        
        setTimeout(() => {
            deferredScripts.forEach(src => {
                const script = document.createElement('script');
                script.src = src;
                script.async = true;
                document.body.appendChild(script);
            });
        }, 2000);
    }
};
```

#### 2. 缓存策略

```javascript
// Service Worker 缓存策略（可选）
const CACHE_NAME = 'daodejing-v1';
const CACHE_URLS = [
    '/',
    '/static/css/bootstrap.min.css',
    '/static/css/custom.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/main.js'
];

// 简化的缓存逻辑
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {
        console.log('Service Worker registration failed');
    });
}
```

#### 3. 代码分割

```javascript
// 按功能模块分割代码
const FeatureLoader = {
    async loadKnowledgeGraph() {
        if (!this.knowledgeGraphModule) {
            const module = await import('./modules/knowledge-graph.js');
            this.knowledgeGraphModule = module.default;
        }
        return this.knowledgeGraphModule;
    },
    
    async loadTTSPlayer() {
        if (!this.ttsModule) {
            const module = await import('./modules/tts-player.js');
            this.ttsModule = module.default;
        }
        return this.ttsModule;
    }
};
```

## 性能目标

### 关键指标

| 指标 | 当前目标 | 优化目标 |
|------|----------|----------|
| First Contentful Paint (FCP) | < 1.8s | < 1.0s |
| Largest Contentful Paint (LCP) | < 2.5s | < 1.5s |
| Time to Interactive (TTI) | < 3.8s | < 2.5s |
| Cumulative Layout Shift (CLS) | < 0.1 | < 0.05 |
| First Input Delay (FID) | < 100ms | < 50ms |

### 优化策略

1. **立即执行**
   - [ ] 启用 Gzip/Brotli 压缩
   - [ ] 配置 CDN 缓存
   - [ ] 优化首屏加载

2. **短期执行**
   - [ ] 实现资源懒加载
   - [ ] 添加 Service Worker
   - [ ] 代码分割和按需加载

3. **长期执行**
   - [ ] 实现预加载策略
   - [ ] 优化关键渲染路径
   - [ ] 图片自适应和 WebP 格式

## 监控工具

### 推荐工具

1. **Lighthouse**: Chrome DevTools 内置
2. **WebPageTest**: 在线性能测试
3. **GTmetrix**: 综合性能分析
4. **Sentry**: 性能监控和错误追踪

### 集成方案

```javascript
// Sentry 性能监控集成示例
if (typeof Sentry !== 'undefined') {
    Sentry.init({
        dsn: 'your-sentry-dsn',
        integrations: [new Sentry.BrowserTracing()],
        tracesSampleRate: 0.1,
    });
}
```

---

*创建日期: 2026-01-29*  
*下次评估: 2026-02-05*
