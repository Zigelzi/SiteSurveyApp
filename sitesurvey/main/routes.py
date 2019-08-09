from flask import Blueprint, render_template

from flask_login import login_required
from sitesurvey.user.models import User, Organization, Orgtype
from sitesurvey.product.models import Charger, Product, Productcategory
from sitesurvey.survey.models import Survey, Location, Workorder

bp_main = Blueprint('main', __name__)

@bp_main.route("/")
@bp_main.route("/home")
def index():
    surveys = Survey.query.all()
    return render_template('main/index.html', surveys=surveys)

@bp_main.route('/features')
@login_required
def features():
    users = User.query.all()
    orgs = Organization.query.all()
    org_types = Orgtype.query.all()
    chargers = Charger.query.all()
    products = Product.query.all()
    prod_cats = Productcategory.query.all()
    surveys = Survey.query.all()
    locations = Location.query.all()
    workorders = Workorder.query.all()

    return render_template('main/features.html', users=users,
                                                 orgs=orgs,
                                                 org_types=org_types,
                                                 chargers=chargers,
                                                 products=products,
                                                 prod_cats=prod_cats,
                                                 surveys=surveys,
                                                 locations=locations,
                                                 workorders=workorders)