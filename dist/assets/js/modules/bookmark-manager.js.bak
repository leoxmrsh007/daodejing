/**
 * 用户认证管理器
 * 管理用户登录、注册、会话状态
 */
const AuthManager = {
    TOKEN_KEY: 'daodejing_auth_token',
    USER_KEY: 'daodejing_user_info',

    /**
     * 用户注册
     * @param {string} username - 用户名
     * @param {string} email - 邮箱
     * @param {string} password - 密码
     * @returns {Promise} 注册结果
     */
    async register(username, email, password) {
        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password })
            });

            const data = await response.json();

            if (data.success) {
                // 注册成功，自动登录
                return await this.login(email, password);
            }

            return {
                success: false,
                error: data.error || '注册失败'
            };
        } catch (error) {
            console.error('[AuthManager] 注册失败:', error);
            return {
                success: false,
                error: '网络错误，请稍后重试'
            };
        }
    },

    /**
     * 用户登录
     * @param {string} usernameOrEmail - 用户名或邮箱
     * @param {string} password - 密码
     * @returns {Promise} 登录结果
     */
    async login(usernameOrEmail, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username_or_email: usernameOrEmail, password })
            });

            const data = await response.json();

            if (data.success) {
                // 保存 token 和用户信息
                this.saveToken(data.token);
                this.saveUser({
                    id: data.user_id,
                    username: data.username,
                });

                console.log('[AuthManager] 登录成功:', data.username);
                return { success: true, user: data };
            }

            return {
                success: false,
                error: data.error || '登录失败'
            };
        } catch (error) {
            console.error('[AuthManager] 登录失败:', error);
            return {
                success: false,
                error: '网络错误，请稍后重试'
            };
        }
    },

    /**
     * 用户登出
     * @returns {Promise} 登出结果
     */
    async logout() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            // 清除本地存储
            this.clearSession();

            console.log('[AuthManager] 已登出');
            return { success: true };
        } catch (error) {
            console.error('[AuthManager] 登出失败:', error);
            // 即使API失败，也清除本地存储
            this.clearSession();
            return { success: true };
        }
    },

    /**
     * 获取当前用户信息
     * @returns {Object|null} 用户信息
     */
    getCurrentUser() {
        try {
            const userJson = localStorage.getItem(this.USER_KEY);
            return userJson ? JSON.parse(userJson) : null;
        } catch (error) {
            console.error('[AuthManager] 获取用户信息失败:', error);
            return null;
        }
    },

    /**
     * 检查是否已登录
     * @returns {boolean} 是否已登录
     */
    isLoggedIn() {
        return !!this.getToken();
    },

    /**
     * 获取认证 Token
     * @returns {string|null} JWT Token
     */
    getToken() {
        return localStorage.getItem(this.TOKEN_KEY);
    },

    /**
     * 保存 Token
     * @param {string} token - JWT Token
     */
    saveToken(token) {
        localStorage.setItem(this.TOKEN_KEY, token);
    },

    /**
     * 保存用户信息
     * @param {Object} user - 用户信息
     */
    saveUser(user) {
        localStorage.setItem(this.USER_KEY, JSON.stringify(user));
    },

    /**
     * 清除会话
     */
    clearSession() {
        localStorage.removeItem(this.TOKEN_KEY);
        localStorage.removeItem(this.USER_KEY);
    },

    /**
     * 获取认证请求头
     * @returns {Object} 请求头
     */
    getAuthHeaders() {
        const token = this.getToken();
        if (!token) return {};

        return {
            'Authorization': `Bearer ${token}`
        };
    },

    /**
     * 获取当前用户ID
     * @returns {string|null} 用户ID
     */
    getCurrentUserId() {
        const user = this.getCurrentUser();
        return user ? user.id : null;
    },

    /**
     * 显示登录模态框
     */
    showLoginModal() {
        const modalHtml = `
            <div class="modal fade" id="authModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">用户登录</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="auth-tabs">
                                <ul class="nav nav-pills nav-fill mb-3" role="tablist">
                                    <li class="nav-item" role="presentation">
                                        <button class="nav-link active" id="loginTab"
                                                data-bs-toggle="pill"
                                                data-bs-target="#loginForm"
                                                type="button"
                                                role="tab"
                                                aria-selected="true">
                                            登录
                                        </button>
                                    </li>
                                    <li class="nav-item" role="presentation">
                                        <button class="nav-link" id="registerTab"
                                                data-bs-toggle="pill"
                                                data-bs-target="#registerForm"
                                                type="button"
                                                role="tab"
                                                aria-selected="false">
                                            注册
                                        </button>
                                    </li>
                                </ul>
                            </div>

                            <!-- 登录表单 -->
                            <div class="tab-content mt-3" id="loginForm">
                                <form id="loginFormElement">
                                    <div class="mb-3">
                                        <label for="loginUsernameOrEmail" class="form-label">用户名/邮箱</label>
                                        <input type="text" class="form-control" id="loginUsernameOrEmail"
                                               name="username_or_email" required
                                               placeholder="请输入用户名或邮箱">
                                    </div>
                                    <div class="mb-3">
                                        <label for="loginPassword" class="form-label">密码</label>
                                        <input type="password" class="form-control" id="loginPassword"
                                               name="password" required
                                               placeholder="请输入密码">
                                    </div>
                                    <div class="mb-3">
                                        <div class="form-check">
                                            <input type="checkbox" class="form-check-input" id="rememberMe">
                                            <label class="form-check-label" for="rememberMe">记住我</label>
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary w-100">
                                        登录
                                    </button>
                                </form>
                            </div>

                            <!-- 注册表单 -->
                            <div class="tab-content mt-3 d-none" id="registerForm">
                                <form id="registerFormElement">
                                    <div class="mb-3">
                                        <label for="registerUsername" class="form-label">用户名</label>
                                        <input type="text" class="form-control" id="registerUsername"
                                               name="username" required
                                               placeholder="请输入用户名（3-20字符）">
                                        <div class="form-text">至少3个字符</div>
                                    </div>
                                    <div class="mb-3">
                                        <label for="registerEmail" class="form-label">邮箱</label>
                                        <input type="email" class="form-control" id="registerEmail"
                                               name="email" required
                                               placeholder="请输入邮箱地址">
                                    </div>
                                    <div class="mb-3">
                                        <label for="registerPassword" class="form-label">密码</label>
                                        <input type="password" class="form-control" id="registerPassword"
                                               name="password" required
                                               placeholder="请输入密码（至少6个字符）">
                                        <div class="form-text">至少6个字符</div>
                                    </div>
                                    <button type="submit" class="btn btn-primary w-100">
                                        注册
                                    </button>
                                </form>
                            </div>

                            <!-- 错误/成功消息 -->
                            <div id="authMessage" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // 添加到页面
        const authModal = document.createElement('div');
        authModal.innerHTML = modalHtml;
        document.body.appendChild(authModal);

        // 初始化模态框
        const modal = new bootstrap.Modal(document.getElementById('authModal'));
        modal.show();

        // 绑定事件
        this._bindAuthEvents();

        // 模态框关闭时移除
        document.getElementById('authModal').addEventListener('hidden.bs.modal', () => {
            authModal.remove();
        });
    },

    /**
     * 绑定认证事件
     */
    _bindAuthEvents() {
        // 标签切换
        document.getElementById('loginTab').addEventListener('shown.bs.tab', () => {
            document.getElementById('loginForm').classList.remove('d-none');
            document.getElementById('registerForm').classList.add('d-none');
        });

        document.getElementById('registerTab').addEventListener('shown.bs.tab', () => {
            document.getElementById('loginForm').classList.add('d-none');
            document.getElementById('registerForm').classList.remove('d-none');
        });

        // 登录表单提交
        document.getElementById('loginFormElement').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            const result = await this.login(
                formData.get('username_or_email'),
                formData.get('password')
            );

            if (result.success) {
                this._showAuthMessage('登录成功！', 'success');
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('authModal'));
                    if (modal) modal.hide();
                    location.reload();
                }, 1000);
            } else {
                this._showAuthMessage(result.error, 'danger');
            }
        });

        // 注册表单提交
        document.getElementById('registerFormElement').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);

            const result = await this.register(
                formData.get('username'),
                formData.get('email'),
                formData.get('password')
            );

            if (result.success) {
                this._showAuthMessage('注册成功！正在登录...', 'success');
            } else {
                this._showAuthMessage(result.error, 'danger');
            }
        });
    },

    /**
     * 显示认证消息
     * @param {string} message - 消息内容
     * @param {string} type - 消息类型 (success/danger)
     */
    _showAuthMessage(message, type) {
        const messageDiv = document.getElementById('authMessage');
        messageDiv.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    },

    /**
     * 更新用户界面
     */
    updateUI() {
        const user = this.getCurrentUser();
        const loginButton = document.getElementById('loginButton');

        if (user && loginButton) {
            // 显示用户信息
            loginButton.innerHTML = `
                <div class="dropdown">
                    <button class="btn btn-sm btn-outline-light dropdown-toggle" type="button"
                            data-bs-toggle="dropdown">
                        👤 ${user.username}
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li><a class="dropdown-item" href="#">个人中心</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <button class="dropdown-item text-danger" id="logoutButton">
                                退出登录
                            </button>
                        </li>
                    </ul>
                </div>
            `;

            // 绑定登出事件
            document.getElementById('logoutButton').addEventListener('click', async () => {
                await this.logout();
                location.reload();
            });
        }
    }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuthManager;
}

if (typeof window !== 'undefined') {
    window.AuthManager = AuthManager;
}
