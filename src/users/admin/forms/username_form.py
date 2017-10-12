from flask_wtf import Form
from wtforms import StringField, validators

__author__ = 'Egbie Uku'


class UsernameForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=4, max=80)])
