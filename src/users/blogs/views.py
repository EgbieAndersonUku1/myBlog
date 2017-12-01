from flask import Blueprint, render_template

from users.blogs.form import BlogForm
from users.decorators import login_required


blogs_app = Blueprint('blogs_app', __name__)


@blogs_app.route('/')
@blogs_app.route('/blog/new')
@login_required
def blog():

    form = BlogForm()
    return render_template('blogs/blog.html', form=form)