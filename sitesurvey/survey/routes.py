from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import current_user, login_required

import sys
from json import loads

from sitesurvey import db
from sitesurvey.survey.models import Survey, Surveypicture, Location, Workorder, Workorderattachment, Lineitem
from sitesurvey.survey.forms import SurveyForm, WorkorderForm, LocationForm
from sitesurvey.survey.utils import save_file
from sitesurvey.user.models import Contactperson, Organization
from sitesurvey.product.models import Charger, Product

bp_survey = Blueprint('survey', __name__)
# Paths to survey and attachment file folders
survey_picture_folder = 'survey_pictures'
workorder_attachment_folder = 'workorder_attachments'

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

        survey = Survey(installation_method=form.installation_method.data,
                        concrete_foundation=form.foundation.data,
                        grid_connection=form.grid_connection.data,
                        grid_cable=form.grid_cable.data,
                        max_power=form.max_power.data,
                        consumption_fuse=form.consumption_point_fuse.data,
                        maincabinet_rating=form.maincabinet_rating.data,
                        empty_fuses=form.empty_fuses.data,
                        number_of_slots=form.number_of_slots.data,
                        signal_strength=form.signal_strength.data,
                        installation_location=form.installation_location.data,
                        user_id=current_user.id)
        
        db.session.add(contact_person)
        db.session.add(survey)
        db.session.commit()


        # Saving the installation location picture to file system and creating DB entry
        pic_installation_location_file = save_file(form.pic_installation_location.data, survey_picture_folder)
        sp_installation_location = Surveypicture(survey_id=survey.id,
                                                    picture_filename=pic_installation_location_file)

        # Saving the main cabinet picture to file system and creating DB entry
        pic_maincabinet_file = save_file(form.pic_maincabinet.data, survey_picture_folder)
        sp_maincabinet = Surveypicture(survey_id=survey.id,
                                        picture_filename=pic_maincabinet_file)

        # Saving the subcabinet picture if it exists to file system and creating DB entry
        if form.pic_subcabinet.data:
            pic_subcabinet_file = save_file(form.pic_subcabinet.data, survey_picture_folder)
            sp_subcabinet = Surveypicture(survey_id=survey.id,
                                            picture_filename=pic_subcabinet_file)
            db.session.add(sp_subcabinet)

        # Saving the additional picture if it exists to file system and creating DB entry
        if form.pic_additional.data:
            pic_additional_file = save_file(form.pic_additional.data, survey_picture_folder)
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
        filenames.append(survey_picture_folder + picture.picture_filename)
    return render_template('survey/survey.html', survey=survey, filenames=filenames)

@bp_survey.route('/survey/create_workorder', methods=['GET', 'POST'])
@login_required
def create_workorder():
    form = WorkorderForm()
    if request.method == 'POST':
        print('Request method: ' + request.method)
        print('Validate on submit: ')
        print(form.validate_on_submit())
        print('Form errors:')
        print(form.errors)
        print(form.requested_date.data)

    # TODO: Send the whole form in XHR rather than default submit.
    if (form.validate_on_submit() and request.method == 'POST'):
        org_id = Organization.query.filter_by(org_name=form.organization_name.data).first().id
        location_id = Location.query.filter_by(name=form.location_name.data).first().id
        workorder = Workorder(title=form.title.data,
                              requested_date=form.requested_date.data,
                              public_chargers=form.public_chargers.data,
                              public_installation_location=form.public_installation_location.data,
                              public_charging_power=form.public_charging_power.data,
                              private_chargers=form.private_chargers.data,
                              private_installation_location=form.private_installation_location.data,
                              private_charging_power=form.private_charging_power.data,
                              installation_type=form.installation_type.data,
                              org_id=org_id,
                              location_id=location_id)

        db.session.add(workorder)
        db.session.commit()

        # If attachments exist save the files to disk and commit the filenames and titles to DB
        if form.attachment_1.data:
            attachment_1_file = save_file(form.attachment_1.data, workorder_attachment_folder)
            attachment_1 = Workorderattachment(workorder_id=workorder.id,
                                               title=form.attachment_1_title.data,
                                               picture_filename=attachment_1_file)
            db.session.add(attachment_1)

        if form.attachment_2.data:
            attachment_2_file = save_file(form.attachment_2.data, workorder_attachment_folder)
            attachment_2 = Workorderattachment(workorder_id=workorder.id,
                                               title=form.attachment_2_title.data,
                                               picture_filename=attachment_2_file)
            db.session.add(attachment_2)

        if form.attachment_3.data:
            attachment_3_file = save_file(form.attachment_3.data, workorder_attachment_folder)
            attachment_3 = Workorderattachment(workorder_id=workorder.id,
                                               title=form.attachment_3_title.data,
                                               picture_filename=attachment_3_file)
            db.session.add(attachment_3)

        # Get the Table data submitted in the JSON part
        json = request.get_json()
        print(workorder.id)
        for item in json['products']:
            product = Product.query.filter_by(product_number=item['product_number']).first()
            line_item = Lineitem(discount=0,
                                 quantity=item['quantity'],
                                 total=item['total'],
                                 product_id=product.id,
                                 workorder_id=workorder.id)
            db.session.add(line_item)
        db.session.commit()
        return redirect(url_for('survey.workorder', workorder_id=workorder.id))

    return render_template('survey/create_workorder.html', form=form)

@bp_survey.route('/survey/workorder/<int:workorder_id>')
@login_required
def workorder(workorder_id):
    workorder = Workorder.query.get_or_404(workorder_id)
    org = Organization.query.get(workorder.org_id)
    location = Location.query.get(workorder.location_id)
    filenames = []
    # Append all the filenames for creating the url_for to display the pictures
    for attachment in workorder.attachments:
        filenames.append(workorder_attachment_folder + attachment.picture_filename)
    return render_template('survey/workorder.html', workorder=workorder, org=org, location=location, filenames=filenames)

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
