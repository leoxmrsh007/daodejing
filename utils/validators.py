# -*- coding: utf-8 -*-
"""
输入验证工具
"""

import re
from typing import Optional


def validate_chapter_id(chapter_id: int) -> bool:
    """
    验证章节 ID 是否有效

    Args:
        chapter_id: 章节编号

    Returns:
        是否有效
    """
    return isinstance(chapter_id, int) and 1 <= chapter_id <= 81


def validate_search_query(query: str) -> tuple[bool, Optional[str]]:
    """
    验证搜索查询

    Args:
        query: 搜索关键词

    Returns:
        (is_valid, error_message)
    """
    if not query:
        return False, "查询不能为空"

    if len(query) > 100:
        return False, "查询长度不能超过100个字符"

    # 检测潜在的 XSS 攻击
    xss_patterns = ['<', '>', '"', "'", '&', ';', 'javascript:', 'onerror=', 'onload=']
    query_lower = query.lower()
    for pattern in xss_patterns:
        if pattern in query_lower:
            return False, "查询包含非法字符"

    return True, None


def sanitize_text(text: str, max_length: int = 1000) -> str:
    """
    清理文本输入

    Args:
        text: 输入文本
        max_length: 最大长度

    Returns:
        清理后的文本
    """
    if not text:
        return ""

    # 移除控制字符
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    # 限制长度
    if len(text) > max_length:
        text = text[:max_length]

    return text.strip()
