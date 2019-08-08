from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required

import sys

from sitesurvey import db
from sitesurvey.survey.models import Survey, Surveypicture, Location, Workorder
from sitesurvey.survey.forms import SurveyForm, WorkorderForm, LocationForm
from sitesurvey.survey.utils import save_picture
from sitesurvey.user.models import Contactperson
from sitesurvey.product.models import Charger

bp_survey = Blueprint('survey', __name__)

@bp_survey.route("/survey/create", methods=["GET", "POST"])
@login_required
def create_survey():
    
    form = SurveyForm()

    if form.validate_on_submit():
        # Query the selected charger model and it's id and enter it as charger_id
        charger_id = Charger.query.get(form.model.data)

        # Create list of pictures and check if any of them has content to be submitted to DB

        # Convert all the from values to DB models and commit them to DB
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
        
        db.session.add(contact_person)
        db.session.add(survey)
        db.session.commit()


        # Saving the installation location picture to file system and creating DB entry
        pic_installation_location_file = save_picture(form.pic_installation_location.data)
        sp_installation_location = Surveypicture(survey_id=survey.id,
                                                    picture_filename=pic_installation_location_file)

        # Saving the main cabinet picture to file system and creating DB entry
        pic_maincabinet_file = save_picture(form.pic_maincabinet.data)
        sp_maincabinet = Surveypicture(survey_id=survey.id,
                                        picture_filename=pic_maincabinet_file)

        # Saving the subcabinet picture if it exists to file system and creating DB entry
        if form.pic_subcabinet.data:
            pic_subcabinet_file = save_picture(form.pic_subcabinet.data)
            sp_subcabinet = Surveypicture(survey_id=survey.id,
                                            picture_filename=pic_subcabinet_file)
            db.session.add(sp_subcabinet)

        # Saving the additional picture if it exists to file system and creating DB entry
        if form.pic_additional.data:
            pic_additional_file = save_picture(form.pic_additional.data)
            sp_additional = Surveypicture(survey_id=survey.id,
                                            picture_filename=pic_additional_file)
            db.session.add(sp_additional)
        
        # Add all information from form to DB session and commit the changes

        db.session.add(sp_installation_location)
        db.session.add(sp_maincabinet)
        print(f'Contact person: {contact_person}', file=sys.stderr)
        print(f'Survey: {survey}', file=sys.stderr)

        # Append the contact person as Surveys contact person
        survey.contact_person.append(contact_person)
        db.session.commit()
        flash(f'Survey created successfully!', 'success')
        return redirect(url_for('survey.survey', survey_id=survey.id))

    return render_template('survey/create_survey.html', title='Survey', form=form)


@bp_survey.route('/survey/<int:survey_id>')
@login_required
def survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    filenames = []
    # Append all the filenames for creating the url_for to display the pictures
    for picture in survey.pictures:
        filenames.append('survey_pictures/'+ picture.picture_filename)
    return render_template('survey/survey.html', survey=survey, filenames=filenames)

@bp_survey.route('/survey/create_workorder')
@login_required
def create_workorder():
    form = WorkorderForm()
    return render_template('survey/create_workorder.html', form=form)

@bp_survey.route('/survey/create_location', methods=["GET", "POST"])
@login_required
def create_location():
    form = LocationForm()
    
    if form.validate_on_submit() and request.method == 'POST':
        location = Location(name=form.location_name.data,
                            address=form.address.data,
                            postal_code=form.postal_code.data,
                            city=form.city.data,
                            country=form.country.data,
                            coordinate_lat=form.coordinate_lat.data,
                            coordinate_long=form.coordinate_long.data)
        print('Location submitted successfully!')
        print(location)
        db.session.add(location)
        db.session.commit()
        flash(f'Location created successfully!', 'success')
        return redirect(url_for('survey.location', location_id=location.id))
    return render_template('survey/create_location.html', title='Create location', form=form)

@bp_survey.route('/survey/location/<int:location_id>')
@login_required
def location(location_id):
    location = Location.query.get_or_404(location_id)
    return render_template('survey/location.html', location=location)
