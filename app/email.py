from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as SendGridMail

def testsendingoneemail(email):
    msg = Message("Hello",recipients=[email])
    msg.body = '!!!'
    with current_app.app_context():
        mail.send(msg)
    return "Sent"

message = SendGridMail(
    from_email='from@example.com',
    to_emails='to@example.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.body)