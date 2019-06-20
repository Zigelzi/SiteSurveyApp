from os import environ

class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    #MAIL_USERNAME = environ.get('EMAIL_USER')
    #MAIL_PW = environ.get('EMAIL_PW')

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True