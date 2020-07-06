
from datetime import datetime
from app import db
from app.models.users import likedPosts, User, followers
from app.models.tags import postTags
from app.models.images import Image

postImages = db.Table('postImages',
    db.Column('image_id', db.Integer, db.ForeignKey('images.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    isLive = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    likers = db.relationship('User', secondary=likedPosts, lazy='dynamic', backref="postLiked")
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')
    #tags = db.relationship('Tag', secondary=postTags, lazy='dynamic', backref="postTagged")
    heroImage_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    images = db.relationship('Image', secondary=postImages, lazy='dynamic', backref=db.backref('posts', lazy='dynamic'))
    ## will need a method to make an image a hero image, and deassociate any images with this post

    def __repr__(self):
        return '{} - {}; Live: {}'.format(self.id, self.title, self.isLive)

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

    def postToggleLive(self):
        if self.isLive:
            self.isLive = False
            return self
        else:
            self.isLive = True
            return self

    def check_tag_for_this_post(self, tag):
        return self.posttags.filter(
            postTags.c.tag_id == tag.id)
    
    def add_tag(self, tag):
        if not self.check_tag_for_this_post(tag).count() > 0:
            self.posttags.append(tag)
    
    def remove_tag(self, tag):
        if self.check_tag_for_this_post(tag):
            self.posttags.remove(tag)

    def get_post_hero_image(self):
        image_id = self.heroImage_id
        if image_id:
            hero = Image.query.filter_by(id=image_id).first()
            image = hero.get_postedit_format_photo()
            return image

    def get_post_hero_image_for_forms(self):
        image_id = self.heroImage_id
        if image_id:
            hero = Image.query.filter_by(id=image_id).first()
            return hero.asset_id

    def get_hero_image_choices(self):
        imagesList = [(image.asset_id, image.id) for image in self.images]
        hero = Image.query.filter_by(id=self.heroImage_id).first()
        heroSelectPair = (hero.asset_id, hero.id)
        if heroSelectPair not in imagesList:
            imagesList.append(heroSelectPair)
        return imagesList

    def set_post_hero_image(self, image_asset_id):
        image = Image.query.filter_by(asset_id=image_asset_id).first()
        self.heroImage_id = image.id
        return self

    def remove_images_from_post(self, images_list):
        """
        will expect a list of image asset_id's
        note this will not 'unset' the hero image, 
        which is set separately to images associated with this post
        (You gotta write a method for this babes)
        """
        for asset_id in images_list:
            image = Image.query.filter_by(asset_id=asset_id).first()
            self.images.remove(image)
        return self

    def posts_by_user_follow(user):
        """
        get the posts of the users I follow. Create two variables. First:
        1. query the Post table
        2. join the _followers_ (join table), with
        3. _followers, 
        gets all the posts
        """
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == user.id, Post.isLive==True).order_by(Post.datePosted.desc()).all()

