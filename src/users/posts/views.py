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
        child_blog.Post.create_new_post(form.title.data, form.post.data)

        Message.display_to_gui_screen("The post was created successfully")
        return redirect(url_for('posts_app.posts', blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id, edit_post=False)


@posts_app.route('/<blog_id>')
@login_required
def posts(blog_id):
    """Takes a blog id and returns all posts associated with that blog"""

    child_blog = _get_blog(blog_id)

    if not child_blog:
        abort(404)
    return render_template("posts/posts.html", posts=child_blog.Post.get_all_posts(),
                           blog_id=blog_id, blog_name=child_blog.blog_name)


@posts_app.route('/edit/<blog_id>/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(blog_id, post_id):
    """"""

    child_blog = _get_blog(blog_id)

    if not child_blog:
        abort(404)

    post = child_blog.Post.get_post_by_id(post_id)
    print(post)
    form = PostForm(obj=post)

    if form.validate_on_submit():

        data = _get_updated_data(form, post)

        if data:
            print(data)
            post.update_post(data)
            Message.display_to_gui_screen("You post has successfully been updated.")
            return redirect(url_for("posts_app.posts", blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id, post_id=post_id, edit_post=True)


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


def _get_updated_data(form, post):
    """_get_updated_data(form_obj, blog_obj) -> return dict

    Checks if the user has updated their data. If the data has
    been updated returns only the updated data otherwise returns
    an empty dictionary.
    """

    data = {}

    if form.title.data != post.title:
        data.update({"title": form.title.data})
    if form.post.data != post.post:
        data.update({"post": form.post.data})
    return data