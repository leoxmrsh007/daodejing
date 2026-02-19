// 设置面板控制
(function() {
    'use strict';

    // 等待DOM加载完成
    document.addEventListener('DOMContentLoaded', function() {
        // 从URL参数恢复设置
        loadSettingsFromUrl();

        initSpeechVoiceSelect();

        if (window.SettingsManager && typeof window.SettingsManager.init === 'function') {
            return;
        }

        initSettingsPanel();
        initFunctionButtons();
    });

    // 从URL参数加载设置
    function loadSettingsFromUrl() {
        const params = new URLSearchParams(window.location.search);

        if (params.has('font')) {
            localStorage.setItem('daodejing_font', params.get('font'));
        }
        if (params.has('fontSize')) {
            localStorage.setItem('daodejing_font_size', params.get('fontSize'));
        }
        if (params.has('layout')) {
            localStorage.setItem('daodejing_text_layout', params.get('layout'));
        }
        if (params.has('mode')) {
            localStorage.setItem('daodejing_reading_mode', params.get('mode'));
        }
        if (params.has('showModern')) {
            localStorage.setItem('daodejing_show_modern', params.get('showModern'));
        }
        if (params.has('showNotes')) {
            localStorage.setItem('daodejing_show_notes', params.get('showNotes'));
        }
        if (params.has('showPinyin')) {
            localStorage.setItem('daodejing_show_pinyin', params.get('showPinyin'));
        }
        if (params.has('showAnnotation')) {
            localStorage.setItem('daodejing_show_annotation', params.get('showAnnotation'));
        }
        if (params.has('showEnglish')) {
            localStorage.setItem('daodejing_show_english', params.get('showEnglish'));
        }
        if (params.has('voiceLanguage')) {
            localStorage.setItem('daodejing_voice_language', params.get('voiceLanguage'));
        }

        // 清除URL参数
        if (params.toString()) {
            const cleanUrl = window.location.pathname;
            window.history.replaceState({}, document.title, cleanUrl);
        }
    }

    // 初始化设置面板
    function initSettingsPanel() {
        const settingsToggle = document.getElementById('settingsToggle');
        const settingsPanel = document.getElementById('settingsPanel');
        const closeSettingsPanel = document.getElementById('closeSettingsPanel');

        if (!settingsToggle || !settingsPanel) {
            console.warn('设置面板元素未找到');
            return;
        }

        // 打开设置面板
        settingsToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            settingsPanel.classList.add('show');
            console.log('设置面板已打开');
        });

        // 关闭设置面板
        if (closeSettingsPanel) {
            closeSettingsPanel.addEventListener('click', function() {
                settingsPanel.classList.remove('show');
                console.log('设置面板已关闭');
            });
        }

        // 点击面板外部关闭
        document.addEventListener('click', function(e) {
            if (settingsPanel.classList.contains('show') &&
                !settingsPanel.contains(e.target) &&
                !settingsToggle.contains(e.target)) {
                settingsPanel.classList.remove('show');
            }
        });

        // ===== 阅读模式 =====
        const modeBtns = document.querySelectorAll('.mode-btn');
        modeBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const mode = this.dataset.mode;
                modeBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                localStorage.setItem('daodejing_reading_mode', mode);

                // 应用阅读模式
                applyReadingMode(mode);
                console.log('阅读模式已切换为:', mode);
            });
        });

        // 恢复保存的阅读模式
        const savedMode = localStorage.getItem('daodejing_reading_mode');
        if (savedMode) {
            modeBtns.forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.mode === savedMode) {
                    btn.classList.add('active');
                    applyReadingMode(savedMode);
                }
            });
        }

        // ===== 文字布局 =====
        const layoutBtns = document.querySelectorAll('.layout-btn');
        layoutBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const layout = this.dataset.layout;
                layoutBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                localStorage.setItem('daodejing_text_layout', layout);

                // 应用布局
                document.body.classList.remove('text-layout-center', 'text-layout-left');
                document.body.classList.add('text-layout-' + layout);
                console.log('文字布局已切换为:', layout);
            });
        });

        // 恢复保存的布局
        const savedLayout = localStorage.getItem('daodejing_text_layout') || localStorage.getItem('daodejing_layout');
        if (savedLayout) {
            layoutBtns.forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.layout === savedLayout) {
                    btn.classList.add('active');
                    document.body.classList.remove('text-layout-center', 'text-layout-left');
                    document.body.classList.add('text-layout-' + savedLayout);
                }
            });
        }

        // ===== 字体选择 =====
        const fontSelect = document.getElementById('fontSelect');
        if (fontSelect) {
            fontSelect.addEventListener('change', function() {
                const font = this.value;
                document.body.className = document.body.className.replace(/font-\w+/g, '');
                if (font !== 'default') {
                    document.body.classList.add('font-' + font);
                }
                localStorage.setItem('daodejing_font', font);
                console.log('字体已切换为:', font);
            });

            // 恢复保存的字体设置
            const savedFont = localStorage.getItem('daodejing_font');
            if (savedFont) {
                fontSelect.value = savedFont;
                if (savedFont !== 'default') {
                    document.body.classList.add('font-' + savedFont);
                }
            }
        }

        // ===== 字体大小 =====
        const sizeBtns = document.querySelectorAll('.size-btn');
        sizeBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const size = this.dataset.size;
                sizeBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                document.body.classList.remove('font-size-small', 'font-size-medium', 'font-size-large');
                document.body.classList.add('font-size-' + size);
                localStorage.setItem('daodejing_font_size', size);
                console.log('字体大小已切换为:', size);
            });
        });

        // 恢复保存的字体大小
        const savedSize = localStorage.getItem('daodejing_font_size');
        if (savedSize) {
            sizeBtns.forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.size === savedSize) {
                    btn.classList.add('active');
                    document.body.classList.add('font-size-' + savedSize);
                }
            });
        }

        // ===== 背景音乐 =====
        const musicSelect = document.getElementById('musicSelect');
        const musicVolumeSlider = document.getElementById('musicVolumeSlider');

        if (musicSelect) {
            musicSelect.addEventListener('change', function() {
                localStorage.setItem('daodejing_music', this.value);
                console.log('背景音乐已切换为:', this.value);
            });

            // 恢复保存的音乐设置
            const savedMusic = localStorage.getItem('daodejing_music');
            if (savedMusic) {
                musicSelect.value = savedMusic;
            }
        }

        if (musicVolumeSlider) {
            const volumeValue = document.getElementById('musicVolumeValue');
            musicVolumeSlider.addEventListener('input', function() {
                const volume = this.value / 100;
                if (volumeValue) volumeValue.textContent = Math.round(volume * 100) + '%';
                localStorage.setItem('daodejing_music_volume', volume);
            });

            // 恢复保存的音量
            const savedVolume = localStorage.getItem('daodejing_music_volume');
            if (savedVolume) {
                const volumeNum = parseFloat(savedVolume);
                const volumePercent = volumeNum > 1 ? Math.min(volumeNum, 100) : Math.round(volumeNum * 100);
                musicVolumeSlider.value = volumePercent;
                if (volumeValue) volumeValue.textContent = volumePercent + '%';
            }
        }

        // ===== 显示选项 - 拼音 =====
        const showPinyin = document.getElementById('showPinyin');
        if (showPinyin) {
            showPinyin.addEventListener('change', function() {
                document.body.classList.toggle('hide-pinyin', !this.checked);
                localStorage.setItem('daodejing_show_pinyin', this.checked);
            });

            const savedShowPinyin = localStorage.getItem('daodejing_show_pinyin');
            if (savedShowPinyin !== null) {
                showPinyin.checked = savedShowPinyin === 'true';
                document.body.classList.toggle('hide-pinyin', !showPinyin.checked);
            }
        }

        // ===== 显示选项 - 释义 =====
        const showAnnotation = document.getElementById('showAnnotation');
        if (showAnnotation) {
            showAnnotation.addEventListener('change', function() {
                document.body.classList.toggle('hide-annotation', !this.checked);
                localStorage.setItem('daodejing_show_annotation', this.checked);
            });

            const savedShowAnnotation = localStorage.getItem('daodejing_show_annotation');
            if (savedShowAnnotation !== null) {
                showAnnotation.checked = savedShowAnnotation === 'true';
                document.body.classList.toggle('hide-annotation', !showAnnotation.checked);
            }
        }

        // ===== 显示选项 - 白话译文 =====
        const showModern = document.getElementById('showModern');
        if (showModern) {
            showModern.addEventListener('change', function() {
                document.body.classList.toggle('hide-modern', !this.checked);
                localStorage.setItem('daodejing_show_modern', this.checked);
            });

            const savedShowModern = localStorage.getItem('daodejing_show_modern');
            if (savedShowModern !== null) {
                showModern.checked = savedShowModern === 'true';
                document.body.classList.toggle('hide-modern', !showModern.checked);
            }
        }

        // ===== 显示选项 - 注解版本 =====
        const showNotes = document.getElementById('showNotes');
        if (showNotes) {
            showNotes.addEventListener('change', function() {
                document.body.classList.toggle('hide-notes', !this.checked);
                localStorage.setItem('daodejing_show_notes', this.checked);
            });

            const savedShowNotes = localStorage.getItem('daodejing_show_notes');
            if (savedShowNotes !== null) {
                showNotes.checked = savedShowNotes === 'true';
                document.body.classList.toggle('hide-notes', !showNotes.checked);
            }
        }

        // ===== 显示选项 - 英文译本 =====
        const showEnglish = document.getElementById('showEnglish');
        if (showEnglish) {
            showEnglish.addEventListener('change', function() {
                document.body.classList.toggle('hide-english', !this.checked);
                localStorage.setItem('daodejing_show_english', this.checked);
            });

            const savedShowEnglish = localStorage.getItem('daodejing_show_english');
            if (savedShowEnglish !== null) {
                showEnglish.checked = savedShowEnglish === 'true';
                document.body.classList.toggle('hide-english', !showEnglish.checked);
            }
        }

        // ===== 分享设置按钮 =====
        const shareSettingsBtn = document.getElementById('shareSettings');
        if (shareSettingsBtn) {
            shareSettingsBtn.addEventListener('click', function(e) {
                if (window.SettingsManager && typeof window.SettingsManager.shareSettings === 'function') {
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    window.SettingsManager.shareSettings();
                    return;
                }
                // 收集当前所有设置
                const settings = {
                    font: localStorage.getItem('daodejing_font'),
                    fontSize: localStorage.getItem('daodejing_font_size'),
                    layout: localStorage.getItem('daodejing_text_layout'),
                    mode: localStorage.getItem('daodejing_reading_mode'),
                    showModern: localStorage.getItem('daodejing_show_modern'),
                    showNotes: localStorage.getItem('daodejing_show_notes'),
                    showPinyin: localStorage.getItem('daodejing_show_pinyin'),
                    showAnnotation: localStorage.getItem('daodejing_show_annotation'),
                    showEnglish: localStorage.getItem('daodejing_show_english'),
                    voiceLanguage: localStorage.getItem('daodejing_voice_language')
                };

                // 生成分享链接
                const baseUrl = window.location.origin + window.location.pathname;
                const params = new URLSearchParams();
                Object.entries(settings).forEach(([key, value]) => {
                    if (value !== null && value !== undefined) params.set(key, value);
                });

                const shareUrl = baseUrl + '?' + params.toString();
                navigator.clipboard.writeText(shareUrl).then(function() {
                    alert('配置链接已复制到剪贴板！');
                }).catch(function() {
                    prompt('请复制以下链接分享您的设置:', shareUrl);
                });
            });
        }

        // ===== 赞赏支持按钮 =====
        const supportBtn = document.getElementById('supportBtn');
        if (supportBtn) {
            supportBtn.addEventListener('click', function() {
                const supportModal = new bootstrap.Modal(document.getElementById('supportModal'));
                supportModal.show();
            });
        }

        // ===== 加入社群按钮 =====
        const communityBtn = document.getElementById('communityBtn');
        if (communityBtn) {
            communityBtn.addEventListener('click', function() {
                const communityModal = new bootstrap.Modal(document.getElementById('communityModal'));
                communityModal.show();
            });
        }

        // ===== AI API配置 =====
        const deepseekKey = document.getElementById('deepseekKey');
        const openaiKey = document.getElementById('openaiKey');

        if (deepseekKey) {
            deepseekKey.value = localStorage.getItem('daodejing_deepseek_key') || '';
            deepseekKey.addEventListener('change', function() {
                localStorage.setItem('daodejing_deepseek_key', this.value);
            });
        }

        if (openaiKey) {
            openaiKey.value = localStorage.getItem('daodejing_openai_key') || '';
            openaiKey.addEventListener('change', function() {
                localStorage.setItem('daodejing_openai_key', this.value);
            });
        }
    }

    function initSpeechVoiceSelect() {
        const browserVoice = document.getElementById('browserVoice');
        const voiceLanguageSelect = document.getElementById('voiceLanguage');
        if (!browserVoice) {
            return;
        }

        // 获取保存的语言偏好
        const savedLanguage = localStorage.getItem('daodejing_voice_language') || 'all';

        // 设置语言选择器的值
        if (voiceLanguageSelect) {
            voiceLanguageSelect.value = savedLanguage;
            voiceLanguageSelect.addEventListener('change', function() {
                localStorage.setItem('daodejing_voice_language', this.value);
                initSpeechVoiceSelect(); // 重新加载语音列表
            });
        }

        // 等待语音API加载
        if ('speechSynthesis' in window) {
            const loadVoices = () => {
                const voices = window.speechSynthesis.getVoices();
                browserVoice.innerHTML = '<option value="">正在加载可用语音...</option>';

                // 根据语言偏好过滤语音
                voices.forEach((voice, index) => {
                    if (savedLanguage !== 'all' && !voice.lang.startsWith(savedLanguage)) {
                        return; // 跳过不符合语言偏好的语音
                    }

                    const option = document.createElement('option');
                    option.value = voice.name;
                    option.textContent = `${voice.name} (${voice.lang})`;
                    if (voice.default) {
                        option.textContent += ' [默认]';
                    }
                    browserVoice.appendChild(option);
                });

                // 恢复保存的语音
                const savedVoice = localStorage.getItem('daodejing_speech_voice');
                if (savedVoice) {
                    browserVoice.value = savedVoice;
                }
            };

            // 加载语音（不同浏览器加载时机不同）
            loadVoices();
            window.speechSynthesis.onvoiceschanged = loadVoices;
        }
    }

        if (!('speechSynthesis' in window)) {
            return;
        }

        const loadVoices = function() {
            const voices = window.speechSynthesis.getVoices();
            browserVoice.innerHTML = '';

            if (voices && voices.length > 0) {
                const priorityCodes = [
                    'nan','zh-min-nan','minnan','nan-TW',      // 闽南语
                    'yue','zh-HK','zh-yue',                   // 粤语
                    'ja','ja-JP',                             // 日语
                    'en','en-US','en-GB'                      // 英语
                ];
                const score = function(v) {
                    const lang = (v.lang || '').toLowerCase();
                    const name = (v.name || '').toLowerCase();
                    let base = 10;
                    for (let i = 0; i < priorityCodes.length; i++) {
                        if (lang.includes(priorityCodes[i]) || name.includes('yue') || name.includes('cantonese') || name.includes('hokkien') || name.includes('min nan')) {
                            base = Math.min(base, i);
                        }
                    }
                    // Microsoft 优先
                    const msBoost = name.includes('microsoft') ? -5 : 0;
                    return base + msBoost;
                };
                voices.sort((a,b)=>score(a)-score(b));
                voices.forEach(function(voice) {
                    const option = document.createElement('option');
                    option.value = voice.lang + '|' + voice.name;
                    option.textContent = voice.name + ' (' + voice.lang + ')';
                    browserVoice.appendChild(option);
                });
            } else {
                browserVoice.innerHTML = '<option value="">当前浏览器未提供语音引擎</option>';
            }

            const savedVoice = localStorage.getItem('daodejing_browser_voice');
            if (savedVoice) {
                browserVoice.value = savedVoice;
            }
        };

        if (window.speechSynthesis.onvoiceschanged !== undefined) {
            window.speechSynthesis.onvoiceschanged = loadVoices;
        }
        loadVoices();

        browserVoice.addEventListener('change', function() {
            localStorage.setItem('daodejing_browser_voice', this.value);
        });
    }

    // 应用阅读模式
    function applyReadingMode(mode) {
        if (window.SettingsManager && typeof window.SettingsManager.setReadingMode === 'function') {
            window.SettingsManager.setReadingMode(mode);
            return;
        }
        const body = document.body;
        const zenOverlay = document.getElementById('zenModeOverlay');

        // 移除所有模式类
        body.classList.remove('mode-reading', 'mode-zen', 'mode-recite');

        if (mode === 'zen') {
            // 禅读模式
            body.classList.add('mode-zen');
            if (zenOverlay) zenOverlay.classList.add('active');
        } else if (mode === 'recite') {
            // 背诵模式 - 隐藏注释
            body.classList.add('mode-recite');
            body.classList.add('hide-notes', 'hide-annotation', 'hide-modern');
            if (zenOverlay) zenOverlay.classList.remove('active');
        } else {
            // 阅读模式 - 默认
            body.classList.add('mode-reading');
            if (zenOverlay) zenOverlay.classList.remove('active');
        }
    }

    // 初始化功能按钮
    function initFunctionButtons() {
        // AI解读按钮
        const aiToggle = document.getElementById('aiToggle');
        const aiSidebar = document.getElementById('aiSidebar');
        const aiCloseSidebar = document.getElementById('aiCloseSidebar');

        if (aiToggle && aiSidebar) {
            aiToggle.addEventListener('click', function() {
                aiSidebar.classList.toggle('show');
                console.log('AI解读面板已' + (aiSidebar.classList.contains('show') ? '打开' : '关闭'));
            });

            if (aiCloseSidebar) {
                aiCloseSidebar.addEventListener('click', function() {
                    aiSidebar.classList.remove('show');
                });
            }
        }

        // 音乐控制按钮
        const musicToggle = document.getElementById('musicToggle');
        const bgMusic = document.getElementById('bgMusic');

        if (musicToggle && bgMusic) {
            musicToggle.addEventListener('click', function() {
                if (bgMusic.paused) {
                    bgMusic.volume = 0.3;
                    bgMusic.play().then(function() {
                        musicToggle.classList.add('active');
                        console.log('背景音乐已播放');
                    }).catch(function(e) {
                        console.log('播放失败:', e);
                        alert('请点击页面任意位置后再播放音乐');
                    });
                } else {
                    bgMusic.pause();
                    musicToggle.classList.remove('active');
                    console.log('背景音乐已暂停');
                }
            });
        }

        // 朗读按钮
        const speechToggle = document.getElementById('speechToggle');
        const speechStop = document.getElementById('speechStop');

        if (speechToggle) {
            let isSpeaking = false;
            let currentUtterance = null;

            speechToggle.addEventListener('click', function() {
                if (isSpeaking) {
                    window.speechSynthesis.pause();
                    isSpeaking = false;
                    this.innerHTML = '<span class="speech-icon">🔊</span>';
                    if (speechStop) speechStop.classList.add('d-none');
                } else {
                    // 获取原文文本
                    const originalText = document.querySelector('.original-text');
                    if (originalText) {
                        const text = originalText.innerText;
                        if (text && 'speechSynthesis' in window) {
                            currentUtterance = new SpeechSynthesisUtterance(text);
                            currentUtterance.lang = 'zh-CN';
                            currentUtterance.rate = 0.8;

                            currentUtterance.onend = function() {
                                isSpeaking = false;
                                speechToggle.innerHTML = '<span class="speech-icon">🔊</span>';
                                if (speechStop) speechStop.classList.add('d-none');
                            };

                            window.speechSynthesis.speak(currentUtterance);
                            isSpeaking = true;
                            this.innerHTML = '<span>⏸</span>';
                            if (speechStop) speechStop.classList.remove('d-none');
                            console.log('开始朗读');
                        } else {
                            alert('您的浏览器不支持语音朗读功能');
                        }
                    }
                }
            });

            if (speechStop) {
                speechStop.addEventListener('click', function() {
                    window.speechSynthesis.cancel();
                    isSpeaking = false;
                    if (speechToggle) speechToggle.innerHTML = '<span class="speech-icon">🔊</span>';
                    speechStop.classList.add('d-none');
                    console.log('朗读已停止');
                });
            }
        }

        // AI功能下拉菜单按钮
        const knowledgeGraphBtn = document.getElementById('knowledgeGraphBtn');
        const commentaryChatBtn = document.getElementById('commentaryChatBtn');
        const philosophyDialogueBtn = document.getElementById('philosophyDialogueBtn');
        const noteBtn = document.getElementById('noteBtn');
        const quoteBtn = document.getElementById('quoteBtn');

        if (knowledgeGraphBtn) {
            knowledgeGraphBtn.addEventListener('click', function() {
                console.log('概念关系图谱功能');
                // 这里可以添加显示知识图谱的逻辑
                alert('概念关系图谱功能开发中');
            });
        }

        if (commentaryChatBtn) {
            commentaryChatBtn.addEventListener('click', function() {
                console.log('与注释家对话功能');
                alert('与注释家对话功能开发中');
            });
        }

        if (philosophyDialogueBtn) {
            philosophyDialogueBtn.addEventListener('click', function() {
                console.log('跨文明哲学对话功能');
                alert('跨文明哲学对话功能开发中');
            });
        }

        if (noteBtn) {
            noteBtn.addEventListener('click', function() {
                console.log('阅读笔记功能');
                alert('阅读笔记功能开发中');
            });
        }

        if (quoteBtn) {
            quoteBtn.addEventListener('click', function() {
                console.log('生成引用卡片功能');
                alert('生成引用卡片功能开发中');
            });
        }
    }
})();
