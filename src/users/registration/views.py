from flask import Blueprint, render_template, redirect, url_for, abort

from users.registration.form import RegistrationForm
from users.users.users import User
from users.utils.security.user_session import UserSession

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/', methods=['GET', 'POST'])
@registration_app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register user to the application from the GUI register page"""

    form, error = RegistrationForm(), False

    if UserSession.get_login_token():
        return redirect(url_for("blogs_app.my_blog"))
    elif form.validate_on_submit():
        user = User.extract_web_form(form)
        user.send_registration_code()
        return redirect(url_for('registration_app.confirm_email_page'))

    return render_template('registrations/register.html', form=form, error=error)


@registration_app.route('/email/confirm')
def confirm_email_page():
    return render_template('confirmations/confirm_email.html')


@registration_app.route('/confirm/<username>/<code>')
def confirm_registration(username, code):
    """"""
    user = User.get_account_by_username(username)

    if user and user.is_registration_code_valid(code):
        user.register()
        return redirect(url_for('registration_app.confirmed_email_page'))
    abort(404)


@registration_app.route('/confirmed/email')
def confirmed_email_page():
    return render_template('confirmations/confirmed_email.html')
