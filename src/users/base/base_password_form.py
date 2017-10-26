from flask_wtf import Form
from wtforms import PasswordField, validators


class BasePasswordForm(Form):

    new_password = PasswordField('New password', validators=[validators.DataRequired(),
                                                                                                                 validators.Length(min=3, max=80),
                                                                                                                validators.EqualTo('confirm')
                                                                                                                ]
                                                                )
    confirm = PasswordField('Confirm new password')


