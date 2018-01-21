from flask import Blueprint, render_template, url_for, redirect, abort

from users.blogs.form import BlogForm
from users.decorators import login_required
from users.users.users import UserBlog
from users.utils.generator.msg import Message

blogs_app = Blueprint('blogs_app', __name__)


@blogs_app.route('/blogs', methods=['GET', 'POST'])
@login_required
def blog():

    blog = UserBlog()
    blogs = blog.get_all_blogs()

    return render_template('blogs/blogs.html', blogs=blogs)


@blogs_app.route('/blogs/create', methods=['GET', 'POST'])
@login_required
def blog_create():

    form = BlogForm()

    if form.validate_on_submit():
        blog = UserBlog()
        blog.create_blog(form)
        Message.display_to_gui_screen("A new blog was successfully created")
        return redirect(url_for("blogs_app.blog"))
    return render_template('blogs/blogs_creation_page.html', form=form)


@blogs_app.route('/blogs/edit/<blog_id>', methods=('GET', 'POST'))
def blog_edit(blog_id):
    """Takes a blog id and edits that blog"""

    blog = UserBlog()
    child_blog = blog.get_blog(blog_id)

    form = BlogForm()

    if not child_blog:
        abort(404)

    form = BlogForm(obj=child_blog)

    if form.validate_on_submit():

        blog_form = {
            "title": form.title.data,
            "description": form.description.data
        }
        blog.update_blog(blog_id, blog_form)
        Message.display_to_gui_screen("You have successfully updated your blog")

    return render_template("blogs/blog_edit.html", form=form, child_blog=child_blog)


@blogs_app.route('/blogs/delete/<blog_id>', methods=['GET', 'POST'])
def blog_delete(blog_id):
    """Takes a blog_id and deletes that blog"""

    blog = UserBlog()
    blog.delete_blog(blog_id)
    Message.display_to_gui_screen("The blog was deleted successfully")
    return redirect(url_for("blogs_app.blog"))
