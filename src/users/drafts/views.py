from flask import Blueprint, render_template, url_for, redirect, abort

from users.utils.generator.msg import Message
from users.users.users import UserBlog
from users.posts.form import PostForm
from users.posts.views import get_updated_data

drafts_app = Blueprint("drafts_app", __name__, url_prefix="/drafts")


@drafts_app.route("/drafts/<blog_id>", methods=['GET', 'POST'])
def drafts(blog_id):
    """"""

    form = PostForm()

    if form.validate_on_submit():
        child_blog = _get_blog(blog_id)
        child_blog.Post.Draft.save(form)

        Message.display_to_gui_screen("The created post has been saved to draft section")
        return redirect(url_for('drafts_app.get_drafts', blog_id=blog_id))

    return render_template('posts/new_post.html', form=form, blog_id=blog_id)


@drafts_app.route("/<blog_id>/drafts/all", methods=['GET', 'POST'])
def get_drafts(blog_id):
    """"""

    child_blog = _get_blog(blog_id)
    drafts = child_blog.Post.Draft.get_all_draft_posts()
    return render_template("drafts/drafts.html", blog_id=blog_id, drafts=drafts, num_of_drafts=len(drafts))


@drafts_app.route('/view/<blog_id>/<draft_id>', methods=['GET', 'POST'])
def view(blog_id, draft_id):
    """"""
    child_blog = _get_blog(blog_id)
    edit_draft = True

    assert child_blog or abort(404)

    draft = child_blog.Post.Draft.get_draft_post(draft_id, to_class=True)

    form = PostForm(obj=draft)

    if form.validate_on_submit():

        draft_data = get_updated_data(form, draft)
        if draft_data:
            draft.update_draft(draft_data)
            Message.display_to_gui_screen("You post has successfully been updated.")
            return redirect(url_for("drafts_app.get_drafts", blog_id=blog_id))
    return render_template('posts/new_post.html', form=form, blog_id=blog_id, draft_id=draft_id, edit_post=False, edit_draft=edit_draft)


@drafts_app.route("/<blog_id>/<draft_id>/publish", methods=['GET', 'POST'])
def publish(blog_id, draft_id):
    """"""

    child_blog = _get_blog(blog_id)
    draft_form = child_blog.Post.Draft.get_draft_post(draft_id)
    child_blog.Post.create_new_post(draft_form.get('title'), draft_form.get('post'))
    child_blog.Post.Draft.delete_draft(draft_id)

    Message.display_to_gui_screen("The draft with the title '{}' has been published.".format(draft_form.get('title')))
    return redirect(url_for('drafts_app.get_drafts', blog_id=blog_id))


@drafts_app.route("/delete/<blog_id>/<draft_id>")
def delete_draft(blog_id, draft_id):

    child_blog = _get_blog(blog_id)
    child_blog.Post.Draft.delete_draft(draft_id)

    Message.display_to_gui_screen("The draft post has been deleted.")
    return redirect(url_for('drafts_app.get_drafts', blog_id=blog_id))


def _get_blog(blog_id):
    """"""
    blog = UserBlog()
    return blog.get_blog(blog_id)