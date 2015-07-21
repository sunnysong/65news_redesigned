#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import create_app, db

from app.models import User, Role, Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

from datetime import datetime
from flask import redirect, render_template, session, url_for, flash, request, current_app


from wtforms import TextAreaField
from wtforms.widgets import TextArea


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += " ckeditor"
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class CKAdmin(ModelView):
    form_overrides = dict(textarea=CKTextAreaField)
    create_template = 'ckeditor.html'
    edit_template = 'ckeditor.html'


app = create_app(os.environ.get('SCRAPING_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


admin = Admin(app, template_mode='bootstrap3')
admin.add_view(CKAdmin(User, db.session))
admin.add_view(CKAdmin(Post, db.session))
admin.add_view(CKAdmin(Role, db.session))

path = op.join(op.dirname(__file__), 'app/static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

@app.route('/', methods=['GET', 'POST'])
def index():
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    liked_posts = Post.query.order_by(Post.likes.desc()).limit(5)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination, liked_posts=liked_posts)


@app.route('/<category>', methods=['GET', 'POST'])
def sections(category):
    cat_list = {
        'news': '新闻',
        'industry': '行业',
        'policy': '政策',
        'baike': '百科'
    }
    cat_item = cat_list.get(category)

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(category=cat_item).order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

    liked_posts = Post.query.order_by(Post.likes.desc()).limit(5)
    posts = pagination.items
    return render_template('index.html', category=category, posts=posts, pagination=pagination, liked_posts=liked_posts)


@app.route('/article/<date>/<int:id>')
def article(id, date):
    post = Post.query.filter_by(id=id).first()
    article_prev = Post.query.filter_by(id=id-1).first()
    article_next = Post.query.filter_by(id=id+1).first()
    if post.likes is None:
        post.likes = 0

    liked_posts = Post.query.order_by(Post.likes.desc()).limit(5)
    return render_template('article.html', post=post, article_prev=article_prev, article_next=article_next, liked_posts=liked_posts)


@app.route('/like/<int:id>', methods=['GET', 'POST'])
def like(id):
    post = Post.query.filter_by(id=id).first()
    if post.likes is None:
        post.likes = 0
    post.likes += 1
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('article', date=post.date, id=post.id))

# added like feature


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
