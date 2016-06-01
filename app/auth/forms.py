#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/11'
__author__ = 'chuan.li'

from  flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from flask_babel import lazy_gettext as _


class LoginForm(Form):
    pass
    username = StringField(validators=[DataRequired()], label=_('用户名'))
    password = PasswordField(validators=[DataRequired()], label=_('密码'))
    submit = SubmitField(_('提交'))


class RegistrationForm(Form):
    email = StringField(_('邮箱地址'), validators=[DataRequired(), Length(1, 64), Email(_('邮箱格式非法！请重新填写！'))])
    username = StringField(_('用户名'), validators=[DataRequired(), Length(1, 64),
                                                 Regexp('^[a-zA-z][A-Za-z0-9_.]*$', 0, _('用户名必须由字母、数字、下划线或 . 组成'))])
    password = PasswordField(_('密码'), validators=[DataRequired(), EqualTo('password2', message=_('密码必须一致！'))])
    password2 = PasswordField(_('确认密码'), validators=[DataRequired()])

    verification_code = StringField(_('验证码'), validators=[DataRequired(), Length(4, 4, message=_('填写4位验证码'))])
    submit = SubmitField(_('马上注册！'))

