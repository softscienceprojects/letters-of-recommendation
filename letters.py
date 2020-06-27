from app import create_app, db
from app.models import User, Post, Tag, postTags, likedPosts, Comment, Message

app = create_app()

# this means when we do `flask shell` we get the context of our app
# no need to import!
# you have to set export FLASK_APP=letters.py to work
@app.shell_context_processor
def make_shell_context():
    return {'db': db,
        'User': User,
        'Post': Post,
        'Tag': Tag,
        'postTags': postTags,
        'likedPosts': likedPosts,
        'Comment': Comment,
        'Message': Message,
        'tags': Tag.query.all(),
        'posts': Post.query.all()
    }