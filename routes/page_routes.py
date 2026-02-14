# -*- coding: utf-8 -*-
"""
页面路由 - 渲染 HTML 页面
支持多经典：道德经、庄子等
"""

from pathlib import Path
from typing import Any, Optional

from flask import Blueprint, redirect, render_template, url_for

from services.classic_service import (
    ClassicService,
    get_all_classics,
    get_default_classic_id,
    validate_classic_id,
)

bp = Blueprint("pages", __name__)


def get_classic_from_request(default: Optional[str] = None) -> str:
    """
    从请求中获取经典ID，如果没有指定则使用默认值

    Args:
        default: 默认经典ID，如果为None则使用系统默认

    Returns:
        经典ID字符串
    """
    from flask import request

    view_args = request.view_args or {}
    classic_id = view_args.get("classic_id") or default or get_default_classic_id()
    return str(classic_id)


@bp.route("/")
def index() -> Any:
    """平台首页 - 展示所有经典"""
    all_classics = get_all_classics()
    return render_template("index.html", all_classics=all_classics)


@bp.route("/platform/")
def platform() -> Any:
    """平台首页 - 保留路由兼容性"""
    all_classics = get_all_classics()
    return redirect(url_for("pages.index"))


@bp.route("/<classic_id>/")
def classic_index(classic_id: str) -> Any:
    """经典首页 - 章节目录"""
    if not validate_classic_id(classic_id):
        return redirect(
            url_for("pages.classic_index", classic_id=get_default_classic_id())
        )

    service = ClassicService(classic_id)
    data = service.load_data()
    classic_config = service.to_dict()
    all_classics = get_all_classics()

    return render_template(
        "classic/index.html",
        data=data,
        classic=classic_config,
        all_classics=all_classics,
    )


@bp.route("/<classic_id>/chapter/<int:chapter_id>")
def chapter_view(classic_id: str, chapter_id: int) -> Any:
    """单章阅读页"""
    if not validate_classic_id(classic_id):
        return redirect(
            url_for("pages.classic_index", classic_id=get_default_classic_id())
        )

    service = ClassicService(classic_id)

    if chapter_id < 1 or chapter_id > service.chapter_count:
        return redirect(url_for("pages.classic_index", classic_id=classic_id))

    chapter = service.get_chapter_with_annotation(chapter_id)
    data = service.load_data()
    classic_config = service.to_dict()
    all_classics = get_all_classics()

    return render_template(
        "classic/chapter.html",
        chapter=chapter,
        data=data,
        classic=classic_config,
        all_classics=all_classics,
    )


@bp.route("/<classic_id>/compare/<int:chapter_id>")
def compare_view(classic_id: str, chapter_id: int) -> Any:
    """多版本对照页"""
    if not validate_classic_id(classic_id):
        return redirect(
            url_for("pages.classic_index", classic_id=get_default_classic_id())
        )

    service = ClassicService(classic_id)

    if chapter_id < 1 or chapter_id > service.chapter_count:
        return redirect(url_for("pages.classic_index", classic_id=classic_id))

    chapter = service.get_chapter_with_annotation(chapter_id)
    data = service.load_data()
    classic_config = service.to_dict()
    all_classics = get_all_classics()

    return render_template(
        "classic/compare.html",
        chapter=chapter,
        data=data,
        classic=classic_config,
        all_classics=all_classics,
    )


# ============ 向后兼容路由 ============


@bp.route("/daodejing/")
def daodejing_index() -> Any:
    """道德经首页 - 向后兼容（直接渲染）"""
    service = ClassicService("ddj")
    data = service.load_data()
    classic_config = service.to_dict()
    all_classics = get_all_classics()

    return render_template(
        "ddj/index.html",
        data=data,
        classic=classic_config,
        all_classics=all_classics,
    )


@bp.route("/daodejing/chapter/<int:chapter_id>")
def daodejing_chapter_view(chapter_id: int) -> Any:
    """道德经单章阅读页 - 向后兼容（直接渲染）"""
    service = ClassicService("ddj")

    if chapter_id < 1 or chapter_id > service.chapter_count:
        return redirect(url_for("pages.daodejing_index"))

    chapter = service.get_chapter_with_annotation(chapter_id)
    data = service.load_data()
    classic_config = service.to_dict()
    all_classics = get_all_classics()

    return render_template(
        "ddj/chapter.html",
        chapter=chapter,
        data=data,
        classic=classic_config,
        all_classics=all_classics,
    )


@bp.route("/daodejing/compare/<int:chapter_id>")
def daodejing_compare_view(chapter_id: int) -> Any:
    """道德经多版本对照页 - 向后兼容（直接渲染）"""
    service = ClassicService("ddj")

    if chapter_id < 1 or chapter_id > service.chapter_count:
        return redirect(url_for("pages.daodejing_index"))

    chapter = service.get_chapter_with_annotation(chapter_id)
    data = service.load_data()
    classic_config = service.to_dict()
    all_classics = get_all_classics()

    return render_template(
        "ddj/compare.html",
        chapter=chapter,
        data=data,
        classic=classic_config,
        all_classics=all_classics,
    )


# ============ API 文档路由 ============


@bp.route("/docs")
@bp.route("/docs/api")
def api_docs() -> Any:
    """API 文档页面"""
    import datetime

    current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
    api_docs_url = "/docs/openapi.yaml"

    return render_template(
        "docs/api_docs.html", current_date=current_date, api_docs_url=api_docs_url
    )


@bp.route("/docs/openapi.yaml")
def openapi_spec() -> Any:
    """提供 OpenAPI 规范文件"""
    from flask import send_from_directory

    docs_dir = Path(__file__).parent.parent / "docs"
    return send_from_directory(docs_dir, "openapi.yaml", mimetype="text/yaml")
