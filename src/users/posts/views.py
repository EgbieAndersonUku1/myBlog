from flask import Blueprint, render_template, request, url_for, redirect, abort

from users.posts.form import PostForm
from users.decorators import login_required
from users.users.users import UserBlog
from users.utils.generator.msg import Message

posts_app = Blueprint('posts_app', __name__)


@posts_app.route('/post/new/<blog_id>', methods=['GET', 'POST'])
@login_required
def new_post(blog_id):
    """Takes a blog id and creates a new post within that blog"""

    form = PostForm()

    if form.validate_on_submit():
        blog = UserBlog()
        child_blog = blog.get_blog(blog_id)
        child_blog.new_post(form)

        Message.display_to_gui_screen("The post was created successfully")
        return redirect(url_for('posts_app.posts', blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id)


@posts_app.route('/posts/<blog_id>')
@login_required
def posts(blog_id):
    """Takes a blog id and returns all posts associated with that blog"""

    blog = UserBlog()
    child_blog = blog.get_blog(blog_id)

    if not child_blog:
       abort(404)
    return render_template("posts/posts.html", posts=child_blog.get_all_posts(), blog_id=blog_id)


@posts_app.route('/posts/edit/<blog_id>/<post_id>')
@login_required
def edit(blog_id, post_id):
    """"""

    blog = UserBlog()
    child_blog = blog.get_blog(blog_id)

    #ToDo
    # Add the method to edit post here
    return redirect(url_for("posts_app.posts", blog_id=blog_id))


@posts_app.route('/posts/<blog_id>/<post_id>')
@login_required
def delete(blog_id, post_id):

    blog = UserBlog()
    child_blog = blog.get_blog(blog_id)
    child_blog.delete_post(post_id)

    Message.display_to_gui_screen("The post has successfully been deleted")
    return redirect(url_for("posts_app.posts", blog_id=blog_id))