# -*- coding: utf-8 -*-
"""
页面路由 - 渲染 HTML 页面
"""

from flask import Blueprint, render_template, redirect, url_for
from services.data_service import DataService

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
    """首页重定向"""
    return redirect(url_for('pages.daodejing_index'))


@bp.route('/daodejing/')
def daodejing_index():
    """道德经首页 - 章节目录"""
    data = DataService.load_data()
    return render_template('ddj/index.html', data=data)


@bp.route('/daodejing/chapter/<int:chapter_id>')
def chapter_view(chapter_id):
    """单章阅读页"""
    if chapter_id < 1 or chapter_id > 81:
        return redirect(url_for('pages.daodejing_index'))

    chapter = DataService.get_chapter_with_annotation(chapter_id)
    data = DataService.load_data()
    return render_template('ddj/chapter.html', chapter=chapter, data=data)


@bp.route('/daodejing/compare/<int:chapter_id>')
def compare_view(chapter_id):
    """多版本对照页"""
    if chapter_id < 1 or chapter_id > 81:
        return redirect(url_for('pages.daodejing_index'))

    chapter = DataService.get_chapter_with_annotation(chapter_id)
    data = DataService.load_data()
    return render_template('ddj/compare.html', chapter=chapter, data=data)
