
from datetime import datetime
from app import db
from app.models.users import likedPosts

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    liker_users = db.relationship('User', secondary=likedPosts, lazy='select', backref="postLiked")
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')


    def __repr__(self):
        return '{} - {}'.format(self.id, self.title)

    def update_time_posted(self):
        #when a post is made or edited, update the time
        pass