#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/14'
__author__ = 'chuan.li'

from flask import Blueprint

auth = Blueprint('auth', __name__)

import forms, views
