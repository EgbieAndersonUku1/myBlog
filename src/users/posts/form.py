
from users.base.base_ckeditor import BaseCKEditorForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField


class PostForm(BaseCKEditorForm):

    image = FileField('Post image', validators=[FileAllowed(['png', 'jpeg', 'jpg', 'gif'],
                                                               'Only the file extension jpg, png, gif and jpeg are allowed')])
    category = SelectField('Choose blog to save post to', coerce=str)
