from flask import Blueprint, redirect, url_for, request

from users.utils.security.user_session import UserSession

logout_app = Blueprint('logout_app', __name__)


@logout_app.route('/logout')
def logout():
    """logs the user out of the application"""

    UserSession.remove_username()
    UserSession.remove_value_by_key('admin')
    UserSession.remove_value_by_key('login_token')
    return redirect(request.referrer)