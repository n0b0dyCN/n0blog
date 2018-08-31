from flask import render_template, redirect, url_for, abort, flash, request, send_from_directory
from flask import current_app, make_response
from flask_sqlalchemy import get_debug_queries

from markdown import Markdown
import os
import imghdr

from . import main
from .. import db
from ..models import Post, Comment, Link

from ..markdown_util import render_md_raw, add_or_update_post


@main.route('/', methods=['GET'])
def index():
    posts = Post.query.filter_by(show=True).order_by(Post.timestamp).limit(10).all()
    print(posts)
    return render_template('main/index.html', posts=[ p.to_dict() for p in posts ])

@main.route('/resume', methods=['GET'])
def resume():
    p = Post.query.filter_by(title='resume', show=True).first()
    print ("RESUME")
    print (p)
    if p:
        return render_template('main/post.html', post=p.to_dict())
    else:
        return render_template('error/404.html'), 404

@main.route('/archive', methods=['GET'])
def archive():
    return "archive"
    return render_template('main/archives.html')

@main.route('/links', methods=['GET'])
def links():
    links = Link.query.all()
    return render_template('main/links.html', links=links)

@main.route('/search', methods=["GET"])
def search():
    return render_template('main/search.html')

@main.route('/test', methods=['GET'])
def test():
    return ""

@main.route('/post/<string:title>/')
def post(title):
    p = Post.query.filter_by(title=title, show=True).first()
    if p:
        return render_template('main/post.html', post=p.to_dict())
    else:
        return render_template('error/404.html')


@main.route('/post/<string:title>/<string:img_name>')
def post_images(title, img_name):
    p = Post.query.filter_by(title=title, show=True).first()
    if (not p) or (not p.isexist):
        return render_template("error/404.html"), 404
    full_path = os.path.join(
        os.getenv("POSTS_PATH"),
        p.path,
        img_name
    )
    if imghdr.what(full_path):
        return send_from_directory(
            os.path.join(os.getenv("POSTS_PATH"), p.path),
            img_name
        )
    else:
        return render_template("error/403.html"), 403
