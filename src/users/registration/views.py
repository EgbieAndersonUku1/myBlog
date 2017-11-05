from flask import Blueprint, render_template, redirect, url_for, abort

from users.registration.form import RegistrationForm
from users.login.views import login_app
from users.users.users import User


registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/confirm/<username>/<code>')
def confirm_registration(username, code):

    user = User.get_by_username(username)
    # Once I written the database retreive in User class the following lines will be uncommented
    # if user and user.configuration_codes['verification_code'] == code:
    #     user.parent_blog_created = True
    #     user.configuration_codes.pop('verification_code')
    #     # Save to database to go here
    #     # Save to Flask-Cache to go here
    #     return redirect('/blogs/blog_creation.html')
    return abort(404)

@registration_app.route('/register', methods=('GET', 'POST'))
def register_user():
    """Allows the user to register to the application from the GUI register page"""

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.extract_web_form(form)
        user.gen_user_verification_code()
        user.email_user_account_verification_code()
        user.save()
        return redirect(url_for('login_app.login'))
    return render_template('registrations/register.html', form=form)


