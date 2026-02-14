# -*- coding: utf-8 -*-
"""
安全相关测试
"""

import os
from unittest.mock import patch

import pytest

from config import DevelopmentConfig, ProductionConfig, get_config


class TestConfigSecurity:
    """配置安全测试"""

    def test_production_config_requires_secret_key(self):
        """测试生产环境配置需要设置SECRET_KEY环境变量"""
        # 清除环境变量
        with patch.dict(os.environ, {}, clear=True):
            config_class = get_config("production")
            config = config_class()

            # 创建测试应用来触发init_app
            from flask import Flask

            app = Flask(__name__)
            app.config.from_object(config)

            # 应该抛出ValueError
            with pytest.raises(ValueError, match="生产环境必须设置SECRET_KEY环境变量"):
                config.init_app(app)

    def test_development_app_has_default_key(self):
        """测试开发环境应用有默认密钥"""
        # 清除环境变量
        with patch.dict(os.environ, {}, clear=True):
            # 创建开发环境应用
            from app import create_app

            app = create_app("development")

            # 应用应该设置了SECRET_KEY
            assert app.config["SECRET_KEY"] == "dev-secret-key-change-in-production"

        # 测试当设置环境变量时使用环境变量
        with patch.dict(os.environ, {"SECRET_KEY": "custom-dev-key"}):
            app = create_app("development")
            assert app.config["SECRET_KEY"] == "custom-dev-key"

    def test_config_selection_by_env(self):
        """测试根据环境变量选择配置"""
        # 默认开发环境
        config_class = get_config()
        assert config_class == DevelopmentConfig

        # 明确指定生产环境
        config_class = get_config("production")
        assert config_class == ProductionConfig


class TestSecurityHeaders:
    """安全头测试"""

    def test_get_security_headers(self):
        """测试获取安全头"""
        from utils.security import get_security_headers

        headers = get_security_headers()

        # 检查必需的安全头
        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
        ]

        for header in required_headers:
            assert header in headers, f"缺少必需的安全头: {header}"

        # 检查值是否正确
        assert headers["X-Content-Type-Options"] == "nosniff"
        assert headers["X-XSS-Protection"] == "1; mode=block"


class TestInputValidation:
    """输入验证测试"""

    def test_validate_chapter_id(self):
        """测试章节ID验证"""
        from utils.validators import validate_chapter_id

        # 有效ID
        assert validate_chapter_id(1) is True
        assert validate_chapter_id(81) is True
        assert validate_chapter_id(50) is True

        # 无效ID
        assert validate_chapter_id(0) is False
        assert validate_chapter_id(82) is False
        assert validate_chapter_id(-1) is False

        # 非整数
        assert validate_chapter_id(1.5) is False

    def test_validate_search_query(self):
        """测试搜索查询验证"""
        from utils.validators import validate_search_query

        # 有效查询
        is_valid, error = validate_search_query("道")
        assert is_valid is True
        assert error is None

        # 空查询
        is_valid, error = validate_search_query("")
        assert is_valid is False
        assert error == "查询不能为空"

        # 过长查询
        long_query = "道" * 101
        is_valid, error = validate_search_query(long_query)
        assert is_valid is False
        assert error == "查询长度不能超过100个字符"

        # 包含XSS字符
        xss_queries = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "onerror=alert(1)",
            "onload=alert(1)",
        ]

        for query in xss_queries:
            is_valid, error = validate_search_query(query)
            assert is_valid is False, f"应该检测到XSS: {query}"
            assert error == "查询包含非法字符"

    def test_sanitize_text(self):
        """测试文本清理"""
        from utils.validators import sanitize_text

        # 基本清理
        text = "  测试文本  "
        cleaned = sanitize_text(text)
        assert cleaned == "测试文本"

        # 移除控制字符
        text_with_control = "测试\x00文本\x08控制字符"
        cleaned = sanitize_text(text_with_control)
        assert cleaned == "测试文本控制字符"

        # 长度限制
        long_text = "道" * 2000
        cleaned = sanitize_text(long_text, max_length=1000)
        assert len(cleaned) <= 1000


class TestCORSConfig:
    """CORS配置测试"""

    def test_cors_config_production(self):
        """测试生产环境CORS配置"""
        from utils.security import get_cors_config

        config = get_cors_config()

        # 当前配置允许所有来源（需要修改为限制具体域名）
        assert config["origins"] == "*"

        # 检查其他配置项
        assert "GET" in config["methods"]
        assert "POST" in config["methods"]
        assert "OPTIONS" in config["methods"]
        assert "Content-Type" in config["allow_headers"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
