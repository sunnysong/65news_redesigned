#!usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
from sqlalchemy.dialects.postgresql import JSON
# what are the JSON format
from flask import current_app, request
from datetime import datetime
from flask.ext.login import UserMixin


class Permission:
	WRITE_ARTICLES = 0x04
	ADMINISTER = 0x80
	COMMENT = 0x02
    FOLLOW = 0x01
    MODERATE_COMMENTS = 0x08

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), unique=True, index=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role')

	@staticmethod
	def insert_roles():
		roles = {
			'User': (Permission.FOLLOW |
					 Permission.COMMENT |
					 Permission.WRITE_ARTICLES, True),
			'Moderator': (Permission.FOLLOW |
						  Permission.COMMENT |
						  Permission.WRITE_ARTICLES |
						  Permission.MODERATE_COMMENTS, False),
			'Admin': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()


class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __init__(self):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			self.role = Role.query.filter_by(default=True).first()

	def can(self, permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permission

	def is_admin(self):
		return self.can(Permission.ADMINISTER)


class Post(db.Model):

	"""
	create a model for news articles,
	each article has nine elements: not including id
	title, summary, source, timestamp, author,
	body_html, comments, likes, keywords, img_href
	"""
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64), index=True, unique=True)
	# title character limit need to be respecified
	summary = db.Column(db.String(200))
	source = db.Column(db.String(64))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	body_html = db.Column(db.Text())
	likes = db.Column(db.Integer, index=True)
	keywords = db.Column(db.String(64))  # keywords should be a sequence
	img_href = db.Column(db.String(120))
	category = db.Column(db.String(32), index=True)

	#add a recent column to track whether the post is recently added to the site

	def __init__(self, title, summary, source, timestamp, keywords, img_href, body_html):
		self.title = title
		self.summary = summary
		self.source = source
		# self.author = author
		self.keywords = keywords
		self.img_href = img_href
		self.timestamp = timestamp
		self.body_html = body_html

	def __repr__(self):
		return '<title {}>'.format(self.title, encoding='utf-8')

	@property
	def date(self):
		return str(self.timestamp.date()).replace('-', '')

