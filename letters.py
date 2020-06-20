from app import create_app, db
from app.models import User, Post, Tag #, postTags, Comment

app = create_app()

# this means when we do `flask shell` we get the context of our app
# no need to import!
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Tag': Tag}
    # , 'postTags': postTags, 'Comment': Comment