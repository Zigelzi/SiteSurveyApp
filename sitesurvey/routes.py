from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from sitesurvey import app, db

from sitesurvey.forms import (SurveyForm, CustomerForm, LocationForm, AddChargerForm, InstallationForm,
                              CreateUserForm, LogInForm, UpdateAccountForm, ChargerForm,
                              AddOrganizationForm, CreateContactForm, AddOrgTypeForm, RequestPasswordForm,
                              ResetPasswordForm)
from sitesurvey.models import User, Organization, Survey, Charger, Orgtype, Contactperson
from sitesurvey.utils import send_email, send_password_reset_email
import sys


@app.route("/")
def index():
    surveys = Survey.query.all()
    dummy_locations = []
    # dummy_locations = [{'name':'Example site name 1', 'street':'Example street 1', 'post_code':'00100', 'city':'Helsinki', 'distance':50}, {'name':'Example site name 2', 'street':'Example street 1', 'post_code':'00100', 'city':'Helsinki', 'distance':50}]
    return render_template('index.html', locations=dummy_locations, surveys=surveys)

@app.route("/survey/create", methods=["GET", "POST"])
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
                        user_id = current_user.id)
        
        # Add all information from form to DB session and commit the changes
        db.session.add(contact_person)
        db.session.add(survey)
        db.session.commit()

        # Append the contact person as Surveys contact person
        survey.contact_person.append(contact_person)
        db.session.commit()

    return render_template('surveys/create_survey.html', title='Survey', form=form)

@app.route('/survey/<int:survey_id>')
def survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template('surveys/survey.html', survey=survey)

@app.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogInForm()

    # Validate the LogIn form input and if user exists log in.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            # Get the next page from URL when trying to access page which requires login but user isn't logged in
            next_page = request.args.get('next')
            # Redirect to next page parsed from URL if exist, if it doesn't exist then go to home page
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            # Login is failed and prompt the user for checking the email/password
            flash('Login failed. Please check the email and password.', 'alert')
    return render_template('forms/login.html', title='Log in', form=form, active='login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Password reset request sent! You will receive password reset email shorty.')
        return redirect(url_for('login'))
    return render_template('users/request_password_reset.html', title='Request new password', form=form)
    
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password has been reset!')
        return redirect(url_for('login'))
    return render_template('users/reset_password.html', form=form)

@app.route('/organizations')
@login_required
def organizations():
    organizations = Organization.query.all()
    return render_template('organizations/organizations.html', title='Organizations', active='organizations', organizations=organizations)

@app.route('/organizations/organization/<int:organization_id>')
@login_required
def organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)
    return render_template('organizations/organization.html', organization=organization)

@app.route('/organizations/create_organization', methods=["GET", "POST"])
@login_required
def create_organization():
    form = AddOrganizationForm()
    if form.validate_on_submit():
        org_type = Orgtype.query.get(form.org_type.data)
        # Take the form input and create db entry and commit it
        organization = Organization(org_name=form.org_name.data,
                     org_number=form.org_number.data,
                     address=form.address.data,
                     postal_code=form.postal_code.data,
                     city=form.city.data,
                     country=form.country.data)
        db.session.add(organization)
        db.session.commit()
        organization.org_type.append(org_type)
        db.session.commit()

        flash(f'Organization has been created.', 'success')
    return render_template('organizations/add_organization.html', title='Create organization', form=form, active='add_organization')

@app.route('/organizations/create_organization_tag', methods=["GET", "POST"])
@login_required
def create_organization_tag():
    form = AddOrgTypeForm()
    if form.validate_on_submit():
        # Take the form input and create db entry and commit it
        org_type = Orgtype(title=form.title.data,
                     description=form.description.data)
        db.session.add(org_type)
        db.session.commit()
        flash(f'Organization type has been created.', 'success')
        return redirect(url_for('create_organization_tag'))
    return render_template('organizations/add_organization_type.html', title='Create organization type', form=form, active='add_organization_type')

@app.route('/organizations/org_type/<int:org_type_id>')
@login_required
def org_type(org_type_id):
    org_type = Orgtype.query.get_or_404(org_type_id)
    return render_template('organizations/org_type.html', org_type=org_type)

@app.route('/users')
@login_required
def users():
    return render_template('/users/users.html', title='Users', active='users')

@app.route('/users/user/<int:user_id>')
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/user.html', user=user)

@app.route('/users/create_contactperson', methods=["GET", "POST"])
@login_required
def create_contact_person():
    form = CreateContactForm()
    if form.validate_on_submit():
        # Take the form input and create db entry and commit it
        contact_person = Contactperson(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     title=form.title.data,
                     email=form.email.data,
                     phone_number=form.phone_number.data)
        db.session.add(contact_person)
        db.session.commit()
        flash(f'Contact person has been created. They can now log in', 'success')
    return render_template('users/create_contactperson.html', title='Create contact', form=form, active='create_contact')

@app.route('/users/contact_person/<int:contact_person_id>')
@login_required
def contact_person(contact_person_id):
    contact_person = Contactperson.query.get_or_404(contact_person_id)
    return render_template('users/contact_person.html', contact_person=contact_person)

@app.route('/users/create_user', methods=["GET", "POST"])
@login_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        # Take the form input and create db entry and commit it
        user = User(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     email=form.email.data,
                     org_id=form.organization.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User has been created. They can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('users/create_user.html', title='Create user', form=form, active='create_user')


@app.route('/account', methods=['GET', 'POST'])
# login_required decorator used to show that this page requires logged in user. Configuration in __init__.py
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('forms/account.html', title='Account', active='account', form=form)

@app.route('/chargers')
@login_required
def chargers():
    chargers = Charger.query.all()
    return render_template('chargers/chargers.html', title='Chargers', active='chargers', chargers=chargers)

@app.route('/chargers/charger/<int:charger_id>')
def charger(charger_id):
    charger = Charger.query.get_or_404(charger_id)
    return render_template('chargers/charger.html', charger=charger)

@app.route('/chargers/add_charger', methods=["GET", "POST"])
@login_required
def add_charger():
    form = AddChargerForm()
    if form.validate_on_submit():

        # Take the form input and create db entry and commit it
        charger = Charger(manufacturer=form.manufacturer.data,
                        model=form.model.data,
                        product_no=form.product_no.data,
                        price=form.price.data,
                        type_of_outlet=form.type_of_outlet.data,
                        no_of_outlets=form.no_of_outlets.data,
                        dc_ac=form.dc_ac.data,
                        communication=form.communication.data,
                        mounting_wall=form.mounting_wall.data,
                        mounting_ground=form.mounting_ground.data,
                        max_power=form.max_power.data,
                        mcb=form.mcb.data,
                        rcd_typea=form.rcd_typea.data,
                        rcd_typeb=form.rcd_typeb.data,
                        automatic_rcd=form.automatic_rcd.data,
                        pwr_outage_eq=form.pwr_outage_eq.data,
                        mid_meter=form.mid_meter.data,
                        mid_readable=form.mid_readable.data,
                        max_cable_d=form.max_cable_d.data,
                        cable_cu_allowed=form.cable_cu_allowed.data,
                        cable_al_allowed=form.cable_al_allowed.data)
        db.session.add(charger)
        db.session.commit()
        flash(f'Charger has been created in the database.', 'success')
        return redirect(url_for('add_charger'))
    return render_template('chargers/add_charger.html', title='Add charger', form=form, active='add_charger')

@app.route('/chargers/view_chargers', methods=["GET"])
@login_required
def view_chargers():
    chargers = Charger.query.all()
    return render_template('chargers/view_chargers.html', title='View chargers', chargers=chargers)