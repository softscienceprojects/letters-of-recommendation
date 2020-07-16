from flask import request
from flask_wtf import FlaskForm, Form
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, FileField, SelectMultipleField, RadioField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Regexp
from wtforms.widgets import CheckboxInput, ListWidget
from app.models import User, Post
import re


class EditProfileForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Regexp('[0-9a-zA-Z]')])
    profile = TextAreaField('about me', validators=[Length(min=0, max=300)])
    profile_picture = FileField('profile picture')
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
    

class SelectHeroPartial(Form):
    selectHero = RadioField("Select hero image: ", choices = [1,2,3])

class PostForm(FlaskForm):
    title = StringField('title: ', validators=[DataRequired()], render_kw={'placeholder': 'title'})
    images = MultipleFileField('images: ')
    selectHeroList = RadioField("Select hero image: ") #FieldList(FormField(SelectHeroPartial))
    removeImages = SelectMultipleField("Remove this image from post: ", widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    body = TextAreaField('write: ', validators=[DataRequired()], render_kw={'placeholder': 'write...'})
    tags = StringField('tags: ', render_kw={'placeholder': 'tag/s comma separated'})
    submit = SubmitField('save post')

    def __init__(self, original_title=None, original_post=None, original_tags=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if original_title:
            self.original_title = original_title
        if original_post:
            self.original_post = original_post
        if original_tags:
            self.original_tags = original_tags


class ImageForm(FlaskForm):
    images = MultipleFileField('upload images (jpg, gif, png only)')
    submit = SubmitField('submit')

    # def __init__(self, original_username, *args, **kwargs):
    #     #inherit the original functionality from FlaskForm
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.original_username = original_username



class CommentForm(FlaskForm):
    #datePosted = db.Column(db.DateTime, default=datetime.utcnow)
    #post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id')) current_user
    message = TextAreaField('write: ', validators=[DataRequired()], render_kw={'placeholder': 'write...'})
    submit = SubmitField('submit')

    def __init__(self, original_message=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        if original_message:
            self.original_message = original_message


