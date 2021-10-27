# config.py

import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'VrZ7Qwx3QwvzsVyPzggpJYWJ'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
