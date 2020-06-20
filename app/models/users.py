import os
from app import db, login
from flask_login import UserMixin
from datetime import datetime, timedelta
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
import base64

followers = db.Table('followers', #since this is an association table no need to make part of a class
  db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

likedPosts = db.Table('postLikes',
  db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
  db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True, index=True)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)
    isWriter = db.Column(db.Boolean, default=False, nullable=False)
    isMember = db.Column(db.Boolean, default=False, nullable=False)
    signupDate = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.Column(db.String(300))
    #awards = db.relationship('Award', backref='winner')
    liked_posts = db.relationship('Post', secondary=likedPosts, lazy='select', backref="liker")
    #profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    usercomments = db.relationship('Comment', backref='commenter', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    #messages = db.relationship('Message', backref='user', lazy='dynamic')
    # messages_sent = db.relationship('Message', 
    #     foreign_keys='Message.sender_id', 
    #     backref='author',
    #     lazy='dynamic')

    # messages_received = db.relationship('Message',
    #     foreign_keys='Message.recipient_id',
    #     backref='recipient',
    #     lazy='dynamic')

    # def __init__(self, data):
    #     self.username = data.get('username')
    #     self.email = data.get('email')
    #     self.password = data.get('password')
    #     self.isAdmin = 0
    #     self.isWriter = 0
    
    def __repr__(self):
        return '{} - {}'.format(self.id, self.username)

# def get_user(self, user_id):
    #     user = User.query.get(user_id)
    #     if user is None:
 
    ## AUTH METHODS ##

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    # need to add password reset tokens
    # def get_reset_password_token(self, expires_in=600):
        # return jwt.encode(
            # {'reset_password': self.id, 'exp': time() + expires_in},
            # current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # @staticmethod
    # def verify_reset_password_token(token):
        # try:
            # id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            # algorithms=['HS256'])['reset_password']
        # except:
            # return
        # return User.query.get(id)


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

    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()
        # return self?
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user): #helper method
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join( #1- followers association table, 2- join condition
            followers, (followers.c.followed_id == Post.user_id)).filter(
                # i want the posts from people where i am their follower
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id) #assign user_id (me) to self.id - try filter_by(self.id) - does this work?
        return followed.union(own).order_by(Post.timestamp.desc())


## HELPER METHODS

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
 
    
