from app import db

# postTags = db.Table('postTags', #since this is an association table no need to make part of a class
#     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
#     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
# )

class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String) # reponse['asset_id']
    filename = db.Column(db.String, nullable=False) # response['secure_url'].split('/')[-1:]  #...for profile pics
    version = db.Column(db.String, nullable=False) # response['secure_url'].split('/')[-3:] ##...for profile pics
    public_id = db.Column(db.String, nullable=False) # response['public_id']
    format = db.Column(db.String) # response['format'] ## the filetype e.g. jpg 
    # posts = db.relationship('Post', secondary=postTags, lazy='dynamic', backref=db.backref('posttags', lazy='dynamic'))

    def __repr__(self):
        return '{} - {}.{}'.format(self.id, self.filename, self.format)

    def get_all_images(self):
        return Image.query.all()





