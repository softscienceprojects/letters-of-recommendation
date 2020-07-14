from app import * #create_app, db
from app.models import User, Post, Tag, postTags, likedPosts, Comment, Message, Image, followers, postImages
from app.email import *

app = create_app()

# this means when we do `flask shell` we get the context of our app
# no need to import!  ## make a script that loads up whatever is new?
# you have to set export FLASK_APP=letters.py to work
@app.shell_context_processor
def make_shell_context():
    return {'db': db,
        'User': User,
        'Post': Post,
        'Tag': Tag,
        'postTags': postTags,
        'likedPosts': likedPosts,
        'posts': Post.query.all(),
        'followers': followers,
        'users': User.query.all(),
        'tags': Tag.query.all(),
        'e': User.query.filter_by(username='e').first(),
        'p1': Post.query.filter_by(id=2).first(),
        'Comment': Comment,
        'Message': Message,
        'Image': Image,
        'images': Image.query.all(),
        'postImages': postImages,
        'testsendingoneemail': testsendingoneemail
    }