/**
 * 道德经 PWA Service Worker
 * 支持离线访问和资源缓存
 */

const CACHE_NAME = 'daodejing-v1';
const STATIC_CACHE = 'daodejing-static-v1';

// 需要缓存的静态资源
const STATIC_ASSETS = [
    '/',
    '/daodejing/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/modules/theme.js',
    '/static/js/modules/sidebar.js',
    '/static/js/modules/music.js',
    '/static/js/modules/shortcuts.js',
    '/static/js/modules/bookmark.js',
    '/static/js/modules/reading-progress.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'
];

// 安装事件 - 缓存静态资源
self.addEventListener('install', (event) => {
    console.log('[SW] 安装 Service Worker');
    event.waitUntil(
        caches.open(STATIC_CACHE).then((cache) => {
            console.log('[SW] 缓存静态资源');
            return cache.addAll(STATIC_ASSETS.map(url => new Request(url, { cache: 'reload' })))
                .catch(err => {
                    console.log('[SW] 部分资源缓存失败:', err);
                    // 继续安装，即使部分资源缓存失败
                });
        })
    );
    self.skipWaiting();
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', (event) => {
    console.log('[SW] 激活 Service Worker');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && cacheName !== CACHE_NAME) {
                        console.log('[SW] 删除旧缓存:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// 拦截网络请求
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // 只处理同源请求
    if (url.origin !== self.location.origin) {
        // 对于CDN资源，尝试网络优先，失败则用缓存
        if (url.hostname === 'cdn.jsdelivr.net') {
            event.respondWith(
                fetch(request).catch(() => caches.match(request))
            );
        }
        return;
    }

    // API请求走网络
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(request).catch(() => {
                // API失败时返回缓存的响应或错误
                return caches.match(request).then(response => {
                    return response || new Response(
                        JSON.stringify({ error: '网络不可用' }),
                        { headers: { 'Content-Type': 'application/json' } }
                    );
                });
            })
        );
        return;
    }

    // 静态资源：缓存优先
    if (url.pathname.startsWith('/static/')) {
        event.respondWith(
            caches.match(request).then((response) => {
                if (response) {
                    return response;
                }
                return fetch(request).then((response) => {
                    // 只缓存成功的响应
                    if (response.status === 200) {
                        const responseClone = response.clone();
                        caches.open(STATIC_CACHE).then((cache) => {
                            cache.put(request, responseClone);
                        });
                    }
                    return response;
                });
            })
        );
        return;
    }

    // 页面请求：网络优先，失败则用缓存
    event.respondWith(
        fetch(request).catch(() => {
            return caches.match(request).then((response) => {
                if (response) {
                    return response;
                }
                // 如果是页面请求，返回离线页面
                if (request.mode === 'navigate') {
                    return caches.match('/daodejing/');
                }
                return new Response('离线状态下无法访问此资源', {
                    status: 503,
                    statusText: 'Service Unavailable',
                    headers: new Headers({ 'Content-Type': 'text/plain' })
                });
            });
        })
    );
});

// 消息处理 - 接收来自客户端的消息
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => caches.delete(cacheName))
                );
            })
        );
    }
});
