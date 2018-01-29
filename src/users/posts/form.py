from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField, FileAllowed

from users.base.base_ckeditor import BaseCKEditorForm
from wtforms import validators


class PostForm(BaseCKEditorForm):

    post = CKEditorField('body', validators=[validators.DataRequired()])
    image = FileField('Post image', validators=[FileAllowed(['png', 'jpeg', 'jpg', 'gif'],
                                                               'Only the file extension jpg, png, gif and jpeg are allowed')])
