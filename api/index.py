# -*- coding: utf-8 -*-
"""
道德经 - Vercel Python 部署入口
使用模块化架构
"""

import sys
import os
from pathlib import Path

# 设置项目根目录路径
project_root = Path('/var/task')
if not project_root.exists():
    project_root = Path(__file__).parent.parent

sys.path.insert(0, str(project_root))
os.chdir(project_root)

# 导入Flask应用工厂
from app import create_app

# 创建应用实例
app = create_app('production')

# Vercel 入口点
vercel_app = app

# 本地测试入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
