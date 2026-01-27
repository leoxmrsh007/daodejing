/**
 * 音乐播放管理模块
 * 背景音乐控制、音量调节
 * 使用本地音乐文件（真实的中国古典音乐）
 */

const MusicManager = {
    STORAGE_KEY: 'daodejing_music_volume',
    MUSIC_TYPE_KEY: 'daodejing_music',
    DEFAULT_VOLUME: 0.3,

    // 音乐列表 - 使用本地文件
    tracks: {
        chinese: [
            { name: '幽兰 (古琴与编钟)', url: '/static/audio/youlan.mp3' },
            { name: '离骚 (管平湖)', url: '/static/audio/lisao.mp3' },
            { name: '阳关三叠', url: '/static/audio/yangguan.mp3' },
            { name: '洞庭秋思', url: '/static/audio/dongting.mp3' },
            { name: '秦王破阵乐', url: '/static/audio/qinwang.mp3' },
            { name: '潇湘水云', url: '/static/audio/xiaoxiang.mp3' }
        ],
        western: [
            // 使用相同的中国古典音乐作为"冥想/阅读"音乐
            { name: '幽兰 - 冥想', url: '/static/audio/youlan.mp3' },
            { name: '洞庭秋思 - 静心', url: '/static/audio/dongting.mp3' },
            { name: '离骚 - 沉思', url: '/static/audio/lisao.mp3' }
        ]
    },

    currentTrackIndex: 0,
    currentType: 'chinese',

    init() {
        console.log('[MusicManager] 初始化音乐播放器');
        this.audio = document.getElementById('bgMusic');
        this.toggleBtn = document.getElementById('musicToggle');
        this.loopBtn = document.getElementById('musicLoop');
        this.volumePanel = document.getElementById('volumePanel');
        this.volumeSlider = document.getElementById('volumeSlider');
        this.volumeValue = document.getElementById('volumeValue');
        this.closeVolumeBtn = document.getElementById('closeVolumePanel');
        this.musicSelect = document.getElementById('musicSelect');
        this.musicVolumeSlider = document.getElementById('musicVolumeSlider');
        this.musicVolumeValue = document.getElementById('musicVolumeValue');

        console.log('[MusicManager] audio:', !!this.audio, 'toggleBtn:', !!this.toggleBtn);

        if (!this.audio || !this.toggleBtn) return;

        // 加载保存的设置
        const savedVolume = localStorage.getItem(this.STORAGE_KEY);
        this.volume = savedVolume ? parseFloat(savedVolume) : this.DEFAULT_VOLUME;
        this.audio.volume = this.volume;
        console.log('[MusicManager] 音量:', this.volume);

        const savedMusicType = localStorage.getItem(this.MUSIC_TYPE_KEY);
        if (savedMusicType && savedMusicType !== 'none') {
            this.currentType = savedMusicType;
            this.loadTrack();
        }

        // 更新滑块显示
        this.updateVolumeDisplay();

        this.bindEvents();

        // 设置音频循环
        this.audio.loop = true;

        // 添加音频事件监听
        this.audio.addEventListener('loadstart', () => console.log('[MusicManager] 音频开始加载'));
        this.audio.addEventListener('canplay', () => console.log('[MusicManager] 音频可以播放'));
        this.audio.addEventListener('play', () => console.log('[MusicManager] 音频播放'));
        this.audio.addEventListener('pause', () => console.log('[MusicManager] 音频暂停'));
        this.audio.addEventListener('error', (e) => console.error('[MusicManager] 音频错误:', e));
    },

    bindEvents() {
        // 播放/暂停
        this.toggleBtn.addEventListener('click', () => this.toggle());

        // 循环按钮
        if (this.loopBtn) {
            this.loopBtn.addEventListener('click', () => this.toggleLoop());
        }

        // 音量滑块（面板内）
        if (this.volumeSlider) {
            this.volumeSlider.addEventListener('input', (e) => {
                this.setVolume(e.target.value / 100);
            });
        }

        // 音乐音量滑块（设置面板内）
        if (this.musicVolumeSlider) {
            this.musicVolumeSlider.addEventListener('input', (e) => {
                this.setVolume(e.target.value / 100);
                if (this.musicVolumeValue) {
                    this.musicVolumeValue.textContent = e.target.value + '%';
                }
            });
        }

        // 音乐类型选择
        if (this.musicSelect) {
            this.musicSelect.addEventListener('change', (e) => {
                this.setMusicType(e.target.value);
            });
        }

        // 关闭音量面板
        if (this.closeVolumeBtn) {
            this.closeVolumeBtn.addEventListener('click', () => {
                this.volumePanel?.classList.remove('show');
            });
        }

        // 点击外部关闭面板
        document.addEventListener('click', (e) => {
            if (this.volumePanel?.classList.contains('show')) {
                if (!this.volumePanel.contains(e.target) && !this.toggleBtn.contains(e.target)) {
                    this.volumePanel.classList.remove('show');
                }
            }
        });

        // 右键点击音乐按钮打开音量面板
        this.toggleBtn.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            this.volumePanel?.classList.toggle('show');
        });

        // 音频事件
        this.audio.addEventListener('play', () => this.updateState());
        this.audio.addEventListener('pause', () => this.updateState());
        this.audio.addEventListener('ended', () => {
            if (!this.audio.loop) {
                this.playNext();
            }
        });
    },

    toggle() {
        console.log('[MusicManager] toggle, paused:', this.audio.paused, 'src:', this.audio.src);
        if (this.audio.paused) {
            if (!this.audio.src || this.audio.error) {
                console.log('[MusicManager] 需要加载曲目');
                this.loadTrack();
            }
            this.audio.play().then(() => {
                console.log('[MusicManager] 播放成功');
                this.updateState();
                if (this.currentTrackName) {
                    this.showToast(`▶️ ${this.currentTrackName}`);
                }
            }).catch(err => {
                console.error('[MusicManager] 播放失败:', err);
                this.showToast('播放失败: ' + err.message);
            });
        } else {
            this.audio.pause();
            this.updateState();
            this.showToast('⏸️ 音乐已暂停');
        }
    },

    setMusicType(type) {
        localStorage.setItem(this.MUSIC_TYPE_KEY, type);

        if (type === 'none') {
            this.audio.pause();
            this.audio.src = '';
            this.updateState();
            this.showToast('音乐已关闭');
        } else {
            this.currentType = type;
            this.currentTrackIndex = 0;
            this.loadTrack();
        }
    },

    loadTrack() {
        const tracks = this.tracks[this.currentType];
        if (!tracks || tracks.length === 0) {
            console.error('[MusicManager] 没有可用的音乐');
            this.showToast('没有可用的音乐');
            return;
        }

        const track = tracks[this.currentTrackIndex];
        this.audio.src = track.url;
        this.audio.load();
        this.currentTrackName = track.name;

        console.log(`[MusicManager] 加载音乐: ${track.name}, URL: ${track.url}`);
    },

    handleAudioError() {
        console.warn('音频加载失败，尝试下一首');
        this.showToast('当前曲目加载失败，切换下一首');
        this.playNext();
    },

    playNext() {
        const tracks = this.tracks[this.currentType];
        if (!tracks || tracks.length <= 1) {
            this.audio.pause();
            this.updateState();
            return;
        }

        this.currentTrackIndex = (this.currentTrackIndex + 1) % tracks.length;
        this.loadTrack();

        if (!this.audio.paused) {
            this.audio.play().catch(() => {
                this.showToast('无法播放下一首');
            });
        }
    },

    setVolume(value) {
        this.volume = Math.max(0, Math.min(1, value));
        this.audio.volume = this.volume;
        localStorage.setItem(this.STORAGE_KEY, this.volume);
        this.updateVolumeDisplay();
    },

    updateVolumeDisplay() {
        const volumePercent = Math.round(this.volume * 100);

        if (this.volumeSlider) {
            this.volumeSlider.value = volumePercent;
        }
        if (this.volumeValue) {
            this.volumeValue.textContent = volumePercent;
        }
        if (this.musicVolumeSlider) {
            this.musicVolumeSlider.value = volumePercent;
        }
        if (this.musicVolumeValue) {
            this.musicVolumeValue.textContent = volumePercent + '%';
        }
    },

    toggleLoop() {
        this.audio.loop = !this.audio.loop;
        this.updateState();
    },

    updateState() {
        const icon = this.toggleBtn?.querySelector('.music-icon');
        if (!this.audio.paused) {
            icon?.classList.add('playing');
            this.toggleBtn?.classList.add('active');
            this.loopBtn?.classList.remove('d-none');

            if (this.currentTrackName) {
                this.toggleBtn?.setAttribute('title', `正在播放: ${this.currentTrackName}`);
            }
        } else {
            icon?.classList.remove('playing');
            this.toggleBtn?.classList.remove('active');
            this.loopBtn?.classList.add('d-none');
            this.toggleBtn?.setAttribute('title', '背景音乐');
        }

        if (this.loopBtn && !this.loopBtn.classList.contains('d-none')) {
            const loopIcon = this.loopBtn.querySelector('.loop-icon');
            if (loopIcon) {
                loopIcon.textContent = this.audio.loop ? '🔁' : '🔂';
            }
        }
    },

    showToast(message) {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            background: rgba(44, 24, 16, 0.95);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 9999;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2500);
    }
};

// 导出模块（兼容多种模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MusicManager;
}

// 自动初始化
if (typeof window !== 'undefined') {
    // 等待 DOM 加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => MusicManager.init());
    } else {
        // DOM 已经加载完成
        MusicManager.init();
    }

    // 导出到全局
    window.MusicManager = MusicManager;
}
