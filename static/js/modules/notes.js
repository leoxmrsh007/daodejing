/**
 * 笔记管理模块
 * 支持添加、编辑、删除、导出笔记
 */

const NotesManager = {
    STORAGE_KEY: 'daodejing_notes',
    EXPORT_KEY: 'daodejing_notes_export',

    init() {
        this.noteBtn = document.getElementById('noteBtn');
        this.currentChapter = this.getCurrentChapter();

        if (!this.noteBtn) return;

        this.bindEvents();
        this.updateButtonState();
    },

    getCurrentChapter() {
        // 从面包屑获取章节号
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            if (match) return parseInt(match[1]);
        }

        // 从URL路径获取
        const pathMatch = window.location.pathname.match(/\/chapter\/?(\d+)/);
        if (pathMatch) {
            return parseInt(pathMatch[1]);
        }

        return null;
    },

    bindEvents() {
        this.noteBtn.addEventListener('click', () => this.openNoteModal());

        // 确保模态框存在
        this.ensureModalExists();
    },

    ensureModalExists() {
        let modal = document.getElementById('noteModal');
        if (!modal) {
            const modalHtml = `
                <div class="modal fade" id="noteModal" tabindex="-1">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">📝 阅读笔记</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="noteTextarea" class="form-label">笔记内容</label>
                                    <textarea id="noteTextarea" class="form-control" rows="8"
                                        placeholder="写下你的阅读心得..."></textarea>
                                </div>
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted">
                                        <span id="noteCharCount">0</span> 字
                                    </small>
                                    <small class="text-muted">保存在本地浏览器中</small>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                <button type="button" class="btn btn-danger me-auto" id="deleteNoteBtn" style="display:none;">删除</button>
                                <button type="button" class="btn btn-primary" id="saveNoteBtn">保存</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            modal = document.getElementById('noteModal');

            // 绑定保存和删除按钮
            modal.querySelector('#saveNoteBtn').addEventListener('click', () => this.saveNote());
            modal.querySelector('#deleteNoteBtn').addEventListener('click', () => this.deleteNote());

            // 字数统计
            const textarea = modal.querySelector('#noteTextarea');
            textarea.addEventListener('input', () => {
                document.getElementById('noteCharCount').textContent = textarea.value.length;
            });
        }
    },

    openNoteModal() {
        this.ensureModalExists();

        const modal = document.getElementById('noteModal');
        const textarea = document.getElementById('noteTextarea');
        const deleteBtn = document.getElementById('deleteNoteBtn');

        // 加载当前章节的笔记
        const note = this.getNote(this.currentChapter);
        textarea.value = note || '';

        // 更新字数统计
        document.getElementById('noteCharCount').textContent = textarea.value.length;

        // 显示/显示删除按钮
        if (note) {
            deleteBtn.style.display = 'block';
        } else {
            deleteBtn.style.display = 'none';
        }

        // 显示模态框
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    },

    getNote(chapter) {
        const notes = this.getAllNotes();
        return notes[chapter] || null;
    },

    getAllNotes() {
        try {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            return saved ? JSON.parse(saved) : {};
        } catch (e) {
            console.error('[NotesManager] 读取笔记失败:', e);
            return {};
        }
    },

    saveNote() {
        const textarea = document.getElementById('noteTextarea');
        const noteText = textarea.value.trim();

        if (!noteText) {
            this.showToast('请输入笔记内容', 'warning');
            return;
        }

        const notes = this.getAllNotes();
        notes[this.currentChapter] = noteText;

        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(notes));
            this.updateButtonState();
            this.showToast('笔记已保存', 'success');

            // 关闭模态框
            const modal = bootstrap.Modal.getInstance(document.getElementById('noteModal'));
            if (modal) modal.hide();
        } catch (e) {
            console.error('[NotesManager] 保存笔记失败:', e);
            this.showToast('保存失败，请重试', 'danger');
        }
    },

    deleteNote() {
        if (!confirm('确定要删除这条笔记吗？')) {
            return;
        }

        const notes = this.getAllNotes();
        delete notes[this.currentChapter];

        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(notes));
            document.getElementById('noteTextarea').value = '';
            document.getElementById('noteCharCount').textContent = '0';
            document.getElementById('deleteNoteBtn').style.display = 'none';
            this.updateButtonState();
            this.showToast('笔记已删除', 'info');
        } catch (e) {
            console.error('[NotesManager] 删除笔记失败:', e);
            this.showToast('删除失败', 'danger');
        }
    },

    updateButtonState() {
        if (!this.noteBtn) return;

        const note = this.getNote(this.currentChapter);
        if (note) {
            this.noteBtn.classList.add('active');
            this.noteBtn.innerHTML = `
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
                <span class="ms-1">编辑笔记</span>
            `;
        } else {
            this.noteBtn.classList.remove('active');
            this.noteBtn.innerHTML = `
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
                <span class="ms-1">笔记</span>
            `;
        }
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
    },

    // 导出所有笔记
    exportNotes() {
        const notes = this.getAllNotes();
        const noteCount = Object.keys(notes).length;

        if (noteCount === 0) {
            this.showToast('暂无笔记可导出', 'warning');
            return;
        }

        // 生成导出数据
        const exportData = {
            exportDate: new Date().toISOString(),
            noteCount: noteCount,
            notes: notes
        };

        // 创建下载链接
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `daodejing_notes_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);

        this.showToast(`已导出 ${noteCount} 条笔记`, 'success');
    },

    // 导入笔记
    importNotes(file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);

                if (!data.notes || typeof data.notes !== 'object') {
                    throw new Error('无效的笔记文件');
                }

                // 合并笔记
                const existingNotes = this.getAllNotes();
                const mergedNotes = { ...existingNotes, ...data.notes };

                localStorage.setItem(this.STORAGE_KEY, JSON.stringify(mergedNotes));

                const importedCount = Object.keys(data.notes).length;
                this.showToast(`已导入 ${importedCount} 条笔记`, 'success');
                this.updateButtonState();
            } catch (err) {
                console.error('[NotesManager] 导入笔记失败:', err);
                this.showToast('导入失败，文件格式错误', 'danger');
            }
        };

        reader.readAsText(file);
    },

    // 获取笔记统计
    getStats() {
        const notes = this.getAllNotes();
        const chapters = Object.keys(notes).map(Number).sort((a, b) => a - b);
        const totalChars = Object.values(notes).reduce((sum, note) => sum + note.length, 0);

        return {
            count: chapters.length,
            chapters: chapters,
            totalChars: totalChars,
            avgChars: chapters.length > 0 ? Math.round(totalChars / chapters.length) : 0
        };
    }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotesManager;
}

// 自动初始化
if (typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => NotesManager.init());
    } else {
        NotesManager.init();
    }
    window.NotesManager = NotesManager;
}
