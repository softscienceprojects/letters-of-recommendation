from app import db
from datetime import datetime

followers = db.Table('followers', #since this is an association table no need to make part of a class
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

class User(db.Model):
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
    #awards = db.relationship() 
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #comments = db.relationship('Comment', backref='writer', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    #messages = db.relationship('Message', backref='user', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)


    # def __init__(self, data):
    #     self.username = data.get('username')
    #     self.email = data.get('email')
    #     self.password = data.get('password')
    #     self.isAdmin = 0
    #     self.isWriter = 0
    
    def __repr__(self):
        return '{}'.format(self.username)

    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()
        # return self?
    
    # def get_user(self, user_id):
    #     user = User.query.get(user_id)
    #     if user is None:
