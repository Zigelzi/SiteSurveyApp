from flask import Blueprint, render_template, redirect, flash
from flask_login import current_user, login_required

import sys

from sitesurvey import db
from sitesurvey.survey.models import Survey
from sitesurvey.survey.forms import SurveyForm
from sitesurvey.user.models import Contactperson
from sitesurvey.charger.models import Charger

bp_survey = Blueprint('survey', __name__)

@bp_survey.route("/survey/create", methods=["GET", "POST"])
@login_required
def create_survey():
    
    form = SurveyForm()

    if form.validate_on_submit():
        # Get the number of surveys in DB and do running numbering (+1)
        survey_id = Survey.query.order_by(Survey.id.desc()).first()
        # Query the selected charger model and it's id and enter it as charger_id
        charger_id = Charger.query.get(form.model.data)
        
        # If Survey query returns None this is the first survey.
        if survey_id == None:
            survey_id = 1
        else:
            survey_id.id += 1

        # Convert all the 
        contact_person = Contactperson(first_name=form.first_name.data,
                                        last_name=form.last_name.data,
                                        title=form.title.data,
                                        email=form.email.data,
                                        phone_number=form.phone_number.data)

        survey = Survey(name=form.location_name.data,
                        address=form.address.data,
                        postal_code=form.postal_code.data,
                        city=form.city.data,
                        country=form.country.data,
                        coordinate_lat=form.coordinate_lat.data,
                        coordinate_long=form.coordinate_long.data,
                        number_of_chargers=form.charger_amount.data,
                        cp_charging_power=form.charging_power.data,
                        installation_method=form.installation_method.data,
                        concrete_foundation=form.foundation.data,
                        requested_date=form.requested_date.data,
                        grid_connection=form.grid_connection.data,
                        grid_cable=form.grid_cable.data,
                        max_power=form.max_power.data,
                        consumption_fuse=form.consumption_point_fuse.data,
                        maincabinet_rating=form.maincabinet_rating.data,
                        empty_fuses=form.empty_fuses.data,
                        number_of_slots=form.number_of_slots.data,
                        signal_strength=form.signal_strength.data,
                        installation_location=form.installation_location.data,
                        charger_id=charger_id,
                        user_id=current_user.id)
        
        # Add all information from form to DB session and commit the changes
        db.session.add(contact_person)
        db.session.add(survey)
        print(f'Contact person: {contact_person}', file=sys.stderr)
        print(f'Survey: {survey}', file=sys.stderr)
        db.session.commit()

        # Append the contact person as Surveys contact person
        survey.contact_person.append(contact_person)
        db.session.commit()
        flash(f'Survey created successfully!', 'success')

    return render_template('survey/create_survey.html', title='Survey', form=form)


@bp_survey.route('/survey/<int:survey_id>')
@login_required
def survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template('survey/survey.html', survey=survey)
