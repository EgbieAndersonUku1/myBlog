from flask import Flask

__author__ = 'Egbie Uku'

app = Flask(__name__)


from users.admin.views import admin_app


def create_app():
    app.secret_key = 'you will never guess'
    app.register_blueprint(admin_app)
    return app