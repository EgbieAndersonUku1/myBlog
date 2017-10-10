from flask import Blueprint, render_template

blogs_app = Blueprint('blogs_app', __name__)


@blogs_app.route('/')
def blog():
    return render_template('index.html')