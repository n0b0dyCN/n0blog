from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from wtforms import ValidationError

class CommentForm(FlaskForm):
    content = TextAreaField("content")
    name = StringField("name", [Length(max=48)])
    url = StringField("url", [Length(max=80)])
    email = StringField("email", [Length(max=48), Email()])
    post = HiddenField("post")

