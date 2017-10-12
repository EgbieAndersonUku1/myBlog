from flask_wtf.file import FileField, FileAllowed
from wtforms.widgets import TextArea
from wtforms import validators, StringField

from users.base_profile_form import BaseProfileForm

__author__ = 'Egbie Uku'


class ProfileForm(BaseProfileForm):
        profile_image = FileField('Upload profile image', validators=[FileAllowed(["jpg", "jpeg", "png", "gif"]),
                                                              "Only files with extenstion jpg, jpeg, png or gif are allowed"])

        bio = StringField('Bio', widget=TextArea(),
                          validators=[validators.Length(max=255)])
