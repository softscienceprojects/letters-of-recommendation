from app import db
from markupsafe import escape
from app.models.users import User, followers, likedPosts
from app.models.posts import Post
from app.models.tags import Tag, postTags
from app.models.comments import Comment
from app.models.messages import Message


## Before save functions
def get_or_create_by(session, model, **kwargs):
    """
    from https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    Suppose my model object is :
    class Country(Base):
        __tablename__ = 'countries'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

    To get or create my object I write :
    myCountry = get_or_create_by(session, Country, name=countryName)
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def find_tags(self, tag_name):
        tag_name = tag_name.lower() #assuming this is a string, from the form data
        tags = get_all_tags()
        #if t.name in [tag.name for tag in tags]:
        #    tag = 
        pass
    # postTags.select(postTags.c.post_id==1)
    # postTags.select(postTags.c.tag_id==1)

## gives you back a list
## can we be combined into one???
def get_tags_for_post(post_id):
    return Tag.query.join(postTags, (postTags.c.post_id == post_id)).all()

def get_posts_for_tag(tag_id):
    return Post.query.join(postTags, (postTags.c.tag_id == tag_id)).all()

def hash_string_value(string_text):
    pass
