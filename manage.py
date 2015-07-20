#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app, db

from app.models import User, Role, Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand, upgrade
from config import config

app = create_app(os.environ.get('SCRAPING_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app, db)

from datetime import datetime
from flask import current_app, redirect, render_template, session, url_for, flash, request


@app.route('/', methods=['GET', 'POST'])
def index():
	# posts = Post.query.order_by(Post.timestamp.desc()).all()
	page=request.args.get('page', 1, type=int)
	pagination=Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	posts=pagination.items
	return render_template('index.html', posts=posts, pagination=pagination)


@app.route('/article/<date>/<int:id>')
def article(id, date):
	post=Post.query.filter_by(id=id).first()
	article_prev=Post.query.filter_by(id=id-1).first()
	article_next=Post.query.filter_by(id=id+1).first()
	return render_template('article.html', post=post, article_prev=article_prev, article_next=article_next)


def make_shell_context():
	return dict(app=app, db=db, Role=Role, User=User, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
    # create user roles
    Role.insert_roles()
    # create self-follows for all users



if __name__ == '__main__':
	manager.run()
