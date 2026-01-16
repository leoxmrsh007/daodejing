/**
 * 音乐播放管理模块
 * 背景音乐控制、音量调节
 */

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

if (typeof module !== 'undefined' && module.exports) {
    module.exports = MusicManager;
}
