from flask import Flask
from sitesurvey.config import Config, DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

from sitesurvey import routes