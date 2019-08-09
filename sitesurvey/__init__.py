from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_marshmallow import Marshmallow

from sitesurvey.config import Config, DevConfig

# Initializing the app, database and bcrypt (hashing)
app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
ma = Marshmallow(app)

# Initializing the login manager and it's settings
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Log in to access this page'
login_manager.session_protection = 'strong'
data_req_msg = 'Required field' # Variable for error message shown in FlaskForms

from sitesurvey.auth.routes import bp_auth
from sitesurvey.product.routes import bp_product
from sitesurvey.main.routes import bp_main
from sitesurvey.survey.routes import bp_survey
from sitesurvey.user.routes import bp_user
from sitesurvey.api.routes import bp_api

app.register_blueprint(bp_auth)
app.register_blueprint(bp_product)
app.register_blueprint(bp_main)
app.register_blueprint(bp_survey)
app.register_blueprint(bp_user)
app.register_blueprint(bp_api)

