from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

def testsendingoneemail(email):
    msg = Message("Hello",recipients=[email])
    msg.body = '!!!'
    with current_app.app_context():
        mail.send(msg)
    return "Sent"