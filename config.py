# -*- coding: utf-8 -*-
"""
应用配置
"""

import os
from pathlib import Path
from typing import Optional, Type

from flask import Flask

# 基础路径
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "daodejing.json"
CLASSICS_FILE = DATA_DIR / "classics.json"


# Flask 配置
class Config:
    """基础配置"""

    SECRET_KEY = os.environ.get("SECRET_KEY")
    JSON_AS_ASCII = False

    @classmethod
    def init_app(cls, _app: Flask) -> None:  # noqa: U101
        """初始化应用（配置检查点）"""
        pass


class DevelopmentConfig(Config):
    """开发环境配置"""

    DEBUG = True
    TESTING = False

    @classmethod
    def init_app(cls, app: Flask) -> None:
        """开发环境初始化"""
        # 开发环境使用默认密钥（如果环境变量没有设置）
        if not app.config.get("SECRET_KEY"):
            # 首先检查环境变量
            env_key = os.environ.get("SECRET_KEY")
            if env_key:
                app.config["SECRET_KEY"] = env_key
            else:
                app.config["SECRET_KEY"] = "dev-secret-key-change-in-production"


class ProductionConfig(Config):
    """生产环境配置"""

    DEBUG = False
    TESTING = False

    @classmethod
    def init_app(cls, app: Flask) -> None:
        """生产环境初始化 - 强制要求SECRET_KEY"""
        if not app.config.get("SECRET_KEY"):
            raise ValueError(
                "生产环境必须设置SECRET_KEY环境变量。"
                "请设置环境变量: export SECRET_KEY='your-secret-key'"
            )


# 根据环境变量选择配置
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(env_name: Optional[str] = None) -> Type[Config]:
    """获取配置对象"""
    if env_name is None:
        env_name = os.environ.get("FLASK_ENV", "development")
    return config.get(env_name, DevelopmentConfig)
