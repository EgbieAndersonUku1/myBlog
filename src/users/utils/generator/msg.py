from flask import flash


class Message(object):

    @staticmethod
    def display_to_gui_screen(msg):
        flash(msg)