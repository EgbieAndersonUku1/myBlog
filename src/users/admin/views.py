from flask import Blueprint, render_template

from users.admin.forms.email_form import EmailForm
from users.admin.forms.password_form import PasswordForm
from users.admin.forms.username_form import UsernameForm
from users.admin.forms.profile_form import ProfileForm
from users.decorators import admin_required, login_required

admin_app = Blueprint('admin_app', __name__)

__author__ = 'Egbie Uku'


@admin_app.route('/admin')
@admin_required
@login_required
def admin():
    return render_template('admin/overview.html')



@admin_app.route('/admin/profile', methods=('GET', 'POST'))
@admin_required
@login_required
def admin_profile():

    password_form = PasswordForm()
    username_form = UsernameForm()
    email_form = EmailForm()
    profile_form = ProfileForm()

    # do something here
    return render_template('admin/profile.html',
                                               password_form=password_form,
                                               username_form=username_form,
                                               email_form=email_form,
                                               profile_form=profile_form
                                                )


@admin_app.route('/admin/page/blogs')
@admin_required
@login_required
def admin_blogs():
    return render_template('admin/blogs_creation_page.html')


@admin_app.route('/admin/page/posts')
@admin_required
@login_required
def admin_posts():
    return render_template('admin/posts.html')


@admin_app.route('/admin/history')
@admin_required
@login_required
def admin_history():
    return render_template('admin/history.html')
