from flask_wtf import Form
from wtforms import PasswordField, validators
from flask_wtf.html5 import EmailField


class _BasePasswordForm(Form):
    new_password = PasswordField('New password', validators=[validators.DataRequired(),
                                                             validators.Length(min=3, max=80),
                                                             validators.EqualTo('confirm')]
                                 )
    confirm = PasswordField('Confirm new password')


class ResetForgottenPassword(Form):
    """"""
    email = EmailField('Email address', validators=[validators.DataRequired()])


class ForgottenPasswordForm(_BasePasswordForm):
    """"""
    pass


class NewPasswordForm(_BasePasswordForm):
    """"""
    old_password = PasswordField('Old password', validators=[validators.DataRequired(),
                                                             validators.Length(min=3, max=80)
                                                             ]
                                 )
