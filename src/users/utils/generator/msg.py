from flask import flash

class Message(object):

    @staticmethod
    def display(msg):
        flash(msg)