from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from wtforms.fields.html5 import EmailField


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


