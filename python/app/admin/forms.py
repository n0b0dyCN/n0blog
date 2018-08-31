from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import ValidationError

class AdminLoginForm(FlaskForm):
    password = StringField("Password")

class LinkAddForm(FlaskForm):
    name = StringField("name")
    link = StringField("link")
    description = StringField("description")
