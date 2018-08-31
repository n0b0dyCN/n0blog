import os
from flask import render_template, redirect, request, \
        url_for, flash, session, jsonify

from . import admin
from .. import db
from ..models import Post, Tag, Comment, Link
from ..markdown_util import render_md_file, render_md_raw, \
        add_or_update_post, make_show, make_hide, delete_post


@admin.route("/api/getposts")
def getposts():
    path_post_dict = {}
    db_posts = Post.query.all()
    for p in db_posts:
        path_post_dict[p.path] = p
        if not os.path.isdir(os.path.join(os.getenv("POSTS_PATH"), p.path)):
            p.exists = False
    for t in os.listdir(os.getenv("POSTS_PATH")):
        folder_path = os.path.join(os.getenv("POSTS_PATH"), t)
        if not os.path.isdir(folder_path):
            continue
        if t in path_post_dict:
            path_post_dict[t].exists = True
            continue
        print ("Add new posts")
        add_or_update_post(t, commit=False)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return ""
    return jsonify([p.to_dict() for p in Post.query.all()])

@admin.route("/api/posts/refresh", methods=["POST"])
def posts_refresh():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    if add_or_update_post(title, commit=True):
        return jsonify({'status':'ok'})
    else:
        return jsonify({'status':'failed'})

@admin.route("/api/posts/hide", methods=["POST"])
def posts_hide():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    if make_hide(title):
        return jsonify({'status':'ok'})
    else:
        return jsonify({'status':'failed'})

@admin.route("/api/posts/show", methods=["POST"])
def posts_show():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    if make_show(title):
        return jsonify({'status':'ok'})
    else:
        return jsonify({'status':'failed'})

@admin.route("/api/posts/del", methods=["POST"])
def posts_del():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    delete_post(title, commit=True)
    return jsonify({"status":"ok"})

