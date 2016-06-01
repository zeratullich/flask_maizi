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
import random, sys
from  PIL import Image, ImageDraw, ImageFont, ImageFilter

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


# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def generate_validate_code():
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('Arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    strs = ''
    for t in range(4):
        str = rndChar()
        strs += str
        draw.text((60 * t + 10, 10), str, font=font, fill=rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('app/static/image/code/code.jpg', 'jpeg')
    image_name = 'code.jpg'
    return image_name, strs


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        print "username is %s"% username
        print 'code_txt is %s' % session['code_text']
        print   '验证码是 %s'%form.verification_code.data
        if get_user(username):
            flash(_('账号已注册！'))
            code_img, code_text = generate_validate_code()
            session['code_text'] = code_text
            return render_template('register.html', title=_('注册'), form=form, code_img=code_img)
        if 'code_txt' in session and session['code_text'] != form.verification_code.data:
            code_img, code_text = generate_validate_code()
            session['code_text'] = code_text
            return render_template('register.html', title=_('注册'), form=form, code_img=code_img)

        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            print 'Yes'
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash(_('注册失败！'))
            code_img, code_text = generate_validate_code()
            session['code_text'] = code_text
            return render_template('register.html', title=_('注册'), form=form)
    code_img, code_text = generate_validate_code()
    # print code_img
    session['code_text'] = code_text
    print session['code_text']
    print form.verification_code.data
    return render_template('register.html', title=_('注册'), form=form, code_img=code_img)
