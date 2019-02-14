import os
import re
from markdown import Markdown

from .models import Post, Tag
from . import db
from . import redis as cache

def render_md_raw(raw):
    config = {
        'markdown.extensions.codehilite': {
            'use_pygments': False,
            'css_class': 'prettyprint',
        }
    }
    exts = ['markdown.extensions.meta',
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables']
    md = Markdown(extensions=exts, extension_configs=config)
    html = md.convert(raw)
    meta = {}
    meta['title'] = md.Meta.get('title', ['Untitled'])[0]
    meta['summary'] = md.Meta.get('summary', ['Unsummarized'])[0]
    meta['tags'] = [tag.strip() for tag in md.Meta.get('tags', [''])[0].split(',')]
    #meta['date'] = md.Meta.get('date', ['Date not set'])[0]
    return raw, html, meta

def render_md_file(foldername):
    content = "File not found"
    try:
        path = "/"
        with open(foldername, "r") as f:
            content = f.read()
    except:
        pass
    return render_md_raw(content)

def add_or_update_post(path, commit=False):
    pattern = re.compile("^\w+$")
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
    p.tags = [ Tag.fromTxt(t) for t in meta['tags'] ]
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
