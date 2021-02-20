from sqlalchemy import PrimaryKeyConstraint
from OurInsta import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    print(db.session.query(Users).filter(Users.email == user_id).first())
    return db.session.query(Users).filter(Users.email == user_id).first()

class Users (db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    secure_password = db.Column(db.String(128))
    profile_image = db.Column(db.String(255), nullable=False)
    is_authenticated = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, name, phone_number, email, secure_password , profile_image):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.secure_password = secure_password
        self.is_authenticated = False
        self.profile_image = profile_image

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def __repr__(self):
        return '<Users {}>'.format(self.name)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False )
    post_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_description = db.Column(db.String(500), index=True)
    post_image = db.Column(db.String(255), nullable=False)
    post_reactions = db.relationship('Reaction', backref='post_reaction', lazy='dynamic')
    post_comments = db.relationship('Comment', backref='post_comment', lazy='dynamic')

    def __init__(self, post_description, post_image, author):
        self.post_description = post_description
        self.post_image = post_image
        self.author = author

