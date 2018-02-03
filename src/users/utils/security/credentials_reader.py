import os
import dotenv

__author__ = 'Egbie Uku'


def cred_reader():
    """Returns the credentials for the user's gmail address"""

    cred_file = get_file()
    username = get_value(cred_file, 'GMAIL_USERNAME')
    password = get_value(cred_file, 'GMAIL_PASSWORD')
    return username, password


def get_file():
    """Returns the file path to user's gmail credential"""
    return os.path.join(os.getcwd(), 'gmail_credentials.env')


def get_value(cred_file, key):
    """Returns the username and password from the OS environment"""

    try:
        dotenv.load_dotenv(cred_file)
    except KeyError:
        print("Could not find the username and password for the gmail account")
    else:
        return os.environ.get(key)
