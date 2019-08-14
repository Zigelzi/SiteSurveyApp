from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from sitesurvey import db
from sitesurvey.user.models import User, Organization, Orgtype, Contactperson
from sitesurvey.user.forms import CreateUserForm, UpdateAccountForm, AddOrganizationForm, AddOrgTypeForm, CreateContactForm

bp_user = Blueprint('user', __name__)

@bp_user.route('/organizations')
@login_required
def organizations():
    organizations = Organization.query.all()
    return render_template('user/organizations.html', title='Organizations', active='organizations', organizations=organizations)

@bp_user.route('/organizations/organization/<int:organization_id>')
@login_required
def organization(organization_id):
    organization = Organization.query.get_or_404(organization_id)
    return render_template('user/organization.html', organization=organization)

@bp_user.route('/organizations/create_organization', methods=["GET", "POST"])
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
        return redirect(url_for('user.organization', organization_id=organization.id))
    return render_template('user/add_organization.html', title='Create organization', form=form, active='add_organization')

@bp_user.route('/organizations/create_organization_tag', methods=["GET", "POST"])
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
        return redirect(url_for('user.create_organization_tag'))
    return render_template('user/add_organization_type.html', title='Create organization type', form=form, active='add_organization_type')

@bp_user.route('/organizations/org_type/<int:org_type_id>')
@login_required
def org_type(org_type_id):
    org_type = Orgtype.query.get_or_404(org_type_id)
    return render_template('user/org_type.html', org_type=org_type)

@bp_user.route('/users')
@login_required
def users():
    return render_template('user/users.html', title='Users', active='users')

@bp_user.route('/users/user/<int:user_id>')
@login_required
def user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user/user.html', user=user)

@bp_user.route('/users/create_contactperson', methods=["GET", "POST"])
@login_required
def create_contact_person():
    form = CreateContactForm()
    if form.validate_on_submit():
        # Take the form input and create db entry and commit it
        contact_person = Contactperson(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     title=form.title.data,
                     email=form.email.data,
                     phone_number=form.phone_number.data,
                     organization=form.organization.data)
        db.session.add(contact_person)
        db.session.commit()
        flash(f'Contact person has been created. They can now log in', 'success')
    return render_template('user/create_contactperson.html', title='Create contact', form=form, active='create_contact')

@bp_user.route('/users/contact_person/<int:contact_person_id>')
@login_required
def contact_person(contact_person_id):
    contact_person = Contactperson.query.get_or_404(contact_person_id)
    return render_template('user/contact_person.html', contact_person=contact_person)

@bp_user.route('/users/create_user', methods=["GET", "POST"])
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
        return redirect(url_for('auth.login'))
    return render_template('user/create_user.html', title='Create user', form=form, active='create_user')


@bp_user.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('user/account.html', title='Account', active='account', form=form)
