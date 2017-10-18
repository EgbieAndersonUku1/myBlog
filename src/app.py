from flask import Flask
from flask_ckeditor import CKEditor

__author__ = 'Egbie Uku'

app = Flask(__name__)
ckeditor = CKEditor(app)

from users.admin.views import admin_app
from users.blogs.views import blogs_app
from users.posts.views import posts_app
from users.login.views import login_app


def create_app():
    app.secret_key = 'you will never guess'
    app.register_blueprint(admin_app)
    app.register_blueprint(blogs_app)
    app.register_blueprint(posts_app)
    app.register_blueprint(login_app)
    return app