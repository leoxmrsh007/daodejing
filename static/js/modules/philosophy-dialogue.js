/**
 * 跨文明哲学对话模块
 * 让老子与西方、印度哲学家进行对话
 */

const PhilosophyDialogueManager = {
    philosophers: null,
    currentDialogue: null,
    currentChapter: null,

    init() {
        this.dialogueBtn = document.getElementById('philosophyDialogueBtn');
        if (!this.dialogueBtn) return;

        this.dialogueBtn.addEventListener('click', () => this.openDialogueModal());
    },

    getCurrentChapter() {
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            return match ? parseInt(match[1]) : null;
        }
        return null;
    },

    async openDialogueModal() {
        this.currentChapter = this.getCurrentChapter();
        if (!this.currentChapter) return;

        // 确保模态框存在
        this.ensureModalExists();

        // 加载哲学家列表
        await this.loadPhilosophers();

        // 显示模态框
        const modal = document.getElementById('philosophyDialogueModal');
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },

    async loadPhilosophers() {
        try {
            const response = await fetch('/api/dialogue/philosophers');
            const data = await response.json();
            this.philosophers = data.philosophers;
        } catch (error) {
            console.error('[PhilosophyDialogue] 加载哲学家失败:', error);
            this.philosophers = this.getMockPhilosophers();
        }

        this.renderPhilosopherSelector();
    },

    getMockPhilosophers() {
        return [
            { id: 'zhuangzi', name: '庄子', culture: '中国', era: '战国中期', school: '道家' },
            { id: 'plato', name: '柏拉图', culture: '古希腊', era: '古典时期', school: '理念论' },
            { id: 'heidegger', name: '海德格尔', culture: '德国', era: '现代', school: '存在主义' },
            { id: 'nagarjuna', name: '龙树', culture: '印度', era: '中世纪', school: '中观派' }
        ];
    },

    ensureModalExists() {
        let modal = document.getElementById('philosophyDialogueModal');

        if (!modal) {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const modalClass = isDark ? 'bg-dark text-light border-secondary' : '';

            const modalHtml = `
                <div class="modal fade" id="philosophyDialogueModal" tabindex="-1">
                    <div class="modal-dialog modal-xl modal-dialog-centered">
                        <div class="modal-content ${modalClass}" style="border: none;">
                            <div class="modal-header ${isDark ? 'bg-dark border-secondary' : ''}">
                                <h5 class="modal-title">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f0ad4e" stroke-width="2" class="me-2">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                                    </svg>
                                    <span class="text-warning">跨文明哲学对话</span>
                                </h5>
                                <button type="button" class="btn-close ${isDark ? 'btn-close-white' : ''}" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-md-4 ${isDark ? 'border-secondary' : 'border-end'}">
                                        <h6 class="mb-3">
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                                <circle cx="9" cy="7" r="4"></circle>
                                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                                            </svg>
                                            选择对话者
                                        </h6>

                                        <div class="mb-3">
                                            <label class="form-label small">
                                                <span class="badge bg-primary">哲学家 1</span>
                                            </label>
                                            <select id="philosopher1Select" class="form-select form-select-sm">
                                                <option value="">请选择...</option>
                                            </select>
                                        </div>

                                        <div class="mb-3">
                                            <label class="form-label small">
                                                <span class="badge bg-success">哲学家 2</span>
                                            </label>
                                            <select id="philosopher2Select" class="form-select form-select-sm">
                                                <option value="">请选择...</option>
                                            </select>
                                        </div>

                                        <div class="mb-3">
                                            <label class="form-label small">
                                                <span class="badge bg-warning text-dark">对话主题</span>
                                            </label>
                                            <select id="dialogueTopic" class="form-select form-select-sm">
                                                <option value="道">道</option>
                                                <option value="无为">无为</option>
                                                <option value="德">德</option>
                                                <option value="自然">自然</option>
                                                <option value="有">有</option>
                                                <option value="无">无</option>
                                            </select>
                                        </div>

                                        <button id="startDialogueBtn" class="btn btn-warning w-100 mb-3">
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                            </svg>
                                            开始对话
                                        </button>

                                        <hr class="my-3">

                                        <h6 class="mb-2">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                                            </svg>
                                            快速对比
                                        </h6>
                                        <div id="quickCompare" class="list-group list-group-flush">
                                            <!-- 快速对比选项 -->
                                        </div>
                                    </div>

                                    <div class="col-md-8">
                                        <div id="dialogueWelcome" class="text-center text-muted p-5">
                                            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" class="mb-3">
                                                <circle cx="12" cy="12" r="10"></circle>
                                                <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                                            </svg>
                                            <h5 class="mb-2">跨时空思想碰撞</h5>
                                            <p class="mb-2">选择两位哲学家，探讨道德经中的核心概念</p>
                                            <p class="small text-muted">体验东西方哲学的深度对话</p>
                                        </div>

                                        <div id="dialogueLoading" class="text-center p-5" style="display: none;">
                                            <div class="spinner-border text-warning mb-3" role="status" style="width: 3rem; height: 3rem;">
                                                <span class="visually-hidden">加载中...</span>
                                            </div>
                                            <p class="text-muted">正在建立跨时空连接...</p>
                                            <small class="text-muted">正在分析哲学观点 · 生成对话内容</small>
                                        </div>

                                        <div id="dialogueArea" style="display: none;">
                                            <!-- 对话内容 -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer ${isDark ? 'bg-dark border-secondary' : ''}">
                                <small class="text-muted">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <line x1="12" y1="16" x2="12" y2="12"></line>
                                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                                    </svg>
                                    AI生成内容仅供学习参考，不代表历史真实观点
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            modal = document.getElementById('philosophyDialogueModal');

            // 绑定事件
            modal.querySelector('#startDialogueBtn').addEventListener('click', () => this.startDialogue());
        }
    },

    renderPhilosopherSelector() {
        const select1 = document.getElementById('philosopher1Select');
        const select2 = document.getElementById('philosopher2Select');

        if (!select1 || !select2 || !this.philosophers) return;

        const options = this.philosophers.map(p =>
            `<option value="${p.id}">${p.name}（${p.culture}·${p.school}）</option>`
        ).join('');

        select1.innerHTML = '<option value="">请选择...</option>' + options;
        select2.innerHTML = '<option value="">请选择...</option>' + options;

        // 默认选择
        select1.value = 'zhuangzi';
        select2.value = 'plato';

        // 渲染快速对比选项
        this.renderQuickCompare();
    },

    renderQuickCompare() {
        const container = document.getElementById('quickCompare');
        if (!container || !this.philosophers) return;

        // 生成一些有趣的对比组合
        const comparisons = [
            { label: '道 vs Sein（存在）', p1: 'zhuangzi', p2: 'heidegger', topic: '道' },
            { label: '道 vs Brahman（梵）', p1: 'zhuangzi', p2: 'nagarjuna', topic: '道' },
            { label: '无为 vs Apatheia', p1: 'zhuangzi', p2: 'plato', topic: '无为' },
            { label: '空性 vs 虚无', p1: 'nagarjuna', p2: 'heidegger', topic: '无' }
        ];

        container.innerHTML = comparisons.map((c, i) => `
            <button class="list-group-item list-group-item-action quick-compare-btn" data-idx="${i}">
                <small>${c.label}</small>
            </button>
        `).join('');

        container.querySelectorAll('.quick-compare-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const cmp = comparisons[btn.dataset.idx];
                document.getElementById('philosopher1Select').value = cmp.p1;
                document.getElementById('philosopher2Select').value = cmp.p2;
                document.getElementById('dialogueTopic').value = cmp.topic;
                this.startDialogue();
            });
        });
    },

    async startDialogue() {
        const philosopher1 = document.getElementById('philosopher1Select').value;
        const philosopher2 = document.getElementById('philosopher2Select').value;
        const topic = document.getElementById('dialogueTopic').value;

        if (!philosopher1 || !philosopher2) {
            this.showToast('请选择两位哲学家', 'warning');
            return;
        }

        if (philosopher1 === philosopher2) {
            this.showToast('请选择两位不同的哲学家', 'warning');
            return;
        }

        // 显示加载状态
        document.getElementById('dialogueWelcome').style.display = 'none';
        document.getElementById('dialogueLoading').style.display = 'block';
        document.getElementById('dialogueArea').style.display = 'none';

        try {
            const response = await fetch('/api/dialogue/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chapter_id: this.currentChapter || 1,
                    concept: topic,
                    philosopher1: philosopher1,
                    philosopher2: philosopher2
                })
            });

            const data = await response.json();

            // 隐藏加载状态
            document.getElementById('dialogueLoading').style.display = 'none';

            if (data.error) {
                document.getElementById('dialogueArea').style.display = 'block';
                document.getElementById('dialogueArea').innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                return;
            }

            this.currentDialogue = data;
            this.renderDialogue(data);

        } catch (error) {
            console.error('[PhilosophyDialogue] 启动对话失败:', error);
            document.getElementById('dialogueLoading').style.display = 'none';
            this.renderOfflineDialogue(philosopher1, philosopher2, topic);
        }
    },

    renderDialogue(data) {
        const dialogueArea = document.getElementById('dialogueArea');

        const p1 = data.participant1;
        const p2 = data.participant2;

        dialogueArea.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5>${data.topic}</h5>
                <button class="btn btn-sm btn-outline-secondary" id="addExchangeBtn">
                    继续对话
                </button>
            </div>

            <div class="row mb-3">
                <div class="col-6">
                    <div class="card border-primary">
                        <div class="card-header bg-primary text-white">
                            <strong>${p1.name}</strong>
                            <small class="ms-2">${p1.culture}</small>
                        </div>
                        <div class="card-body">
                            <p class="mb-1"><small>${p1.era} · ${p1.school}</small></p>
                            <p class="mb-0">${p1.opening || '...'}</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card border-success">
                        <div class="card-header bg-success text-white">
                            <strong>${p2.name}</strong>
                            <small class="ms-2">${p2.culture}</small>
                        </div>
                        <div class="card-body">
                            <p class="mb-1"><small>${p2.era} · ${p2.school}</small></p>
                            <p class="mb-0">${p2.opening || '...'}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-4">
                <h6>概念对应</h6>
                <div id="conceptMapping" class="p-3 bg-light rounded">
                    <!-- 概念对应关系 -->
                </div>
            </div>
        `;

        // 绑定继续对话按钮
        dialogueArea.querySelector('#addExchangeBtn')?.addEventListener('click', () => {
            this.continueDialogue();
        });
    },

    renderOfflineDialogue(p1, p2, topic) {
        const dialogueArea = document.getElementById('dialogueArea');
        dialogueArea.style.display = 'block';

        const p1Info = this.philosophers.find(p => p.id === p1);
        const p2Info = this.philosophers.find(p => p.id === p2);

        dialogueArea.innerHTML = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="text-warning">关于「${topic}」的跨文明对话</h5>
                <button class="btn btn-sm btn-outline-warning" id="backToWelcomeBtn">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                        <path d="M19 12H5M12 19l-7-7 7-7"></path>
                    </svg>
                    返回
                </button>
            </div>

            <div class="row mb-3">
                <div class="col-6">
                    <div class="card border-primary">
                        <div class="card-header bg-primary text-white">
                            <strong>${p1Info?.name || p1}</strong>
                            <small class="ms-2">${p1Info?.culture || ''}</small>
                        </div>
                        <div class="card-body">
                            <p class="mb-1"><small>${p1Info?.era || ''} · ${p1Info?.school || ''}</small></p>
                            <p class="mb-0 text-muted">在线模式下可获取完整对话内容</p>
                        </div>
                    </div>
                </div>
                <div class="col-6">
                    <div class="card border-success">
                        <div class="card-header bg-success text-white">
                            <strong>${p2Info?.name || p2}</strong>
                            <small class="ms-2">${p2Info?.culture || ''}</small>
                        </div>
                        <div class="card-body">
                            <p class="mb-1"><small>${p2Info?.era || ''} · ${p2Info?.school || ''}</small></p>
                            <p class="mb-0 text-muted">在线模式下可获取完整对话内容</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="alert alert-info">
                <strong>💡 提示</strong>：部署到Vercel后可获得完整的跨文明AI对话体验。
                当前展示的是离线预览模式。
            </div>
        `;

        // 绑定返回按钮
        dialogueArea.querySelector('#backToWelcomeBtn')?.addEventListener('click', () => {
            dialogueArea.style.display = 'none';
            document.getElementById('dialogueWelcome').style.display = 'block';
        });
    },

    async continueDialogue() {
        if (!this.currentDialogue) return;

        // 这里可以调用AI继续生成对话
        this.showToast('继续对话功能需要配置AI API', 'info');
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
    module.exports = PhilosophyDialogueManager;
}

// 自动初始化 - 使用事件委托
if (typeof window !== 'undefined') {
    window.PhilosophyDialogueManager = PhilosophyDialogueManager;

    // 使用事件委托，确保即使按钮是动态创建的也能工作
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#philosophyDialogueBtn');
        if (btn) {
            e.preventDefault();
            PhilosophyDialogueManager.openDialogueModal();
        }
    });
}
