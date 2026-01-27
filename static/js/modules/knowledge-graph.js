/**
 * 知识图谱可视化模块
 * 展示道德经概念关系网络和注释观点谱系
 */

const KnowledgeGraphManager = {
    graphData: null,
    svg: null,
    simulation: null,
    currentChapter: null,

    init() {
        this.graphBtn = document.getElementById('knowledgeGraphBtn');
        if (!this.graphBtn) return;

        this.graphBtn.addEventListener('click', () => this.showKnowledgeGraph());
    },

    async showKnowledgeGraph() {
        console.log('[KnowledgeGraph] showKnowledgeGraph 开始执行');
        const chapter = this.getCurrentChapter();
        console.log('[KnowledgeGraph] 当前章节:', chapter);

        if (!chapter) {
            this.showToast('无法获取当前章节', 'warning');
            return;
        }

        // 创建模态框
        this.ensureModalExists();
        console.log('[KnowledgeGraph] 模态框已创建');

        // 显示加载状态
        const modal = document.getElementById('knowledgeGraphModal');
        if (!modal) {
            console.error('[KnowledgeGraph] 模态框未找到');
            return;
        }

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        console.log('[KnowledgeGraph] 模态框已显示');

        // 显示加载动画
        this.showLoadingState();

        // 加载数据
        await this.loadGraphData(chapter);
        console.log('[KnowledgeGraph] 数据已加载');

        // 渲染图谱
        this.hideLoadingState();
        this.renderGraph();
        console.log('[KnowledgeGraph] 图谱已渲染');
    },

    showLoadingState() {
        const graphContainer = document.getElementById('graphContainer');
        if (graphContainer) {
            graphContainer.innerHTML = `
                <div class="d-flex flex-column align-items-center justify-content-center h-100">
                    <div class="spinner-border text-warning mb-3" role="status" style="width: 3rem; height: 3rem;">
                        <span class="visually-hidden">加载中...</span>
                    </div>
                    <p class="text-muted mb-0">正在构建概念关系网络...</p>
                    <small class="text-muted">分析概念关联 · 生成关系图谱</small>
                </div>
            `;
        }
    },

    hideLoadingState() {
        const graphContainer = document.getElementById('graphContainer');
        if (graphContainer) {
            graphContainer.innerHTML = '<svg id="knowledgeGraphSvg" style="width: 100%; height: 100%;"></svg>';
        }
    },

    getCurrentChapter() {
        const breadcrumb = document.querySelector('.breadcrumb .active');
        if (breadcrumb) {
            const match = breadcrumb.textContent.match(/第(\d+)章/);
            const chapter = match ? parseInt(match[1]) : null;
            this.currentChapter = chapter;
            return chapter;
        }
        return null;
    },

    async loadGraphData(chapter) {
        try {
            const response = await fetch(`/api/knowledge/graph/${chapter}`);
            this.graphData = await response.json();
        } catch (error) {
            console.error('[KnowledgeGraph] 加载数据失败:', error);
            this.graphData = this.getMockData();
        }
    },

    getMockData() {
        // 模拟数据用于静态版本
        return {
            concept_graph: {
                nodes: [
                    { id: '道', label: '道', level: 1, size: 40, chapters: [1, 4, 14, 21, 25, 30, 35, 40, 42, 51, 62] },
                    { id: '德', label: '德', level: 1, size: 35, chapters: [1, 10, 21, 23, 38, 41, 51, 54, 55, 59, 60, 61, 65, 79] },
                    { id: '无为', label: '无为', level: 2, size: 30, chapters: [2, 3, 10, 29, 37, 43, 48, 57, 63, 64] },
                    { id: '自然', label: '自然', level: 2, size: 28, chapters: [2, 17, 23, 25, 51, 64, 73] },
                    { id: '无', label: '无', level: 2, size: 25, chapters: [1, 2, 5, 6, 7, 8, 9, 11, 14, 15, 16, 20] },
                    { id: '有', label: '有', level: 2, size: 25, chapters: [1, 2, 6, 11, 13, 15, 20, 22, 24, 40, 51, 63] },
                    { id: '圣人', label: '圣人', level: 3, size: 22, chapters: [2, 3, 4, 5, 7, 12, 22, 26, 30, 32, 36, 39, 41, 47, 49, 57, 58, 60, 64, 66, 70, 71, 72, 73, 75, 78, 79, 81] },
                    { id: '水', label: '水', level: 4, size: 18, chapters: [8, 15, 36, 43, 61, 66, 78] },
                    { id: '朴', label: '朴', level: 4, size: 18, chapters: [15, 19, 28, 32, 37, 57] }
                ],
                edges: [
                    { source: '道', target: '德', weight: 5, label: '体用关系' },
                    { source: '道', target: '无', weight: 4, label: '包含关系' },
                    { source: '道', target: '有', weight: 4, label: '包含关系' },
                    { source: '无', target: '有', weight: 5, label: '对立统一' },
                    { source: '道', target: '无为', weight: 3, label: '方法关系' },
                    { source: '道', target: '自然', weight: 3, label: '属性关系' },
                    { source: '无为', target: '圣人', weight: 3, label: '实践关系' },
                    { source: '德', target: '圣人', weight: 3, label: '体现关系' },
                    { source: '道', target: '水', weight: 2, label: '比喻关系' },
                    { source: '道', target: '朴', weight: 2, label: '比喻关系' }
                ],
                concept_count: 9,
                edge_count: 10
            },
            commentary_spectrum: {
                chapter: this.currentChapter,
                commentaries: {},
                comparisons: [],
                clusters: [],
                summary: '本章知识图谱'
            }
        };
    },

    ensureModalExists() {
        let modal = document.getElementById('knowledgeGraphModal');

        if (!modal) {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            const graphBgClass = isDark ? 'bg-dark border-secondary' : 'bg-light';
            const modalClass = isDark ? 'bg-dark text-light border-secondary' : '';

            const modalHtml = `
                <div class="modal fade" id="knowledgeGraphModal" tabindex="-1">
                    <div class="modal-dialog modal-xl modal-dialog-centered">
                        <div class="modal-content ${modalClass}" style="border: none;">
                            <div class="modal-header ${isDark ? 'bg-dark border-secondary' : ''}">
                                <h5 class="modal-title">
                                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#f0ad4e" stroke-width="2" class="me-2">
                                        <circle cx="12" cy="12" r="3"></circle>
                                        <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83"></path>
                                    </svg>
                                    <span class="text-warning">概念关系图谱</span>
                                </h5>
                                <button type="button" class="btn-close ${isDark ? 'btn-close-white' : ''}" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row mb-3">
                                    <div class="col-md-6">
                                        <div class="btn-group" role="group">
                                            <button type="button" class="btn btn-outline-warning btn-sm" id="graphViewBtn">
                                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                    <circle cx="12" cy="12" r="10"></circle>
                                                    <circle cx="12" cy="12" r="3"></circle>
                                                </svg>
                                                关系图
                                            </button>
                                            <button type="button" class="btn btn-outline-warning btn-sm" id="conceptListViewBtn">
                                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                    <line x1="8" y1="6" x2="21" y2="6"></line>
                                                    <line x1="8" y1="12" x2="21" y2="12"></line>
                                                    <line x1="8" y1="18" x2="21" y2="18"></line>
                                                    <line x1="3" y1="6" x2="3.01" y2="6"></line>
                                                    <line x1="3" y1="12" x2="3.01" y2="12"></line>
                                                    <line x1="3" y1="18" x2="3.01" y2="18"></line>
                                                </svg>
                                                概念列表
                                            </button>
                                        </div>
                                    </div>
                                    <div class="col-md-6 text-end">
                                        <button type="button" class="btn btn-outline-secondary btn-sm" id="resetZoomBtn">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                                                <path d="M3 3v5h5"></path>
                                            </svg>
                                            重置视图
                                        </button>
                                        <button type="button" class="btn btn-outline-warning btn-sm ms-2" id="animateGraphBtn">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                <polygon points="5 3 19 12 5 21 5 3"></polygon>
                                            </svg>
                                            动画效果
                                        </button>
                                    </div>
                                </div>
                                <div id="graphContainer" class="border rounded ${graphBgClass}" style="height: 500px; position: relative; overflow: hidden;">
                                    <svg id="knowledgeGraphSvg" style="width: 100%; height: 100%;"></svg>
                                </div>
                                <div id="conceptListContainer" style="display: none;">
                                    <div class="table-responsive">
                                        <table class="table table-sm">
                                            <thead>
                                                <tr>
                                                    <th>概念</th>
                                                    <th>层级</th>
                                                    <th>出现章节数</th>
                                                    <th>相关章节</th>
                                                </tr>
                                            </thead>
                                            <tbody id="conceptTableBody"></tbody>
                                        </table>
                                    </div>
                                </div>
                                <div id="nodeInfoPanel" class="mt-3 p-3 border rounded ${isDark ? 'bg-secondary border-warning' : 'bg-light'}" style="display: none;">
                                    <h6 id="nodeInfoTitle" class="text-warning"></h6>
                                    <div id="nodeInfoContent"></div>
                                </div>
                            </div>
                            <div class="modal-footer ${isDark ? 'bg-dark border-secondary' : ''}">
                                <small class="text-muted">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <line x1="12" y1="16" x2="12" y2="12"></line>
                                        <line x1="12" y1="8" x2="12.01" y2="8"></line>
                                    </svg>
                                    点击节点查看详情 | 滚轮缩放 | 拖拽移动
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            modal = document.getElementById('knowledgeGraphModal');

            // 绑定事件
            modal.querySelector('#graphViewBtn').addEventListener('click', () => {
                document.getElementById('graphContainer').style.display = 'block';
                document.getElementById('conceptListContainer').style.display = 'none';
            });

            modal.querySelector('#conceptListViewBtn').addEventListener('click', () => {
                this.showConceptList();
            });

            modal.querySelector('#resetZoomBtn').addEventListener('click', () => {
                this.resetZoom();
            });

            modal.querySelector('#animateGraphBtn').addEventListener('click', () => {
                this.animateNodes();
            });
        }
    },

    renderGraph() {
        const svg = document.getElementById('knowledgeGraphSvg');
        if (!svg || !this.graphData) return;

        const container = document.getElementById('graphContainer');
        const width = container.clientWidth;
        const height = container.clientHeight;

        // 清空SVG
        svg.innerHTML = '';

        // 创建主组
        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        svg.appendChild(g);

        // 缩放和平移变量
        let transform = { x: 0, y: 0, k: 1 };
        let isDragging = false;
        let isNodeDragging = false;
        let draggedNode = null;
        let startX, startY;

        // 通用坐标转换函数
        const getEventCoords = (e) => {
            if (e.touches && e.touches.length > 0) {
                return { x: e.touches[0].clientX, y: e.touches[0].clientY };
            }
            return { x: e.clientX, y: e.clientY };
        };

        // 开始处理函数
        const handleStart = (e) => {
            const coords = getEventCoords(e);
            const target = document.elementFromPoint(coords.x, coords.y);

            if (target && target.tagName === 'circle') {
                isNodeDragging = true;
                const nodeId = target.getAttribute('data-id');
                draggedNode = this.nodes.find(n => n.id === nodeId);
            } else if (!target || target.tagName !== 'circle') {
                isDragging = true;
                startX = coords.x - transform.x;
                startY = coords.y - transform.y;
            }
        };

        // 移动处理函数
        const handleMove = (e) => {
            const coords = getEventCoords(e);

            if (isNodeDragging && draggedNode) {
                // 将屏幕坐标转换为SVG坐标
                const rect = svg.getBoundingClientRect();
                const svgX = (coords.x - rect.left - transform.x) / transform.k;
                const svgY = (coords.y - rect.top - transform.y) / transform.k;

                draggedNode.x = svgX;
                draggedNode.y = svgY;
                this.updateGraphPositions();
            } else if (isDragging) {
                transform.x = coords.x - startX;
                transform.y = coords.y - startY;
                g.setAttribute('transform', `translate(${transform.x}, ${transform.y}) scale(${transform.k})`);
            }
        };

        // 结束处理函数
        const handleEnd = () => {
            isDragging = false;
            isNodeDragging = false;
            draggedNode = null;
        };

        // 鼠标事件
        svg.addEventListener('mousedown', handleStart);
        svg.addEventListener('mousemove', handleMove);
        svg.addEventListener('mouseup', handleEnd);
        svg.addEventListener('mouseleave', handleEnd);

        // 触摸事件（移动端支持）
        svg.addEventListener('touchstart', (e) => {
            // 只在SVG元素上处理，防止默认滚动
            if (e.target.closest('#knowledgeGraphSvg')) {
                handleStart(e);
            }
        }, { passive: false });

        svg.addEventListener('touchmove', (e) => {
            if (e.target.closest('#knowledgeGraphSvg')) {
                e.preventDefault(); // 防止滚动
                handleMove(e);
            }
        }, { passive: false });

        svg.addEventListener('touchend', handleEnd);
        svg.addEventListener('touchcancel', handleEnd);

        // 缩放事件（滚轮）
        svg.addEventListener('wheel', (e) => {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            transform.k *= delta;
            transform.k = Math.max(0.3, Math.min(3, transform.k));
            g.setAttribute('transform', `translate(${transform.x}, ${transform.y}) scale(${transform.k})`);
        }, { passive: false });

        const graph = this.graphData.concept_graph;

        // 使用力导向布局初始化节点位置
        const nodes = this.applyForceDirectedLayout(graph.nodes, graph.edges, width, height);

        // 存储边和节点的引用
        this.graphEdges = [];
        this.edgeElements = [];
        this.edgeLabels = [];

        // 创建边的组和动画元素
        const edgesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        edgesGroup.setAttribute('class', 'edges-group');
        g.appendChild(edgesGroup);

        // 绘制边（带动画）
        graph.edges.forEach((edge, index) => {
            const source = nodes.find(n => n.id === edge.source);
            const target = nodes.find(n => n.id === edge.target);

            if (source && target) {
                // 创建边的容器
                const edgeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                edgeGroup.setAttribute('class', 'edge-group');
                edgeGroup.setAttribute('data-source', edge.source);
                edgeGroup.setAttribute('data-target', edge.target);

                // 主连线
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', source.x);
                line.setAttribute('y1', source.y);
                line.setAttribute('x2', target.x);
                line.setAttribute('y2', target.y);
                line.setAttribute('stroke', this.getEdgeColor(edge.weight));
                line.setAttribute('stroke-width', Math.min(edge.weight, 3));
                line.setAttribute('opacity', '0.6');
                line.setAttribute('class', 'edge-line');
                line.style.transition = 'all 0.3s ease';

                // 动画粒子（沿边移动）
                const particle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                particle.setAttribute('r', '3');
                particle.setAttribute('fill', this.getEdgeColor(edge.weight));
                particle.setAttribute('class', 'edge-particle');
                particle.style.opacity = '0';

                edgeGroup.appendChild(line);
                edgeGroup.appendChild(particle);
                edgesGroup.appendChild(edgeGroup);

                // 添加边标签
                if (edge.label) {
                    const labelGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                    labelGroup.setAttribute('class', 'edge-label');

                    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                    text.setAttribute('text-anchor', 'middle');
                    text.setAttribute('font-size', '10');
                    text.setAttribute('fill', '#666');
                    text.textContent = edge.label;

                    const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                    bg.setAttribute('fill', 'white');
                    bg.setAttribute('opacity', '0.8');
                    bg.setAttribute('rx', '3');

                    labelGroup.appendChild(bg);
                    labelGroup.appendChild(text);
                    edgesGroup.appendChild(labelGroup);

                    this.edgeLabels.push({
                        element: labelGroup,
                        text: text,
                        bg: bg,
                        source: source,
                        target: target
                    });
                }

                this.graphEdges.push({ source, target, weight: edge.weight, label: edge.label });
                this.edgeElements.push({ line, particle, source, target });
            }
        });

        // 创建节点的组
        const nodesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        nodesGroup.setAttribute('class', 'nodes-group');
        g.appendChild(nodesGroup);

        // 绘制节点
        nodes.forEach(node => {
            const nodeGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            nodeGroup.setAttribute('class', 'node-group');
            nodeGroup.setAttribute('data-id', node.id);
            nodeGroup.style.cursor = 'pointer';

            // 节点光晕效果
            const glow = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            glow.setAttribute('cx', node.x);
            glow.setAttribute('cy', node.y);
            glow.setAttribute('r', node.size + 5);
            glow.setAttribute('fill', this.getNodeColor(node.level));
            glow.setAttribute('opacity', '0');
            glow.setAttribute('class', 'node-glow');
            glow.style.transition = 'opacity 0.3s ease';

            // 主节点圆
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', node.x);
            circle.setAttribute('cy', node.y);
            circle.setAttribute('r', node.size);
            circle.setAttribute('fill', this.getNodeColor(node.level));
            circle.setAttribute('opacity', '0.85');
            circle.setAttribute('stroke', '#fff');
            circle.setAttribute('stroke-width', '2');
            circle.setAttribute('class', 'node-circle');
            circle.style.transition = 'all 0.3s ease';
            circle.style.filter = 'drop-shadow(2px 2px 3px rgba(0,0,0,0.3))';

            // 节点标签
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', node.x);
            text.setAttribute('y', node.y + 4);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('font-size', '12');
            text.setAttribute('fill', '#fff');
            text.setAttribute('font-weight', 'bold');
            text.setAttribute('pointer-events', 'none');
            text.setAttribute('class', 'node-text');
            text.textContent = node.label;

            nodeGroup.appendChild(glow);
            nodeGroup.appendChild(circle);
            nodeGroup.appendChild(text);
            nodesGroup.appendChild(nodeGroup);

            // 节点交互
            nodeGroup.addEventListener('click', (e) => {
                e.stopPropagation();
                this.highlightNodeAndConnections(node);
            });

            nodeGroup.addEventListener('mouseenter', function() {
                circle.setAttribute('opacity', '1');
                circle.setAttribute('stroke-width', '3');
                glow.setAttribute('opacity', '0.3');
            });

            nodeGroup.addEventListener('mouseleave', function() {
                circle.setAttribute('opacity', '0.85');
                circle.setAttribute('stroke-width', '2');
                glow.setAttribute('opacity', '0');
            });
        });

        this.nodes = nodes;
        this.transform = transform;
        this.g = g;
        this.nodesGroup = nodesGroup;
        this.edgesGroup = edgesGroup;

        // 启动边动画
        this.startEdgeAnimation();

        // 初始将视图居中
        setTimeout(() => this.centerView(), 100);
    },

    // 力导向布局算法
    applyForceDirectedLayout(nodes, edges, width, height) {
        const centerX = width / 2;
        const centerY = height / 2;

        // 初始化节点位置（按层级环形分布）
        const levelGroups = {};
        nodes.forEach(n => {
            if (!levelGroups[n.level]) levelGroups[n.level] = [];
            levelGroups[n.level].push(n);
        });

        const levelAngles = {};
        Object.keys(levelGroups).forEach(level => {
            const levelNodes = levelGroups[level];
            const angleStep = (2 * Math.PI) / levelNodes.length;
            const radius = 50 + (4 - level) * 60; // 中心概念在中间

            levelNodes.forEach((node, i) => {
                const angle = angleStep * i - Math.PI / 2;
                node.x = centerX + radius * Math.cos(angle);
                node.y = centerY + radius * Math.sin(angle);
                node.vx = 0;
                node.vy = 0;
            });
        });

        // 力导向模拟迭代
        const iterations = 100;
        const k = 100; // 理想边长度
        const repulsion = 5000; // 斥力常数

        for (let iter = 0; iter < iterations; iter++) {
            const cooling = 1 - iter / iterations;

            // 计算斥力（所有节点之间）
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const dx = nodes[j].x - nodes[i].x;
                    const dy = nodes[j].y - nodes[i].y;
                    const dist = Math.sqrt(dx * dx + dy * dy) || 1;
                    const force = repulsion / (dist * dist);

                    const fx = (dx / dist) * force * cooling;
                    const fy = (dy / dist) * force * cooling;

                    nodes[i].vx -= fx;
                    nodes[i].vy -= fy;
                    nodes[j].vx += fx;
                    nodes[j].vy += fy;
                }
            }

            // 计算引力（连接的节点之间）
            edges.forEach(edge => {
                const source = nodes.find(n => n.id === edge.source);
                const target = nodes.find(n => n.id === edge.target);

                if (source && target) {
                    const dx = target.x - source.x;
                    const dy = target.y - source.y;
                    const dist = Math.sqrt(dx * dx + dy * dy) || 1;

                    const force = (dist - k) * 0.05 * cooling;
                    const fx = (dx / dist) * force;
                    const fy = (dy / dist) * force;

                    source.vx += fx;
                    source.vy += fy;
                    target.vx -= fx;
                    target.vy -= fy;
                }
            });

            // 中心引力（将节点拉向中心）
            nodes.forEach(node => {
                const dx = centerX - node.x;
                const dy = centerY - node.y;
                node.vx += dx * 0.01 * cooling;
                node.vy += dy * 0.01 * cooling;
            });

            // 更新位置
            nodes.forEach(node => {
                const maxSpeed = 10 * cooling;
                const speed = Math.sqrt(node.vx * node.vx + node.vy * node.vy);
                if (speed > maxSpeed) {
                    node.vx = (node.vx / speed) * maxSpeed;
                    node.vy = (node.vy / speed) * maxSpeed;
                }

                node.x += node.vx;
                node.y += node.vy;

                // 边界约束
                const padding = node.size + 20;
                node.x = Math.max(padding, Math.min(width - padding, node.x));
                node.y = Math.max(padding, Math.min(height - padding, node.y));

                node.vx *= 0.8; // 阻尼
                node.vy *= 0.8;
            });
        }

        return nodes;
    },

    // 更新图形位置（用于拖拽后）
    updateGraphPositions() {
        const nodeCircles = this.nodesGroup.querySelectorAll('.node-circle');
        const nodeTexts = this.nodesGroup.querySelectorAll('.node-text');
        const nodeGlows = this.nodesGroup.querySelectorAll('.node-glow');

        this.nodes.forEach((node, i) => {
            const circle = nodeCircles[i];
            const text = nodeTexts[i];
            const glow = nodeGlows[i];

            if (circle) {
                circle.setAttribute('cx', node.x);
                circle.setAttribute('cy', node.y);
            }
            if (text) {
                text.setAttribute('x', node.x);
                text.setAttribute('y', node.y + 4);
            }
            if (glow) {
                glow.setAttribute('cx', node.x);
                glow.setAttribute('cy', node.y);
            }
        });

        // 更新边位置
        this.edgeElements.forEach(edge => {
            edge.line.setAttribute('x1', edge.source.x);
            edge.line.setAttribute('y1', edge.source.y);
            edge.line.setAttribute('x2', edge.target.x);
            edge.line.setAttribute('y2', edge.target.y);
        });

        // 更新边标签位置
        this.edgeLabels.forEach(label => {
            const midX = (label.source.x + label.target.x) / 2;
            const midY = (label.source.y + label.target.y) / 2;

            label.text.setAttribute('x', midX);
            label.text.setAttribute('y', midY);

            const bboxWidth = label.text.getComputedTextLength() + 10;
            const bboxHeight = 14;
            label.bg.setAttribute('x', midX - bboxWidth / 2);
            label.bg.setAttribute('y', midY - bboxHeight / 2);
            label.bg.setAttribute('width', bboxWidth);
            label.bg.setAttribute('height', bboxHeight);
        });
    },

    // 高亮节点和连接
    highlightNodeAndConnections(selectedNode) {
        this.showNodeInfo(selectedNode);

        // 淡化所有元素
        this.nodesGroup.querySelectorAll('.node-circle').forEach(circle => {
            circle.style.opacity = '0.3';
        });
        this.nodesGroup.querySelectorAll('.node-text').forEach(text => {
            text.style.opacity = '0.3';
        });
        this.edgeElements.forEach(edge => {
            edge.line.style.opacity = '0.1';
            edge.particle.style.opacity = '0';
        });

        // 高亮选中的节点
        const selectedGroup = this.nodesGroup.querySelector(`[data-id="${selectedNode.id}"]`);
        if (selectedGroup) {
            selectedGroup.querySelector('.node-circle').style.opacity = '1';
            selectedGroup.querySelector('.node-text').style.opacity = '1';
            selectedGroup.querySelector('.node-glow').setAttribute('opacity', '0.5');
        }

        // 高亮相关节点和边
        this.edgeElements.forEach(edge => {
            if (edge.source.id === selectedNode.id || edge.target.id === selectedNode.id) {
                edge.line.style.opacity = '1';
                edge.line.style.strokeWidth = '4';

                // 高亮相关节点
                const relatedNodeId = edge.source.id === selectedNode.id ? edge.target.id : edge.source.id;
                const relatedGroup = this.nodesGroup.querySelector(`[data-id="${relatedNodeId}"]`);
                if (relatedGroup) {
                    relatedGroup.querySelector('.node-circle').style.opacity = '1';
                    relatedGroup.querySelector('.node-text').style.opacity = '1';
                }
            }
        });

        // 添加重置按钮到节点信息面板
        const infoPanel = document.getElementById('nodeInfoContent');
        const resetBtn = document.getElementById('resetHighlightBtn');
        if (!resetBtn) {
            infoPanel.innerHTML += `
                <button class="btn btn-sm btn-outline-warning mt-2" id="resetHighlightBtn">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                                                        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                                                        <path d="M3 3v5h5"></path>
                                                    </svg>
                                                    重置高亮
                </button>
            `;
            document.getElementById('resetHighlightBtn').addEventListener('click', () => {
                this.resetHighlight();
            });
        }
    },

    // 重置高亮
    resetHighlight() {
        this.nodesGroup.querySelectorAll('.node-circle').forEach(circle => {
            circle.style.opacity = '0.85';
        });
        this.nodesGroup.querySelectorAll('.node-text').forEach(text => {
            text.style.opacity = '1';
        });
        this.nodesGroup.querySelectorAll('.node-glow').forEach(glow => {
            glow.setAttribute('opacity', '0');
        });
        this.edgeElements.forEach(edge => {
            edge.line.style.opacity = '0.6';
            edge.line.style.strokeWidth = Math.min(edge.weight, 3);
        });

        document.getElementById('nodeInfoPanel').style.display = 'none';
    },

    // 边动画（粒子沿边移动）
    startEdgeAnimation() {
        let progress = 0;
        const animate = () => {
            progress += 0.005;
            if (progress > 1) progress = 0;

            this.edgeElements.forEach((edge, index) => {
                const offset = (progress + index * 0.2) % 1;
                const x = edge.source.x + (edge.target.x - edge.source.x) * offset;
                const y = edge.source.y + (edge.target.y - edge.source.y) * offset;

                edge.particle.setAttribute('cx', x);
                edge.particle.setAttribute('cy', y);

                // 淡入淡出效果
                const opacity = Math.sin(offset * Math.PI) * 0.8;
                edge.particle.style.opacity = opacity;
            });

            this.animationFrame = requestAnimationFrame(animate);
        };
        animate();
    },

    // 居中视图
    centerView() {
        if (!this.nodes || !this.nodes.length) return;

        const container = document.getElementById('graphContainer');
        const width = container.clientWidth;
        const height = container.clientHeight;

        // 计算节点中心
        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
        this.nodes.forEach(node => {
            minX = Math.min(minX, node.x - node.size);
            maxX = Math.max(maxX, node.x + node.size);
            minY = Math.min(minY, node.y - node.size);
            maxY = Math.max(maxY, node.y + node.size);
        });

        const graphCenterX = (minX + maxX) / 2;
        const graphCenterY = (minY + maxY) / 2;

        // 调整变换使图形居中
        this.transform.x = (width - (minX + maxX)) / 2;
        this.transform.y = (height - (minY + maxY)) / 2;
        this.transform.k = 1;

        this.g.setAttribute('transform', `translate(${this.transform.x}, ${this.transform.y}) scale(1)`);
    },

    getNodeColor(level) {
        const colors = {
            1: '#8b6914',  // 一级概念 - 金色
            2: '#c9a67a',  // 二级概念 - 铜色
            3: '#6b8e23',  // 三级概念 - 橄榄绿
            4: '#4682b4'   // 其他 - 钢蓝
        };
        return colors[level] || '#888';
    },

    getEdgeColor(weight) {
        if (weight >= 4) return '#8b6914';
        if (weight >= 3) return '#c9a67a';
        return '#ccc';
    },

    showNodeInfo(node) {
        const panel = document.getElementById('nodeInfoPanel');
        const title = document.getElementById('nodeInfoTitle');
        const content = document.getElementById('nodeInfoContent');

        panel.style.display = 'block';
        panel.classList.add('fade-in');
        setTimeout(() => panel.classList.remove('fade-in'), 300);

        title.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 16v-4M12 8h.01"></path>
            </svg>
            ${node.label}
        `;

        const levelNames = { 1: '一级核心概念', 2: '二级核心概念', 3: '衍生概念', 4: '具体概念' };
        const levelBadges = {
            1: 'bg-danger',
            2: 'bg-warning',
            3: 'bg-info',
            4: 'bg-secondary'
        };

        content.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <p class="mb-1">
                        <span class="badge ${levelBadges[node.level] || 'bg-secondary'}">${levelNames[node.level] || '未知'}</span>
                    </p>
                    <p class="mb-1"><strong class="text-warning">出现次数：</strong>${node.chapters.length} 章</p>
                </div>
                <div class="col-md-6">
                    <p class="mb-1"><strong>相关概念：</strong></p>
                    <p class="mb-0 text-muted small">${this.getRelatedConcepts(node.id)}</p>
                </div>
            </div>
            <div class="mt-2">
                <p class="mb-1"><strong class="text-warning">相关章节：</strong></p>
                <div class="d-flex flex-wrap gap-1">
                    ${node.chapters.slice(0, 15).map(ch =>
                        `<a href="/daodejing/chapter/${ch}" class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;">第${ch}章</a>`
                    ).join('')}
                    ${node.chapters.length > 15 ? `<span class="text-muted">+${node.chapters.length - 15} 更多</span>` : ''}
                </div>
            </div>
        `;
    },

    getRelatedConcepts(nodeId) {
        if (!this.graphData || !this.graphData.concept_graph) return '-';

        const edges = this.graphData.concept_graph.edges;
        const related = edges
            .filter(e => e.source === nodeId || e.target === nodeId)
            .map(e => e.source === nodeId ? e.target : e.source);

        return related.length > 0 ? related.join('、') : '-';
    },

    showConceptList() {
        document.getElementById('graphContainer').style.display = 'none';
        document.getElementById('conceptListContainer').style.display = 'block';

        const tbody = document.getElementById('conceptTableBody');
        const graph = this.graphData.concept_graph;

        const levelNames = { 1: '一级核心', 2: '二级核心', 3: '衍生', 4: '具体' };

        tbody.innerHTML = graph.nodes
            .sort((a, b) => b.chapters.length - a.chapters.length)
            .map(node => `
                <tr>
                    <td><span class="badge" style="background: ${this.getNodeColor(node.level)}">${node.label}</span></td>
                    <td>${levelNames[node.level]}</td>
                    <td>${node.chapters.length}</td>
                    <td><small>${node.chapters.slice(0, 5).join(', ')}${node.chapters.length > 5 ? '...' : ''}</small></td>
                </tr>
            `).join('');
    },

    resetZoom() {
        if (this.transform && this.g) {
            this.transform = { x: 0, y: 0, k: 1 };
            this.g.setAttribute('transform', 'translate(0, 0) scale(1)');
            this.showToast('视图已重置', 'info');
        }
    },

    animateNodes() {
        if (!this.nodes || !this.nodesGroup) return;

        // 添加脉动动画效果
        const nodeGroups = this.nodesGroup.querySelectorAll('.node-group');
        nodeGroups.forEach((group, index) => {
            setTimeout(() => {
                const circle = group.querySelector('.node-circle');
                const glow = group.querySelector('.node-glow');

                circle.style.transition = 'all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
                glow.style.transition = 'all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)';

                const currentR = parseFloat(circle.getAttribute('r'));
                circle.setAttribute('r', currentR * 1.6);
                circle.setAttribute('opacity', '1');
                glow.setAttribute('r', currentR + 15);
                glow.setAttribute('opacity', '0.6');

                setTimeout(() => {
                    circle.setAttribute('r', currentR);
                    circle.setAttribute('opacity', '0.85');
                    glow.setAttribute('r', currentR + 5);
                    glow.setAttribute('opacity', '0');
                }, 400);
            }, index * 60);
        });

        this.showToast('动画效果已触发', 'success');
    },

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 1100;';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="me-1">
                        <circle cx="12" cy="12" r="10"></circle>
                    </svg>
                    ${message}
                </div>
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
    module.exports = KnowledgeGraphManager;
}

// 自动初始化 - 使用事件委托
if (typeof window !== 'undefined') {
    window.KnowledgeGraphManager = KnowledgeGraphManager;

    // 使用事件委托，确保即使按钮是动态创建的也能工作
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('#knowledgeGraphBtn');
        if (btn) {
            e.preventDefault();
            e.stopPropagation();
            console.log('[KnowledgeGraph] 按钮被点击');
            KnowledgeGraphManager.showKnowledgeGraph().catch(err => {
                console.error('[KnowledgeGraph] 错误:', err);
            });
        }
    });
}
