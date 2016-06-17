#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/12'
__author__ = 'chuan.li'

import sys
from flask import Flask,make_response
from flask_bootstrap import Bootstrap
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from datetime import timedelta
from flask_pagedown import PageDown
from flask_gravatar import Gravatar
from flask_babel import Babel, lazy_gettext

reload(sys)
sys.setdefaultencoding("utf-8")

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = lazy_gettext('登陆后方可访问该页面！')
pagedown = PageDown()
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'THIS IS JUST A TEST WEBPAGE !'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:R0boo@Sip$@127.0.0.1/maizi'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    from flask.json import JSONEncoder

    class CustomJSONEncoder(JSONEncoder):
        """This class adds support for lazy translation texts to Flask's
        JSON encoder. This is necessary when flashing translated texts."""

        def default(self, obj):
            from speaklater import is_lazy_string
            if is_lazy_string(obj):
                try:
                    return unicode(obj)  # python 2
                except NameError:
                    return str(obj)  # python 3
            return super(CustomJSONEncoder, self).default(obj)

    app.json_encoder = CustomJSONEncoder

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    Gravatar(app, size=64)
    babel.init_app(app)

    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    app.permanent_session_lifetime = timedelta(minutes=5)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    @babel.localeselector
    def get_locale():
        return current_user.locale

    return app
