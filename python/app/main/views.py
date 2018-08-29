from flask import render_template, redirect, url_for, abort, flash, request
from flask import current_app, make_response
from flask_sqlalchemy import get_debug_queries

from markdown import Markdown

from . import main
from .. import db
from ..models import Post, Comment, Link

from ..markdown_util import render_md_raw

class L():
    def __init__(self, time, url, desc):
        self.time=str(time)
        self.url=url
        self.desc=desc

@main.route('/', methods=['GET'])
def index():
    posts=[]
    for i in range(10):
        posts.append(L("2018 Apr 30th", url_for('main.search', i=i), "test{}".format(i)))
    return render_template('main/index.html', posts=posts)

@main.route('/resume', methods=['GET'])
def resume():
    return "resume"
    return render_template('main/resume.html')

@main.route('/archive', methods=['GET'])
def archive():
    return "archive"
    return render_template('main/archives.html')

@main.route('/links', methods=['GET'])
def links():
    return "links"
    return render_template('main/links.html')

@main.route('/search', methods=["GET"])
def search():
    return render_template('main/search.html')

@main.route('/test', methods=['GET'])
def test():
    raw = open("/posts/test/post.md", "r").read()
    html, meta = render_md_raw(raw)
    return render_template('main/post.html', html=html, meta=meta)

@main.route('/post/<int:id>')
def post(id):
    return "Post {}".format(id)
    pass
