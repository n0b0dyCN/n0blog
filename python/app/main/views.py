from flask import render_template, redirect, url_for, abort, flash, request
from flask import current_app, make_response
from flask_sqlalchemy import get_debug_queries

from . import main
from .. import db
from ..models import Post, Comment, Link

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/resume', methods=['GET'])
def resume():
    return render_template('resume.html')

@main.route('/archive', methods=['GET'])
def archive():
    return render_template('archives.html')

@main.route('/links', methods=['GET'])
def links():
    return render_template('links.html')

@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/test', methods=['GET'])
def test():
    return "test"
