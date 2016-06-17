#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/14'
__author__ = 'chuan.li'

from flask import render_template, redirect, url_for, flash, make_response, session
from . import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db
from flask_login import logout_user, login_user
from flask_babel import lazy_gettext, gettext as _

try:
    import cStringIO as StringIO
except:
    import StringIO

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
        if user is not None:
            login_user(user)
            print user
            return redirect(url_for('main.index'))
    return render_template('login.html', form=form, title=_('登陆'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def get_user(username):
    user = User.query.filter_by(name=username).first()
    if user is not None:
        return True
    else:
        return False


@auth.route('/get/code')
def get_code():
    from verify_code import generate_validate_code
    code_img, strs = generate_validate_code()
    buf = StringIO.StringIO()
    code_img.save(buf, 'JPEG', quality=80)
    session['code_text'] = strs.lower()
    print session['code_text']
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print 'the code text is %s' % session.get('code_text', 'not exist!')
    if form.validate_on_submit():
        print 'yes'
        username = form.username.data
        print 'the user is %s'% username
        print 'the session is %s'%session['code_text']
        if get_user(username):
            flash(lazy_gettext('账号已注册！'))
            return render_template('register.html', title=_('注册'), form=form)
        if 'code_text' in session and session['code_text'] != form.verification_code.data.lower():
            flash(lazy_gettext('验证码错误，请刷新重填！'))
            return render_template('register.html', title=_('注册'), form=form)
        user = User(email=form.email.data, name=form.username.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash(_('注册失败！'))
            return render_template('register.html', title=_('注册'), form=form)
    return render_template('register.html', title=_('注册'), form=form)
