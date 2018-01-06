import time
from flask import Flask
from flask_caching import Cache
from flask_ckeditor import CKEditor
from users.records.database.database import Database


__author__ = 'Egbie Uku'

app = Flask(__name__)

ckeditor  = CKEditor(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) # will change to a memcached
cache.init_app(app)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

from users.admin.views import admin_app
from users.blogs.views import blogs_app
from users.posts.views import posts_app
from users.login.views import login_app
from users.registration.views import registration_app
from users.logout.views import logout_app
from users.passwords.views import password_app


@app.before_first_request
def init_db():
   Database.db_init()


def create_app():

    app.config.from_pyfile("settings.py")


    app.register_blueprint(admin_app)
    app.register_blueprint(blogs_app)
    app.register_blueprint(posts_app)
    app.register_blueprint(login_app)
    app.register_blueprint(registration_app)
    app.register_blueprint(password_app)
    app.register_blueprint(logout_app)


    return app