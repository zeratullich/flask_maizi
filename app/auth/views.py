#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/14'
__author__ = 'chuan.li'

from flask import render_template, redirect, url_for, flash
from . import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app import db
from flask_login import logout_user, login_user, session
from flask_babel import lazy_gettext, gettext as _
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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    from verify_code import generate_validate_code
    if form.validate_on_submit():
        username = form.username.data
        print "username is %s" % username
        print 'code_txt is %s' % session['code_text']
        print '验证码是 %s' % form.verification_code.data.lower()
        if get_user(username):
            flash(lazy_gettext('账号已注册！'))
            code_img, code_text = generate_validate_code()
            session['code_text'] = code_text
            return render_template('register.html', title=_('注册'), form=form, code_img=code_img)
        if 'code_text' in session and session['code_text'] != form.verification_code.data.lower():
            flash(lazy_gettext('验证码错误，请刷新重填！'))
            code_img, code_text = generate_validate_code()
            session['code_text'] = code_text
            return render_template('register.html', title=_('注册'), form=form, code_img=code_img)
        user = User(email=form.email.data, name=form.username.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash(_('注册失败！'))
            code_img, code_text = generate_validate_code()
            session['code_text'] = code_text
            return render_template('register.html', title=_('注册'), form=form)
    code_img, code_text = generate_validate_code()
    session['code_text'] = code_text
    return render_template('register.html', title=_('注册'), form=form, code_img=code_img)
