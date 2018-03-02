from flask import Blueprint, render_template, redirect, url_for

from users.comments.form import CommentForm
from users.users.users import UserBlog
from users.users.users import User
from users.utils.security.user_session import UserSession

comment_app = Blueprint("comment_app", __name__, url_prefix="/comments")


@comment_app.route("/delete/<blog_id>/<post_id>/<comment_id>")
def delete_comment(blog_id, post_id, comment_id):
    """"""
    post, blog = None, UserBlog()
    child_blog = blog.get_blog(blog_id)

    if child_blog:
        post = child_blog.Post.get_post_by_id(post_id)
    if post:
        post.Comment.delete_comment(comment_id)

    return redirect(url_for("posts_app.post_permalink", blog_id=blog_id, post_id=post_id, comment_id=comment_id))


@comment_app.route("/edit/<user_id>/<blog_id>/<post_id>/<comment_id>")
def edit_comment(user_id, blog_id, post_id, comment_id):
    # ToDo
    # Write the function needed to edit comments.
    pass 