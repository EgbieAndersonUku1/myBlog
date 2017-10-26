from flask import Blueprint, render_template

from users.registration.form import RegistrationForm
from users.utils.implementer.password_implementer import PasswordImplementer
from users.users.users import User
from users.utils.generator.id_generator import gen_id as gen_code

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register', methods=('GET', 'POST'))
def register_user():
    """Allows the user to register to the application from the GUI register page"""

    form = RegistrationForm()

    if form.validate_on_submit():

        user = _extract_user_details_from_web_form(form)
        user.configuration_codes['verification_code'] = gen_code()
        user.email_user_account_verification_code()
        user.save()
        # will add a page re-direct here after I the details built the database saver

    return render_template('registrations/register.html', form=form)


def _extract_user_details_from_web_form(form):
    """_extract_user_details_from_web_form(<form object>) returns <user object>

    Take a web form and extracts all the users details. Returns an
    object containing the user's extracted details.

    :param
        'form`: The web form containing the user details'
    :returns
        `user`: Returns a user object
    """
    return User(
                form.first_name.data, form.last_name.data,
                form.username.data, form.email.data,
                form.author_name.data,
                PasswordImplementer.hash_password(form.password.data)
                )

