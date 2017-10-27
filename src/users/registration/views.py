from flask import Blueprint, render_template, redirect

from users.registration.form import RegistrationForm
from users.users.users import User

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register', methods=('GET', 'POST'))
def register_user():
    """Allows the user to register to the application from the GUI register page"""

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User.extract_web_form(form)
        user.gen_user_verification_code()
        user.email_user_account_verification_code()
        user.save()
        return redirect('blogs/creation.html')

    return render_template('registrations/register.html', form=form)


