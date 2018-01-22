from flask import Blueprint, render_template, redirect, url_for, abort

from users.registration.form import RegistrationForm
from users.users.users import User

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Allows the user to register to the application from the GUI register page"""

    form, error = RegistrationForm(), False

    if form.validate_on_submit():
        user = User.extract_web_form(form)

        if not user.get_by_email(form.email.data):
            user.register()
            return redirect(url_for('registration_app.confirm_email'))

        error = 'The email address used is already in use'

    return render_template('registrations/register.html', form=form, error=error)


@registration_app.route('/confirm/<username>/<code>')
def confirm_registration(username, code):
    """"""

    if User.confirm_registration(username, code):
        return redirect(url_for('registration_app.confirmed_email', code=code))
    return abort(404)


@registration_app.route('/Confirmed/email/code_<code>_success')
def confirmed_email(code):
    return render_template('confirmations/confirmed_email.html')


@registration_app.route('/confirmEmail')
def confirm_email():
    return render_template('confirmations/confirm_email.html')
