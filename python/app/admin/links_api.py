import os
from flask import render_template, redirect, request, \
        url_for, flash, session, jsonify

from . import admin
from .. import db
from ..models import Post, Tag, Comment, Link

@admin.route("/api/links/getlinks")
def getlinks():
    links = Link.query.all()
    return jsonify([ l.to_dict() for l in links ])

@admin.route("/api/links/add", methods=["POST"])
def links_add():
    l = Link()
    l.name = request.form["name"]
    l.link = request.form["link"]
    l.description = request.form["description"]
    db.session.add(l)
    db.session.commit()
    return jsonify({"status":"ok"})

@admin.route("/api/links/update", methods=["POST"])
def links_update():
    l = Link.query.filter_by(id=request.form["id"]).first()
    if not l:
        return jsonify({"status":"failed"})
    l.name = request.form["name"]
    l.link = request.form["link"]
    l.description = request.form["description"]
    db.session.commit()
    return jsonify({"status":"ok"})

@admin.route("/api/links/delete", methods=["POST"])
def links_delete():
    l = Link.query.filter_by(id=request.form["id"]).first()
    if not l:
        return jsonify({"status":"failed"})
    db.session.delete(l)
    db.session.commit()
    return jsonify({"status":"ok"})

