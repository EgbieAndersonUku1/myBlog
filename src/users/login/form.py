from flask_wtf import Form
from wtforms import StringField, PasswordField, validators


class LoginForm(Form):
    """Allows the user to log into the blog application"""

    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(min=3, max=80)])
    password = PasswordField('Password', validators=[validators.DataRequired()])




