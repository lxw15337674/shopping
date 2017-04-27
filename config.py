import os

SECRET_KEY = "maybe"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
imgurl = os.path.join(basedir, 'photo')
