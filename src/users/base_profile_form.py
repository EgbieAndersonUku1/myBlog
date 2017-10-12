from flask_wtf import Form
from wtforms import StringField, validators


class BaseProfileForm(Form):
    """The users profile"""

    first_name = StringField('First name', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    last_name = StringField('Last name', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    author_name = StringField('Author name', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])

