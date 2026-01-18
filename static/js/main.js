/**
 * 道德经 - 主应用文件
 * 整合所有功能模块
 */

(function() {
    'use strict';

    // ==================== 应用配置 ====================
    const CONFIG = {
        apiBaseUrl: '',
        chapters: 81,
        storagePrefix: 'daodejing_'
    };

    // ==================== 搜索管理器 ====================
    const SearchManager = {
        init() {
            this.searchInput = document.getElementById('searchInput');
            this.searchModal = document.getElementById('searchModal');
            this.searchResults = document.getElementById('searchResults');
            this.debounceTimer = null;
            this.currentScope = localStorage.getItem('daodejing_search_scope') || 'all';
            this.useRegex = localStorage.getItem('daodejing_search_regex') === 'true';

            if (!this.searchInput) return;

            this.bindEvents();
        },

        bindEvents() {
            // 实时搜索（防抖）
            this.searchInput.addEventListener('input', (e) => {
                clearTimeout(this.debounceTimer);
                const query = e.target.value.trim();

                if (query.length < 2) {
                    this.hideModal();
                    return;
                }

                this.debounceTimer = setTimeout(() => {
                    this.search(query);
                }, 300);
            });

            // 回车搜索
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const query = this.searchInput.value.trim();
                    if (query.length >= 2) {
                        this.search(query);
                    }
                }
            });

            // 失去焦点隐藏
            this.searchInput.addEventListener('blur', () => {
                setTimeout(() => this.hideModal(), 200);
            });
        },

        async search(query) {
            try {
                const params = new URLSearchParams({
                    q: query,
                    scope: this.currentScope,
                    regex: this.useRegex
                });
                const response = await fetch(`${CONFIG.apiBaseUrl}/api/daodejing/search?${params}`);
                const data = await response.json();
                this.displayResults(data);
            } catch (error) {
                console.error('搜索失败:', error);
                // 降级到客户端搜索
                this.clientSideSearch(query);
            }
        },

        clientSideSearch(query) {
            const results = [];
            const queryLower = query.toLowerCase();

            // 从页面中搜索章节链接
            const chapterLinks = document.querySelectorAll('.chapter-item');
            chapterLinks.forEach(link => {
                const text = link.textContent.toLowerCase();
                if (text.includes(queryLower) || queryLower.includes(text)) {
                    results.push({
                        id: parseInt(link.dataset.chapter),
                        title: link.textContent.trim(),
                        excerpt: link.textContent.trim()
                    });
                }
            });

            this.displayResults({ results, count: results.length, query });
        },

        displayResults(data) {
            const { results, count, query, scope } = data;

            if (!results || results.length === 0) {
                const scopeName = this.getScopeName(this.currentScope);
                this.showModal(`
                    <div class="text-center text-muted py-4">
                        <p class="mb-2">在 <strong>${scopeName}</strong> 范围内未找到包含"${query}"的内容</p>
                        <small>尝试切换搜索范围或取消正则表达式</small>
                    </div>
                `);
                return;
            }

            // 搜索选项和结果统计
            let html = `
                <div class="search-options-bar d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
                    <div class="d-flex align-items-center gap-2">
                        <select class="form-select form-select-sm" id="searchScope" style="width: auto;">
                            <option value="all" ${this.currentScope === 'all' ? 'selected' : ''}>全部</option>
                            <option value="original" ${this.currentScope === 'original' ? 'selected' : ''}>原文</option>
                            <option value="translation" ${this.currentScope === 'translation' ? 'selected' : ''}>白话译文</option>
                            <option value="commentary" ${this.currentScope === 'commentary' ? 'selected' : ''}>注解</option>
                            <option value="english" ${this.currentScope === 'english' ? 'selected' : ''}>英译</option>
                            <option value="ancient" ${this.currentScope === 'ancient' ? 'selected' : ''}>古籍</option>
                            <option value="idiom" ${this.currentScope === 'idiom' ? 'selected' : ''}>成语</option>
                        </select>
                        <div class="form-check form-check-inline">
                            <input class="form-check-input" type="checkbox" id="regexToggle" ${this.useRegex ? 'checked' : ''}>
                            <label class="form-check-label small" for="regexToggle">正则</label>
                        </div>
                    </div>
                    <span class="badge bg-primary">${count} 条结果</span>
                </div>
            `;

            // 结果列表
            html += '<div class="search-results-list">';
            for (const result of results) {
                if (result.type === 'idiom') {
                    html += this.renderIdiomResult(result);
                } else {
                    html += this.renderChapterResult(result);
                }
            }
            html += '</div>';

            this.showModal(html);
            this.bindResultClicks();
            this.bindOptionEvents();
        },

        renderIdiomResult(result) {
            const { title, meaning, chapter, source, match_reason } = result;
            const reasonText = match_reason ? match_reason.join('、') : '';

            return `
                <div class="search-result-item idiom-result" data-type="idiom" data-chapter="${chapter || ''}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <span class="badge bg-warning text-dark me-2">成语</span>
                            <span class="fw-bold">${title}</span>
                        </div>
                        ${chapter ? `<small class="text-muted">出自第${chapter}章</small>` : ''}
                    </div>
                    <div class="small text-muted mt-1">${meaning}</div>
                    ${source ? `<div class="small text-muted fst-italic mt-1">「${source}」</div>` : ''}
                    ${reasonText ? `<div class="small text-primary mt-1">匹配: ${reasonText}</div>` : ''}
                </div>
            `;
        },

        renderChapterResult(result) {
            const { id, title, matches } = result;

            let matchesHtml = '';
            if (matches && matches.length > 0) {
                matchesHtml = '<div class="matches-list mt-2">';
                matches.forEach(match => {
                    matchesHtml += `
                        <div class="match-item small">
                            <span class="badge bg-secondary me-1">${match.field}</span>
                            <span class="text-muted">${match.text}</span>
                        </div>
                    `;
                });
                matchesHtml += '</div>';
            }

            return `
                <div class="search-result-item chapter-result" data-type="chapter" data-chapter="${id}">
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="fw-bold">${title}</span>
                        <small class="text-muted">点击跳转</small>
                    </div>
                    ${matchesHtml}
                </div>
            `;
        },

        getScopeName(scope) {
            const names = {
                all: '全部',
                original: '原文',
                translation: '白话译文',
                commentary: '注解',
                english: '英译',
                ancient: '古籍',
                idiom: '成语'
            };
            return names[scope] || '全部';
        },

        bindOptionEvents() {
            // 搜索范围切换
            const scopeSelect = document.getElementById('searchScope');
            if (scopeSelect) {
                scopeSelect.addEventListener('change', (e) => {
                    this.currentScope = e.target.value;
                    localStorage.setItem('daodejing_search_scope', this.currentScope);
                    // 重新搜索
                    const query = this.searchInput?.value?.trim();
                    if (query && query.length >= 2) {
                        this.search(query);
                    }
                });
            }

            // 正则表达式切换
            const regexToggle = document.getElementById('regexToggle');
            if (regexToggle) {
                regexToggle.addEventListener('change', (e) => {
                    this.useRegex = e.target.checked;
                    localStorage.setItem('daodejing_search_regex', this.useRegex);
                    // 重新搜索
                    const query = this.searchInput?.value?.trim();
                    if (query && query.length >= 2) {
                        this.search(query);
                    }
                });
            }
        },

        bindResultClicks() {
            document.querySelectorAll('.search-result-item').forEach(item => {
                item.addEventListener('click', () => {
                    const type = item.dataset.type;
                    const chapter = item.dataset.chapter;
                    if (chapter) {
                        window.location.href = `/daodejing/chapter/${chapter}`;
                    }
                });
            });
        },

        showModal(content) {
            if (!this.searchResults) return;
            this.searchResults.innerHTML = content;

            if (!this.modalInstance) {
                this.modalInstance = new bootstrap.Modal(this.searchModal);
            }
            this.modalInstance.show();
        },

        hideModal() {
            if (this.modalInstance) {
                this.modalInstance.hide();
            }
        }
    };

    // ==================== 阅读进度管理器 ====================
    const ProgressManager = {
        STORAGE_KEY: 'daodejing_reading_progress',
        HISTORY_KEY: 'daodejing_reading_history',
        MAX_HISTORY: 20,

        init() {
            this.currentChapter = this.getCurrentChapterId();
            if (!this.currentChapter) return;

            this.saveProgress();
            this.updateLastReadUI();
        },

        getCurrentChapterId() {
            // 从 URL 获取章节 ID
            const match = window.location.pathname.match(/\/chapter\/(\d+)/);
            return match ? parseInt(match[1]) : null;
        },

        saveProgress() {
            const now = new Date();
            const progress = {
                chapter: this.currentChapter,
                timestamp: now.getTime(),
                date: now.toLocaleDateString('zh-CN'),
                time: now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
            };

            // 保存最后阅读位置
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(progress));

            // 添加到阅读历史
            let history = this.getHistory();
            history = history.filter(item => item.chapter !== this.currentChapter);
            history.unshift(progress);
            if (history.length > this.MAX_HISTORY) {
                history = history.slice(0, this.MAX_HISTORY);
            }
            localStorage.setItem(this.HISTORY_KEY, JSON.stringify(history));
        },

        getLastReadChapter() {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            return saved ? JSON.parse(saved) : null;
        },

        getHistory() {
            const saved = localStorage.getItem(this.HISTORY_KEY);
            return saved ? JSON.parse(saved) : [];
        },

        getReadingProgress() {
            const history = this.getHistory();
            const uniqueChapters = new Set(history.map(item => item.chapter));
            return {
                total: 81,
                read: uniqueChapters.size,
                percentage: Math.round((uniqueChapters.size / 81) * 100)
            };
        },

        updateLastReadUI() {
            // 更新"继续阅读"按钮
            const lastRead = this.getLastReadChapter();
            const continueBtn = document.getElementById('continueReadingBtn');
            if (continueBtn && lastRead) {
                continueBtn.href = `/daodejing/chapter/${lastRead.chapter}`;
                continueBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M11.251.068a.5.5 0 0 1 .227.58L9.677 6.5H13a.5.5 0 0 1 .364.843l-8 8.5a.5.5 0 0 1-.842-.49L6.323 9.5H3a.5.5 0 0 1-.364-.843l8-8.5a.5.5 0 0 1 .615-.09z"/>
                    </svg>
                    继续阅读 第${lastRead.chapter}章
                `;
                continueBtn.classList.remove('d-none');
            }
        },

        // 静态方法：在首页显示阅读进度
        static renderHomePageProgress() {
            const progress = JSON.parse(localStorage.getItem('daodejing_reading_progress') || '{}');
            const history = JSON.parse(localStorage.getItem('daodejing_reading_history') || '[]');
            const readCount = new Set(history.map(h => h.chapter)).size;
            const percentage = Math.round((readCount / 81) * 100);

            return {
                lastChapter: progress.chapter,
                lastDate: progress.date,
                readCount,
                percentage
            };
        }
    };

    // ==================== 复制管理器 ====================
    const CopyManager = {
        init() {
            this.copyButtons = document.querySelectorAll('[data-copy-target]');
            console.log('[CopyManager] 找到复制按钮:', this.copyButtons.length);
            if (this.copyButtons.length === 0) return;

            this.bindEvents();
        },

        bindEvents() {
            this.copyButtons.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    const targetId = btn.dataset.copyTarget;
                    console.log('[CopyManager] 复制目标:', targetId);
                    const target = document.getElementById(targetId);
                    if (target) {
                        // 获取纯文本（去除HTML标签）
                        const text = target.innerText || target.textContent;
                        const cleanText = text.trim();
                        console.log('[CopyManager] 复制文本长度:', cleanText.length);
                        this.copyToClipboard(cleanText, btn);
                    } else {
                        console.error('[CopyManager] 找不到目标元素:', targetId);
                    }
                });
            });
        },

        async copyToClipboard(text, btn) {
            console.log('[CopyManager] 开始复制...');
            try {
                await navigator.clipboard.writeText(text);
                console.log('[CopyManager] Clipboard API 成功');
                this.showSuccess(btn);
            } catch (err) {
                console.log('[CopyManager] Clipboard API 失败，使用降级方案:', err);
                // 降级方案
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                textarea.style.top = '0';
                textarea.style.left = '0';
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    const success = document.execCommand('copy');
                    console.log('[CopyManager] execCommand 结果:', success);
                    if (success) {
                        this.showSuccess(btn);
                    } else {
                        console.error('[CopyManager] execCommand 返回 false');
                    }
                } catch (e) {
                    console.error('[CopyManager] 复制失败:', e);
                }
                document.body.removeChild(textarea);
            }
        },

        showSuccess(btn) {
            console.log('[CopyManager] 显示成功状态');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = `<span style="color: green;">✓</span>`;
            btn.classList.add('btn-success');
            btn.classList.remove('btn-outline-secondary');

            setTimeout(() => {
                btn.innerHTML = originalHTML;
                btn.classList.remove('btn-success');
                btn.classList.add('btn-outline-secondary');
            }, 2000);
        }
    };

    // ==================== 引用卡片管理器 ====================
    const QuoteCardManager = {
        init() {
            this.quoteBtn = document.getElementById('quoteBtn');
            this.quoteModal = document.getElementById('quoteModal');
            console.log('[QuoteCardManager] 初始化, quoteBtn:', !!this.quoteBtn, 'quoteModal:', !!this.quoteModal);
            if (!this.quoteBtn) {
                console.log('[QuoteCardManager] 未找到 quoteBtn，跳过初始化');
                return;
            }

            this.bindEvents();
        },

        bindEvents() {
            this.quoteBtn.addEventListener('click', () => {
                console.log('[QuoteCardManager] 按钮被点击');
                this.generateQuoteCard();
            });
        },

        generateQuoteCard() {
            const chapter = this.getCurrentChapter();
            const original = document.querySelector('#originalText')?.textContent?.trim() || '';
            const chapterNum = document.querySelector('#chapterNum')?.textContent || '';

            console.log('[QuoteCardManager] 生成卡片, 章节:', chapter, '文本长度:', original.length);

            if (!original) {
                console.error('[QuoteCardManager] 未找到原文内容');
                return;
            }

            // 创建预览
            const preview = document.getElementById('quotePreview');
            const canvas = document.getElementById('quoteCanvas');
            if (!preview || !canvas) {
                console.error('[QuoteCardManager] 未找到 canvas 或 preview');
                return;
            }

            const ctx = canvas.getContext('2d');
            const width = 600;
            const height = 400;

            canvas.width = width;
            canvas.height = height;

            // 背景
            const gradient = ctx.createLinearGradient(0, 0, width, height);
            gradient.addColorStop(0, '#2c1810');
            gradient.addColorStop(1, '#1a0f0a');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, width, height);

            // 边框装饰
            ctx.strokeStyle = '#c9a227';
            ctx.lineWidth = 3;
            ctx.strokeRect(15, 15, width - 30, height - 30);

            // 章节号
            ctx.fillStyle = '#c9a227';
            ctx.font = 'bold 24px serif';
            ctx.textAlign = 'center';
            ctx.fillText(chapterNum, width / 2, 60);

            // 原文（分行）
            ctx.fillStyle = '#e8e0d8';
            ctx.font = '20px serif';
            const lines = this.wrapText(ctx, original, width - 100);
            let y = 120;
            lines.forEach(line => {
                ctx.fillText(line, width / 2, y);
                y += 35;
            });

            // 底部署名
            ctx.fillStyle = '#888';
            ctx.font = '14px sans-serif';
            ctx.fillText('— 老子《道德经》', width / 2, height - 40);

            // 显示下载按钮
            const downloadBtn = document.getElementById('downloadQuoteBtn');
            if (downloadBtn) {
                downloadBtn.onclick = () => {
                    const link = document.createElement('a');
                    link.download = `道德经-${chapterNum}.png`;
                    link.href = canvas.toDataURL();
                    link.click();
                };
            }

            // 显示模态框
            const modal = new bootstrap.Modal(this.quoteModal);
            modal.show();
        },

        wrapText(ctx, text, maxWidth) {
            const chars = text.split('');
            const lines = [];
            let currentLine = '';

            for (const char of chars) {
                const testLine = currentLine + char;
                const metrics = ctx.measureText(testLine);
                if (metrics.width > maxWidth && currentLine !== '') {
                    lines.push(currentLine);
                    currentLine = char;
                } else {
                    currentLine = testLine;
                }
            }
            if (currentLine !== '') {
                lines.push(currentLine);
            }

            return lines.slice(0, 6); // 最多6行
        },

        getCurrentChapter() {
            const match = window.location.pathname.match(/\/chapter\/(\d+)/);
            return match ? parseInt(match[1]) : null;
        }
    };

    // ==================== 朗读管理器 ====================
    const SpeechManager = {
        STORAGE_KEY: 'daodejing_speech',
        isPlaying: false,
        currentUtterance: null,
        selectedLang: 'zh-CN',
        voices: [],

        init() {
            this.toggleBtn = document.getElementById('speechToggle');
            this.stopBtn = document.getElementById('speechStop');
            this.voiceSelect = document.getElementById('browserVoice');

            if (!this.toggleBtn) return;

            this.loadSettings();
            this.loadVoices();
            this.bindEvents();
        },

        loadVoices() {
            // 加载可用语音列表
            const loadVoices = () => {
                this.voices = speechSynthesis.getVoices();
                console.log('可用语音:', this.voices.map(v => `${v.name} (${v.lang})`));
            };

            loadVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = loadVoices;
            }
        },

        loadSettings() {
            const settings = JSON.parse(localStorage.getItem(this.STORAGE_KEY) || '{}');
            this.selectedLang = settings.lang || 'zh-CN';

            if (this.voiceSelect) {
                this.voiceSelect.value = this.selectedLang;
            }
        },

        saveSettings() {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify({
                lang: this.selectedLang
            }));
        },

        // 根据语言代码查找匹配的语音
        findVoiceForLanguage(langCode) {
            if (!this.voices || this.voices.length === 0) return null;

            // 精确匹配语言代码
            let voice = this.voices.find(v => v.lang === langCode);
            if (voice) return voice;

            // 匹配语言前缀 (如 zh-CN 匹配 zh)
            const prefix = langCode.split('-')[0];
            voice = this.voices.find(v => v.lang.startsWith(prefix));
            if (voice) return voice;

            // 特殊处理：英语
            if (langCode.startsWith('en')) {
                voice = this.voices.find(v => v.lang.startsWith('en'));
                return voice || this.voices[0];
            }

            // 如果没找到，使用第一个可用语音
            return this.voices[0];
        },

        bindEvents() {
            this.toggleBtn?.addEventListener('click', () => this.toggle());
            this.stopBtn?.addEventListener('click', () => this.stop());

            this.voiceSelect?.addEventListener('change', (e) => {
                this.selectedLang = e.target.value;
                this.saveSettings();

                // 如果正在朗读，重新开始
                if (this.isPlaying) {
                    this.stop();
                    this.speak();
                }
            });
        },

        toggle() {
            if (this.isPlaying) {
                this.stop();
            } else {
                this.speak();
            }
        },

        speak() {
            const originalText = document.querySelector('.original-text');
            if (!originalText) {
                this.showToast('没有找到可朗读的内容');
                return;
            }

            const text = originalText.textContent.trim();
            if (!text) {
                this.showToast('没有找到可朗读的内容');
                return;
            }

            this.stop();

            this.currentUtterance = new SpeechSynthesisUtterance(text);
            this.currentUtterance.lang = this.selectedLang;
            this.currentUtterance.rate = 0.8;

            // 查找匹配的语音
            const matchedVoice = this.findVoiceForLanguage(this.selectedLang);
            if (matchedVoice) {
                this.currentUtterance.voice = matchedVoice;
                console.log(`使用语音: ${matchedVoice.name} (${matchedVoice.lang})`);
            } else {
                console.warn('未找到匹配的语音，使用默认');
            }

            this.currentUtterance.onstart = () => {
                this.isPlaying = true;
                this.updateState();
            };

            this.currentUtterance.onend = () => {
                this.isPlaying = false;
                this.updateState();
            };

            this.currentUtterance.onerror = (e) => {
                console.error('语音合成错误:', e);
                this.isPlaying = false;
                this.updateState();
            };

            speechSynthesis.speak(this.currentUtterance);
        },

        stop() {
            speechSynthesis.cancel();
            this.isPlaying = false;
            this.updateState();
        },

        updateState() {
            const icon = this.toggleBtn?.querySelector('.speech-icon');
            if (this.isPlaying) {
                icon?.classList.add('speaking');
                this.toggleBtn?.classList.add('active');
                this.stopBtn?.classList.remove('d-none');
            } else {
                icon?.classList.remove('speaking');
                this.toggleBtn?.classList.remove('active');
                this.stopBtn?.classList.add('d-none');
            }
        },

        showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'position-fixed bottom-0 end-0 p-3';
            toast.style.zIndex = '1100';
            toast.innerHTML = `
                <div class="toast show">
                    <div class="toast-body">${message}</div>
                </div>
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2000);
        }
    };

    // ==================== 设置管理器 ====================
    const SettingsManager = {
        init() {
            this.settingsPanel = document.getElementById('settingsPanel');
            this.settingsToggle = document.getElementById('settingsToggle');
            this.closeSettingsBtn = document.getElementById('closeSettingsPanel');
            this.fontSelect = document.getElementById('fontSelect');
            this.musicSelect = document.getElementById('musicSelect');
            this.musicVolumeSlider = document.getElementById('musicVolumeSlider');
            this.musicVolumeValue = document.getElementById('musicVolumeValue');

            console.log('[SettingsManager] 初始化, settingsPanel:', !!this.settingsPanel, 'settingsToggle:', !!this.settingsToggle);

            if (!this.settingsPanel) return;

            this.loadSettings();
            this.bindEvents();
            this.highlightCurrentChapter();
        },

        loadSettings() {
            // 字体选择
            const savedFont = localStorage.getItem('daodejing_font');
            if (savedFont) {
                this.setFont(savedFont);
                if (this.fontSelect) {
                    this.fontSelect.value = savedFont;
                }
            }

            // 字体大小
            const savedSize = localStorage.getItem('daodejing_fontSize');
            if (savedSize) {
                this.setFontSize(savedSize);
            }

            // 文字布局
            const savedLayout = localStorage.getItem('daodejing_textLayout');
            if (savedLayout) {
                this.setTextLayout(savedLayout);
            }

            // 音乐选择
            const savedMusic = localStorage.getItem('daodejing_music');
            if (savedMusic && this.musicSelect) {
                this.musicSelect.value = savedMusic;
            }

            // 音乐音量
            const savedMusicVolume = localStorage.getItem('daodejing_music_volume');
            if (savedMusicVolume && this.musicVolumeSlider) {
                this.musicVolumeSlider.value = savedMusicVolume * 100;
                if (this.musicVolumeValue) {
                    this.musicVolumeValue.textContent = Math.round(savedMusicVolume * 100) + '%';
                }
            }

            // 显示选项
            this.loadDisplayOptions();

            // 版本显示
            this.loadVersionOptions();

            // AI Keys
            this.loadAIKeys();
        },

        bindEvents() {
            console.log('[SettingsManager] 绑定事件, settingsToggle:', !!this.settingsToggle, 'closeSettingsBtn:', !!this.closeSettingsBtn);

            // 打开/关闭设置面板
            this.settingsToggle?.addEventListener('click', (e) => {
                console.log('[SettingsManager] 设置按钮被点击');
                e.preventDefault();
                e.stopPropagation();
                this.settingsPanel.classList.toggle('show');
            });

            this.closeSettingsBtn?.addEventListener('click', (e) => {
                console.log('[SettingsManager] 关闭按钮被点击');
                e.preventDefault();
                this.settingsPanel.classList.remove('show');
            });

            // 点击外部关闭
            document.addEventListener('click', (e) => {
                if (this.settingsPanel?.classList.contains('show')) {
                    if (!this.settingsPanel.contains(e.target) &&
                        !this.settingsToggle?.contains(e.target)) {
                        this.settingsPanel.classList.remove('show');
                    }
                }
            });

            // 字体选择
            this.fontSelect?.addEventListener('change', (e) => {
                this.setFont(e.target.value);
            });

            // 字体大小
            document.querySelectorAll('.size-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const size = btn.dataset.size;
                    this.setFontSize(size);
                    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                });
            });

            // 文字布局
            document.querySelectorAll('.layout-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const layout = btn.dataset.layout;
                    this.setTextLayout(layout);
                    document.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                });
            });

            // 阅读模式
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const mode = btn.dataset.mode;
                    this.setReadingMode(mode);
                    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                });
            });

            // 音乐选择
            this.musicSelect?.addEventListener('change', (e) => {
                this.setMusic(e.target.value);
            });

            // 音乐音量
            this.musicVolumeSlider?.addEventListener('input', (e) => {
                const volume = e.target.value / 100;
                localStorage.setItem('daodejing_music_volume', volume);
                if (this.musicVolumeValue) {
                    this.musicVolumeValue.textContent = e.target.value + '%';
                }
                const audio = document.getElementById('bgMusic');
                if (audio) audio.volume = volume;
            });

            // 显示选项
            document.getElementById('showPinyin')?.addEventListener('change', (e) => {
                document.body.classList.toggle('hide-pinyin', !e.target.checked);
                localStorage.setItem('daodejing_showPinyin', e.target.checked);
            });

            document.getElementById('showAnnotation')?.addEventListener('change', (e) => {
                document.body.classList.toggle('hide-annotation', !e.target.checked);
                localStorage.setItem('daodejing_showAnnotation', e.target.checked);
            });

            // 版本显示
            document.getElementById('showModern')?.addEventListener('change', (e) => {
                document.body.classList.toggle('hide-modern', !e.target.checked);
                localStorage.setItem('daodejing_showModern', e.target.checked);
            });

            document.getElementById('showNotes')?.addEventListener('change', (e) => {
                document.body.classList.toggle('hide-notes', !e.target.checked);
                localStorage.setItem('daodejing_showNotes', e.target.checked);
            });

            document.getElementById('showEnglish')?.addEventListener('change', (e) => {
                document.body.classList.toggle('hide-english', !e.target.checked);
                localStorage.setItem('daodejing_showEnglish', e.target.checked);
            });

            // AI Keys
            document.getElementById('deepseekKey')?.addEventListener('change', (e) => {
                localStorage.setItem('daodejing_deepseek_key', e.target.value);
            });

            document.getElementById('openaiKey')?.addEventListener('change', (e) => {
                localStorage.setItem('daodejing_openai_key', e.target.value);
            });

            // 赞赏按钮
            document.getElementById('supportBtn')?.addEventListener('click', () => {
                const modal = new bootstrap.Modal(document.getElementById('supportModal'));
                modal.show();
            });

            // 社群按钮
            document.getElementById('communityBtn')?.addEventListener('click', () => {
                const modal = new bootstrap.Modal(document.getElementById('communityModal'));
                modal.show();
            });

            // 分享设置
            document.getElementById('shareSettings')?.addEventListener('click', () => {
                this.shareSettings();
            });
        },

        setFont(font) {
            document.body.classList.remove('font-default', 'font-kaiti', 'font-songti',
                'font-fangsong', 'font-mingliu', 'font-xkai');
            document.body.classList.add(`font-${font}`);
            localStorage.setItem('daodejing_font', font);
        },

        setFontSize(size) {
            document.body.classList.remove('font-size-small', 'font-size-medium', 'font-size-large');
            document.body.classList.add(`font-size-${size}`);
            localStorage.setItem('daodejing_fontSize', size);
        },

        setTextLayout(layout) {
            document.body.classList.remove('text-layout-center', 'text-layout-left');
            document.body.classList.add(`text-layout-${layout}`);
            localStorage.setItem('daodejing_textLayout', layout);
        },

        setReadingMode(mode) {
            const zenOverlay = document.getElementById('zenModeOverlay');

            if (mode === 'zen') {
                // 禅读模式
                const originalText = document.querySelector('.original-text');
                if (originalText && zenOverlay) {
                    zenOverlay.innerHTML = `
                        <button class="zen-exit-btn" id="zenExitBtn">退出禅读</button>
                        <div class="original-text">${originalText.innerHTML}</div>
                    `;
                    zenOverlay.classList.add('active');
                    document.getElementById('zenExitBtn')?.addEventListener('click', () => {
                        zenOverlay.classList.remove('active');
                        document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                        document.querySelector('[data-mode="reading"]')?.classList.add('active');
                    });
                }
            } else {
                zenOverlay?.classList.remove('active');
            }
        },

        setMusic(music) {
            localStorage.setItem('daodejing_music', music);

            const audio = document.getElementById('bgMusic');
            if (!audio) return;

            if (music === 'none') {
                audio.pause();
                audio.src = '';
            } else if (window.musicTracks && window.musicTracks[music]) {
                const tracks = window.musicTracks[music];
                audio.src = tracks[Math.floor(Math.random() * tracks.length)];
                audio.load();
            }
        },

        loadDisplayOptions() {
            const showPinyin = localStorage.getItem('daodejing_showPinyin') !== 'false';
            const showAnnotation = localStorage.getItem('daodejing_showAnnotation') !== 'false';

            document.getElementById('showPinyin').checked = showPinyin;
            document.getElementById('showAnnotation').checked = showAnnotation;

            if (!showPinyin) document.body.classList.add('hide-pinyin');
            if (!showAnnotation) document.body.classList.add('hide-annotation');
        },

        loadVersionOptions() {
            const showModern = localStorage.getItem('daodejing_showModern') !== 'false';
            const showNotes = localStorage.getItem('daodejing_showNotes') !== 'false';
            const showEnglish = localStorage.getItem('daodejing_showEnglish') === 'true';

            document.getElementById('showModern').checked = showModern;
            document.getElementById('showNotes').checked = showNotes;
            document.getElementById('showEnglish').checked = showEnglish;

            if (!showModern) document.body.classList.add('hide-modern');
            if (!showNotes) document.body.classList.add('hide-notes');
            if (!showEnglish) document.body.classList.add('hide-english');
        },

        loadAIKeys() {
            const deepseekKey = localStorage.getItem('daodejing_deepseek_key');
            const openaiKey = localStorage.getItem('daodejing_openai_key');

            if (deepseekKey && document.getElementById('deepseekKey')) {
                document.getElementById('deepseekKey').value = deepseekKey;
            }
            if (openaiKey && document.getElementById('openaiKey')) {
                document.getElementById('openaiKey').value = openaiKey;
            }
        },

        highlightCurrentChapter() {
            // 高亮当前章节
            const currentPath = window.location.pathname;
            const match = currentPath.match(/\/chapter\/(\d+)/);
            if (match) {
                const chapterNum = match[1];
                document.querySelectorAll('.chapter-item').forEach(item => {
                    item.classList.remove('active');
                    if (item.dataset.chapter === chapterNum) {
                        item.classList.add('active');
                    }
                });
            }
        },

        shareSettings() {
            const settings = {
                f: localStorage.getItem('daodejing_font') || 'default',
                s: localStorage.getItem('daodejing_fontSize') || 'medium',
                l: localStorage.getItem('daodejing_textLayout') || 'center'
            };

            const url = new URL(window.location);
            url.searchParams.set('settings', btoa(JSON.stringify(settings)));

            navigator.clipboard.writeText(url.toString()).then(() => {
                this.showToast('配置链接已复制到剪贴板');
            });
        },

        showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'position-fixed top-0 end-0 p-3';
            toast.style.zIndex = '9999';
            toast.innerHTML = `
                <div class="toast show align-items-center text-white bg-success">
                    <div class="d-flex">
                        <div class="toast-body">${message}</div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.parentElement.remove()"></button>
                    </div>
                </div>
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2000);
        }
    };

    // ==================== 分享管理器 ====================
    const ShareManager = {
        init() {
            this.shareToggle = document.getElementById('shareToggle');
            this.shareModal = document.getElementById('shareModal');
            this.shareWechat = document.getElementById('shareWechat');
            this.shareWeibo = document.getElementById('shareWeibo');
            this.shareLink = document.getElementById('shareLink');
            this.shareUrlInput = document.getElementById('shareUrlInput');

            if (!this.shareToggle) return;

            this.bindEvents();
        },

        bindEvents() {
            this.shareToggle?.addEventListener('click', () => this.showModal());

            this.shareWechat?.addEventListener('click', () => {
                this.showToast('请截图分享或点击复制链接');
            });

            this.shareWeibo?.addEventListener('click', () => {
                const url = encodeURIComponent(window.location.href);
                const title = encodeURIComponent(document.title);
                window.open(`https://service.weibo.com/share/share.php?url=${url}&title=${title}`, '_blank');
            });

            this.shareLink?.addEventListener('click', () => {
                this.copyLink();
            });
        },

        showModal() {
            if (this.shareUrlInput) {
                this.shareUrlInput.value = window.location.href;
            }
            const modal = new bootstrap.Modal(this.shareModal);
            modal.show();
        },

        copyLink() {
            navigator.clipboard.writeText(window.location.href).then(() => {
                this.showToast('链接已复制到剪贴板');
            }).catch(() => {
                // 降级方案
                const textarea = document.createElement('textarea');
                textarea.value = window.location.href;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                this.showToast('链接已复制到剪贴板');
            });
        },

        showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'position-fixed top-0 end-0 p-3';
            toast.style.zIndex = '9999';
            toast.innerHTML = `
                <div class="toast show align-items-center text-white bg-success">
                    <div class="d-flex">
                        <div class="toast-body">${message}</div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.parentElement.parentElement.parentElement.remove()"></button>
                    </div>
                </div>
            `;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 2000);
        }
    };

    // ==================== AI 管理器 ====================
    const AIManager = {
        init() {
            this.sidebar = document.getElementById('aiSidebar');
            this.toggle = document.getElementById('aiToggle');
            this.closeBtn = document.getElementById('aiCloseSidebar');
            this.newChatBtn = document.getElementById('aiNewChat');
            this.overlay = document.getElementById('aiOverlay');
            this.messages = document.getElementById('aiMessages');
            this.input = document.getElementById('aiInput');
            this.sendBtn = document.getElementById('aiSend');
            this.modelSelect = document.getElementById('aiModel');
            this.suggestions = document.getElementById('aiSuggestions');

            if (!this.sidebar) return;

            this.chatHistory = [];
            this.bindEvents();
        },

        bindEvents() {
            this.toggle?.addEventListener('click', () => this.toggleSidebar());
            this.closeBtn?.addEventListener('click', () => this.closeSidebar());
            this.overlay?.addEventListener('click', () => this.closeSidebar());

            this.newChatBtn?.addEventListener('click', () => this.newChat());

            this.sendBtn?.addEventListener('click', () => this.sendMessage());
            this.input?.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });

            // 快捷问题
            this.suggestions?.querySelectorAll('.ai-suggestion-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const question = btn.dataset.question;
                    if (this.input) {
                        this.input.value = question;
                        this.sendMessage();
                    }
                });
            });
        },

        toggleSidebar() {
            this.sidebar?.classList.toggle('show');
            this.overlay?.classList.toggle('show');
        },

        closeSidebar() {
            this.sidebar?.classList.remove('show');
            this.overlay?.classList.remove('show');
        },

        newChat() {
            this.chatHistory = [];
            this.showWelcome();
        },

        showWelcome() {
            if (!this.messages) return;
            this.messages.innerHTML = `
                <div class="ai-welcome">
                    <div class="ai-welcome-icon">🤖</div>
                    <h6>道德经AI助手</h6>
                    <p>您可以：</p>
                    <ul>
                        <li>点击下方快捷问题开始</li>
                        <li>或直接输入您的问题</li>
                    </ul>
                </div>
            `;
        },

        async sendMessage() {
            const message = this.input?.value.trim();
            if (!message) return;

            // 添加用户消息
            this.addMessage('user', message);
            this.input.value = '';

            // 获取当前章节内容
            const chapterInfo = this.getChapterInfo();

            // 显示输入状态
            this.showTyping();

            // 获取 API 配置
            const model = this.modelSelect?.value || 'auto';
            let apiKey, apiUrl;

            if (model === 'deepseek' || model === 'auto') {
                apiKey = localStorage.getItem('daodejing_deepseek_key');
                if (apiKey) {
                    apiUrl = 'https://api.deepseek.com/v1/chat/completions';
                }
            }

            if (!apiKey && (model === 'openai' || model === 'auto')) {
                apiKey = localStorage.getItem('daodejing_openai_key');
                if (apiKey) {
                    apiUrl = 'https://api.openai.com/v1/chat/completions';
                }
            }

            if (!apiKey || !apiUrl) {
                this.hideTyping();
                this.addMessage('assistant', '请先在设置中配置 API Key（支持 DeepSeek 或 OpenAI）。');
                return;
            }

            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${apiKey}`
                    },
                    body: JSON.stringify({
                        model: apiUrl.includes('deepseek') ? 'deepseek-chat' : 'gpt-3.5-turbo',
                        messages: [
                            {
                                role: 'system',
                                content: `你是《道德经》研究专家。用户正在阅读第${chapterInfo.number}章"${chapterInfo.title}"。
                                请用通俗易懂的语言，结合现代生活，为用户解读《道德经》。
                                回答要简洁深入，一般在200字以内。`
                            },
                            ...this.chatHistory,
                            { role: 'user', content: message }
                        ],
                        max_tokens: 500,
                        temperature: 0.7
                    })
                });

                const data = await response.json();
                this.hideTyping();

                if (data.choices && data.choices[0]) {
                    const reply = data.choices[0].message.content;
                    this.addMessage('assistant', reply);
                    this.chatHistory.push({ role: 'user', content: message });
                    this.chatHistory.push({ role: 'assistant', content: reply });
                } else {
                    this.addMessage('assistant', '抱歉，AI 解读暂时不可用，请稍后重试。');
                }
            } catch (error) {
                this.hideTyping();
                this.addMessage('assistant', '网络请求失败，请检查 API Key 配置或网络连接。');
            }
        },

        addMessage(role, content) {
            if (!this.messages) return;

            // 移除欢迎界面
            const welcome = this.messages.querySelector('.ai-welcome');
            if (welcome) welcome.remove();

            const msgDiv = document.createElement('div');
            msgDiv.className = `ai-message ${role}`;
            msgDiv.innerHTML = `
                <div class="ai-message-content">${this.formatContent(content)}</div>
            `;
            this.messages.appendChild(msgDiv);
            this.messages.scrollTop = this.messages.scrollHeight;
        },

        formatContent(content) {
            // 简单格式化
            return content
                .replace(/\n/g, '<br>')
                .replace(/《([^》]+)》/g, '<strong>《$1》</strong>')
                .replace(/「([^」]+)」/g, '<em>「$1」</em>');
        },

        showTyping() {
            if (!this.messages) return;
            const typing = document.createElement('div');
            typing.className = 'ai-message assistant';
            typing.id = 'aiTyping';
            typing.innerHTML = `
                <div class="ai-typing">
                    <span></span><span></span><span></span>
                </div>
            `;
            this.messages.appendChild(typing);
            this.messages.scrollTop = this.messages.scrollHeight;
        },

        hideTyping() {
            document.getElementById('aiTyping')?.remove();
        },

        getChapterInfo() {
            const breadcrumb = document.querySelector('.breadcrumb .active');
            const title = document.querySelector('h1, h2, h3, h4, h5')?.textContent || '';
            let number = 1, chapterTitle = '';

            if (breadcrumb) {
                const match = breadcrumb.textContent.match(/第(\d+)章/);
                if (match) number = parseInt(match[1]);
            }

            const originalText = document.querySelector('.original-text');
            if (originalText) {
                chapterTitle = originalText.textContent.substring(0, 20) + '...';
            }

            return { number, title: chapterTitle };
        }
    };

    // ==================== 生僻字管理器 ====================
    const DifficultCharManager = {
        init() {
            // 疑难字标注通过CSS实现
            // 这里可以添加额外的交互功能
            this.enhanceTooltips();
        },

        enhanceTooltips() {
            // 为移动端添加点击显示功能
            if ('ontouchstart' in window) {
                document.querySelectorAll('.difficult').forEach(char => {
                    char.addEventListener('click', (e) => {
                        e.preventDefault();
                        this.showMobileTooltip(char);
                    });
                });
            }
        },

        showMobileTooltip(element) {
            const pinyin = element.dataset.pinyin;
            const meaning = element.dataset.meaning;

            // 移除之前的提示
            document.querySelectorAll('.mobile-tooltip').forEach(t => t.remove());

            const tooltip = document.createElement('div');
            tooltip.className = 'mobile-tooltip';
            tooltip.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(44, 24, 16, 0.95);
                color: white;
                padding: 16px 24px;
                border-radius: 8px;
                z-index: 9999;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            `;
            tooltip.innerHTML = `
                <div style="font-size: 24px; margin-bottom: 8px;">${pinyin}</div>
                <div style="font-size: 14px; opacity: 0.8;">${meaning}</div>
                <button style="margin-top: 12px; padding: 4px 12px; background: var(--accent-color); border: none; border-radius: 4px; color: white;">关闭</button>
            `;

            tooltip.querySelector('button').addEventListener('click', () => tooltip.remove());
            document.body.appendChild(tooltip);

            // 3秒后自动关闭
            setTimeout(() => tooltip.remove(), 3000);
        }
    };

    // ==================== 应用初始化 ====================
    function init() {
        console.log('[App] 开始初始化, readyState:', document.readyState);
        console.log('[App] 当前页面:', window.location.pathname);

        // 初始化各模块（只初始化本文件中定义的管理器）
        const modules = [
            { name: 'SearchManager', init: () => SearchManager?.init() },
            { name: 'ProgressManager', init: () => ProgressManager?.init() },
            { name: 'CopyManager', init: () => CopyManager?.init() },
            { name: 'QuoteCardManager', init: () => QuoteCardManager?.init() },
            { name: 'SpeechManager', init: () => SpeechManager?.init() },
            { name: 'SettingsManager', init: () => SettingsManager?.init() },
            { name: 'ShareManager', init: () => ShareManager?.init() },
            { name: 'AIManager', init: () => AIManager?.init() },
            { name: 'DifficultCharManager', init: () => DifficultCharManager?.init() }
        ];

        modules.forEach(module => {
            try {
                console.log('[App] 初始化模块:', module.name);
                module.init();
            } catch (e) {
                console.warn(`模块 ${module.name} 初始化失败:`, e);
            }
        });

        console.log('[App] 道德经应用初始化完成');
    }

    // 等待 DOM 加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // 导出到全局
    window.DaoDeJingApp = {
        SearchManager,
        ProgressManager,
        CopyManager,
        QuoteCardManager,
        SpeechManager,
        SettingsManager,
        ShareManager,
        AIManager,
        DifficultCharManager,
        init
    };

    // 兼容性别名
    window.SearchManager = SearchManager;
    window.ProgressManager = ProgressManager;
    window.CopyManager = CopyManager;
    window.QuoteCardManager = QuoteCardManager;
    window.SpeechManager = SpeechManager;
    window.SettingsManager = SettingsManager;
    window.ShareManager = ShareManager;
    window.AIManager = AIManager;

})();
