from functools import wraps
from flask import request, redirect, url_for, abort
from users.utils.session.user_session import UserSession


def login_required(f):
    return _decorator(f, 'username', True)


def admin_required(f):
    return _decorator(f, 'admin')


def _decorator(f, key, logging_required=False):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if UserSession.get_value_by_key(key) is None:
            if logging_required:
                return redirect(url_for('login_app.login', next=request.url))
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
