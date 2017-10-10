from flask import Blueprint, render_template

admin_app = Blueprint('admin_app', __name__)


@admin_app.route('/admin')
def admin():
    return render_template('admin/overview.html')


@admin_app.route('/admin/profile')
def admin_profile():
    return render_template('admin/profile.html')


@admin_app.route('/admin/page/blogs')
def admin_blogs():
    return render_template('admin/blogs.html')


@admin_app.route('/admin/page/posts')
def admin_posts():
    return render_template('admin/posts.html')


@admin_app.route('/admin/history')
def admin_history():
    return render_template('admin/history.html')
