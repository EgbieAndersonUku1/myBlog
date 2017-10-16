from flask_wtf import Form
from flask_ckeditor import CKEditorField
from wtforms import SelectField, StringField, validators


class PostForm(Form):
    """The post form"""

    title = StringField('Title', validators=[validators.DataRequired()])
    post = CKEditorField('Post', validators=[ validators.DataRequired()])
    category = SelectField('Choose blog to save post to', coerce=str)