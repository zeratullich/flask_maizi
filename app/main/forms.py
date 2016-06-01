#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/5/16'
__author__ = 'chuan.li'

from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField
from flask_babel import lazy_gettext as _


class PostForm(Form):
    title = StringField(label=_('标题'), validators=[DataRequired()])
    body = PageDownField(label=_('正文'), validators=[DataRequired()])
    submit = SubmitField(label=_('发表'))


class CommentForm(Form):
    body = PageDownField(label=_('评论'), validators=[DataRequired()])
    submit = SubmitField(label=_('发表'))
