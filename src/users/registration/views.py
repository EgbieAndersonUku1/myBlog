from flask import Blueprint, render_template

from users.registration.form import RegistrationForm

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register')
def register_user():

    form = RegistrationForm()
    return render_template('registrations/register.html', form=form)