from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from sitesurvey.config import Config, DevConfig

# Initializing the app, database and bcrypt (hashing)
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initializing the login manager and it's settings
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Log in to access this page'
login_manager.session_protection = 'strong'

from sitesurvey import routes