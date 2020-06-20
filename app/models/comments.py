from app import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.relationship('Post', db.ForeignKey("posts.id"))
    user_id = db.relationship('User', db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text)
    
    def __repr__(self):
        return 'Comment {}'.format(self.message)