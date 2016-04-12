#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/12'
__author__ = 'chuan.li'

from flask import render_template, flash, redirect, url_for


def init_views(app):
    @app.route('/')
    def index():
        return render_template('index.html', title='hello')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # if request.method=='POST':
        #     username=request.form['username']
        #     password=request.form['password']
        # else:
        #     username=request.args['username']
        #     password=request.args['password']
        from  forms import LoginForm
        form = LoginForm()
        flash('您已登录！')
        return render_template('login.html', form=form, title='登陆')

    @app.route('/about')
    def about():
        return 'about'

    @app.route('/project')
    def project():
        return 'Project!'
