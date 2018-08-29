import os
from flask import render_template, redirect, request, \
        url_for, flash, session, jsonify

from . import admin
from .forms import AdminLoginForm
from ..models import Post
from ..markdown_util import render_md_file, render_md_raw

@admin.before_request
def before_request():
    if request.path == url_for('admin.login'):
        return
    if 'login' in session:
        if session['login'] == True:
            return
    return redirect(url_for('admin.login'))

@admin.route("/login", methods=["GET", "POST"])
def login():
    if 'login' in session and session['login'] == True:
        flash('Already logged in.')
        return redirect(url_for('admin.index'))
    session.permanent = True
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.password.data == os.getenv("ADMIN_PASS"):
            session['login'] = True
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('admin.login'))
    return render_template("admin/login.html", form=form)

@admin.route("/logout")
def logout():
    if 'login' not in session:
        return redirect(url_for('main.index'))
    session['login'] = False
    return redirect(url_for('main.index'))


@admin.route("/")
def index():
    return render_template('admin/index.html')

@admin.route("/posts")
def posts():
    return "Posts"

@admin.route("/comments")
def comments():
    return "Comments"

@admin.route("/links")
def links():
    return "Links"

@admin.route("/getposts")
def getposts():
    posts = []
    for t in os.listdir(os.getenv("POSTS_PATH")):
        d = {}
        path = os.path.join(os.getenv("POSTS_PATH"), t)
        if not os.path.isdir(path):
            continue
        md_path = os.path.join(path, "post.md")
        if not os.path.exists(md_path):
            continue
        html, meta = render_md_file(md_path)
        d['path'] = path
        d['title'] = meta['title']
        d['date'] = meta['date']
        d['tags'] = meta['tags']
        d['show'] = 1
        posts.append(d)
    return jsonify(posts)

@admin.route("/posts/refresh", methods=["POST"])
def posts_refresh():
    print (request.headers)
    print (request.form)
    return "success"

@admin.route("/posts/hide", methods=["POST"])
def posts_hide():
    return "success";

@admin.route("/posts/show", methods=["POST"])
def posts_show():
    return "success";
