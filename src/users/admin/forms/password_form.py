from users.base_password_form import BasePasswordForm
from wtforms import validators, PasswordField

__author__ = 'Egbie Uku'


class PasswordForm(BasePasswordForm):
    """Allows the user of the blog to change their password"""
    old_password = PasswordField('Old password', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
