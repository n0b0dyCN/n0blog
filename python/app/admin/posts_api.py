import os
import re
from flask import render_template, redirect, request, \
        url_for, flash, session, jsonify

from . import admin
from .. import db
from .. import redis as cache
from ..models import Post, Tag, Comment, Link
from ..markdown_util import render_md_file, render_md_raw

def add_or_update_post(path, commit=False):
    pattern = re.compile("^[\w\-]+$")
    if not re.match(pattern, path):
        print("pattern not matched.")
        return False
    md_path = os.path.join(os.getenv("POSTS_PATH"), path, "post.md")
    if not os.path.exists(md_path):
        print("file not exists.")
        return False
    raw, html, meta = render_md_file(md_path)
    p = Post.query.filter_by(path=path).first()
    insert = (p==None)
    if insert:
        p = Post()
        p.show = False
    p.path = path
    p.title = meta['title']
    p.body = raw
    p.body_html = html
    p.tags = [ Tag.query.filter_by(txt=t).one_or_none() or Tag.fromTxt(t) for t in meta['tags'] ]
    p.isexist = True
    if insert:
        db.session.add(p)
    else:
        cache.delete_post(p.title)
    if commit:
        db.session.commit()
    return True

def make_show_hide(title, show):
    p = Post.query.filter_by(title=title).first()
    if not p:
        return False
    p.show = show
    db.session.commit()
    cache.delete_post_list()
    return True

def make_show(title):
    return make_show_hide(title, show=True)

def make_hide(title):
    return make_show_hide(title, show=False)

def delete_post(title, commit=False):
    p = Post.query.filter_by(title=title).first()
    db.session.delete(p)
    if commit:
        db.session.commit()

@admin.route("/api/getposts")
def getposts():
    path_post_dict = {}
    db_posts = Post.query.all()
    for p in db_posts:
        path_post_dict[p.path] = p
        if not os.path.isdir(os.path.join(os.getenv("POSTS_PATH"), p.path)):
            #cache.delete_post(p.title)
            p.exists = False
    for t in os.listdir(os.getenv("POSTS_PATH")):
        # print(t)
        if t[0] == ".":
            continue
        folder_path = os.path.join(os.getenv("POSTS_PATH"), t)
        if not os.path.isdir(folder_path):
            # print("not dir")
            continue
        if t in path_post_dict:
            # print("in dict")
            path_post_dict[t].exists = True
            continue
        add_or_update_post(t, commit=False)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return ""
    return jsonify([p.to_dict() for p in Post.query.order_by(Post.timestamp).all()])

@admin.route("/api/posts/refresh", methods=["POST"])
def posts_refresh():
    if 'path' not in request.form:
        return jsonify({'status':'failed'})
    path = request.form['path']
    if add_or_update_post(path, commit=True):
        return jsonify({'status':'ok'})
    else:
        return jsonify({'status':'failed'})

@admin.route("/api/posts/hide", methods=["POST"])
def posts_hide():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    cache.delete_post(title)
    if make_hide(title):
        return jsonify({'status':'ok'})
    else:
        return jsonify({'status':'failed'})

@admin.route("/api/posts/show", methods=["POST"])
def posts_show():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    cache.delete_post(title)
    if make_show(title):
        return jsonify({'status':'ok'})
    else:
        return jsonify({'status':'failed'})

@admin.route("/api/posts/del", methods=["POST"])
def posts_del():
    if 'title' not in request.form:
        return jsonify({'status':'failed'})
    title = request.form['title']
    cache.delete_post(title)
    delete_post(title, commit=True)
    return jsonify({"status":"ok"})

