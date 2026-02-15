// 设置面板控制
(function() {
    'use strict';

    // 等待DOM加载完成
    document.addEventListener('DOMContentLoaded', function() {
        initSettingsPanel();
        initFunctionButtons();
    });

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

        // 字体选择
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

        // 字体大小
        const sizeBtns = document.querySelectorAll('.size-btn');
        sizeBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const size = this.dataset.size;
                sizeBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                document.body.classList.remove('text-small', 'text-medium', 'text-large');
                document.body.classList.add('text-' + size);
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
                    document.body.classList.add('text-' + savedSize);
                }
            });
        }

        // 显示选项
        const showModern = document.getElementById('showModern');
        const showNotes = document.getElementById('showNotes');

        if (showModern) {
            showModern.addEventListener('change', function() {
                document.body.classList.toggle('hide-modern', !this.checked);
                localStorage.setItem('daodejing_show_modern', this.checked);
            });

            // 恢复保存的设置
            const savedShowModern = localStorage.getItem('daodejing_show_modern');
            if (savedShowModern !== null) {
                showModern.checked = savedShowModern === 'true';
                document.body.classList.toggle('hide-modern', !showModern.checked);
            }
        }

        if (showNotes) {
            showNotes.addEventListener('change', function() {
                document.body.classList.toggle('hide-notes', !this.checked);
                localStorage.setItem('daodejing_show_notes', this.checked);
            });

            // 恢复保存的设置
            const savedShowNotes = localStorage.getItem('daodejing_show_notes');
            if (savedShowNotes !== null) {
                showNotes.checked = savedShowNotes === 'true';
                document.body.classList.toggle('hide-notes', !showNotes.checked);
            }
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

        // 暗黑模式切换
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            const html = document.documentElement;
            const currentTheme = localStorage.getItem('theme') || 'auto';
            
            // 恢复保存的主题
            if (currentTheme !== 'auto') {
                html.setAttribute('data-theme', currentTheme);
                updateThemeIcon(currentTheme);
            }

            themeToggle.addEventListener('click', function() {
                const currentTheme = html.getAttribute('data-theme') || 'auto';
                let newTheme;
                
                if (currentTheme === 'light') {
                    newTheme = 'dark';
                } else if (currentTheme === 'dark') {
                    newTheme = 'auto';
                } else {
                    newTheme = 'light';
                }
                
                if (newTheme === 'auto') {
                    html.removeAttribute('data-theme');
                    localStorage.removeItem('theme');
                } else {
                    html.setAttribute('data-theme', newTheme);
                    localStorage.setItem('theme', newTheme);
                }
                
                updateThemeIcon(newTheme);
                console.log('主题已切换为:', newTheme);
            });

            function updateThemeIcon(theme) {
                const icon = themeToggle.querySelector('.theme-icon');
                if (icon) {
                    if (theme === 'dark') {
                        icon.textContent = '☀️';
                    } else if (theme === 'light') {
                        icon.textContent = '🌙';
                    } else {
                        icon.textContent = '🌓';
                    }
                }
            }
        }
    }
})();
