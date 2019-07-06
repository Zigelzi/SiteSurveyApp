from flask import Blueprint, render_template

from sitesurvey.survey.models import Survey

bp_main = Blueprint('main', __name__)

@bp_main.route("/")
@bp_main.route("/home")
def index():
    surveys = Survey.query.all()
    return render_template('main/index.html', surveys=surveys)