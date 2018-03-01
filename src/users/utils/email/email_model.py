##############################################################################
# EmailGmail: Allows the user to send any email via Gmail .
# This Class takes the the source address (user's gmail address),
# the recipient address, the subject, text to send in html and in plaintext
# and the user's gmail password
#
# Sending Emails
# ==============
#
#  But in order to begin sending emails the 'less secure app'
#  located in the settings of gmail must be turned on.
#  Once this done the user will be able to send emails to any account
#
# Egbie Uku
#
###############################################################################

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from users.utils.email.base_email import BaseEmail


class EmailGmail(BaseEmail):
    """Email:(class) -> Allows the user to send an email to another
       email address to another using Gmail services.
    """

    def __init__(self, source_addr, receiver_addr, subject, body_html, body_txt, passwd):
        BaseEmail.__init__(self, source_addr, receiver_addr, subject, body_html, body_txt)
        self.passwd = passwd
        self._msg = self._construct_email()

    def _construct_email(self):
        """Creates the typical stuff associated with an email,
        e.g. sender address, receiver addrss, subject, body, etc.
        """
        # construct the email
        email_msg = MIMEMultipart('alternative')
        email_msg['Subject'] = self.subject
        email_msg['From'] = self.source_addr
        email_msg['To'] = self.receiver_addr

        text_part = MIMEText(self.body_text, 'plain')
        html_part = MIMEText(self.body_html, 'html')

        email_msg.attach(text_part)
        email_msg.attach(html_part)
        return email_msg

    def send_email(self):
        """send_email(None) -> return(dict or boolean)

        Sends an email address from one email to another.
        Returns True if the email was sent or returns a dict
        containing elements of the fields that were not sent.
        """
        conn = self._login()
        res = conn.sendmail(self.source_addr, self.receiver_addr, self._msg.as_string())
        conn.quit()
        return True if not res else res

    def _login(self):
        """Login into the email address"""

        conn = self._secure_and_connect()
        try:
            conn.login(self.source_addr, self.passwd)
        except ValueError:
            raise Exception('Failed to login, check username, password or the internet connection.')
        return conn

    def _secure_and_connect(self):
        """Creates a secure connection between the email addresses"""

        assert self.passwd, 'Password cannot be empty.'
        conn = smtplib.SMTP('smtp.gmail.com', 587)
        conn.ehlo()

        try:
            conn.starttls()  # Uses TLS to encrypt the connection.
        except:
            raise Exception('Failed to connect your system does not support TLS')
        else:
            conn.ehlo()
            return conn