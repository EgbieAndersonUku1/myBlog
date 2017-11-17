from flask import Blueprint, render_template

from users.login.form import LoginForm
from users.utils.implementer.password_implementer import PasswordImplementer
from users.users.users import User

from users.utils.session.user_session import UserSession

login_app = Blueprint('login_app', __name__)


@login_app.route('/login')
def login():

    form = LoginForm()

    if form.validate_on_submit():
        if has_user_be_confirmed():
            user = User.get_by_username(UserSession.get_username())
            if user and PasswordImplementer.check_password(form.password, user.password):
                # redirect the user to go here
                pass

    return render_template("login/login.html", form=form)


def has_user_be_confirmed():
    """"""
    # Check the flask-cache to see whether the user has confirmed
    return True # This will be replaced with an actually flask-cache function