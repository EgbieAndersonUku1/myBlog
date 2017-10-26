from flask import Blueprint, render_template, session

from users.login.form import LoginForm
from users.utils.implementer.password_implementer import PasswordImplementer
from users.users.user import UsersDetails

login_app = Blueprint('login_app', __name__)


@login_app.route('/login')
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = UsersDetails.get_by_email(session.email)
        if user and PasswordImplementer.check_password(form.password, user.password):
            # redirect the user somewhere
            pass

    return render_template("login/login.html", form=form)