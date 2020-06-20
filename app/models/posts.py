
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
    liker_users = db.relationship('User', secondary=likedPosts, lazy='dynamic', backref="postLiked")
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')


    def __repr__(self):
        return '{} - {}'.format(self.id, self.title)

    def update_time_posted(self):
        #when a post is made or edited, update the time
        pass

    def users_that_liked(self):
        """
        returns list of dicts so we can get the id and username
        """
        users = []
        for user in self.liker_users.all():
            users.append({'id': user.id, 'username': user.username})
        return users

    def number_of_likes(self):
        likes = self.liker_users.count()
        return likes

    def get_latest_post():
        latest_post = Post.query.order_by(Post.datePosted.desc()).first()        
        return latest_post