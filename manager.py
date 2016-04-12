#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/12'
__author__ = 'chuan.li'

from  flask_script import Manager
from app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def dev():
    '''Runs the Flask development server i.e. app.run() when all files changed'''
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*')
    live_server.serve(open_url=True)


@manager.command
def test():
    pass


@manager.command
def deploy():
    pass


def debug(*args, **kwargs):
    return app.run(*args, **kwargs)


if __name__ == '__main__':
    # debug(debug=True, port=80)
    # debug(debug=True,port=80)
    manager.run()
