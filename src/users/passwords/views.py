from flask import Blueprint, url_for, redirect, render_template, abort

from users.passwords.form import ForgottenPasswordForm, NewPasswordForm, ResetForgottenPassword
from users.users.users import User
from users.utils.implementer.password_implementer import PasswordImplementer
from users.utils.generator.msg import Message

password_app = Blueprint('password_app', __name__)


@password_app.route('/forgottenPassword', methods=('GET', 'POST'))
def forgotten_password():

    form = ResetForgottenPassword()

    if form.validate_on_submit():

        user = User.get_by_email(form.email.data)

        if user:
           user.reset_forgotten_password()

        Message.display_to_gui_screen("""A reset password code link has been sent to your email. 
                                         Click on the link to reset your password
                                      """)
    return render_template('password/forgotten_password.html', form=form)


@password_app.route('/password/reset/<username>/<code>', methods=('GET', 'POST'))
def reset_password(username, code):
    """"""

    form = ForgottenPasswordForm()
    user = User.get_by_username(username)

    if user and user.configuration_codes.get('forgotten_password_code') != code:
        abort(404)
    elif form.validate_on_submit():

        user.configuration_codes.pop('forgotten_password_code')
        user.password = PasswordImplementer.hash_password(form.new_passwd.data)
        user.update()
        Message.display_to_gui_screen('You have successfully changed your password.')
        return redirect(url_for('login_app.login'))

    return render_template('/password/reset_password.html', form=form, username=username, code=code)