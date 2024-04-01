import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blogify import mail
"""Utils file for the blogify app"""

def save_picture(form_picture):
    """Save picture"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    out_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(out_size)
    i.save(picture_path)
    
    return picture_fn


def send_email(subject, sender, recipients, body):
    """Sends an email to a user"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)


def send_reset_email(user):
    """Function to send the reset_email"""
    token = user.get_reset_token()
    subject = 'Password Reset Request'
    sender = 'noreply@demo.com'
    recipients =[user.email]
    body = f""" To reset your password visit the following link
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not send this request then simply ignore this message.
    """
    send_email(subject, sender, recipients, body)


def send_registration_email(user):
    token = user.get_reset_token()
    subject = 'Welcome to Blogify! Confirm Your Registration'
    sender = 'noreply@demo.com'
    recipients = [user.email]
    body = f"""Welcome to Blogify! To complete your registration, please click the link below:
    {url_for('users.confirm_registration', token=token, _external=True)}
    If you did not sign up for an account on Blogify, please disregard this email.
    """
    send_email(subject, sender, recipients, body)