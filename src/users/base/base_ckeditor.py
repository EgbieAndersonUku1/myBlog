from flask_wtf import Form
from wtforms import StringField, validators


class BaseCKEditorForm(Form):
    """The base form that enables Ck editor to be generated"""

    title = StringField('Title', validators=[validators.DataRequired()])

