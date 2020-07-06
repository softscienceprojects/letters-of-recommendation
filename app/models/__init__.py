from app import db
from markupsafe import escape
from app.models.users import User, followers, likedPosts
from app.models.posts import Post, postImages
from app.models.tags import Tag, postTags
from app.models.comments import Comment
from app.models.messages import Message
from app.models.images import Image, upload_image, get_self_image_for_select_buttons


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

def get_tags_for_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return post.posttags.order_by(Post.datePosted.desc()).all()

def get_posts_for_tag(tag_id, filterLive=True):
    tag = Tag.query.filter_by(id=tag_id).first()
    if filterLive==False:
        return tag.posts.order_by(Post.datePosted.desc()).all()
    else:
        return Post.query.join(postTags, (postTags.c.tag_id == tag.id)).filter(Post.isLive==True).order_by(Post.datePosted.desc()).all()

def get_posts_by_user(user_id, isLive=True):
    return Post.query.filter_by(user_id=user_id, isLive=isLive).order_by(Post.datePosted.desc()).all()

def hash_string_value(string_text):
    pass
