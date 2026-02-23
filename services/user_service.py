# -*- coding: utf-8 -*-
"""
用户服务 - 用户认证和会话管理
"""

import secrets
import time
from typing import Any, Dict, Optional

import bcrypt
import jwt
from flask import current_app


class UserService:
    """
    用户服务
    管理用户注册、登录、登出
    """

    def __init__(self) -> None:
        """初始化用户服务"""
        # 内存存储用户数据（生产环境应使用数据库）
        self._users: Dict[str, Dict[str, Any]] = {}

    def register_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """
        用户注册

        Args:
            username: 用户名
            email: 邮箱
            password: 密码（明文）

        Returns:
            注册结果
        """
        # 验证用户名和邮箱
        if self._user_exists(username, email):
            return {"success": False, "error": "用户名或邮箱已存在"}

        # 哈希密码
        password_hash = self._hash_password(password)

        # 创建用户
        user_id = secrets.token_hex(16)
        user = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "created_at": self._get_timestamp(),
        }

        self._users[user_id] = user

        return {"success": True, "user_id": user_id, "message": "注册成功"}

    def login_user(self, username_or_email: str, password: str) -> Dict[str, Any]:
        """
        用户登录

        Args:
            username_or_email: 用户名或邮箱
            password: 密码

        Returns:
            登录结果
        """
        # 查找用户
        user = self._find_user(username_or_email)
        if not user:
            return {"success": False, "error": "用户名或密码错误"}

        # 验证密码
        if not self._verify_password(password, user["password_hash"]):
            return {"success": False, "error": "用户名或密码错误"}

        # 生成 JWT Token
        token = self._generate_token(user)

        return {
            "success": True,
            "token": token,
            "user_id": user["id"],
            "username": user["username"],
            "message": "登录成功",
        }

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        根据用户 ID 获取用户信息

        Args:
            user_id: 用户 ID

        Returns:
            用户信息（不包含密码）
        """
        user = self._users.get(user_id)
        if not user:
            return None

        # 返回不包含密码的用户信息
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
        }

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证 JWT Token

        Args:
            token: JWT Token

        Returns:
            用户信息（如果有效）
        """
        try:
            secret = self._get_secret_key()
            payload = jwt.decode(token, secret, algorithms=["HS256"])

            user_id = payload.get("user_id")
            if user_id:
                user = self.get_user_by_id(str(user_id))
                return user
            return None

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def _user_exists(self, username: str, email: str) -> bool:
        """检查用户是否已存在"""
        return any(
            user["username"] == username or user["email"] == email
            for user in self._users.values()
        )

    def _find_user(self, username_or_email: str) -> Optional[Dict[str, Any]]:
        """查找用户"""
        for user in self._users.values():
            if (
                user["username"] == username_or_email
                or user["email"] == username_or_email
            ):
                return user
        return None

    def _hash_password(self, password: str) -> str:
        """哈希密码"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def _generate_token(self, user: Dict[str, Any]) -> str:
        """生成 JWT Token"""
        secret = self._get_secret_key()
        payload = {
            "user_id": user["id"],
            "username": user["username"],
            "exp": self._get_timestamp() + (7 * 24 * 60 * 60),  # 7 天过期
        }

        return jwt.encode(payload, secret, algorithm="HS256")

    def _get_secret_key(self) -> str:
        """获取密钥"""
        try:
            return current_app.config.get("SECRET_KEY", "dev-secret-key")
        except RuntimeError:
            # 不在应用上下文中时使用默认密钥
            return "dev-secret-key"

    def _get_timestamp(self) -> int:
        """获取当前时间戳（秒）"""
        return int(time.time())


# 全局用户服务实例
_user_service: Optional[UserService] = None


def get_user_service() -> UserService:
    """获取全局用户服务实例"""
    global _user_service

    if _user_service is None:
        _user_service = UserService()

    return _user_service
