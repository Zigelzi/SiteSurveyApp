"""
Helper and utility functions for the application
"""
from datetime import datetime
from sitesurvey import app, mail
from flask import render_template
from flask_mail import Message

def send_async_email(msg):
    """

    """

def send_email(subject, sender, recipients, text_body, html_body):
    """
    Utility function for sending emails from the application. Using threding to send the mails \
    asynchronously
    """
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
def send_password_reset_email(user):
    token = user.get_password_token()
    reset_time=datetime.now()
    send_email('[SiteSurveyApp] Account password reset',
                recipients=[user.email],
                sender=app.config['MAIL_DEFAULT_SENDER'],
                text_body=render_template('users/email/reset_password.txt',
                                           user=user, token=token, reset_time=reset_time),
                html_body=render_template('users/email/reset_password.html',
                                           user=user, token=token, reset_time=reset_time))