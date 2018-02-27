from flask import Blueprint, url_for, redirect, render_template, abort

from users.passwords.form import ForgottenPasswordForm, NewPasswordForm, ResetForgottenPassword
from users.users.users import User
from users.utils.security.user_session import UserSession
from users.utils.generator.msg import Message

password_app = Blueprint('password_app', __name__)


@password_app.route('/forgottenPassword', methods=('GET', 'POST'))
def forgotten_password():

    form = ResetForgottenPassword()

    if UserSession.get_login_token():
        return redirect(url_for("blogs_app.blog"))
    elif form.validate_on_submit():

        user = User.get_account_by_email(form.email.data)

        if user:
            user.send_forgotten_password_code()
            return redirect(url_for('password_app.reset_password_msg'))
    return render_template('password/forgotten_password.html', form=form)


@password_app.route("/Message/sent")
def reset_password_msg():
    return render_template("password/forgotten_password_msg.html")


@password_app.route('/password/reset/<username>/<code>', methods=('GET', 'POST'))
def reset_password(username, code):
    """Allows the user to reset their previous password"""

    form = ForgottenPasswordForm()
    user = User.get_account_by_username(username)

    if not user and not user.verify_forgotten_password_code(code):
       assert user or abort(404)

    elif form.validate_on_submit():
        user.reset_forgotten_password(new_password=form.new_passwd.data)
        return redirect(url_for('password_app.password_changed'))

    return render_template('/password/reset_password.html', form=form, username=username, code=code)


@password_app.route("/password-changed")
def password_changed():
    """"""
    return render_template("/password/password_changed_page.html")