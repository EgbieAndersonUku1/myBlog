from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
import re

from users.users.users import User

_match = re.compile(r'^[A-Za-z0-9_]+$')

class RegistrationForm(Form):
    """The RegistrationForm allows the user to enter the fields needed to register the application in the GUI"""

    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm',message='The password entered does not match'),
                                                     validators.Length(min=3, max=80)])

    confirm = PasswordField('Repeat password')

    def validate_email(form, field):
        """"""
        if User.get_by_email(form.email.data):
            raise ValidationError('The email is already in use')


    def validate_username(form, field):

        username = form.username.data

        if not _match.search(username):
            raise ValidationError("Invalid username format!")
        if User.get_by_username(username):
            raise ValidationError('The username is already in use')
