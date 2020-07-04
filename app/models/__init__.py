from app import db
from markupsafe import escape
from app.models.users import User, followers, likedPosts
from app.models.posts import Post
from app.models.tags import Tag, postTags
from app.models.comments import Comment
from app.models.messages import Message
from app.models.images import Image


# Before save functions

def save_post(**kwargs):
    post = Post(**kwargs)
    db.session.add(post)
    db.session.commit()
    return post

def break_up_tags(post, tags):
    all_tags = []
    for tag in tags.split(','):
        tag = tag.strip().lower()
        if tag != '':
            found_or_made_tag = get_or_create_by(Tag, name=tag)
            all_tags.append(found_or_made_tag)    
    create_or_remove_postTag(all_tags, post)


def create_or_remove_postTag(tags_list, post):
    """
    if the tag already exists in posttags, nothing
    if the tag doesn't exist in posttags, add
    if there is a tag in posttags not here, remove (clean-up after)
    """
    this_post_tags = post.posttags.all()
    for tag in tags_list:
        post.add_tag(tag)
        db.session.commit()
    for tag in this_post_tags:
        if tag not in tags_list:
            post.remove_tag(tag)
            db.session.commit()
    

def get_or_create_by(model, **kwargs):
    """
    Adapted from https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    Suppose my model object is :
    class Country(Base):
        __tablename__ = 'countries'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

    To get or create my object I write :
    myCountry = get_or_create_by(Country, name=countryName)
    """
    #instance = model.query.filter_by(**kwargs).first()
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

def find_tag(tag_name):
        #assuming this is a string, from request params
    tag = Tag.query.filter_by(name=tag_name).first()
    return tag
    # postTags.select(postTags.c.post_id==1)
    # postTags.select(postTags.c.tag_id==1)

## can we be combined into one???
## see above. Do we work? to test
def get_tags_for_post(post_id):
    #return Tag.query.join(postTags, (postTags.c.post_id == post_id)).all()
    post = Post.query.filter_by(id=post_id).first()
    return post.posttags.order_by(Post.datePosted.desc()).all()

def get_posts_for_tag(tag_id):
    #return Post.query.join(postTags, (postTags.c.tag_id == tag_id)).all()
    tag = Tag.query.filter_by(id=tag_id).first()
    return tag.posts.order_by(Post.datePosted.desc()).all()

def hash_string_value(string_text):
    pass
