# -*- coding: utf-8 -*-
"""
用户服务测试
"""

import sys
from pathlib import Path

import pytest

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.user_service import UserService, get_user_service  # noqa: E402


@pytest.fixture
def user_service():
    """创建用户服务实例"""
    return UserService()


@pytest.fixture
def registered_user(user_service):
    """创建一个已注册用户"""
    result = user_service.register_user(
        username="testuser", email="test@example.com", password="securepassword123"
    )
    return {
        "service": user_service,
        "user_id": result["user_id"],
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepassword123",
    }


class TestUserServiceRegistration:
    """用户注册测试"""

    def test_register_user_success(self, user_service):
        """测试成功注册"""
        result = user_service.register_user(
            username="newuser", email="new@example.com", password="password123"
        )
        assert result["success"] is True
        assert "user_id" in result
        assert result["message"] == "注册成功"

    def test_register_user_duplicate_username(self, user_service):
        """测试重复用户名注册失败"""
        # 第一次注册
        result1 = user_service.register_user(
            username="duplicate", email="unique1@example.com", password="password123"
        )
        assert result1["success"] is True

        # 第二次注册相同用户名
        result2 = user_service.register_user(
            username="duplicate", email="unique2@example.com", password="password456"
        )
        assert result2["success"] is False
        assert "已存在" in result2["error"]

    def test_register_user_duplicate_email(self, user_service):
        """测试重复邮箱注册失败"""
        # 第一次注册
        result1 = user_service.register_user(
            username="unique1", email="duplicate@example.com", password="password123"
        )
        assert result1["success"] is True

        # 第二次注册相同邮箱
        result2 = user_service.register_user(
            username="unique2", email="duplicate@example.com", password="password456"
        )
        assert result2["success"] is False
        assert "已存在" in result2["error"]

    def test_register_user_empty_username(self, user_service):
        """测试空用户名注册"""
        result = user_service.register_user(
            username="", email="test@example.com", password="password123"
        )
        # 空用户名应该允许注册（但实际使用可能不允许）
        assert result["success"] is True

    def test_register_user_empty_email(self, user_service):
        """测试空邮箱注册"""
        result = user_service.register_user(
            username="testuser", email="", password="password123"
        )
        assert result["success"] is True

    def test_register_user_empty_password(self, user_service):
        """测试空密码注册"""
        result = user_service.register_user(
            username="testuser", email="test@example.com", password=""
        )
        assert result["success"] is True

    def test_register_user_special_characters(self, user_service):
        """测试特殊字符用户名注册"""
        result = user_service.register_user(
            username="test@user#123", email="test@example.com", password="p@$$w0rd!23"
        )
        assert result["success"] is True

    def test_register_user_unicode_username(self, user_service):
        """测试 Unicode 用户名注册"""
        result = user_service.register_user(
            username="测试用户", email="test@example.com", password="password123"
        )
        assert result["success"] is True


class TestUserServiceLogin:
    """用户登录测试"""

    def test_login_success(self, registered_user):
        """测试成功登录"""
        service = registered_user["service"]
        result = service.login_user(
            username_or_email=registered_user["username"],
            password=registered_user["password"],
        )
        assert result["success"] is True
        assert "token" in result
        assert result["username"] == registered_user["username"]
        assert result["message"] == "登录成功"

    def test_login_with_email(self, registered_user):
        """测试使用邮箱登录"""
        service = registered_user["service"]
        result = service.login_user(
            username_or_email=registered_user["email"],
            password=registered_user["password"],
        )
        assert result["success"] is True
        assert "token" in result

    def test_login_wrong_password(self, registered_user):
        """测试错误密码登录失败"""
        service = registered_user["service"]
        result = service.login_user(
            username_or_email=registered_user["username"], password="wrongpassword"
        )
        assert result["success"] is False
        assert "错误" in result["error"]

    def test_login_nonexistent_user(self, user_service):
        """测试不存在的用户登录失败"""
        result = user_service.login_user(
            username_or_email="nonexistent", password="password123"
        )
        assert result["success"] is False
        assert "错误" in result["error"]

    def test_login_empty_username(self, user_service):
        """测试空用户名登录"""
        result = user_service.login_user(username_or_email="", password="password123")
        assert result["success"] is False

    def test_login_empty_password(self, registered_user):
        """测试空密码登录"""
        service = registered_user["service"]
        result = service.login_user(
            username_or_email=registered_user["username"], password=""
        )
        assert result["success"] is False


class TestUserServiceGetUser:
    """获取用户信息测试"""

    def test_get_user_by_id_success(self, registered_user):
        """测试成功获取用户信息"""
        service = registered_user["service"]
        user = service.get_user_by_id(registered_user["user_id"])
        assert user is not None
        assert user["id"] == registered_user["user_id"]
        assert user["username"] == registered_user["username"]
        assert user["email"] == registered_user["email"]
        # 确保不包含密码
        assert "password_hash" not in user

    def test_get_user_by_id_nonexistent(self, user_service):
        """测试获取不存在的用户"""
        user = user_service.get_user_by_id("nonexistent_id")
        assert user is None

    def test_get_user_by_id_empty_id(self, user_service):
        """测试获取空 ID 用户"""
        user = user_service.get_user_by_id("")
        assert user is None


