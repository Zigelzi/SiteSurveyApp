import os

# Create absolute path for database
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USERNAME = environ.get('EMAIL_USER')
    #MAIL_PW = environ.get('EMAIL_PW')

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True