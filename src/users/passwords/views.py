from flask import Blueprint, url_for, redirect, render_template, abort

from users.passwords.form import ForgottenPasswordForm, NewPasswordForm, ResetForgottenPassword
from users.users.users import User
from users.utils.security.user_session import UserSession
from users.utils.generator.msg import Message

password_app = Blueprint('password_app', __name__)


@password_app.route('/forgottenPassword', methods=('GET', 'POST'))
def forgotten_password():

    form = ResetForgottenPassword()

    if UserSession.get_username():
        return redirect(url_for("blogs_app.blog"))
    elif form.validate_on_submit():

        user = User.get_by_email(form.email.data)

        if user:
            user.reset_forgotten_password()
            return redirect(url_for('password_app.reset_password_msg'))
    return render_template('password/forgotten_password.html', form=form)


@password_app.route("/Message/sent")
def reset_password_msg():
    return render_template("password/forgotten_password_msg.html")


@password_app.route('/password/reset/<username>/<code>', methods=('GET', 'POST'))
def reset_password(username, code):
    """"""

    form = ForgottenPasswordForm()
    user = User.verify_forgotten_password_code(username, code)

    assert user or abort(404)

    if form.validate_on_submit():
        user.update_forgotten_password(form)
        Message.display_to_gui_screen('You have successfully changed your password.')
        return redirect(url_for('login_app.login'))

    return render_template('/password/reset_password.html', form=form, username=username, code=code)