/**
 * 道德经多版本对照平台 - 主脚本文件
 * 功能：暗黑模式切换、侧边栏、搜索、键盘导航
 */

(function() {
    'use strict';

    // ==================== 暗黑模式管理 ====================
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

    // ==================== 侧边栏管理 ====================
    const SidebarManager = {
        init() {
            this.sidebar = document.getElementById('sidebar');
            this.toggleBtn = document.getElementById('sidebarToggle');
            this.overlay = null;

            if (!this.sidebar || !this.toggleBtn) return;

            this.createOverlay();
            this.bindEvents();
        },

        createOverlay() {
            this.overlay = document.createElement('div');
            this.overlay.className = 'sidebar-overlay';
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
        }
    };

    // ==================== 搜索功能 ====================
    const SearchManager = {
        API_ENDPOINT: '/api/daodejing/search',
        DEBOUNCE_DELAY: 300,

        init() {
            this.searchInput = document.getElementById('searchInput');
            this.searchModal = document.getElementById('searchModal');
            this.searchResults = document.getElementById('searchResults');
            this.debounceTimer = null;

            if (!this.searchInput) return;

            this.bindEvents();
        },

        bindEvents() {
            // 输入事件（带防抖）
            this.searchInput.addEventListener('input', (e) => {
                clearTimeout(this.debounceTimer);
                this.debounceTimer = setTimeout(() => {
                    this.search(e.target.value);
                }, this.DEBOUNCE_DELAY);
            });

            // 回车键直接搜索
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    clearTimeout(this.debounceTimer);
                    this.search(e.target.value);
                    this.showModal();
                }
            });

            // Escape 键清空
            this.searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.searchInput.value = '';
                    this.searchInput.blur();
                }
            });
        },

        async search(query) {
            if (!query || query.trim().length < 1) {
                return;
            }

            try {
                const response = await fetch(`${this.API_ENDPOINT}?q=${encodeURIComponent(query)}`);
                const data = await response.json();
                this.displayResults(data.results);
                if (data.results.length > 0) {
                    this.showModal();
                }
            } catch (error) {
                console.error('搜索失败:', error);
            }
        },

        displayResults(results) {
            if (results.length === 0) {
                this.searchResults.innerHTML = '<p class="text-muted text-center">未找到相关内容</p>';
                return;
            }

            this.searchResults.innerHTML = results.map(result => `
                <div class="search-result-item" onclick="location.href='/daodejing/chapter/${result.id}'">
                    <h6 class="mb-1">${result.title}</h6>
                    <p class="small text-muted mb-0">${result.excerpt}</p>
                </div>
            `).join('');
        },

        showModal() {
            if (!this.searchModal) return;
            const modal = new bootstrap.Modal(this.searchModal);
            modal.show();
        }
    };

    // ==================== 音乐播放管理 ====================
    const MusicManager = {
        STORAGE_KEY: 'daodejing_music_volume',
        DEFAULT_VOLUME: 0.3,

        init() {
            this.audio = document.getElementById('bgMusic');
            this.toggleBtn = document.getElementById('musicToggle');
            this.loopBtn = document.getElementById('musicLoop');
            this.volumePanel = document.getElementById('volumePanel');
            this.volumeSlider = document.getElementById('volumeSlider');
            this.volumeValue = document.getElementById('volumeValue');
            this.closeVolumeBtn = document.getElementById('closeVolumePanel');

            if (!this.audio || !this.toggleBtn) return;

            // 加载保存的音量
            const savedVolume = localStorage.getItem(this.STORAGE_KEY);
            this.volume = savedVolume ? parseFloat(savedVolume) : this.DEFAULT_VOLUME;
            this.audio.volume = this.volume;

            // 更新滑块显示
            if (this.volumeSlider) {
                this.volumeSlider.value = this.volume * 100;
                this.volumeValue.textContent = Math.round(this.volume * 100);
            }

            this.bindEvents();
        },

        bindEvents() {
            // 播放/暂停
            this.toggleBtn.addEventListener('click', () => this.toggle());

            // 循环按钮
            if (this.loopBtn) {
                this.loopBtn.addEventListener('click', () => this.toggleLoop());
            }

            // 音量滑块
            if (this.volumeSlider) {
                this.volumeSlider.addEventListener('input', (e) => {
                    this.setVolume(e.target.value / 100);
                });
            }

            // 关闭音量面板
            if (this.closeVolumeBtn) {
                this.closeVolumeBtn.addEventListener('click', () => {
                    this.volumePanel.classList.remove('show');
                });
            }

            // 点击外部关闭面板
            document.addEventListener('click', (e) => {
                if (this.volumePanel && this.volumePanel.classList.contains('show')) {
                    if (!this.volumePanel.contains(e.target) && !this.toggleBtn.contains(e.target)) {
                        this.volumePanel.classList.remove('show');
                    }
                }
            });

            // 右键点击音乐按钮打开音量面板
            this.toggleBtn.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                this.volumePanel.classList.toggle('show');
            });

            // 音频事件
            this.audio.addEventListener('play', () => this.updateState());
            this.audio.addEventListener('pause', () => this.updateState());
            this.audio.addEventListener('ended', () => this.updateState());
        },

        toggle() {
            if (this.audio.paused) {
                this.audio.play().then(() => {
                    this.updateState();
                }).catch(err => {
                    console.warn('自动播放被阻止，需要用户交互:', err);
                });
            } else {
                this.audio.pause();
                this.updateState();
            }
        },

        setVolume(value) {
            this.volume = Math.max(0, Math.min(1, value));
            this.audio.volume = this.volume;
            localStorage.setItem(this.STORAGE_KEY, this.volume);
            if (this.volumeValue) {
                this.volumeValue.textContent = Math.round(this.volume * 100);
            }
        },

        toggleLoop() {
            this.audio.loop = !this.audio.loop;
            this.updateState();
        },

        updateState() {
            const icon = this.toggleBtn.querySelector('.music-icon');
            if (!this.audio.paused) {
                icon.classList.add('playing');
                this.toggleBtn.classList.add('active');
                if (this.loopBtn) {
                    this.loopBtn.classList.remove('d-none');
                }
            } else {
                icon.classList.remove('playing');
                this.toggleBtn.classList.remove('active');
                if (this.loopBtn) {
                    this.loopBtn.classList.add('d-none');
                }
            }

            // 更新循环按钮状态
            if (this.loopBtn && !this.loopBtn.classList.contains('d-none')) {
                const loopIcon = this.loopBtn.querySelector('.loop-icon');
                loopIcon.textContent = this.audio.loop ? '🔁' : '🔂';
            }
        }
    };

    // ==================== 朗读管理 ====================
    const SpeechManager = {
        STORAGE_KEY: 'daodejing_speech_rate',
        DEFAULT_RATE: 0.8,

        init() {
            this.toggleBtn = document.getElementById('speechToggle');
            this.stopBtn = document.getElementById('speechStop');
            this.speechPanel = document.getElementById('speechPanel');
            this.closeSpeechBtn = document.getElementById('closeSpeechPanel');
            this.speechRate = document.getElementById('speechRate');
            this.rateValue = document.getElementById('rateValue');
            this.speechStatus = document.getElementById('speechStatus');

            // 检查浏览器支持
            if (!('speechSynthesis' in window)) {
                if (this.toggleBtn) {
                    this.toggleBtn.disabled = true;
                    this.toggleBtn.title = '您的浏览器不支持朗读功能';
                }
                return;
            }

            // 加载保存的语速
            const savedRate = localStorage.getItem(this.STORAGE_KEY);
            this.rate = savedRate ? parseFloat(savedRate) : this.DEFAULT_RATE;

            if (this.speechRate) {
                this.speechRate.value = this.rate * 100;
                this.rateValue.textContent = this.rate.toFixed(1);
            }

            this.synth = window.speechSynthesis;
            this.currentUtterance = null;
            this.isPaused = false;
            this.currentChapter = 1;
            this.speechMode = 'current'; // 'current' or 'all'

            this.bindEvents();
        },

        bindEvents() {
            if (!this.toggleBtn) return;

            // 朗读按钮
            this.toggleBtn.addEventListener('click', () => this.toggle());

            // 停止按钮
            if (this.stopBtn) {
                this.stopBtn.addEventListener('click', () => this.stop());
            }

            // 语速滑块
            if (this.speechRate) {
                this.speechRate.addEventListener('input', (e) => {
                    this.setRate(e.target.value / 100);
                });
            }

            // 关闭面板
            if (this.closeSpeechBtn) {
                this.closeSpeechBtn.addEventListener('click', () => {
                    this.speechPanel.classList.remove('show');
                });
            }

            // 点击外部关闭面板
            document.addEventListener('click', (e) => {
                if (this.speechPanel && this.speechPanel.classList.contains('show')) {
                    if (!this.speechPanel.contains(e.target) && !this.toggleBtn.contains(e.target)) {
                        this.speechPanel.classList.remove('show');
                    }
                }
            });

            // 右键打开面板
            this.toggleBtn.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                this.speechPanel.classList.toggle('show');
            });

            // 朗读模式切换
            const modeInputs = document.querySelectorAll('input[name="speechMode"]');
            modeInputs.forEach(input => {
                input.addEventListener('change', (e) => {
                    this.speechMode = e.target.value;
                });
            });
        },

        toggle() {
            if (this.synth.speaking) {
                if (this.isPaused) {
                    this.resume();
                } else {
                    this.pause();
                }
            } else {
                this.start();
            }
        },

        start() {
            // 获取当前章节原文
            const originalText = document.getElementById('originalText');
            if (!originalText) {
                this.setStatus('无法找到原文内容', false);
                return;
            }

            // 清理文本（移除HTML标签）
            const text = this.cleanText(originalText.textContent);
            if (!text) {
                this.setStatus('原文内容为空', false);
                return;
            }

            // 获取当前章节号
            const breadcrumb = document.querySelector('.breadcrumb .active');
            if (breadcrumb) {
                const match = breadcrumb.textContent.match(/第(\d+)章/);
                if (match) {
                    this.currentChapter = parseInt(match[1]);
                }
            }

            this.speak(text);
        },

        speak(text) {
            this.stop(); // 先停止之前的朗读

            this.currentUtterance = new SpeechSynthesisUtterance(text);
            this.currentUtterance.lang = 'zh-CN';
            this.currentUtterance.rate = this.rate;
            this.currentUtterance.pitch = 1;

            this.currentUtterance.onstart = () => {
                this.updateState();
                this.setStatus(`正在朗读第${this.currentChapter}章`, true);
            };

            this.currentUtterance.onend = () => {
                if (this.speechMode === 'all' && this.currentChapter < 81 && !this.isPaused) {
                    // 继续下一章
                    this.nextChapter();
                } else {
                    this.updateState();
                    this.setStatus('朗读完成', false);
                }
            };

            this.currentUtterance.onerror = (event) => {
                // interrupted 和 canceled 是正常情况（切换章节、手动停止），不显示为错误
                if (event.error !== 'interrupted' && event.error !== 'canceled') {
                    console.error('朗读错误:', event.error);
                    this.setStatus('朗读出错: ' + event.error, false);
                }
                this.updateState();
            };

            this.synth.speak(this.currentUtterance);
        },

        pause() {
            if (this.synth.speaking && !this.isPaused) {
                this.synth.pause();
                this.isPaused = true;
                this.updateState();
                this.setStatus('已暂停', false);
            }
        },

        resume() {
            if (this.isPaused) {
                this.synth.resume();
                this.isPaused = false;
                this.updateState();
                this.setStatus('正在朗读...', true);
            }
        },

        stop() {
            this.synth.cancel();
            this.isPaused = false;
            this.updateState();
            this.setStatus('已停止', false);
        },

        nextChapter() {
            this.currentChapter++;
            // 跳转到下一章
            const nextLink = document.querySelector(`.chapter-item[data-chapter="${this.currentChapter}"]`);
            if (nextLink) {
                nextLink.click();
                // 等待页面加载后继续朗读
                setTimeout(() => {
                    this.start();
                }, 500);
            }
        },

        setRate(value) {
            this.rate = Math.max(0.5, Math.min(1.5, value));
            localStorage.setItem(this.STORAGE_KEY, this.rate);
            if (this.rateValue) {
                this.rateValue.textContent = this.rate.toFixed(1);
            }
        },

        cleanText(text) {
            // 移除多余空白和标点符号之间的空格
            return text
                .replace(/\s+/g, '')
                .replace(/([，。；：！？、])/g, '$1 ')
                .trim();
        },

        setStatus(text, isActive) {
            if (this.speechStatus) {
                this.speechStatus.textContent = text;
                if (isActive) {
                    this.speechStatus.classList.add('active');
                } else {
                    this.speechStatus.classList.remove('active');
                }
            }
        },

        updateState() {
            const icon = this.toggleBtn.querySelector('.speech-icon');
            const isSpeaking = this.synth.speaking && !this.isPaused;

            if (isSpeaking) {
                icon.classList.add('speaking');
                this.toggleBtn.classList.add('active');
                if (this.stopBtn) {
                    this.stopBtn.classList.remove('d-none');
                }
            } else {
                icon.classList.remove('speaking');
                this.toggleBtn.classList.remove('active');
                if (this.stopBtn) {
                    this.stopBtn.classList.add('d-none');
                }
            }
        }
    };

    // ==================== 滚动高亮目录 ====================
    const ScrollHighlight = {
        init() {
            this.sidebar = document.getElementById('sidebar');
            this.chapterItems = document.querySelectorAll('.chapter-item');

            if (this.chapterItems.length === 0) return;

            // 使用 Intersection Observer
            this.setupObserver();
        },

        setupObserver() {
            const options = {
                root: null,
                rootMargin: '-20% 0px -60% 0px',
                threshold: 0
            };

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const id = entry.target.dataset.chapter;
                        this.highlightChapter(id);
                    }
                });
            }, options);

            // 观察所有章节内容
            document.querySelectorAll('.original-text, .original-section').forEach(el => {
                this.observer.observe(el);
            });
        },

        highlightChapter(chapterId) {
            this.chapterItems.forEach(item => {
                item.classList.remove('active');
                if (item.dataset.chapter == chapterId) {
                    item.classList.add('active');
                    // 滚动目录到可见区域
                    item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
            });
        }
    };

    // ==================== 设置管理 ====================
    const SettingsManager = {
        // 存储键
        STORAGE_KEY: 'daodejing_settings',

        // 默认设置
        defaults: {
            mode: 'reading',      // reading, zen, recite
            font: 'default',      // default, kaiti, songti, fangsong, mingliu, xkai
            fontSize: 'medium',   // small, medium, large
            textLayout: 'center', // center, left
            musicType: 'none',    // none, chinese, western
            musicVolume: 30,
            showPinyin: true,
            showAnnotation: true,
            showModern: true,
            showNotes: true,
            showEnglish: false
        },

        // 当前设置
        settings: {},

        // 当前音乐索引
        currentMusicIndex: 0,

        init() {
            this.settingsBtn = document.getElementById('settingsToggle');
            this.settingsPanel = document.getElementById('settingsPanel');
            this.closeSettingsBtn = document.getElementById('closeSettingsPanel');
            this.zenOverlay = document.getElementById('zenModeOverlay');
            this.zenExitBtn = document.getElementById('zenExitBtn');

            if (!this.settingsBtn) return;

            // 加载保存的设置
            this.loadSettings();

            // 从URL参数加载设置
            this.loadFromURL();

            // 应用设置
            this.applySettings();

            // 绑定事件
            this.bindEvents();
        },

        bindEvents() {
            // 打开设置面板
            this.settingsBtn.addEventListener('click', () => this.togglePanel());

            // 关闭设置面板
            if (this.closeSettingsBtn) {
                this.closeSettingsBtn.addEventListener('click', () => this.closePanel());
            }

            // 点击外部关闭
            document.addEventListener('click', (e) => {
                if (this.settingsPanel && this.settingsPanel.classList.contains('show')) {
                    if (!this.settingsPanel.contains(e.target) && !this.settingsBtn.contains(e.target)) {
                        this.closePanel();
                    }
                }
            });

            // 阅读模式切换
            const modeBtns = this.settingsPanel?.querySelectorAll('.mode-btn');
            modeBtns?.forEach(btn => {
                btn.addEventListener('click', () => {
                    const mode = btn.dataset.mode;
                    this.setMode(mode);
                });
            });

            // 字体选择
            const fontSelect = document.getElementById('fontSelect');
            if (fontSelect) {
                fontSelect.addEventListener('change', (e) => {
                    this.setFont(e.target.value);
                });
            }

            // 字体大小
            const sizeBtns = this.settingsPanel?.querySelectorAll('.size-btn');
            sizeBtns?.forEach(btn => {
                btn.addEventListener('click', () => {
                    const size = btn.dataset.size;
                    this.setFontSize(size);
                });
            });

            // 文字布局
            const layoutBtns = this.settingsPanel?.querySelectorAll('.layout-btn');
            layoutBtns?.forEach(btn => {
                btn.addEventListener('click', () => {
                    const layout = btn.dataset.layout;
                    this.setTextLayout(layout);
                });
            });

            // 音乐类型选择
            const musicSelect = document.getElementById('musicSelect');
            if (musicSelect) {
                musicSelect.addEventListener('change', (e) => {
                    this.setMusicType(e.target.value);
                });
            }

            // 音乐音量
            const volumeSlider = document.getElementById('musicVolumeSlider');
            const volumeValue = document.getElementById('musicVolumeValue');
            if (volumeSlider) {
                volumeSlider.addEventListener('input', (e) => {
                    this.setMusicVolume(e.target.value);
                    if (volumeValue) {
                        volumeValue.textContent = e.target.value + '%';
                    }
                });
            }

            // 显示选项
            const showPinyin = document.getElementById('showPinyin');
            const showAnnotation = document.getElementById('showAnnotation');
            if (showPinyin) {
                showPinyin.addEventListener('change', (e) => {
                    this.setShowPinyin(e.target.checked);
                });
            }
            if (showAnnotation) {
                showAnnotation.addEventListener('change', (e) => {
                    this.setShowAnnotation(e.target.checked);
                });
            }

            // 版本显示
            const showModern = document.getElementById('showModern');
            const showNotes = document.getElementById('showNotes');
            const showEnglish = document.getElementById('showEnglish');
            if (showModern) {
                showModern.addEventListener('change', (e) => {
                    this.setShowModern(e.target.checked);
                });
            }
            if (showNotes) {
                showNotes.addEventListener('change', (e) => {
                    this.setShowNotes(e.target.checked);
                });
            }
            if (showEnglish) {
                showEnglish.addEventListener('change', (e) => {
                    this.setShowEnglish(e.target.checked);
                });
            }

            // 退出禅读模式
            if (this.zenExitBtn) {
                this.zenExitBtn.addEventListener('click', () => {
                    this.exitZenMode();
                });
            }

            // ESC键关闭面板/退出禅读
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    if (this.zenOverlay?.classList.contains('active')) {
                        this.exitZenMode();
                    } else if (this.settingsPanel?.classList.contains('show')) {
                        this.closePanel();
                    }
                }
            });

            // 分享设置
            const shareBtn = document.getElementById('shareSettings');
            if (shareBtn) {
                shareBtn.addEventListener('click', () => this.shareSettings());
            }
        },

        togglePanel() {
            this.settingsPanel.classList.toggle('show');
        },

        closePanel() {
            this.settingsPanel.classList.remove('show');
        },

        loadSettings() {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            if (saved) {
                try {
                    this.settings = { ...this.defaults, ...JSON.parse(saved) };
                } catch (e) {
                    this.settings = { ...this.defaults };
                }
            } else {
                this.settings = { ...this.defaults };
            }
        },

        saveSettings() {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.settings));
        },

        loadFromURL() {
            const params = new URLSearchParams(window.location.search);
            const config = params.get('config');
            if (config) {
                try {
                    const urlSettings = JSON.parse(atob(config));
                    this.settings = { ...this.settings, ...urlSettings };
                    this.saveSettings();
                } catch (e) {
                    console.error('解析URL配置失败:', e);
                }
            }
        },

        applySettings() {
            // 应用模式
            this.setMode(this.settings.mode, false);
            // 应用字体
            this.setFont(this.settings.font, false);
            // 应用字体大小
            this.setFontSize(this.settings.fontSize, false);
            // 应用文字布局
            this.setTextLayout(this.settings.textLayout, false);
            // 应用音乐类型
            this.setMusicType(this.settings.musicType, false);
            // 应用音乐音量
            this.setMusicVolume(this.settings.musicVolume, false);
            // 应用显示选项
            this.setShowPinyin(this.settings.showPinyin, false);
            this.setShowAnnotation(this.settings.showAnnotation, false);
            this.setShowModern(this.settings.showModern, false);
            this.setShowNotes(this.settings.showNotes, false);
            this.setShowEnglish(this.settings.showEnglish, false);

            // 更新UI状态
            this.updateUIState();
        },

        updateUIState() {
            // 更新模式按钮
            const modeBtns = this.settingsPanel?.querySelectorAll('.mode-btn');
            modeBtns?.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.mode === this.settings.mode);
            });

            // 更新字体选择
            const fontSelect = document.getElementById('fontSelect');
            if (fontSelect) {
                fontSelect.value = this.settings.font;
            }

            // 更新字体大小按钮
            const sizeBtns = this.settingsPanel?.querySelectorAll('.size-btn');
            sizeBtns?.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.size === this.settings.fontSize);
            });

            // 更新布局按钮
            const layoutBtns = this.settingsPanel?.querySelectorAll('.layout-btn');
            layoutBtns?.forEach(btn => {
                btn.classList.toggle('active', btn.dataset.layout === this.settings.textLayout);
            });

            // 更新音乐选择
            const musicSelect = document.getElementById('musicSelect');
            if (musicSelect) {
                musicSelect.value = this.settings.musicType;
            }

            // 更新音量滑块
            const volumeSlider = document.getElementById('musicVolumeSlider');
            const volumeValue = document.getElementById('musicVolumeValue');
            if (volumeSlider) {
                volumeSlider.value = this.settings.musicVolume;
            }
            if (volumeValue) {
                volumeValue.textContent = this.settings.musicVolume + '%';
            }

            // 更新复选框
            const showPinyin = document.getElementById('showPinyin');
            const showAnnotation = document.getElementById('showAnnotation');
            const showModern = document.getElementById('showModern');
            const showNotes = document.getElementById('showNotes');
            const showEnglish = document.getElementById('showEnglish');

            if (showPinyin) showPinyin.checked = this.settings.showPinyin;
            if (showAnnotation) showAnnotation.checked = this.settings.showAnnotation;
            if (showModern) showModern.checked = this.settings.showModern;
            if (showNotes) showNotes.checked = this.settings.showNotes;
            if (showEnglish) showEnglish.checked = this.settings.showEnglish;
        },

        setMode(mode, save = true) {
            this.settings.mode = mode;
            if (save) this.saveSettings();

            const body = document.body;
            body.classList.remove('mode-reading', 'mode-zen', 'mode-recite');
            body.classList.add(`mode-${mode}`);

            // 禅读模式特殊处理
            if (mode === 'zen') {
                this.enterZenMode();
            } else {
                this.exitZenMode();
            }

            // 背诵模式：隐藏译文和注解
            if (mode === 'recite') {
                body.classList.add('hide-modern', 'hide-notes', 'hide-english');
            } else {
                body.classList.remove('hide-modern', 'hide-notes', 'hide-english');
            }

            this.updateUIState();
        },

        setFont(font, save = true) {
            this.settings.font = font;
            if (save) this.saveSettings();

            const body = document.body;
            body.classList.remove('font-default', 'font-kaiti', 'font-songti', 'font-fangsong', 'font-mingliu', 'font-xkai');
            body.classList.add(`font-${font}`);

            this.updateUIState();
        },

        setFontSize(size, save = true) {
            this.settings.fontSize = size;
            if (save) this.saveSettings();

            const body = document.body;
            body.classList.remove('font-size-small', 'font-size-medium', 'font-size-large');
            body.classList.add(`font-size-${size}`);

            this.updateUIState();
        },

        setTextLayout(layout, save = true) {
            this.settings.textLayout = layout;
            if (save) this.saveSettings();

            const body = document.body;
            body.classList.remove('text-layout-center', 'text-layout-left');
            body.classList.add(`text-layout-${layout}`);

            this.updateUIState();
        },

        setMusicType(type, save = true) {
            this.settings.musicType = type;
            if (save) this.saveSettings();

            const audio = document.getElementById('bgMusic');
            if (!audio) return;

            // 停止当前播放
            const wasPlaying = !audio.paused;
            audio.pause();

            if (type === 'none') {
                audio.removeAttribute('src');
                this.updateUIState();
                return;
            }

            // 获取音乐列表
            const tracks = window.musicTracks?.[type] || [];
            if (tracks.length === 0) return;

            // 设置新的音频源
            this.currentMusicIndex = Math.floor(Math.random() * tracks.length);
            audio.src = tracks[this.currentMusicIndex];
            audio.load();

            // 如果之前在播放，重新开始播放
            if (wasPlaying) {
                audio.play().catch(err => {
                    console.warn('自动播放被阻止:', err);
                });
            }

            this.updateUIState();
        },

        setMusicVolume(volume, save = true) {
            this.settings.musicVolume = parseInt(volume);
            if (save) this.saveSettings();

            const audio = document.getElementById('bgMusic');
            if (audio) {
                audio.volume = this.settings.musicVolume / 100;
            }
        },

        setShowPinyin(show, save = true) {
            this.settings.showPinyin = show;
            if (save) this.saveSettings();

            const body = document.body;
            if (show) {
                body.classList.remove('hide-pinyin');
            } else {
                body.classList.add('hide-pinyin');
            }

            this.updateUIState();
        },

        setShowAnnotation(show, save = true) {
            this.settings.showAnnotation = show;
            if (save) this.saveSettings();

            const body = document.body;
            if (show) {
                body.classList.remove('hide-annotation');
            } else {
                body.classList.add('hide-annotation');
            }

            this.updateUIState();
        },

        setShowModern(show, save = true) {
            this.settings.showModern = show;
            if (save) this.saveSettings();

            const body = document.body;
            if (show) {
                body.classList.remove('hide-modern');
            } else {
                body.classList.add('hide-modern');
            }

            this.updateUIState();
        },

        setShowNotes(show, save = true) {
            this.settings.showNotes = show;
            if (save) this.saveSettings();

            const body = document.body;
            if (show) {
                body.classList.remove('hide-notes');
            } else {
                body.classList.add('hide-notes');
            }

            this.updateUIState();
        },

        setShowEnglish(show, save = true) {
            this.settings.showEnglish = show;
            if (save) this.saveSettings();

            const body = document.body;
            if (show) {
                body.classList.remove('hide-english');
            } else {
                body.classList.add('hide-english');
            }

            this.updateUIState();
        },

        enterZenMode() {
            // 获取当前章节原文
            const originalText = document.querySelector('.original-text');
            if (!originalText) return;

            // 复制原文内容到禅读遮罩
            const content = originalText.innerHTML;
            this.zenOverlay.innerHTML = `
                <button class="zen-exit-btn" id="zenExitBtn">退出禅读</button>
                <div class="zen-content">
                    <div class="original-text">${content}</div>
                </div>
            `;

            // 绑定退出按钮
            this.zenOverlay.querySelector('#zenExitBtn').addEventListener('click', () => {
                this.exitZenMode();
            });

            // 显示禅读模式
            this.zenOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        },

        exitZenMode() {
            this.zenOverlay.classList.remove('active');
            document.body.style.overflow = '';

            // 如果当前不是禅读模式，切换回阅读模式
            if (this.settings.mode === 'zen') {
                // 保持设置但退出禅读视图
            }
        },

        shareSettings() {
            const config = btoa(JSON.stringify(this.settings));
            const url = `${window.location.origin}${window.location.pathname}?config=${config}`;

            // 复制到剪贴板
            navigator.clipboard.writeText(url).then(() => {
                // 显示提示
                const shareBtn = document.getElementById('shareSettings');
                const originalText = shareBtn.innerHTML;
                shareBtn.innerHTML = '<span>✓</span> 已复制链接';
                setTimeout(() => {
                    shareBtn.innerHTML = originalText;
                }, 2000);
            }).catch(() => {
                alert('分享链接：' + url);
            });
        }
    };

    // ==================== 分享管理 ====================
    const ShareManager = {
        init() {
            this.shareBtn = document.getElementById('shareToggle');
            this.supportBtn = document.getElementById('supportBtn');
            this.communityBtn = document.getElementById('communityBtn');
            this.shareModal = document.getElementById('shareModal');
            this.shareUrlInput = document.getElementById('shareUrlInput');

            if (!this.shareBtn) return;

            this.bindEvents();
        },

        bindEvents() {
            // 分享按钮
            this.shareBtn?.addEventListener('click', () => this.openShareModal());

            // 赞赏按钮
            this.supportBtn?.addEventListener('click', () => {
                const modal = new bootstrap.Modal(document.getElementById('supportModal'));
                modal.show();
            });

            // 社群按钮
            this.communityBtn?.addEventListener('click', () => {
                const modal = new bootstrap.Modal(document.getElementById('communityModal'));
                modal.show();
            });

            // 微信分享
            document.getElementById('shareWechat')?.addEventListener('click', () => {
                this.shareToWechat();
            });

            // 微博分享
            document.getElementById('shareWeibo')?.addEventListener('click', () => {
                this.shareToWeibo();
            });

            // 复制链接
            document.getElementById('shareLink')?.addEventListener('click', () => {
                this.copyLink();
            });
        },

        openShareModal() {
            if (!this.shareModal) return;

            // 更新链接输入框
            const shareUrl = window.location.href.split('?')[0];
            if (this.shareUrlInput) {
                this.shareUrlInput.value = shareUrl;
            }

            const modal = new bootstrap.Modal(this.shareModal);
            modal.show();
        },

        shareToWechat() {
            // 微信需要用户手动截图或复制链接
            const shareUrl = window.location.href.split('?')[0];
            const title = '道德经多版本对照阅读平台';
            const text = `《道德经》81章完整版，支持王弼、河上公、王夫之、帛书、楚简多版本对照，疑难字注音，暗黑模式。`;

            // 显示提示
            alert(`请复制链接在微信中分享：\n${shareUrl}\n\n${text}`);
        },

        shareToWeibo() {
            const shareUrl = encodeURIComponent(window.location.href.split('?')[0]);
            const title = encodeURIComponent('道德经多版本对照阅读平台 - 王弼·河上公·王夫之·帛书·英文译本');
            const text = encodeURIComponent('《道德经》81章完整版，支持多版本对照，疑难字注音，暗黑模式，手机阅读。');

            window.open(`https://service.weibo.com/share/share.php?url=${shareUrl}&title=${title}&pic=`, '_blank');
        },

        copyLink() {
            const shareUrl = window.location.href.split('?')[0];
            const title = '道德经多版本对照阅读平台';
            const text = `《道德经》81章完整版，支持王弼、河上公、王夫之、帛书、楚简多版本对照。`;

            navigator.clipboard.writeText(`${title}\n${text}\n${shareUrl}`).then(() => {
                // 显示提示
                const shareBtn = document.getElementById('shareLink');
                const originalHTML = shareBtn.innerHTML;
                shareBtn.innerHTML = '<span class="share-icon">✓</span><span>已复制</span>';
                setTimeout(() => {
                    shareBtn.innerHTML = originalHTML;
                }, 2000);
            }).catch(() => {
                // 备用方案
                const textArea = document.createElement('textarea');
                textArea.value = `${title}\n${text}\n${shareUrl}`;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('链接已复制！');
            });
        }
    };

    // ==================== 初始化 ====================
    document.addEventListener('DOMContentLoaded', () => {
        ThemeManager.init();
        SidebarManager.init();
        SearchManager.init();
        MusicManager.init();
        SpeechManager.init();
        ScrollHighlight.init();
        SettingsManager.init();
        ShareManager.init();
    });

})();