class TestUserServiceToken:
    """Token 验证测试"""

    def test_verify_valid_token(self, registered_user):
        """测试验证有效 Token"""
        service = registered_user["service"]
        # 先登录获取 Token
        login_result = service.login_user(
            username_or_email=registered_user["username"],
            password=registered_user["password"],
        )
        token = login_result["token"]

        # 使用 Flask 应用上下文验证 Token
        from flask import Flask

        from config import DevelopmentConfig

        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)

        with app.app_context():
            user = service.verify_token(token)
            assert user is not None
            assert user["id"] == registered_user["user_id"]
            assert user["username"] == registered_user["username"]

    def test_verify_invalid_token(self, user_service):
        """测试验证无效 Token"""
        from flask import Flask

        from config import DevelopmentConfig

        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)

        with app.app_context():
            user = user_service.verify_token("invalid_token")
            assert user is None

    def test_verify_empty_token(self, user_service):
        """测试验证空 Token"""
        from flask import Flask

        from config import DevelopmentConfig

        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)

        with app.app_context():
            user = user_service.verify_token("")
            assert user is None

    def test_verify_expired_token(self, registered_user):
        """测试验证过期 Token"""
        service = registered_user["service"]

        # 模拟过期 Token（通过修改时间）
        import time

        import jwt
        from flask import Flask

        from config import DevelopmentConfig

        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)

        with app.app_context():
            # 创建一个过期的 payload
            secret = app.config.get("SECRET_KEY", "dev-secret-key")
            expired_payload = {
                "user_id": registered_user["user_id"],
                "exp": int(time.time()) - 3600,  # 1 小时前过期
            }
            expired_token = jwt.encode(expired_payload, secret, algorithm="HS256")

            user = service.verify_token(expired_token)
            assert user is None


class TestUserServicePassword:
    """密码处理测试"""

    def test_hash_password_different_results(self, user_service):
        """测试密码哈希每次结果不同（加盐）"""
        password = "samepassword"
        hash1 = user_service._hash_password(password)
        hash2 = user_service._hash_password(password)
        assert hash1 != hash2  # 加盐后应该不同

    def test_hash_password_same_password_verifies(self, user_service):
        """测试相同密码可以验证通过"""
        password = "testpassword123"
        password_hash = user_service._hash_password(password)
        assert user_service._verify_password(password, password_hash) is True

    def test_hash_password_wrong_password_fails(self, user_service):
        """测试错误密码验证失败"""
        password = "correctpassword"
        wrong_password = "wrongpassword"
        password_hash = user_service._hash_password(password)
        assert user_service._verify_password(wrong_password, password_hash) is False

    def test_hash_password_empty_password(self, user_service):
        """测试空密码哈希"""
        password = ""
        password_hash = user_service._hash_password(password)
        assert user_service._verify_password(password, password_hash) is True

    def test_hash_password_unicode_password(self, user_service):
        """测试 Unicode 密码"""
        password = "密码测试 123"
        password_hash = user_service._hash_password(password)
        assert user_service._verify_password(password, password_hash) is True

    def test_hash_password_special_characters(self, user_service):
        """测试特殊字符密码"""
        password = "p@$$w0rd!@#$%^&*()"
        password_hash = user_service._hash_password(password)
        assert user_service._verify_password(password, password_hash) is True


class TestUserServiceTimestamp:
    """时间戳测试"""

    def test_get_timestamp_returns_integer(self, user_service):
        """测试获取时间戳返回整数"""
        timestamp = user_service._get_timestamp()
        assert isinstance(timestamp, int)

    def test_get_timestamp_increases(self, user_service):
        """测试时间戳递增"""
        ts1 = user_service._get_timestamp()
        import time

        time.sleep(0.01)  # 短暂等待
        ts2 = user_service._get_timestamp()
        assert ts2 >= ts1


class TestUserServiceGlobal:
    """全局服务测试"""

    def test_get_user_service_returns_instance(self):
        """测试获取全局服务返回实例"""
        service = get_user_service()
        assert isinstance(service, UserService)

    def test_get_user_service_returns_same_instance(self):
        """测试获取全局服务返回相同实例"""
        service1 = get_user_service()
        service2 = get_user_service()
        assert service1 is service2


class TestUserServiceEdgeCases:
    """边界情况测试"""

    def test_register_user_very_long_username(self, user_service):
        """测试注册超长用户名"""
        long_username = "a" * 1000
        result = user_service.register_user(
            username=long_username, email="test@example.com", password="password123"
        )
        assert result["success"] is True

    def test_register_user_very_long_email(self, user_service):
        """测试注册超长邮箱"""
        long_email = "a" * 1000 + "@example.com"
        result = user_service.register_user(
            username="testuser", email=long_email, password="password123"
        )
        assert result["success"] is True

    def test_register_user_very_long_password(self, user_service):
        """测试注册超长密码"""
        long_password = "p" * 1000
        result = user_service.register_user(
            username="testuser", email="test@example.com", password=long_password
        )
        assert result["success"] is True

    def test_login_case_insensitive_username(self, registered_user):
        """测试用户名大小写不敏感（可选功能）"""
        service = registered_user["service"]
        # 注意：当前实现是大小写敏感的，这是边界测试
        result = service.login_user(
            username_or_email=registered_user["username"].upper(),
            password=registered_user["password"],
        )
        # 当前实现应该失败（大小写敏感）
        assert result["success"] is False

    def test_multiple_users_registration(self, user_service):
        """测试多用户注册"""
        users = [
            ("user1", "user1@example.com", "pass1"),
            ("user2", "user2@example.com", "pass2"),
            ("user3", "user3@example.com", "pass3"),
        ]

        for username, email, password in users:
            result = user_service.register_user(username, email, password)
            assert result["success"] is True

        # 验证所有用户都存在
        assert len(user_service._users) == 3
