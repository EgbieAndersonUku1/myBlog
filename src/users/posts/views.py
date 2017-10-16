from flask import Blueprint, render_template

from users.posts.form import PostForm

posts_app = Blueprint('posts_app', __name__)


@posts_app.route('/post/new', methods=('GET', 'POST'))
def new_post():

    form = PostForm()
    form.category.choices = [('blog Id', 'Dummy blog 1'), ('blog id 2', 'Dummy blog 2'), ('blog id 3', 'Dummy blog 3')] # replace this with data from database
    return render_template('posts/new_post.html', form=form)