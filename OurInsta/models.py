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

