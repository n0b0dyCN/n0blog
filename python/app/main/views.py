from flask import render_template, redirect, url_for, abort, flash, request, send_from_directory
from flask import current_app, make_response
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import and_, or_
from functools import wraps

from markdown import Markdown
import os
import imghdr

from . import main
from .forms import CommentForm
from .. import db
from .. import redis as cache
from ..models import Post, Comment, Link, Tag

def cached(timeout=600, key='main_view_%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                print("Cached ", cache_key)
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

@main.route('/', methods=['GET'])
@cached()
def index():
    posts = Post.query \
                .filter(and_(Post.title!="resume", Post.title!="about")) \
                .filter_by(show=True) \
                .order_by(Post.timestamp) \
                .limit(10).all()
    return render_template('main/index.html', posts=posts)

@main.route('/resume', methods=['GET'])
@cached()
def resume():
    return post("resume")
    p = Post.query.filter_by(title='resume', show=True).first()
    if p:
        return render_template('main/post.html', post=p)
    else:
        return render_template('error/404.html'), 404

@main.route('/archive', methods=['GET'])
@cached()
def archive():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query \
                    .filter(and_(Post.title!="resume", Post.title!="about")) \
                    .filter_by(show=True) \
                    .order_by(Post.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('main/archive.html', posts=posts, pagination=pagination)

@main.route('/links', methods=['GET'])
@cached()
def links():
    links = Link.query.all()
    return render_template('main/links.html', links=links)

@main.route('/post/<string:title>/', methods=["GET", "POST"])
@cached()
def post(title):
    p = Post.query.filter_by(title=title, show=True).first()
    if not p:
        return render_template('error/404.html')
    comment_form = CommentForm(post=str(p.id))
    if comment_form.validate_on_submit():
        c = Comment(
            name=comment_form.name.data,
            email=comment_form.email.data,
            url=comment_form.url.data,
            content=comment_form.content.data
        )
        p.comments.append(c)
        db.session.commit()
    comments = p.comments.filter_by(show=True).all()
    return render_template(
        'main/post.html',
        post=p,
        comment_form=comment_form,
        comments=comments
    )

@main.route('/tag/<string:txt>')
@cached()
def tag(txt):
    posts = Tag.query.filter_by(txt=txt).first().posts
    return render_template('main/tag.html', posts=posts, tag=txt)

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

@main.route('/search', methods=["GET"])
@cached()
def search():
    page = request.args.get('page', 1, type=int)
    q = request.args.get("s")
    if q == None:
        return redirect(url_for("main.index"))
    pagination = Post.query \
                    .filter(or_(Post.title.ilike("%{}%".format(q)), Post.body.ilike("%{}%".format(q)))) \
                    .filter_by(show=True) \
                    .order_by(Post.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('main/search.html', posts=posts, pagination=pagination,q=q)

@main.route('/test', methods=['GET'])
def test():
    return ""

