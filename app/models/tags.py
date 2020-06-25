from app import db

postTags = db.Table('postTags', #since this is an association table no need to make part of a class
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', secondary=postTags, lazy='dynamic', backref=db.backref('posttags', lazy='dynamic'))

    def __repr__(self):
        return '{} - {}'.format(self.id, self.name)

    def get_all_tags(self):
        return Tag.query.all()

    



