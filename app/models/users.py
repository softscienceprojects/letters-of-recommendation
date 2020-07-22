import os
from app import db, login
from flask import url_for
from flask_login import UserMixin
from datetime import datetime, timedelta
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from cloudinary.uploader import upload as _cloudinary_upload


followers = db.Table('followers', #since this is an association table no need to make part of a class
  db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

likedPosts = db.Table('likedPosts',
  db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
  db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True, index=True)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=False)
    isWriter = db.Column(db.Boolean, default=False)
    isEditor = db.Column(db.Boolean, default=False)
    isMember = db.Column(db.Boolean, default=False)
    signupDate = db.Column(db.DateTime, default=datetime.utcnow)
    lastLoggedIn = db.Column(db.DateTime, default = datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    profile = db.Column(db.String(300))
    liked_posts = db.relationship('Post', secondary=likedPosts, lazy='dynamic', backref="liker")
    profile_picture = db.Column(db.String, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    messages_sent = db.relationship('Message', 
        foreign_keys='Message.sender_id', 
        backref='sender',
        lazy='dynamic')
    messages_received = db.relationship('Message',
        foreign_keys='Message.recipient_id',
        backref='recipient',
        lazy='dynamic')

    # def __init__(self, data):
    #     print(data)
    #     self.isAdmin = 0
    #     self.isWriter = 0
    
    def __repr__(self):
        return '{} - {}'.format(self.id, self.username)

    def set_profile_photo(self, image):
        """
        image gets uploaded to storage
        get reference to filename
        image_uri is either the cloudinary version, or deleting it means that we revert back to 'default.jpg'

        """
        if image.content_type in ['image/gif', 'image/jpeg', 'image/png']: ## Also need to check for file size!!!
            filename = "{}{}".format(self.id, self.username)
            try:
                upload_result = _cloudinary_upload(image, folder="profile_pics", public_id=filename, resource_type="image")
                return f"v{upload_result.get('version')}/{upload_result.get('public_id')}.{upload_result.get('format')}"
            except:
                pass
        else:
            return self.profile_picture

    def get_profile_photo(self):
        """
        find the user by their username
        get result in users.profile_picture
        if result == 'default.jpg' or result == None
            url to image file is app/static/images/default.jpg
        else 
            url to image file is cloudinary
        """
        if self.profile_picture in ['default.jpg', None]:
            return url_for('static', filename='images/mobile.png')
        else:
            #return url_for('static', filename='images/mobile.png')
            return f"https://res.cloudinary.com/{os.environ.get('CLOUDINARY_CLOUD_NAME')}/image/upload/{self.profile_picture}"

# def get_user(self, user_id):
    #     user = User.query.get(user_id)
    #     if user is None:
 
    ## AUTH METHODS ##

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#     # need to add password reset tokens
#     # def get_reset_password_token(self, expires_in=600):
#         # return jwt.encode(
#             # {'reset_password': self.id, 'exp': time() + expires_in},
#             # current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

#     # @staticmethod
#     # def verify_reset_password_token(token):
#         # try:
#             # id = jwt.decode(token, current_app.config['SECRET_KEY'],
#                             # algorithms=['HS256'])['reset_password']
#         # except:
#             # return
#         # return User.query.get(id)


    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user): #helper method
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


    def get_liked_posts(self, post):
        """
        our helper method to see if we already like this post or not
        """
        return self.liked_posts.filter(
            likedPosts.c.post_id == post.id).count() > 0

    def like_post(self, post):
        if not self.get_liked_posts(post):
            self.liked_posts.append(post)

    def unlike_post(self, post):
        if self.get_liked_posts(post):
            self.liked_posts.remove(post)

    def toggle_writer(self, user):
        if self.isWriter == False:
            self.isWriter = True
        else:
            self.isWriter = False
        

# ## HELPER METHODS

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
 
    
