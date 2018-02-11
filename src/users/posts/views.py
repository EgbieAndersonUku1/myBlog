from flask import Blueprint, render_template, url_for, redirect, abort

from users.posts.form import PostForm
from users.decorators import login_required
from users.users.users import UserBlog
from users.utils.generator.msg import Message
from users.utils.generator.date_generator import time_now
from users.comments.form import CommentForm

posts_app = Blueprint('posts_app', __name__, url_prefix="/posts")


@posts_app.route('/new/<blog_id>', methods=['GET', 'POST'])
@login_required
def new_post(blog_id):
    """Takes a blog id and creates a new post within that blog"""

    form = PostForm()
    edit_draft = False

    if form.validate_on_submit():

        child_blog = _get_blog(blog_id)
        child_blog.Post.create_new_post(form.title.data, form.post.data)

        Message.display_to_gui_screen("The post was created successfully")
        return redirect(url_for('posts_app.posts', blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id, edit_post=False, edit_draft=edit_draft)


@posts_app.route('/<blog_id>')
@login_required
def posts(blog_id):
    """Takes a blog id and returns all posts associated with that blog"""

    child_blog = _get_blog(blog_id)

    assert child_blog or abort(404)
    return render_template("posts/posts.html", posts=child_blog.Post.get_all_posts(),
                           blog_id=blog_id, blog_name=child_blog.blog_name)


@posts_app.route('/edit/<blog_id>/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(blog_id, post_id):
    """"""

    child_blog = _get_blog(blog_id)
    edit_draft = False

    assert child_blog or abort(404)

    post = child_blog.Post.get_post_by_id(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():

        post_data = get_updated_data(form, post)

        if post_data:
            post.update_post(post_data)
            Message.display_to_gui_screen("You post has successfully been updated.")
            return redirect(url_for("posts_app.posts", blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id, post_id=post_id,
                           edit_post=True, edit_draft=edit_draft)


@posts_app.route('/<blog_id>/<post_id>')
@login_required
def delete_post(blog_id, post_id):
    """"""

    child_blog = _get_blog(blog_id)
    child_blog.Post.delete_post(post_id)

    Message.display_to_gui_screen("The post has successfully been deleted")
    return redirect(url_for("posts_app.posts", blog_id=blog_id))


@posts_app.route("/mode/preview/<blog_id>", methods=['GET', 'POST'])
@login_required
def post_preview(blog_id):
    """Allows the user to preview a post before it is published"""

    form = PostForm()

    if form.validate_on_submit():
        return render_template("posts/post_preview.html", form=form, date=time_now())
    return redirect(url_for("posts_app.new_post", blog_id=blog_id))



@posts_app.route("/permalink/<blog_id>/<post_id>", methods=['GET', 'POST'])
def post_permalink(blog_id, post_id):
    """"""
    form = CommentForm()

    child_blog = _get_blog(blog_id)

    post = child_blog.Post.get_post_by_id(post_id)

    if form.validate_on_submit():
        post.Comment.save_comment(comment=form.comment.data)
        return redirect(url_for("posts_app.post_permalink", blog_id=blog_id, post_id=post_id))

    return render_template("posts/post_permalink.html", form=form, post=post)



def _get_blog(blog_id):
    """"""
    blog = UserBlog()
    return blog.get_blog(blog_id)


def get_updated_data(form, post_obj):
    """get_updated_data(form_obj, post_obj) -> return dict

    Checks if the user has updated their data. If the data has
    been updated returns only the updated data otherwise returns
    an empty dictionary.
    """

    data = {}

    if form.title.data != post_obj.title:
        data.update({"title": form.title.data})
    if form.post.data != post_obj.post:
        data.update({"post": form.post.data})
    return data