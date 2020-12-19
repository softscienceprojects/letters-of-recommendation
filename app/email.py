from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as SendGridMail

def send_email(subject, to, template, sender=None):
    msg = Message(
        subject,
        recipients=[to],
        body=subject,
        html=template)

    if sender:
        msg.sender = sender
    
    with current_app.app_context():
        # print('sending: ', msg)
        try:
            mail.send(msg)
            print('sent')
        except Exception as e:
            print(e)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    html = render_template('auth/password_reset.html', user=user, token=token)
    send_email("Letters of Recommendation: reset your password", 
        user.email, html)
#### TESTS ###################################

def testsendingoneemail(email):
    msg = Message("Hello",recipients=[email])
    msg.body = '!!!'
    with current_app.app_context():
        mail.send(msg)
    return "Sent"

def sendgridtestemail(fromemail):
    message = SendGridMail(
        from_email=fromemail,
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


