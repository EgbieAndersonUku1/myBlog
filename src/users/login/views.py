from flask import Blueprint, render_template, request, redirect, url_for

from users.login.form import LoginForm
from users.users.users import User
from users.utils.security.user_session import UserSession
from users.utils.generator.msg import Message

login_app = Blueprint('login_app', __name__)


@login_app.route('/login', methods=['GET', 'POST'])
def login():
    """Allows the user to login to the application using the GUI"""

    form, error = LoginForm(), False

    _is_next_in_url()

    if UserSession.get_login_token():
        return _redirect_user_to_blog_creation_page()

    elif form.validate_on_submit():

        user = User.get_account_by_username(username=form.username.data)

        if user:
            email_status = user.get_email_confirmed_status()

            if email_status == 'EMAIL_CONFIRMED':

                if user.is_login_valid(password=form.password.data):
                    user.login()
                    return _redirect_user_to_url_in_next_if_found_or_to_blog_creation_page()

                error = _display_error_msg()

            else:
                error = _display_error_msg(email_status)
        else:
            error = _display_error_msg()

    return render_template("login/login.html", form=form, error=error)


def _display_error_msg(error="Incorrect username and password"):
    """"""
    Message.display_to_gui_screen(error)
    return True


def _is_next_in_url():
    """"""
    if request.method == 'GET' and request.args.get('next'):
        UserSession.add_next_url(request.args.get('next'))


def _redirect_user_to_url_in_next_if_found_or_to_blog_creation_page():
    """"""

    if UserSession.get_value_by_key('next'):
        next = UserSession.get_value_by_key('next')
        UserSession.remove_next_url()
        return redirect(next)
    return _redirect_user_to_blog_creation_page()


def _redirect_user_to_blog_creation_page():
    """Redirects the user to the blog creation page"""
    return redirect(url_for('blogs_app.blog'))