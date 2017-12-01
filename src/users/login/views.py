from flask import Blueprint, render_template, request, redirect, url_for

from users.login.form import LoginForm
from users.utils.implementer.password_implementer import PasswordImplementer
from users.users.users import User
from users.utils.session.user_session import UserSession

login_app = Blueprint('login_app', __name__)


@login_app.route('/login', methods=('GET', 'POST'))
def login():
    """Allows the user to login to the application using the GUI"""

    form, error = LoginForm(), ''

    _is_next_in_url()

    if UserSession.get_username():  # if user is already logged in redirect them to blog/post creation page
        return _redirect_user_to_blog_creation_page()
    if form.validate_on_submit():
        if _has_user_be_confirmed():

            user = User.get_by_username(form.username.data)

            if user and PasswordImplementer.check_password(form.password.data, user.password):
                UserSession.add_username(user.username)
                UserSession.add_value_to_session('admin', True)
                return _redirect_user_to_url_in_next_if_found_or_to_blog_creation_page()
            error = 'Incorrect username and password!'

    return render_template("login/login.html", form=form, error=error)


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
    """"""
    return redirect(url_for('blogs_app.blog'))


def _has_user_be_confirmed():
    """"""
    # Check the flask-cache to see whether the user has confirmed
    return True  # This will be replaced with an actually flask-cache function
