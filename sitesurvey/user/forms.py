from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SelectField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from sitesurvey import data_req_msg
from sitesurvey.user.models import User, Organization, Orgtype


class CreateUserForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Last name', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email',
                        validators=[DataRequired(message=data_req_msg), Email(message="Not valid email")])
    organization = SelectField('Organization', validators=[DataRequired(message=data_req_msg)],
                                coerce=int)
    password = PasswordField('Password',
                             validators=[DataRequired(message=data_req_msg),
                                         Length(min=8, message="Password must be at least 8 characters")])
    confirm_pw = PasswordField('Confirm password',
                               validators= [DataRequired(message=data_req_msg), EqualTo('password', message="Passwords do not match")])
    submit = SubmitField('Create account')

    def __init__(self, *args, **kwargs):
        """Initialize the class with the most recent DB data for SelectField."""
        # Query list of existing organizations from DB when form is created
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.organization.choices = [(org.id, org.org_name) for org in Organization.query.all()]

    # Custom validation to validate that email is not in use
    def validate_email(self, email):
        """Check if email is already in DB. If it is, raise ValidationError"""
        # Get the email from the form and query the DB for it
        email = User.query.filter_by(email=email.data).first()

        # If the DB query returns something, raise validation error
        if email:
            raise ValidationError('This email is already in use')

class CreateContactForm(FlaskForm):
    # Query list of existing organizations from DB
    first_name = StringField('First name', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Last name', validators=[DataRequired(message=data_req_msg)])
    title = StringField('Title', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email',
                        validators=[DataRequired(message=data_req_msg), Email(message="Not valid email")])
    phone_number = StringField('Phone number', validators=[DataRequired(message=data_req_msg)])
    submit = SubmitField('Create contact person')


# Form for registering new users.
class UpdateAccountForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Last name', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email',
                        validators=[DataRequired(message=data_req_msg), Email(message="Not valid email")])
    submit = SubmitField('Update account')

    # Custom validation to validate that email is not in use
    def validate_email(self, email):
        if email.data != current_user.email:
            # Get the email from the form and query the DB for it
            email = User.query.filter_by(email=email.data).first()
            # If the DB query returns something, raise validation error
            if email:
                raise ValidationError('Entered email is already in use')
class AddOrganizationForm(FlaskForm):
    # List of countries for the country selection
    # TODO: Should this be queried from DB or from external API?
    countries = [('Finland', 'Finland'), ('Sweden', 'Sweden'), ('Norway', 'Norway'), ('Germany', 'Germany')]
    
    # contact_persons = Contactperson.query.all()
    # contact_person_list = []
    # Loop through the contact persons and create array for SelectField with format ('id', 'value')
    # TODO: Don't show users full names to everyone!
    # for contact_person in contact_persons:
    #     fullname_id = contact_person.first_name[:2].lower() + contact_person.last_name.lower()
    #     fullname = contact_person.first_name + ' ' + contact_person.last_name
    #     contact_person_list.append((fullname_id, fullname))

    org_name = StringField('Organization name', validators=[DataRequired(message=data_req_msg)])
    org_number = StringField('Organization id', validators=[DataRequired(message=data_req_msg)])
    address = StringField('Address', validators=[DataRequired(message=data_req_msg)])
    postal_code = StringField('Postal code', validators=[DataRequired(message=data_req_msg)])
    city = StringField('City', validators=[DataRequired(message=data_req_msg)])
    country = SelectField('Country', validators=[DataRequired(message=data_req_msg)], choices=countries)
    # Select field is not good field for this use case. Should be multiple checkboxes.
    # TODO: Add logic to add BooleanFields for each organization type
    org_type = SelectField('Organization type', coerce=int)
    submit = SubmitField('Create organization')

    def __init__(self, *args, **kwargs):
        """Initialize the class with the most recent DB data for SelectField."""
        # Query list of existing organizations types from DB when form is created
        super(AddOrganizationForm, self).__init__(*args, **kwargs)
        self.org_type.choices = [(org.id, org.title) for org in Orgtype.query.all()]

class AddOrgTypeForm(FlaskForm):
    title = StringField('Organization type title', validators=[DataRequired(message=data_req_msg)])
    description = TextAreaField('Description', validators=[DataRequired(message=data_req_msg)])
    submit = SubmitField('Create organization type')
