from flask_wtf import Form
from wtforms import PasswordField, validators
from flask_wtf.html5 import EmailField


class _BasePasswordForm(Form):
    """"""
    new_passwd = PasswordField('New password', validators=[validators.DataRequired(),
                                                           validators.Length(min=3, max=80),
                                                           validators.EqualTo('confirm')]
                               )
    confirm = PasswordField('Confirm new password')


class ResetForgottenPassword(Form):
    """This class triggers the process needed for the user to reset their password"""
    email = EmailField('Email address', validators=[validators.DataRequired()])


class ForgottenPasswordForm(_BasePasswordForm):
    """This class allows the user change their existing password by entering a new one"""
    pass


class NewPasswordForm(_BasePasswordForm):
    """This class allows the user to create a new password"""
    old_passwd = PasswordField('Old password', validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
