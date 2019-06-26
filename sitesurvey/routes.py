from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from sitesurvey import app, db
from sitesurvey.forms import Customer, Location, Chargers, Installation, CreateUser, LogIn, UpdateAccount, AddCharger
from sitesurvey.models import User, Organization, Survey, Charger, Location, Orgtype, Contactperson

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

@app.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogIn()

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
    return render_template('login.html', title='Log in', form=form, active='login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    form = CreateUser()
    if form.validate_on_submit():
        # Hash the given PW to enter it to database

        # Take the form input and create db entry and commit it
        user = User(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User has been created. They can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('create_user.html', title='Create user', form=form, active='create_user')

@app.route('/account', methods=['GET', 'POST'])
# login_required decorator used to show that this page requires logged in user. Configuration in __init__.py
@login_required
def account():
    form = UpdateAccount()
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
    return render_template('account.html', title='Account', active='account', form=form)

@app.route('/add_charger', methods=["GET", "POST"])
@login_required
def add_charger():
    form = AddCharger()
    if form.validate_on_submit():
        # Hash the given PW to enter it to database

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
    return render_template('add_charger.html', title='Add charger', form=form, active='add_charger')

@app.route('/view_chargers', methods=["GET"])
@login_required
def view_chargers():
    chargers = Charger.query.all()
    return render_template('view_chargers.html', title='View chargers', chargers=chargers)