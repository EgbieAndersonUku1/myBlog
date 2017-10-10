from flask import Flask


app = Flask(__name__)

from users.admin.views import admin_app


def create_app():

    app.register_blueprint(admin_app)
    return app