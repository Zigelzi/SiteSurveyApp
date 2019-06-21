from flask import render_template, redirect, url_for
from sitesurvey import app
from sitesurvey.forms import Customer, Location, Chargers, Installation

@app.route("/")
def index():
    dummy_locations = [{'name':'Example site name 1', 'street':'Example street 1', 'post_code':'00100', 'city':'Helsinki', 'distance':50}, {'name':'Example site name 2', 'street':'Example street 1', 'post_code':'00100', 'city':'Helsinki', 'distance':50}]
    return render_template('index.html', locations=dummy_locations)

@app.route("/survey/create")
def create_survey():
    customer_form = Customer()
    location_form = Location()
    charger_form = Chargers()
    installation_form = Installation()
    return render_template('survey.html', title='Survey',
                            customer_form=customer_form,
                            location_form=location_form,
                            charger_form=charger_form,
                            installation_form=installation_form)
