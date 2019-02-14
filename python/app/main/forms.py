from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length
from wtforms import ValidationError

class CommentForm(FlaskForm):
    content = TextAreaField("content")
    name = StringField("name", [Length(max=48, message="Name too long!")])
    url = StringField("url", [Length(max=80, message="Link to long!")])
    email = StringField("email", [Length(max=48), Email(message="Invalid email format!")])
    post = HiddenField("post")

