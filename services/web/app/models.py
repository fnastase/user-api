import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(128), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    activation_email_date = db.Column(db.DateTime, default=datetime.utcnow)
    activation_code = db.Column(db.String(4))

    is_active = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def insert_user(email: str, password: str) -> User:
    '''Inserts a new User into the DB'''
    user = User()
    user.email = email
    user.uuid = str(uuid.uuid4())
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


def is_registered(email: str):
    '''Checks if a user is already registered with this email'''

    user = User.query.filter_by(email=email).first()

    if user:
        return True
    else:
        return False


def get_user_by_email(email: str) -> User:
    '''Gets User object from DB by email address'''

    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_uuid(uuid: str) -> User:
    '''Gets User object from DB by uuid'''

    user = User.query.filter_by(uuid=uuid).first()
    return user


def update_user_activated(user: User) -> User:
    '''Activate the coresponding user'''

    user.is_active = True
    db.session.commit()
    return user


def set_activation_email_date(user: User) -> User:
    '''Sets the current timestamp for activation email date'''

    user.activation_email_date = datetime.utcnow()
    db.session.commit()
    return user


def set_activation_code(user: User, activation_code: str) -> User:
    '''Updates the activation code for the specified user'''

    user.activation_code = activation_code
    db.session.commit()
    return user
