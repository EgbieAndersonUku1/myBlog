from flask import Blueprint, render_template, redirect, url_for, abort

from users.registration.form import RegistrationForm
from users.users.users import User

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register user to the  application from the GUI register page"""

    form, error = RegistrationForm(), False

    if form.validate_on_submit():

        user = User.extract_web_form(form)
        user.register()
        return redirect(url_for('registration_app.confirm_email'))

    return render_template('registrations/register.html', form=form, error=error)


@registration_app.route('/confirm/<username>/<code>')
def confirm_registration(username, code):
    """"""

    if User.verify_registration_code(username, code):
        return redirect(url_for('registration_app.confirmed_email', code=code))
    abort(404)


@registration_app.route('/confirmed/email/code_<code>_success')
def confirmed_email(code):
    return render_template('confirmations/confirmed_email.html')


@registration_app.route('/email/confirm')
def confirm_email():
    return render_template('confirmations/confirm_email.html')
