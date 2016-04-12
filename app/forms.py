#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/11'
__author__ = 'chuan.li'

from  flask_wtf import Form
from wtforms import StringField,IntegerField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username=StringField(validators=[DataRequired()],label='用户名')
    password=PasswordField(validators=[DataRequired()],label='密码')
    submit=SubmitField('提交')