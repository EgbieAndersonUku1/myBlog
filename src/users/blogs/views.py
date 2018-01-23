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
    return render_template('blogs/blogs.html', blogs=blog.get_all_blogs())


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

    if not child_blog:
        abort(404)

    form = BlogForm(obj=child_blog)

    if form.validate_on_submit():

        blog.update_blog(blog_id, data={"title": form.title.data, "description": form.description.data})
        Message.display_to_gui_screen("You have successfully updated your blog")

    return render_template("blogs/blog_edit.html", form=form, child_blog=child_blog)


@blogs_app.route('/blogs/<blog_id>')
def my_blog(blog_id):
    """Takes a blog id and returns that blog"""
    return redirect(url_for('blogs_app.blog_posts', blog_id=blog_id))


@blogs_app.route('/blogs/blog/id/<blog_id>/posts')
def blog_posts(blog_id):
    """Takes an id belonging to a blog and returns all post that associated with that blog"""
    return redirect(url_for("posts_app.posts", blog_id=blog_id))


@blogs_app.route('/blogs/delete/<blog_id>', methods=['GET', 'POST'])
def blog_delete(blog_id):
    """Takes a blog_id and deletes that blog"""

    blog = UserBlog()
    blog.delete_blog(blog_id)
    Message.display_to_gui_screen("The blog was deleted successfully")
    return redirect(url_for("blogs_app.blog"))