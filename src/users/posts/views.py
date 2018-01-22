from flask import Blueprint, render_template, request, url_for, redirect

from users.posts.form import PostForm
from users.decorators import login_required
from users.users.users import UserBlog

posts_app = Blueprint('posts_app', __name__)


@posts_app.route('/post/new/<blog_id>', methods=['GET', 'POST'])
@login_required
def new_post(blog_id):

    form = PostForm()

    if form.validate_on_submit():
        blog = UserBlog()
        child_blog = blog.get_blog(blog_id)
        child_blog.new_post(form)

    return render_template('posts/new_post.html', form=form, blog_id=blog_id)


@posts_app.route('/posts/<blog_id>')
@login_required
def posts(blog_id):

    blog = UserBlog()
    child_blog = blog.get_blog(blog_id)
    posts = child_blog.get_all_posts()

    print(posts)

    return render_template("posts/posts.html", posts=posts)