from flask import session

__author__ = 'Egbie Uku'


class UserSession(object):
    """Stores or removes values from within the user's session"""

    @staticmethod
    def add_value_to_session(key, value):
        """"""
        session[key] = value

    @staticmethod
    def add_username(username):
        """Add a username to the register's session"""
        session['username'] = username.lower()

    @staticmethod
    def add_next_url(url):
        """Adds a URL to the register's session"""
        session['next'] = url

    @staticmethod
    def update(key, value):
        """
        Updates the values within the session.

        :param
            `key`: The key used to index the dictionary
            `value`: The value to update_db the key with.

        :return:
            None
        """
        session[key] = value.lower()

    @staticmethod
    def get_login_token():
        return UserSession.get_username()

    @staticmethod
    def get_username():
        """Returns the username from the register's session"""
        return session.get('username')

    @staticmethod
    def get_value_by_key(key):
        return session.get(key)

    @staticmethod
    def remove_value_by_key(key):
        """"""
        return UserSession._remove_from_session(key)

    @staticmethod
    def remove_username():
        """Removes the username from the register's session"""
        UserSession._remove_from_session('username')

    @staticmethod
    def remove_next_url():
        """Removes the url from the user's session"""
        return UserSession._remove_from_session('next')

    @staticmethod
    def _remove_from_session(val):
        """A helper function that additional functionality to methods
           by removing the values from the user's sessions"""
        try:
            return session.pop(val)
        except KeyError:
            pass