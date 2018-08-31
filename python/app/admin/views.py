import os
from flask import render_template, redirect, request, \
        url_for, flash, session, jsonify

from . import admin
from .forms import AdminLoginForm, LinkAddForm
from .. import db
from ..models import Post, Tag, Comment, Link
from ..markdown_util import render_md_file, render_md_raw, \
        add_or_update_post, make_show, make_hide, delete_post

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
    link_add_form = LinkAddForm()
    return render_template('admin/index.html', link_add_form=link_add_form)

@admin.route("/posts")
def posts():
    return "Posts"

@admin.route("/comments")
def comments():
    return "Comments"

@admin.route("/links")
def links():
    return "Links"

