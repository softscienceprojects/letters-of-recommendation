from app.models.users import User, followers, likedPosts
from app.models.posts import Post
from app.models.tags import Tag, postTags
from app.models.comments import Comment
from app.models.messages import Message

def get_or_create(session, model, **kwargs):
    """
    from https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    Suppose my model object is :
    class Country(Base):
        __tablename__ = 'countries'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

    To get or create my object I write :
    myCountry = get_or_create(session, Country, name=countryName)
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

