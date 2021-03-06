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
    profile_picture = FileField('choose profile picture:')
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
    

# class SelectHeroPartial(Form):
#     selectHero = RadioField("Select hero image: ", choices = [1,2,3])

class PostHero(FlaskForm):
    selectHeroList = RadioField("Select hero image: ") #FieldList(FormField(SelectHeroPartial))
    submit = SubmitField('set image')

    def __init__(self, *args, **kwargs):
        super(PostHero, self).__init__(*args, **kwargs)


class PostForm(FlaskForm):
    title = StringField('title: ', validators=[DataRequired()], render_kw={'placeholder': 'title'})
    intro = StringField('intro: ', render_kw={'placeholder': 'intro...'})
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
    images = MultipleFileField('select images (jpg, gif, png only)')
    submit = SubmitField('submit')

    # def __init__(self, original_username, *args, **kwargs):
    #     #inherit the original functionality from FlaskForm
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     self.original_username = original_username

class ImageSlideshowForm(FlaskForm):
    image_options = SelectMultipleField("Choose images for slideshow: ", widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('save selection')

    def __init__(self, original_images=None, *args, **kwargs):
        super(ImageSlideshowForm, self).__init__(*args, **kwargs)
        if original_images:
            self.original_images = original_images

class EditImageForm(FlaskForm):
    alt_tag = StringField('alt tag')
    caption = StringField('caption', validators=[Length(min=0, max=160)])
    submit = SubmitField('save changes')

    def __init__(self, *args, **kwargs):
        super(EditImageForm, self).__init__(*args, **kwargs)


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


