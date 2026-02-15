const UserPanelManager={STORAGE_KEY:'daodejing_user_data',init(){this.createUserPanel();this.bindEvents();this.loadUserData();},createUserPanel(){if(document.getElementById('userPanel'))return;const panelHtml=`
            <div id="userPanel" class="offcanvas offcanvas-end" tabindex="-1" style="width: 400px;">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        用户中心
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
                </div>
                <div class="offcanvas-body p-0">
                    <ul class="nav nav-tabs nav-fill" id="userTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active" id="bookmarks-tab" data-bs-toggle="tab" data-bs-target="#bookmarks-panel" type="button">
                                书签
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="notes-tab" data-bs-toggle="tab" data-bs-target="#notes-panel" type="button">
                                笔记
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link" id="history-tab" data-bs-toggle="tab" data-bs-target="#history-panel" type="button">
                                历史
                            </button>
                        </li>
                    </ul>
                    <div class="tab-content p-3" id="userTabContent">
                        <div class="tab-pane fade show active" id="bookmarks-panel">
                            <div id="bookmarksList" class="bookmarks-container">
                                <p class="text-muted text-center py-4">暂无书签</p>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="notes-panel">
                            <div id="notesList" class="notes-container">
                                <p class="text-muted text-center py-4">暂无笔记</p>
                            </div>
                        </div>
                        <div class="tab-pane fade" id="history-panel">
                            <div id="historyList" class="history-container">
                                <p class="text-muted text-center py-4">暂无阅读历史</p>
                            </div>
                        </div>
                    </div>
                    <div class="border-top p-3">
                        <div class="d-grid gap-2">
                            <button class="btn btn-outline-primary btn-sm" id="exportDataBtn">
                                导出数据
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" id="importDataBtn">
                                导入数据
                            </button>
                            <input type="file" id="importFileInput" accept=".json" style="display: none;">
                        </div>
                    </div>
                </div>
            </div>
        `;document.body.insertAdjacentHTML('beforeend',panelHtml);this.createPanelTrigger();},createPanelTrigger(){const navbar=document.querySelector('.navbar-nav')||document.querySelector('.nav');if(navbar&&!document.getElementById('userPanelBtn')){const btnHtml=`
                <li class="nav-item">
                    <button class="nav-link btn btn-link" id="userPanelBtn" title="用户中心">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                            <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                    </button>
                </li>
            `;navbar.insertAdjacentHTML('beforeend',btnHtml);}},bindEvents(){document.addEventListener('click',(e)=>{const btn=e.target.closest('#userPanelBtn');if(btn){e.preventDefault();this.openPanel();}});document.addEventListener('click',(e)=>{if(e.target.closest('#exportDataBtn')){this.exportAllData();}});document.addEventListener('click',(e)=>{if(e.target.closest('#importDataBtn')){document.getElementById('importFileInput').click();}});document.addEventListener('change',(e)=>{if(e.target.id==='importFileInput'&&e.target.files.length>0){this.importAllData(e.target.files[0]);}});document.querySelectorAll('#userTabs button').forEach(tab=>{tab.addEventListener('shown.bs.tab',(e)=>{const target=e.target.getAttribute('data-bs-target');if(target==='#bookmarks-panel'){this.refreshBookmarksList();}else if(target==='#notes-panel'){this.refreshNotesList();}else if(target==='#history-panel'){this.refreshHistoryList();}});});},openPanel(){const panel=document.getElementById('userPanel');if(panel){const bsPanel=new bootstrap.Offcanvas(panel);bsPanel.show();this.refreshBookmarksList();}},loadUserData(){this.refreshBookmarksList();},refreshBookmarksList(){const container=document.getElementById('bookmarksList');if(!container)return;const bookmarks=BookmarkManager.getBookmarks?BookmarkManager.getBookmarks():{chapters:[]};if(!bookmarks.chapters||bookmarks.chapters.length===0){container.innerHTML=`
                <div class="text-center text-muted py-4">
                    <p>暂无书签</p>
                    <small>在阅读页面点击收藏按钮添加书签</small>
                </div>
            `;return;}
let html='<div class="list-group list-group-flush">';bookmarks.chapters.forEach(ch=>{html+=`
                <div class="list-group-item d-flex justify-content-between align-items-center">
                    <a href="/daodejing/chapter/${ch}" class="text-decoration-none flex-grow-1">
                        第${ch}章
                    </a>
                    <button class="btn btn-sm btn-link text-danger" onclick="UserPanelManager.removeBookmark(${ch})">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            `;});html+='</div>';if(bookmarks.chapters.length>0){html+=`
                <div class="mt-3 text-center">
                    <button class="btn btn-outline-danger btn-sm" onclick="BookmarkManager.clearAll()">
                        清空所有书签
                    </button>
                </div>
            `;}
container.innerHTML=html;},refreshNotesList(){const container=document.getElementById('notesList');if(!container)return;const stats=NotesManager.getStats?NotesManager.getStats():{count:0,chapters:[],totalChars:0};if(stats.count===0){container.innerHTML=`
                <div class="text-center text-muted py-4">
                    <p>暂无笔记</p>
                    <small>在阅读页面点击笔记按钮添加笔记</small>
                </div>
            `;return;}
const notes=NotesManager.getAllNotes?NotesManager.getAllNotes():{};let html=`
            <div class="mb-3 text-muted small">
                共 ${stats.count} 条笔记，${stats.totalChars} 字
            </div>
            <div class="list-group list-group-flush">
        `;stats.chapters.forEach(ch=>{const note=notes[ch];const preview=note.substring(0,50)+(note.length>50?'...':'');html+=`
                <div class="list-group-item">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                        <a href="/daodejing/chapter/${ch}" class="fw-bold text-decoration-none">
                            第${ch}章
                        </a>
                        <span class="badge bg-light text-dark">${note.length}字</span>
                    </div>
                    <p class="mb-1 text-muted small">${this.escapeHtml(preview)}</p>
                </div>
            `;});html+='</div>';container.innerHTML=html;},refreshHistoryList(){const container=document.getElementById('historyList');if(!container)return;let history=[];if(window.ReadingProgressManager&&ReadingProgressManager.getHistory){history=ReadingProgressManager.getHistory();}
if(!history||history.length===0){container.innerHTML=`
                <div class="text-center text-muted py-4">
                    <p>暂无阅读历史</p>
                    <small>系统会自动记录您的阅读进度</small>
                </div>
            `;return;}
let html='<div class="list-group list-group-flush">';history.slice(0,20).forEach(item=>{const date=new Date(item.timestamp).toLocaleDateString('zh-CN');html+=`
                <div class="list-group-item">
                    <a href="/daodejing/chapter/${item.chapter}" class="text-decoration-none">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>第${item.chapter}章</span>
                            <small class="text-muted">${date}</small>
                        </div>
                    </a>
                </div>
            `;});html+='</div>';if(history.length>0){html+=`
                <div class="mt-3 text-center">
                    <button class="btn btn-outline-secondary btn-sm" onclick="localStorage.removeItem('daodejing_reading_history'); UserPanelManager.refreshHistoryList();">
                        清空历史记录
                    </button>
                </div>
            `;}
container.innerHTML=html;},removeBookmark(chapter){if(BookmarkManager.toggleChapterBookmark){BookmarkManager.toggleChapterBookmark(chapter);this.refreshBookmarksList();}},exportAllData(){const bookmarks=BookmarkManager.getBookmarks?BookmarkManager.getBookmarks():{chapters:[]};const notes=NotesManager.getAllNotes?NotesManager.getAllNotes():{};let history=[];if(window.ReadingProgressManager&&ReadingProgressManager.getHistory){history=ReadingProgressManager.getHistory();}
const exportData={version:'1.0',exportDate:new Date().toISOString(),bookmarks:bookmarks,notes:notes,history:history};const blob=new Blob([JSON.stringify(exportData,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`daodejing_backup_${new Date().toISOString().split('T')[0]}.json`;a.click();URL.revokeObjectURL(url);this.showToast('数据已导出','success');},importAllData(file){const reader=new FileReader();reader.onload=(e)=>{try{const data=JSON.parse(e.target.result);if(data.bookmarks){localStorage.setItem('daodejing_bookmarks',JSON.stringify(data.bookmarks));}
if(data.notes){localStorage.setItem('daodejing_notes',JSON.stringify(data.notes));}
if(data.history){localStorage.setItem('daodejing_reading_history',JSON.stringify(data.history));}
if(BookmarkManager.loadBookmarks)BookmarkManager.loadBookmarks();if(BookmarkManager.setupBookmarkButtons)BookmarkManager.setupBookmarkButtons();this.refreshBookmarksList();this.refreshNotesList();this.refreshHistoryList();this.showToast('数据导入成功','success');}catch(err){console.error('[UserPanelManager] 导入数据失败:',err);this.showToast('导入失败，文件格式错误','danger');}};reader.readAsText(file);},escapeHtml(text){const div=document.createElement('div');div.textContent=text;return div.innerHTML;},showToast(message,type='info'){const toast=document.createElement('div');toast.className=`toast align-items-center text-white bg-${type} border-0`;toast.style.cssText='position: fixed; bottom: 20px; right: 20px; z-index: 1100;';toast.innerHTML=`
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;document.body.appendChild(toast);const bsToast=new bootstrap.Toast(toast,{delay:2000});bsToast.show();toast.addEventListener('hidden.bs.toast',()=>{toast.remove();});}};if(typeof module!=='undefined'&&module.exports){module.exports=UserPanelManager;}
if(typeof window!=='undefined'){window.UserPanelManager=UserPanelManager;if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',()=>UserPanelManager.init());}else{UserPanelManager.init();}}