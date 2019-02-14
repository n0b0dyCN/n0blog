import os
from flask import render_template, redirect, request, \
        url_for, flash, session, jsonify

from . import admin
from .. import db
from .. import redis as cache
from ..models import Post, Tag, Comment, Link

@admin.route("/api/comments/getcomments")
def getcomments():
    comments = Comment.query.all()
    return jsonify([ c.to_dict() for c in comments ])

@admin.route("/api/comments/hide", methods=["POST"])
def comments_hide():
    c = Comment.query.filter_by(id=request.form['id']).first()
    if not c:
        return jsonify({"status":"failed"})
    c.show = False
    db.session.commit()
    cache.delete_post(c.post.title)
    return jsonify({"status":"ok"})

@admin.route("/api/comments/show", methods=["POST"])
def comments_show():
    c = Comment.query.filter_by(id=request.form['id']).first()
    if not c:
        return jsonify({"status":"failed"})
    c.show = True
    db.session.commit()
    cache.delete_post(c.post.title)
    return jsonify({"status":"ok"})

@admin.route("/api/comments/delete", methods=["POST"])
def comments_delete():
    c = Comment.query.filter_by(id=request.form['id']).first()
    if not c:
        return jsonify({"status":"failed"})
    db.session.delete(c)
    db.session.commit()
    cache.delete_post(c.post.title)
    return jsonify({"status":"ok"})

