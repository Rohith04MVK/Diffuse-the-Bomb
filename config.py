import os

# Get the absolute path of the directory the script is in
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "EPIC!!"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False