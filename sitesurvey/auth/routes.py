from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from sitesurvey import db
from sitesurvey.auth.forms import LogInForm, RequestPasswordForm, ResetPasswordForm
from sitesurvey.auth.utils import send_email, send_password_reset_email
from sitesurvey.user.models import User, Organization, Orgtype, Contactperson



bp_auth = Blueprint('auth', __name__)

@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    # If user is already logged in, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LogInForm()

    # Validate the LogIn form input and if user exists log in.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            # Get the next page from URL when trying to access page which requires login but user isn't logged in
            next_page = request.args.get('next')
            # Redirect to next page parsed from URL if exist, if it doesn't exist then go to home page
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            # Login is failed and prompt the user for checking the email/password
            flash('Login failed. Please check the email and password.', 'alert')
    return render_template('login.html', title='Log in', form=form, active='login')

@bp_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp_auth.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Password reset request sent! You will receive password reset email shorty.')
        return redirect(url_for('auth.login'))
    return render_template('request_password_reset.html', title='Request new password', form=form)
    
@bp_auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Password has been reset!')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
