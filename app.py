# -*- coding: utf-8 -*-
"""
道德经多版本对照平台 - Flask 主应用
模块化架构版本
"""

from flask import Flask
from config import get_config
from routes import register_blueprints
from services.data_service import DataService
from utils.security import init_security


def create_app(config_name=None):
    """
    应用工厂函数

    Args:
        config_name: 配置名称 ('development' 或 'production')

    Returns:
        Flask 应用实例
    """
    app = Flask(__name__)

    # 加载配置
    config = get_config(config_name)
    app.config.from_object(config)

    # 初始化安全配置
    init_security(app)

    # 注册蓝图
    register_blueprints(app)

    # 注册错误处理器
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """注册错误处理器"""
    from flask import request, render_template, jsonify

    @app.errorhandler(404)
    def not_found(error):
        from services.data_service import DataService
        return render_template('ddj/index.html', data=DataService.load_data()), 404

    @app.errorhandler(429)
    def rate_limited(error):
        """请求过于频繁"""
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Too many requests'}), 429
        return render_template('ddj/index.html', data=DataService.load_data()), 429

    @app.errorhandler(500)
    def server_error(error):
        from services.data_service import DataService
        return render_template('ddj/index.html', data=DataService.load_data()), 500


# 创建应用实例
app = create_app()

# Vercel 部署入口
vercel_app = app

# 本地开发入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
