import os
from markdown import Markdown

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
    meta['date'] = md.Meta.get('date', ['Date not set'])[0]
    return html, meta

def render_md_file(foldername):
    content = "File not found"
    try:
        path = "/"
        with open(foldername, "r") as f:
            content = f.read()
    except:
        pass
    return render_md_raw(content)

