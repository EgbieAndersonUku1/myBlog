from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.widgets import TextArea


class CommentForm(Form):
    """"""
    comment = StringField("Comment", widget=TextArea(), validators=[validators.DataRequired()])