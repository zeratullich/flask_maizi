#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/12'
__author__ = 'chuan.li'

from flask import render_template, redirect, url_for, request
from . import main
from flask_login import login_required, current_user
from app.models import Post, Comment
from forms import CommentForm, PostForm
from app import db
from flask_babel import lazy_gettext, gettext as _


@main.route('/')
@login_required
def index():
    # posts = Post.query.all()
    page_index = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.created.desc())
    pagination = query.paginate(page_index, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('index.html', title=lazy_gettext('欢迎来到我的博客'), posts=posts, pagination=pagination)


@main.route('/about')
def about():
    return 'about'


@main.route('/project')
def project():
    return 'Project!'


@main.route('/posts/<int:id>', methods=['POST', 'GET'])
def post(id):
    # 详情页
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(author=current_user, body=form.body.data, post=post)
        db.session.add(comment)
        db.session.commit()
    return render_template('posts/detail.html', title=post.title, form=form, post=post)


@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()
    if id == 0:
        print current_user
        print current_user._get_current_object
        post = Post(author_id=current_user.id)
    else:
        post = Post.query.get_or_404(id)
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('.post', id=post.id))

    title = _('添加新文章')
    if id > 0:
        title = _('编辑 - %(title)', title=post.title)
    return render_template('posts/edit.html', title=title, form=form, post=post)


@main.errorhandler(404)
def page_not_found(e):
    return '404', 404

# @main.add_app_template_test('current_link')
# def is_current_link(link):
#     return link == request.path
