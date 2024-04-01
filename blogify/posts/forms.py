from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
"""WTF forms for posting and updating on blogify"""


class PostForm(FlaskForm):
    """Form used to post blogs on blogify"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    """Form to commment on blogify"""
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Enter')