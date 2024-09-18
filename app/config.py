import os

class Config:
    SECRET_KEY = os.environ.get('54caa23b2c3107e7cfede4513602ef5c') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
