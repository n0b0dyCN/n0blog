import os
from flask import jsonify
from sqlalchemy import and_
from . import admin
from .. import db
from ..models import Post, Tag, Comment, Link

@admin.route("/api/statistics/getstatistics")
def getstatistics():
    ret = []
    ret.append({
        "key": "public posts",
        "value": Post.query \
                        .filter(Post.title!="resume") \
                        .filter_by(show=True) \
                        .count()
    })
    ret.append({
        "key": "total posts",
        "value": Post.query.count()
    })
    ret.append({
        "key": "comments",
        "value": Comment.query.count()
    })
    ret.append({
        "key": "link",
        "value": Link.query.count()
    })
    return jsonify(ret)