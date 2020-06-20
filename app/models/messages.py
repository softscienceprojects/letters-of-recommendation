from app import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    datePosted = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.relationship('User', db.ForeignKey("users.id"))
    recipient_id = db.relationship('User', db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    txtmessage = db.Column(db.Text)

    def __repr__(self):
        return 'Message {}'.format(self.txtmessage)