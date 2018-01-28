from flask import Blueprint, render_template, request, url_for, redirect, abort

from users.posts.form import PostForm
from users.decorators import login_required
from users.users.users import UserBlog
from users.utils.generator.msg import Message

posts_app = Blueprint('posts_app', __name__, url_prefix="/posts")


@posts_app.route('/new/<blog_id>', methods=['GET', 'POST'])
@login_required
def new_post(blog_id):
    """Takes a blog id and creates a new post within that blog"""

    form = PostForm()

    if form.validate_on_submit():

        child_blog = _get_blog(blog_id)
        child_blog.Post.create_new_post(form.title.data, form.description.data)

        Message.display_to_gui_screen("The post was created successfully")
        return redirect(url_for('posts_app.posts', blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id)


@posts_app.route('/<blog_id>')
@login_required
def posts(blog_id):
    """Takes a blog id and returns all posts associated with that blog"""

    child_blog = _get_blog(blog_id)

    if not child_blog:
        abort(404)
    return render_template("posts/posts.html", posts=child_blog.Post.get_all_posts(),
                           blog_id=blog_id, blog_name=child_blog.blog_name)


@posts_app.route('/edit/<blog_id>/<post_id>')
@login_required
def edit_(blog_id, post_id):
    """"""

    child_blog = _get_blog(blog_id)

    #ToDo
    # Add the method to edit post here
    return redirect(url_for("posts_app.posts", blog_id=blog_id))


@posts_app.route('/<blog_id>/<post_id>')
@login_required
def delete_post(blog_id, post_id):
    """"""

    child_blog = _get_blog(blog_id)
    child_blog.Post.delete_post(post_id)

    Message.display_to_gui_screen("The post has successfully been deleted")
    return redirect(url_for("posts_app.posts", blog_id=blog_id))


def _get_blog(blog_id):
    """"""
    blog = UserBlog()
    return blog.get_blog(blog_id)
