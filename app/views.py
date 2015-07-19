#!usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask import redirect, render_template, session, url_for, flash, request
from . import db
from .models import User, Role, Post, Permission

@app.route('/')
def index():
	posts = Post.query.filter_by(timestamp.desc()).limit(10)
	return render_template('index.html', posts=posts)