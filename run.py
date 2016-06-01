#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/5/11'
__author__ = 'chuan.li'

from app import create_app

app = create_app()
app.run(debug=True, port=80)
