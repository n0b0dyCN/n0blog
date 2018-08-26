from flask import render_template, redirect, url_for, abort, flash, request
from flask import current_app, make_response
from flask_sqlalchemy import get_debug_queries

from markdown import Markdown

from . import main
from .. import db
from ..models import Post, Comment, Link

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
    return render_template('index.html', posts=posts)

@main.route('/resume', methods=['GET'])
def resume():
    return "resume"
    return render_template('resume.html')

@main.route('/archive', methods=['GET'])
def archive():
    return "archive"
    return render_template('archives.html')

@main.route('/links', methods=['GET'])
def links():
    return "links"
    return render_template('links.html')

@main.route('/search', methods=["GET"])
def search():
    return render_template('search.html')

@main.route('/test', methods=['GET'])
def test():
    config = {
        'markdown.extensions.codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint',
        }
    }
    raw = open("/home/n0blog/app/static/test.md", "r").read()
    md = Markdown(extensions = ['markdown.extensions.meta', 'markdown.extensions.fenced_code', 'markdown.extensions.codehilite', 'markdown.extensions.tables'],
                 extension_configs=config)
    html = md.convert(raw)
    meta = md.Meta
    if 'title' not in meta:
        meta['title'] = ["Untitled"]
    if 'summary' not in meta:
        meta['summary'] = ["Unsumarized."]
    if 'tags' not in meta:
        meta['tags'] = []
    else:
        meta['tags'] = [i.strip() for i in meta['tags'][0].split(',')]
    if 'date' not in meta:
        meta['date'] = ['Unknown date']

    return render_template('post.html', html=html, meta=md.Meta)
