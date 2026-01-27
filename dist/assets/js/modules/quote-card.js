/**
 * 引用卡片生成模块
 * 创建精美的道德经引用卡片图片
 */

const QuoteCardManager = {
    init() {
        this.quoteBtn = document.getElementById('quoteBtn');
        if (!this.quoteBtn) return;

        this.quoteBtn.addEventListener('click', () => this.generateCard());
    },

    generateCard() {
        const chapterTitle = document.querySelector('.card-header h5')?.textContent || '道德经';
        const originalText = document.querySelector('#originalText')?.textContent || '';
        const chapterNum = this.getCurrentChapter();

        if (!originalText) {
            this.showToast('无法获取原文内容', 'warning');
            return;
        }

        // 创建模态框
        this.ensureModalExists(chapterTitle, originalText, chapterNum);

        // 生成卡片
        setTimeout(() => {
            this.drawCard(chapterTitle, originalText, chapterNum);
        }, 100);
    },

    getCurrentChapter() {
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            return match ? parseInt(match[1]) : null;
        }
        return null;
    },

    ensureModalExists(title, text, chapter) {
        let modal = document.getElementById('quoteCardModal');

        if (!modal) {
            const modalHtml = `
                <div class="modal fade" id="quoteCardModal" tabindex="-1">
                    <div class="modal-dialog modal-lg modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">📜 引用卡片</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="text-center mb-3">
                                    <canvas id="quoteCanvas" class="img-fluid border rounded shadow-sm" style="max-width: 100%;"></canvas>
                                </div>
                                <div class="d-flex justify-content-center gap-2">
                                    <button class="btn btn-success" id="downloadQuoteBtn">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="me-1">
                                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/>
                                            <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/>
                                        </svg>
                                        下载图片
                                    </button>
                                    <button class="btn btn-outline-primary" id="copyQuoteBtn">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="me-1">
                                            <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                                            <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                                        </svg>
                                        复制文字
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            modal = document.getElementById('quoteCardModal');

            // 绑定按钮事件
            modal.querySelector('#downloadQuoteBtn').addEventListener('click', () => this.downloadCard());
            modal.querySelector('#copyQuoteBtn').addEventListener('click', () => this.copyText());
        }

        // 显示模态框
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },

    drawCard(title, text, chapter) {
        const canvas = document.getElementById('quoteCanvas');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');

        // 设置画布尺寸（2x以支持高清屏）
        const width = 800;
        const height = 600;
        canvas.width = width * 2;
        canvas.height = height * 2;
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
        ctx.scale(2, 2);

        // 获取当前主题
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

        // 背景渐变
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        if (isDark) {
            gradient.addColorStop(0, '#1a1a2e');
            gradient.addColorStop(1, '#16213e');
        } else {
            gradient.addColorStop(0, '#faf8f5');
            gradient.addColorStop(1, '#f0ebe3');
        }
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);

        // 装饰边框
        ctx.strokeStyle = isDark ? '#d4a574' : '#c9a67a';
        ctx.lineWidth = 4;
        ctx.strokeRect(20, 20, width - 40, height - 40);

        // 内边框
        ctx.strokeStyle = isDark ? 'rgba(212, 165, 116, 0.3)' : 'rgba(201, 166, 122, 0.3)';
        ctx.lineWidth = 2;
        ctx.strokeRect(30, 30, width - 60, height - 60);

        // 太极符号装饰
        this.drawTaijitu(ctx, width - 80, 80, 40, isDark ? '#d4a574' : '#8b6914');

        // 标题
        ctx.fillStyle = isDark ? '#d4a574' : '#8b6914';
        ctx.font = 'bold 28px "KaiTi", "楷体", serif';
        ctx.textAlign = 'center';
        ctx.fillText(title, width / 2, 80);

        // 分隔线
        ctx.beginPath();
        ctx.moveTo(width / 2 - 100, 100);
        ctx.lineTo(width / 2 + 100, 100);
        ctx.strokeStyle = isDark ? '#d4a574' : '#c9a67a';
        ctx.lineWidth = 2;
        ctx.stroke();

        // 文字处理
        ctx.fillStyle = isDark ? '#e8e0d8' : '#2c1810';
        ctx.font = '24px "KaiTi", "楷体", serif';

        const lines = this.wrapText(ctx, text, width - 120);
        const lineHeight = 40;
        const startY = 150;

        lines.forEach((line, index) => {
            ctx.fillText(line, width / 2, startY + index * lineHeight);
        });

        // 底部装饰
        ctx.fillStyle = isDark ? '#d4a574' : '#8b6914';
        ctx.font = '16px sans-serif';
        ctx.fillText('道德经多版本对照平台', width / 2, height - 50);

        // 存储文本用于复制
        this.currentQuoteText = text;
    },

    drawTaijitu(ctx, x, y, radius, color) {
        ctx.save();
        ctx.translate(x, y);

        // 外圆
        ctx.beginPath();
        ctx.arc(0, 0, radius, 0, Math.PI * 2);
        ctx.fillStyle = color + '40';
        ctx.fill();

        // 阳鱼（白色部分）
        ctx.beginPath();
        ctx.arc(0, -radius / 2, radius / 2, Math.PI, 0);
        ctx.arc(0, 0, radius / 2, 0, Math.PI);
        ctx.fillStyle = '#ffffff';
        ctx.fill();

        // 阴鱼（颜色部分）
        ctx.beginPath();
        ctx.arc(0, radius / 2, radius / 2, 0, Math.PI);
        ctx.arc(0, 0, radius / 2, Math.PI, 0);
        ctx.fillStyle = color;
        ctx.fill();

        // 阳中阴点
        ctx.beginPath();
        ctx.arc(0, -radius / 2, radius / 6, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();

        // 阴中阳点
        ctx.beginPath();
        ctx.arc(0, radius / 2, radius / 6, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();

        ctx.restore();
    },

    wrapText(ctx, text, maxWidth) {
        const lines = [];
        const paragraphs = text.split('\n');

        for (const paragraph of paragraphs) {
            const chars = paragraph.split('');
            let line = '';

            for (const char of chars) {
                const testLine = line + char;
                const metrics = ctx.measureText(testLine);

                if (metrics.width > maxWidth && line !== '') {
                    lines.push(line);
                    line = char;
                } else {
                    line = testLine;
                }
            }
            lines.push(line);
        }

        return lines;
    },

    downloadCard() {
        const canvas = document.getElementById('quoteCanvas');
        if (!canvas) return;

        // 创建下载链接
        const link = document.createElement('a');
        link.download = `daodejing_quote_${this.getCurrentChapter()}_${Date.now()}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();

        this.showToast('图片已下载', 'success');
    },

    copyText() {
        if (!this.currentQuoteText) return;

        navigator.clipboard.writeText(this.currentQuoteText).then(() => {
            this.showToast('文字已复制', 'success');
        }).catch(() => {
            this.showToast('复制失败', 'danger');
        });
    },

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 1100;';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        document.body.appendChild(toast);

        const bsToast = new bootstrap.Toast(toast, { delay: 2000 });
        bsToast.show();

        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = QuoteCardManager;
}

// 自动初始化
if (typeof window !== 'undefined') {
    window.QuoteCardManager = QuoteCardManager;

    // 使用事件委托，确保即使按钮是动态创建的也能工作
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#quoteBtn');
        if (btn) {
            e.preventDefault();
            QuoteCardManager.generateCard();
        }
    });
}
