# -*- coding: utf-8 -*-
"""
路由模块初始化
"""

from flask import Blueprint
from routes.page_routes import bp as page_bp
from routes.api_routes import bp as api_bp

# 蓝图列表
blueprints = [page_bp, api_bp]


def register_blueprints(app):
    """注册所有蓝图到 Flask 应用"""
    for bp in blueprints:
        app.register_blueprint(bp)
