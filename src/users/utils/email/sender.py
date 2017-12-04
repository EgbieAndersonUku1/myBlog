from flask import render_template

from users.utils.credentials_reader import cred_reader
from users.utils.email.email_model import EmailGmail


__author__ = 'Egbie Uku'


def email_user_verification_code(receipent_addr, username, verification_code):
    """_email_user_verification_code(str, obj, obj) -> returns None

    Sends a verification code to the user's email address.

    :param
        `recipient_addr`: The email address of the recipient
        `user`: The object model containing all the user's information
        `username`: The username belonging to the user
        `verification_code`: The verification code that to be verified by the user
    """
    _email_user_helper(receipent_addr, username, verification_code,
                       subject="Re: Please verify your email address",
                       body_html_path="mail/register/register.html",
                       body_text_path="mail/register/register.txt",
                       )


def email_user_forgotten_password_verification_code(receipent_addr, username, verification_code):
    """"""
    _email_user_helper(receipent_addr, username, verification_code,
                       subject="Re: Reset forgotten password",
                       body_html_path="mail/password/forgotten_password.html",
                       body_text_path="mail/password/forgotten_password.txt",
                       )


def _email_user_helper(receipent_addr, username, verification_code, **kwargs):
    """"""

    """_send_email_verification_code(str, obj, obj) -> returns None

       Sends a verification code to the user's email address.

       :param
           `recipient_addr`: The email address of the recipient
           `user`: The object model containing all the user's information
           `username`: The username belonging to the user
           `verification_code`: The verification code that to be verified by the user
       """

    email = _FlaskEmailer(receipent_addr,
                          subject=kwargs['subject'],
                          body_html_path=kwargs['body_html_path'],
                          body_text_path=kwargs['body_text_path'],
                          username=username,
                          verification_code=verification_code)
    email.send_email()


class _FlaskEmailer(object):
    """This class allows the email message to be rendered using a Flask HTML template
       before finally been sent to its destination.
    """

    def __init__(self, receiptant_addr, subject, body_html_path, body_text_path, username, verification_code):

        self._receiptant_addr = receiptant_addr
        self._subject = subject
        self._body_html = render_template(body_html_path, username=username, verification_code=verification_code)
        self._body_text = render_template(body_text_path, username=username, verification_code=verification_code)

    def send_email(self):
        """Sends the email message to the receiver"""

        email = self._construct_email_body(self._receiptant_addr, self._subject)
        email.send_email()

    def _construct_email_body(self, receiver_addr, subject):
        """_construct_email_body(str, str) -> returns class instance

        Constructs the body of the email, e.g.the subject, receiver and src email address, etc
        """

        src_addr, password = cred_reader()
        return EmailGmail(src_addr, receiver_addr, subject, self._body_html, self._body_text, password)
