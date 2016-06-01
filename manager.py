#!/usr/bin/env python
# coding=utf-8

__date__ = '2016/4/12'
__author__ = 'chuan.li'

from  flask_script import Manager, Server
from app import create_app, db
from app.models import *
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("runserver", Server(use_debugger=True))
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    '''Runs the Flask development server i.e. app.run() when all files changed'''
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*')
    live_server.serve(open_url_delay=True, debug=True, port=80)


@manager.command
def test():
    pass


@manager.command
def forged():
    from forgery_py import basic, lorem_ipsum, name, internet, date
    from random import randint

    db.drop_all()
    db.create_all()

    Role.seed()

    def generate_comment(func_author, func_post):
        return Comment(body=lorem_ipsum.paragraphs(),
                       created=date.date(past=True),
                       author=func_author(),
                       post=func_post())

    def generate_post(func_author):
        return Post(title=lorem_ipsum.title(),
                    body=lorem_ipsum.paragraphs(),
                    created=date.date(),
                    author=func_author())

    def generate_user():
        return User(name=internet.user_name(), email=internet.email_address(),
                    password=basic.text(6, at_least=6, spaces=False))

    users = [generate_user() for i in range(0, 9)]

    db.session.add_all(users)

    random_user = lambda: users[randint(0, 8)]

    posts = [generate_post(random_user) for i in range(0, randint(360, 400))]
    db.session.add_all(posts)

    random_post = lambda: posts[randint(0, len(posts) - 1)]

    comments = [generate_comment(random_user, random_post) for i in range(0, randint(300, 400))]
    db.session.add_all(comments)

    db.session.commit()


@manager.command
def deploy():
    pass


def debug(*args, **kwargs):
    return app.run(*args, **kwargs)


if __name__ == '__main__':
    # debug(debug=True, port=80)
    # debug(debug=True,port=80)
    manager.run()
