from users.base.base_ckeditor import BaseCKEditorForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, validators


class BlogForm(BaseCKEditorForm):
    blog_name = StringField("Blog name", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    description = CKEditorField('body', validators=[validators.DataRequired()])
