# -*- coding: utf-8 -*-
"""
应用配置
"""

import os
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "daodejing.json"
CLASSICS_FILE = DATA_DIR / "classics.json"

# Flask 配置
class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JSON_AS_ASCII = False


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False


# 根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env_name=None):
    """获取配置对象"""
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'development')
    return config.get(env_name, DevelopmentConfig)
