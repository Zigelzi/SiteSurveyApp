from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user
from sitesurvey import app
from sitesurvey.forms import Customer, Location, Chargers, Installation, CreateUser, LogIn, UpdateAccount
from sitesurvey.models import User

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