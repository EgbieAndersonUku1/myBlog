from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
import re

_match = re.compile(r'^[A-Za-z0-9_]+$')

class RegistrationForm(Form):
    """The RegistrationForm allows the user to enter the fields needed to register the application in the GUI"""

    first_name = StringField('First Name', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    last_name  = StringField('Last Name', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm',
                                                                        message='The password entered does not match'),
                                                     validators.Length(min=3, max=80)])

    confirm = PasswordField('Repeat password')
    author_name = StringField('Author name', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])

    @staticmethod
    def _check_name_value(name):
        found = _match.search(name)
        if not found:
            raise ValidationError("The name can contain an uppercase, a lowercase, digits(0-9) or an underscore"
                                  " but must not contain any special characters!")

    def validate_first_name(form, field):
        RegistrationForm._check_name_value(form.first_name.data)

    def validate_last_name(form, field):
        RegistrationForm._check_name_value(form.last_name.data)

    def validate_username(form, field):
        RegistrationForm._check_name_value(form.username.data)