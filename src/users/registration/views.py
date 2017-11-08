from flask import Blueprint, render_template, redirect, url_for, abort, flash

from users.registration.form import RegistrationForm
from users.login.views import login_app
from users.users.users import User
from users.utils.generator.msg import Message

registration_app = Blueprint('registration_app', __name__)


@registration_app.route('/register', methods=('GET', 'POST'))
def register_user():
    """Allows the user to register to the application from the GUI register page"""

    form, registered = RegistrationForm(), False

    if form.validate_on_submit():
        user = User.extract_web_form(form)
        user.gen_user_verification_code()
        user.email_user_account_verification_code()
        user.save()
        registered = True
        Message.display('You have successful registered your account. '
                        'Please confirm your account using the link sent to your email')
    return render_template('registrations/register.html', form=form, registered=registered)


@registration_app.route('/confirm/<username>/<code>')
def confirm_registration(username, code):

    user = User.get_by_username(username)
    if user and user.configuration_codes['verification_code'] == code:
        user.parent_blog_created = True
        user.configuration_codes.pop('verification_code')
        #Todo
        # Save to database to go here
        # Save to Flask-Cache to go here for rendering
        return render_template('/confirmations/user_account.html')
    return abort(404)


@registration_app.route('/create/parent/blog')
def register_parent_blog():
    """The main parent blog will be registered here. From the parent blog all blogs can be created"""
    return render_template('/blogs/blog_creation.html')


