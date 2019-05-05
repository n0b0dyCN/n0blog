from datetime import datetime
from markdown import markdown

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from . import db

post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text, unique=True)
    title = db.Column(db.Text, unique=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    show = db.Column(db.Boolean)
    isexist = db.Column(db.Boolean)
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    tags = db.relationship('Tag', secondary=post_tag, backref=db.backref('posts'), cascade='all', passive_deletes=True)

    def to_dict(self):
        d = {}
        d['path'] = self.path
        d['title'] = self.title
        d['body'] = self.body
        d['body_html'] = self.body_html
        d['timestamp'] = self.timestamp
        d['date'] = self.timestamp.strftime('%b %d, %Y')
        d['show'] = self.show
        d['isexist'] = self.isexist
        d['tags'] = [t.txt for t in self.tags]
        return d

    @property
    def date(self):
        return self.timestamp.strftime("%b %d, %Y")

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    txt = db.Column(db.Text)

    @staticmethod
    def fromTxt(s):
        ret = Tag()
        ret.txt = s
        return ret

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    url = db.Column(db.Text)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    show = db.Column(db.Boolean, default=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    @property
    def time(self):
        return self.timestamp.strftime("%b %d, %Y  %H:%M")

    def to_dict(self):
        d = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "url": self.url,
            "content": self.content,
            "time": self.time,
            "show": self.show,
            "post_title": self.post.title
        }
        return d

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    link = db.Column(db.Text)
    description = db.Column(db.Text)

    def to_dict(self):
        d = {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "description": self.description,
            "action": 7
        }
        return d
