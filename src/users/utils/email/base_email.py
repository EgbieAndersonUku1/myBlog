__author__ = 'Egbie Uku'


class BaseEmail(object):
    """BaseEmail(class): The base that would be used for the Email classes"""

    def __init__(self, source_addr, receiver_addr, subject, body_html, body_text):
        self.source_addr = source_addr
        self.receiver_addr = receiver_addr
        self.subject = subject
        self.body_html = body_html
        self.body_text = body_text
        self._are_fields_empty()

    def _are_fields_empty(self):
        """Check whether the parameters are empty. Raises an exception if the
        fields are empty.
        """
        if not self.source_addr:
            raise Exception('The source address cannot be empty.')
        if not self.receiver_addr:
            raise Exception("The receiver address cannot be empty.")
        if not self.subject:
            self.subject = ''
        if not self.body_html and not self.body_text:
            raise Exception('The html and text cannot both be empty.')

    def set_source_addr(self, source_addr):
        """set a new source address"""
        self.source_addr = source_addr

    def set_receiver_addr(self, receiver_addr):
        """set a new receiver address"""
        self.receiver_addr = receiver_addr

    def set_subject(self, subject):
        """set a new subject"""
        self.subject = subject

    def set_body_html(self, body_html):
        """File:html. Set a new body for the html body"""
        self.body_html = body_html

    def set_body_text(self, body_text):
        """File:text. Set a new body for text body"""
        self.body_text = body_text
