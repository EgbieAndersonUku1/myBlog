from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import EmailField

__author__ = 'Egbie Uku'


class EmailForm(Form):
    """Allows the user to change their username"""
    email = EmailField('Email', validators=[validators.DataRequired()])
