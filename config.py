import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nananana boo boo you will never guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # turn off update messages from sqlalchemy