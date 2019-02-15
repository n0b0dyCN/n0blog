#!/usr/bin/python
import os

from app import create_app, db
from flask_migrate import Migrate, upgrade, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, Post=Post)

@app.cli.command()
def deploy():
    db.create_all()
    pass

