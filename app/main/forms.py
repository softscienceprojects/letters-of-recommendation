from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from app.models import User, Post
import re


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Regexp('[0-9a-zA-Z]')])
    profile = TextAreaField('about me', validators=[Length(min=0, max=300)])
    submit = SubmitField('submit')

    def __init__(self, original_username, *args, **kwargs):
        #inherit the original functionality from FlaskForm
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')
            if re.search('[^0-9a-zA-Z]', username.data):
                raise ValidationError('Username can only contains letters and numbers')
    

class PostForm(FlaskForm):
    title = StringField('title: ', validators=[DataRequired()], render_kw={'placeholder': 'title'})
    body = TextAreaField('write: ', validators=[DataRequired()], render_kw={'placeholder': 'write...'})
    submit = SubmitField('submit')

    def __init__(self, original_title=None, original_post=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if original_title:
            self.original_title = original_title
        if original_post:
            self.original_post = original_post


