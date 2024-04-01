from datetime import datetime, timezone, timedelta
from blogify import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
"""Database tables and columns for the blogify app"""


@login_manager.user_loader
def load_user(user_id):
    """loads up a user"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User table for creating a new blogify user or updating a
        user's account info
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def get_reset_token(self):
        """Uses Urlsafetimedserializer to generate a token using the app's
            secret key
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=600):
        """
            verifies the token
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except Exception as e:
            print(e)
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """str representation of the User class"""
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """Handles the storing of post data for users of blogify"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        """str representation of the post class"""
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    """Comment class for user's comments on posts"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    """Like class for users to like posts"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)