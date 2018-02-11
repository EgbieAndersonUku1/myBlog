from flask import Blueprint, render_template, request, redirect, url_for

from users.login.form import LoginForm
from users.users.users import User
from users.utils.security.user_session import UserSession
from users.utils.generator.msg import Message

login_app = Blueprint('login_app', __name__)


@login_app.route('/login', methods=['GET', 'POST'])
def login():
    """Allows the user to login to the application using the GUI"""

    form = LoginForm()

    _is_next_in_url()

    if UserSession.get_username():  # if user is already logged in redirect them to blog/post creation page
        return _redirect_user_to_blog_creation_page()
    elif form.validate_on_submit():

        user = User.get_account_by_username(form.username.data)

        if user:

            email_status = user.is_user_email_confirmed()

            if email_status == 'EMAIL_CONFIRMED':
                if user.login(password=form.password.data):
                    _add_username_email_and_admin_to_secure_user_session(user, admin='admin')
                    return _redirect_user_to_url_in_next_if_found_or_to_blog_creation_page()

                Message.display_to_gui_screen('Incorrect username and password!')
            else:
                Message.display_to_gui_screen(_get_account_status(email_status))

    return render_template("login/login.html", form=form)


def _is_next_in_url():
    """"""
    if request.method == 'GET' and request.args.get('next'):
        UserSession.add_next_url(request.args.get('next'))


def _add_username_email_and_admin_to_secure_user_session(user, admin):
    """Adds the username and admin name to the user's secure session"""

    UserSession.add_username(user.username)
    UserSession.add_value_to_session('email', user.email.lower())
    UserSession.add_value_to_session(admin, True)


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


def _get_account_status(confirmation_status):
    """Returns the appropriate status of the user's account"""

    return {
        'NOT_CONFIRMED': 'You need to confirm your email address before you can login',
        'ACCOUNT_NOT_FOUND': 'Incorrect password and username'
    }.get(confirmation_status)
