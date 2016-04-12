#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/12'
__author__ = 'chuan.li'

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from views import init_views
import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")

basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'THIS IS JUST A TEST WEBPAGE !'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = True
    nav.register_element('top', Navbar('Flask',
                                       View('主页', 'index'),
                                       View('关于', 'about'),
                                       View('项目', 'project')))
    nav.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    init_views(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=80)
