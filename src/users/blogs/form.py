from users.base.base_ckeditor import BaseCKEditorForm
from wtforms import StringField, validators


class BlogForm(BaseCKEditorForm):
    name = StringField("Blog name", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])