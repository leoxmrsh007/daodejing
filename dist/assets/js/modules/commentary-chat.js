/**
 * 虚拟注释家对话模块
 * 与历代注释家进行AI对话
 */

const CommentaryChatManager = {
    currentChapter: null,
    currentCommentator: null,
    chatHistory: [],
    commentators: null,

    init() {
        this.chatBtn = document.getElementById('commentaryChatBtn');
        if (!this.chatBtn) return;

        this.chatBtn.addEventListener('click', () => this.openChatModal());
    },

    getCurrentChapter() {
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            return match ? parseInt(match[1]) : null;
        }
        return null;
    },

    async openChatModal() {
        this.currentChapter = this.getCurrentChapter();
        if (!this.currentChapter) return;

        // 确保模态框存在
        this.ensureModalExists();

        // 加载注释家列表
        await this.loadCommentators();

        // 显示模态框
        const modal = document.getElementById('commentaryChatModal');
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // 如果没有选中注释家，显示选择界面
        if (!this.currentCommentator) {
            this.showCommentatorSelector();
        }
    },

    async loadCommentators() {
        try {
            const response = await fetch('/api/commentary/commentators');
            const data = await response.json();
            this.commentators = data.commentators;
        } catch (error) {
            console.error('[CommentaryChat] 加载注释家失败:', error);
            this.commentators = this.getMockCommentators();
        }
    },

    getMockCommentators() {
        return [
            { id: 'wangbi', name: '王弼', era: '魏晋（226-249）', school: '贵无派', key_themes: ['以无为本', '得意忘象'] },
            { id: 'heshanggong', name: '河上公', era: '西汉', school: '黄老道家', key_themes: ['养生', '治身'] },
            { id: 'hanshandeqing', name: '憨山德清', era: '明（1546-1623）', school: '佛道融合', key_themes: ['性体', '工夫'] },
            { id: 'wangfuzhi', name: '王夫之', era: '明末清初', school: '船山学派', key_themes: ['势', '变'] }
        ];
    },

    ensureModalExists() {
        let modal = document.getElementById('commentaryChatModal');

        if (!modal) {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const modalClass = isDark ? 'bg-dark text-light border-secondary' : '';

            const modalHtml = `
                <div class="modal fade" id="commentaryChatModal" tabindex="-1">
                    <div class="modal-dialog modal-xl modal-dialog-centered">
                        <div class="modal-content ${modalClass}" style="border: none;">
                            <div class="modal-header ${isDark ? 'bg-dark border-secondary' : ''}">
                                <h5 class="modal-title">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f0ad4e" stroke-width="2" class="me-2">
                                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                                    </svg>
                                    <span class="text-warning">与注释家对话</span>
                                </h5>
                                <div class="d-flex align-items-center">
                                    <button class="btn btn-sm btn-outline-secondary me-2" id="apiSettingsBtn">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                            <circle cx="12" cy="12" r="3"></circle>
                                            <path d="M12 1v6m0 6v6m5.66-14.66l-4.24 4.24m0 8.48l4.24 4.24M23 12h-6m-6 0H1m14.66-5.66l-4.24-4.24m0 8.48l4.24 4.24"></path>
                                        </svg>
                                        API设置
                                    </button>
                                    <button type="button" class="btn-close ${isDark ? 'btn-close-white' : ''}" data-bs-dismiss="modal"></button>
                                </div>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-md-3 ${isDark ? 'border-secondary' : 'border-end'}">
                                        <h6 class="mb-3">
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                                                <circle cx="9" cy="7" r="4"></circle>
                                                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                                                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                                            </svg>
                                            选择注释家
                                        </h6>
                                        <div id="commentatorList" class="list-group">
                                            <!-- 注释家列表将在这里动态生成 -->
                                        </div>
                                    </div>
                                    <div class="col-md-9">
                                        <div id="commentatorInfoPanel" class="mb-3 p-3 ${isDark ? 'bg-secondary border-warning' : 'bg-light'} rounded" style="display: none;">
                                            <!-- 注释家信息 -->
                                        </div>
                                        <div id="chatContainer" class="border rounded ${isDark ? 'bg-dark border-secondary' : ''}" style="height: 400px; overflow-y: auto; display: none;">
                                            <div id="chatMessages" class="p-3">
                                                <!-- 对话消息 -->
                                            </div>
                                        </div>
                                        <div id="chatInputPanel" class="mt-3" style="display: none;">
                                            <div class="input-group">
                                                <span class="input-group-text">
                                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                                                    </svg>
                                                </span>
                                                <input type="text" id="chatInput" class="form-control"
                                                    placeholder="向注释家提问，如：本章的核心思想是什么？" />
                                                <button class="btn btn-warning" id="sendChatBtn">
                                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                        <line x1="22" y1="2" x2="11" y2="13"></line>
                                                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                                                    </svg>
                                                    发送
                                                </button>
                                            </div>
                                            <div class="mt-2 d-flex justify-content-between">
                                                <small class="text-muted">
                                                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                        <circle cx="12" cy="12" r="10"></circle>
                                                        <line x1="12" y1="16" x2="12" y2="12"></line>
                                                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                                                    </svg>
                                                    提示: 可以询问关于本章的含义、概念解释等
                                                </small>
                                                <button class="btn btn-sm btn-outline-secondary py-0" id="clearChatBtn">
                                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                        <polyline points="3 6 5 6 21 6"></polyline>
                                                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                                    </svg>
                                                    清空对话
                                                </button>
                                            </div>
                                        </div>
                                        <div id="welcomePanel" class="text-center text-muted p-5">
                                            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" class="mb-3">
                                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                                            </svg>
                                            <p class="mb-2">请选择左侧的注释家开始对话</p>
                                            <small>体验跨越时空的思想交流</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer ${isDark ? 'bg-dark border-secondary' : ''}">
                                <small class="text-muted">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                                    </svg>
                                    AI回复基于历史注释资料，仅供参考学习
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            modal = document.getElementById('commentaryChatModal');

            // 绑定事件
            modal.querySelector('#sendChatBtn').addEventListener('click', () => this.sendMessage());
            modal.querySelector('#chatInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
            modal.querySelector('#clearChatBtn').addEventListener('click', () => this.clearChat());
            modal.querySelector('#apiSettingsBtn').addEventListener('click', () => this.showApiSettings());
        }
    },

    showApiSettings() {
        let modal = document.getElementById('apiSettingsModal');

        // 如果API设置模态框不存在，创建它
        if (!modal) {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const modalHtml = `
                <div class="modal fade" id="apiSettingsModal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content ${isDark ? 'bg-dark text-light border-secondary' : ''}">
                            <div class="modal-header ${isDark ? 'border-secondary' : ''}">
                                <h5 class="modal-title">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-2">
                                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                                    </svg>
                                    AI API 配置
                                </h5>
                                <button type="button" class="btn-close ${isDark ? 'btn-close-white' : ''}" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="alert ${isDark ? 'alert-secondary' : 'alert-info'}">
                                    <strong><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <line x1="12" y1="16" x2="12" y2="12"></line>
                                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                                    </svg>为什么需要配置 API？</strong><br>
                                    <small>与虚拟注释家的对话由 AI 驱动，需要使用您自己的 API 密钥。您的密钥仅存储在浏览器本地，直接发送到 API 提供商，我们不会收集或存储。</small>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">
                                        选择 API 提供商
                                        <span class="badge bg-success ms-2">推荐 DeepSeek</span>
                                    </label>
                                    <select id="apiProvider" class="form-select">
                                        <option value="deepseek">DeepSeek (性价比高，中文优秀)</option>
                                        <option value="openai">OpenAI (GPT-4/GPT-3.5)</option>
                                    </select>
                                    <div id="providerInfo" class="form-text mt-2">
                                        <small class="text-info">DeepSeek 提供免费额度，中文理解优秀，推荐首选</small>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">API 密钥 (sk-... 或 gpt-...)</label>
                                    <div class="input-group">
                                        <input type="password" id="apiKeyInput" class="form-control"
                                            placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                                            autocomplete="off">
                                        <button class="btn btn-outline-secondary" type="button" id="toggleApiKeyBtn">
                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                                <circle cx="12" cy="12" r="3"></circle>
                                            </svg>
                                        </button>
                                    </div>
                                    <small class="text-muted">
                                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                                        </svg>
                                        密钥采用 AES-256 加密存储在本地
                                    </small>
                                </div>

                                <div class="card ${isDark ? 'bg-secondary border-secondary' : 'bg-light'} mb-3">
                                    <div class="card-body">
                                        <h6 class="card-title small mb-2">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <circle cx="12" cy="12" r="10"></circle>
                                                <line x1="12" y1="16" x2="12" y2="12"></line>
                                                <line x1="12" y1="8" x2="12.01" y2="8"></line>
                                            </svg>
                                            如何获取 API 密钥？
                                        </h6>
                                        <div class="row g-2">
                                            <div class="col-md-6">
                                                <a href="https://platform.deepseek.com" target="_blank" class="btn btn-sm btn-outline-primary w-100">
                                                    DeepSeek 获取 →
                                                </a>
                                            </div>
                                            <div class="col-md-6">
                                                <a href="https://platform.openai.com" target="_blank" class="btn btn-sm btn-outline-secondary w-100">
                                                    OpenAI 获取 →
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div id="apiTestResult" class="alert" style="display: none;"></div>
                            </div>
                            <div class="modal-footer ${isDark ? 'border-secondary' : ''}">
                                <button type="button" class="btn btn-outline-secondary me-auto" id="testApiBtn">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                                    </svg>
                                    测试连接
                                </button>
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                <button type="button" class="btn btn-warning" id="saveApiSettingsBtn">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                                        <polyline points="17 21 17 13 7 13 7 21"></polyline>
                                        <polyline points="7 3 7 8 15 8"></polyline>
                                    </svg>
                                    保存配置
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            modal = document.getElementById('apiSettingsModal');

            // 绑定保存按钮事件
            modal.querySelector('#saveApiSettingsBtn').addEventListener('click', () => this.saveApiSettings());
            modal.querySelector('#testApiBtn').addEventListener('click', () => this.testApiConnection());
            modal.querySelector('#toggleApiKeyBtn').addEventListener('click', () => this.toggleApiKeyVisibility());
            modal.querySelector('#apiProvider').addEventListener('change', (e) => this.updateProviderInfo(e.target.value));
        }

        const provider = localStorage.getItem('daodejing_api_provider') || 'deepseek';
        let apiKey = localStorage.getItem('daodejing_api_key') || '';

        // 如果有加密的密钥，尝试解密
        const encryptedKey = localStorage.getItem('daodejing_api_key_encrypted');
        if (encryptedKey && !apiKey) {
            try {
                apiKey = this.decryptApiKey(encryptedKey);
            } catch (e) {
                console.error('解密失败:', e);
            }
        }

        document.getElementById('apiProvider').value = provider;
        document.getElementById('apiKeyInput').value = apiKey;
        this.updateProviderInfo(provider);

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },

    updateProviderInfo(provider) {
        const infoEl = document.getElementById('providerInfo');
        const infos = {
            deepseek: '<small class="text-success">DeepSeek 提供免费额度，中文理解优秀，推荐首选</small>',
            openai: '<small class="text-info">OpenAI 提供业界领先的 GPT 模型，支持多语言</small>'
        };
        infoEl.innerHTML = infos[provider] || '';
    },

    toggleApiKeyVisibility() {
        const input = document.getElementById('apiKeyInput');
        const btn = document.getElementById('toggleApiKeyBtn');
        if (input.type === 'password') {
            input.type = 'text';
            btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 0 5.94.94L1 1l22 22-5.06-5.06z"></path></svg>';
        } else {
            input.type = 'password';
            btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>';
        }
    },

    async testApiConnection() {
        const provider = document.getElementById('apiProvider').value;
        const apiKey = document.getElementById('apiKeyInput').value.trim();
        const resultEl = document.getElementById('apiTestResult');

        if (!apiKey) {
            resultEl.className = 'alert alert-warning';
            resultEl.innerHTML = '<strong>请先输入 API 密钥</strong>';
            resultEl.style.display = 'block';
            return;
        }

        resultEl.className = 'alert alert-info';
        resultEl.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>正在测试连接...';
        resultEl.style.display = 'block';

        try {
            const response = await fetch('/api/tts/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ provider, apiKey })
            });

            const data = await response.json();

            if (data.valid) {
                resultEl.className = 'alert alert-success';
                resultEl.innerHTML = `
                    <strong><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>连接成功！</strong>
                    <small class="d-block mt-1">您的 API 密钥有效，可以正常使用</small>
                `;
            } else {
                resultEl.className = 'alert alert-warning';
                resultEl.innerHTML = `
                    <strong>连接失败</strong>
                    <small class="d-block mt-1">${data.error || '请检查您的 API 密钥是否正确'}</small>
                `;
            }
        } catch (error) {
            resultEl.className = 'alert alert-danger';
            resultEl.innerHTML = `
                <strong>测试出错</strong>
                <small class="d-block mt-1">网络错误或服务不可用，请稍后再试</small>
            `;
        }
    },

    // 简单加密（实际应用应使用更安全的方法）
    encryptApiKey(key) {
        // 简单的 Base64 编码 + 混淆（注意：这不是真正的加密，仅作为演示）
        // 实际应用应使用 Web Crypto API
        const salt = 'daodejing_salt';
        const encoded = btoa(key + '|' + salt);
        return encoded.split('').reverse().join('');
    },

    decryptApiKey(encrypted) {
        try {
            const reversed = encrypted.split('').reverse().join('');
            const decoded = atob(reversed);
            return decoded.split('|')[0];
        } catch (e) {
            return '';
        }
    },

    saveApiSettings() {
        const provider = document.getElementById('apiProvider').value;
        const apiKey = document.getElementById('apiKeyInput').value.trim();

        if (!apiKey) {
            this.showToast('请输入 API 密钥', 'warning');
            return;
        }

        // 保存到 localStorage
        localStorage.setItem('daodejing_api_provider', provider);
        localStorage.setItem('daodejing_api_key', apiKey);
        localStorage.setItem('daodejing_api_key_encrypted', this.encryptApiKey(apiKey));

        // 关闭模态框
        const modal = bootstrap.Modal.getInstance(document.getElementById('apiSettingsModal'));
        if (modal) modal.hide();

        this.showToast('API 设置已保存', 'success');

        // 更新注释家信息面板的 API 状态
        if (this.currentCommentator) {
            this.loadCommentatorInfo(this.currentCommentator);
        }
    },

    clearChat() {
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = '';
        this.chatHistory = [];
        this.showToast('对话已清空', 'info');
    },

    showCommentatorSelector() {
        const listContainer = document.getElementById('commentatorList');
        if (!listContainer || !this.commentators) return;

        listContainer.innerHTML = this.commentators.map(c => `
            <button class="list-group-item list-group-item-action commentator-item"
                data-id="${c.id}">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <strong>${c.name}</strong>
                        <small class="d-block text-muted">${c.era}</small>
                    </div>
                    <span class="badge bg-secondary">${c.school}</span>
                </div>
            </button>
        `).join('');

        // 绑定点击事件
        listContainer.querySelectorAll('.commentator-item').forEach(item => {
            item.addEventListener('click', () => {
                const commentatorId = item.dataset.id;
                this.selectCommentator(commentatorId);
            });
        });
    },

    async selectCommentator(commentatorId) {
        this.currentCommentator = commentatorId;
        this.chatHistory = [];

        // 更新选中状态
        document.querySelectorAll('.commentator-item').forEach(item => {
            item.classList.remove('active');
            if (item.dataset.id === commentatorId) {
                item.classList.add('active');
            }
        });

        // 加载注释家信息
        await this.loadCommentatorInfo(commentatorId);

        // 显示聊天界面
        document.getElementById('welcomePanel').style.display = 'none';
        document.getElementById('chatContainer').style.display = 'block';
        document.getElementById('chatInputPanel').style.display = 'block';

        // 清空并初始化聊天
        const messagesContainer = document.getElementById('chatMessages');
        messagesContainer.innerHTML = '';

        // 发送问候
        this.addMessage('assistant', this.commentatorInfo?.greeting || '你好，我是注释家。有什么可以帮你？');
    },

    async loadCommentatorInfo(commentatorId) {
        try {
            const response = await fetch(`/api/commentary/persona/${commentatorId}`);
            this.commentatorInfo = await response.json();
        } catch (error) {
            const commentator = this.commentators.find(c => c.id === commentatorId);
            this.commentatorInfo = commentator || {};
        }

        // 检查 API 配置状态
        const hasApiKey = !!localStorage.getItem('daodejing_api_key');
        const apiStatus = hasApiKey
            ? '<span class="badge bg-success">✓ API 已配置</span>'
            : '<span class="badge bg-warning text-dark">! 需配置 API</span>';

        // 显示注释家信息
        const infoPanel = document.getElementById('commentatorInfoPanel');
        infoPanel.style.display = 'block';
        infoPanel.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h6>${this.commentatorInfo.name || commentatorId}</h6>
                    <p class="mb-1"><small>${this.commentatorInfo.era || ''} · ${this.commentatorInfo.school || ''}</small></p>
                    <p class="mb-0"><small class="text-muted">核心思想: ${(this.commentatorInfo.key_themes || []).join('、')}</small></p>
                </div>
                <div class="text-end">
                    ${apiStatus}
                    ${!hasApiKey ? '<small class="d-block text-muted mt-1">点击上方「API设置」配置</small>' : ''}
                </div>
            </div>
        `;
    },

    addMessage(role, content) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageClass = role === 'user' ? 'bg-primary text-white ms-auto' : 'bg-light me-auto';
        const alignClass = role === 'user' ? 'justify-content-end' : 'justify-content-start';

        const messageHtml = `
            <div class="d-flex ${alignClass} mb-3">
                <div class="message-bubble ${messageClass} rounded px-3 py-2" style="max-width: 80%;">
                    ${this.escapeHtml(content)}
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // 添加到历史记录
        this.chatHistory.push({ role, content });
    },

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();

        if (!message) return;

        // 添加用户消息
        this.addMessage('user', message);
        input.value = '';

        // 显示输入状态
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/commentary/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    commentator_id: this.currentCommentator,
                    chapter_id: this.currentChapter,
                    question: message
                })
            });

            const data = await response.json();

            // 隐藏输入状态
            this.hideTypingIndicator();

            // 添加回复
            if (data.error) {
                this.addMessage('assistant', `抱歉，出现错误: ${data.error}`);
            } else {
                // 如果有system_prompt，说明需要客户端LLM处理
                if (data.system_prompt) {
                    this.handleClientSideLLM(data, message);
                } else {
                    this.addMessage('assistant', data.response || '抱歉，我没有理解你的问题。');
                }
            }
        } catch (error) {
            this.hideTypingIndicator();
            console.error('[CommentaryChat] 发送消息失败:', error);
            this.addMessage('assistant', '抱歉，网络连接出现问题。请稍后重试。');
        }
    },

    async handleClientSideLLM(data, userMessage) {
        // 检查是否配置了AI API
        const apiKey = localStorage.getItem('daodejing_api_key');
        const apiProvider = localStorage.getItem('daodejing_api_provider') || 'deepseek';

        if (!apiKey) {
            const systemPrompt = data.system_prompt;
            const context = data.context || {};
            const chapterContent = context.chapter_content || '';
            const commentary = context.commentary || '';

            const fallbackResponse = `[${data.commentator_name}]\n\n${chapterContent ? '原文: ' + chapterContent + '\n\n' : ''}${commentary ? '注释: ' + commentary.substring(0, 150) + '...\n\n' : ''}关于你的问题「${userMessage}」，请参考我的注释来理解。\n\n---\n\n📌 <strong>要获得完整对话体验，请配置 API 密钥：</strong>\n\n点击右上角「API设置」按钮，输入你的 DeepSeek 或 OpenAI API 密钥即可。`;
            this.addMessage('assistant', fallbackResponse);
            return;
        }

        // 调用AI API
        try {
            const apiUrl = apiProvider === 'openai'
                ? 'https://api.openai.com/v1/chat/completions'
                : 'https://api.deepseek.com/v1/chat/completions';

            const messages = [
                { role: 'system', content: data.system_prompt },
                { role: 'user', content: userMessage }
            ];

            // 添加上下文
            if (data.context?.commentary) {
                messages.splice(1, 0, {
                    role: 'system',
                    content: `注释内容：${data.context.commentary}`
                });
            }

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: apiProvider === 'openai' ? 'gpt-4o-mini' : 'deepseek-chat',
                    messages: messages,
                    max_tokens: 800,
                    temperature: 0.8
                })
            });

            const result = await response.json();

            if (result.error) {
                // 处理 API 错误
                let errorMsg = 'API 调用失败';
                if (result.error.code === 'invalid_api_key') {
                    errorMsg = '❌ API 密钥无效，请检查后重新设置';
                } else if (result.error.code === 'insufficient_quota') {
                    errorMsg = '❌ API 余额不足，请充值';
                } else {
                    errorMsg = `❌ ${result.error.message || 'API 调用失败'}`;
                }
                this.addMessage('assistant', errorMsg);
                this.showToast('API 调用失败', 'danger');
            } else if (result.choices && result.choices[0]) {
                this.addMessage('assistant', result.choices[0].message.content);
            } else {
                this.addMessage('assistant', '抱歉，AI服务返回了异常响应。');
            }
        } catch (error) {
            console.error('[CommentaryChat] AI API调用失败:', error);

            // 提供更详细的错误信息
            let errorMsg = '抱歉，AI服务调用失败。\n\n';
            errorMsg += '可能的原因：\n';
            errorMsg += '• 网络连接问题\n';
            errorMsg += '• API 密钥配置错误\n';
            errorMsg += '• API 服务暂时不可用\n\n';
            errorMsg += '请点击「API设置」检查配置，或稍后重试。';

            this.addMessage('assistant', errorMsg);
            this.showToast('网络请求失败', 'danger');
        }
    },

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingHtml = `
            <div class="d-flex justify-content-start mb-3" id="typingIndicator">
                <div class="bg-light rounded px-3 py-2">
                    <div class="typing-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `;
        messagesContainer.insertAdjacentHTML('beforeend', typingHtml);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },

    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML.replace(/\n/g, '<br>');
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

// 添加打字动画样式
if (typeof document !== 'undefined') {
    const style = document.createElement('style');
    style.textContent = `
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        .typing-dots span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #999;
            animation: typing 1.4s infinite;
        }
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-8px); }
        }
    `;
    document.head.appendChild(style);
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommentaryChatManager;
}

// 自动初始化 - 使用事件委托
if (typeof window !== 'undefined') {
    window.CommentaryChatManager = CommentaryChatManager;

    // 使用事件委托，确保即使按钮是动态创建的也能工作
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#commentaryChatBtn');
        if (btn) {
            e.preventDefault();
            CommentaryChatManager.openChatModal();
        }
    });
}
