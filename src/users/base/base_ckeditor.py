from flask_wtf import Form
from flask_ckeditor import CKEditorField
from wtforms import StringField, validators


class BaseCKEditorForm(Form):
    """The base form that enables Ck editor to be generated"""

    title = StringField('Title', validators=[validators.DataRequired()])
    description = CKEditorField('body', validators=[validators.DataRequired()])
