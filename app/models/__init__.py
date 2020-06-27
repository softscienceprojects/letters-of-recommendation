from app import db
from markupsafe import escape
from app.models.users import User, followers, likedPosts
from app.models.posts import Post
from app.models.tags import Tag, postTags
from app.models.comments import Comment
from app.models.messages import Message
import pdb


## Before save functions

def save_post(**kwargs):
    post = Post(**kwargs)
    db.session.add(post)
    db.session.commit()
    return post

def break_up_tags(post, tags):
    all_tags = []
    for tag in tags.split(','):
        tag = tag.strip().lower()
        print("TAG: ", tag)
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
    print("CREATE OR REMOVE******")
    this_post_tags = post.posttags.all()
    print(this_post_tags)
    for tag in tags_list:
        post.add_tag(tag)
        db.session.commit()
    for tag in this_post_tags:
        if tag not in tags_list:
            db.session.delete(tag)
            db.session.commit()
    
        

    # remove
    # if postTags finds this post but not this tag
    # add this tag
    # if postTags finds this t
    # search_for_existing_postTag = tag.posts.filter(postTags.c.post_id == post.id)
    # if search_for_existing_postTag.count() > 0:
    #     return #
    # else:
    #     new_postTag = tag.posts.append(post)
    #     db.session.add(new_postTag)
    #     print(new_postTag)
    #     return new_postTag

# def is_following(self, user): #helper method
    # return self.followed.filter(
        # followers.c.followed_id == user.id).count() > 0

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
        print("instance ", instance)
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        print('newly created: ', instance)
        return instance

def find_tags(self, tag_name):
        #assuming this is a string, from the form data
        #if t.name in [tag.name for tag in tags]:
        #    tag = 
        pass
    # postTags.select(postTags.c.post_id==1)
    # postTags.select(postTags.c.tag_id==1)

def get_join(model, join_table, join_query, query):
    """
    *****doesn't work - need to interpolate join_query
    KeyError: 'join_query'
    e.g. get tags for post
    get_join(Tag, postTags, post_id, post.id)
        return Tag.query.join(postTags, (postTags.c.post_id == post_id)).all()

    get posts for tag
    get_join(Post, postTags, 'tag_id', tag.id)
        return Post.query.join(postTags, (postTags.c.tag_id == tag_id)).all()

    returns a list
    """
    return model.query.join(join_table, (join_table.c.join_query == query)).all()


## can we be combined into one???
## see above. Do we work? to test
def get_tags_for_post(post_id):
    # Tag.query.join(postTags, (postTags.c.post_id == p1.id)).all()
    return Tag.query.join(postTags, (postTags.c.post_id == post_id)).all()

def get_posts_for_tag(tag_id):
    return Post.query.join(postTags, (postTags.c.tag_id == tag_id)).all()

def hash_string_value(string_text):
    pass
