
from datetime import datetime
from app import db
from app.models.users import likedPosts, User, followers
from app.models.tags import postTags


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    likers = db.relationship('User', secondary=likedPosts, lazy='dynamic', backref="postLiked")
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    #tags = db.relationship('Tag', secondary=postTags, lazy='dynamic', backref="postTagged")

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
        for user in self.likers.all():
            users.append({'id': user.id, 'username': user.username})
        return users

    def number_of_likes(self):
        likes = self.likers.count()
        return likes

    def get_latest_post():
        latest_post = Post.query.order_by(Post.datePosted.desc()).first()        
        return latest_post

    def check_tag_for_this_post(self, tag):
        return self.posttags.filter(
            postTags.c.tag_id == tag.id)
    
    def add_tag(self, tag):
        if not self.check_tag_for_this_post(tag).count() > 0:
            self.posttags.append(tag)
    
    def remove_tag(self, tag):
        if self.check_tag_for_this_post(tag):
            self.posttags.remove(tag)

    def posts_by_user_follow(user):
        """
        get the posts of the users I follow. Create two variables. First:
        1. query the Post table
        2. join the _followers_ (join table), with
        3. _followers, 
        gets all the posts
        """
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == user.id).order_by(Post.datePosted.desc()).all()