from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (StringField, IntegerField, SelectField, FloatField,
                     RadioField, TextAreaField, BooleanField, PasswordField, SubmitField)
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from sitesurvey.models import User

data_req_msg = 'Pakollinen kenttä'
chargers = [{'manufacturer':'Ensto', 'model':'EVF200', 'DC/AC':'AC'}, {'manufacturer':'Garo', 'model':'LS4', 'DC/AC':'AC'}, {'manufacturer':'Tritium', 'model':'Veefil', 'DC/AC':'DC'}]


class Customer(FlaskForm):
    first_name = StringField('Full name', validators=[DataRequired(message=data_req_msg)])
    title = StringField('Title', validators=[DataRequired(message=data_req_msg)])
    phone_number = StringField('Phone number', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email', validators=[DataRequired(message=data_req_msg),
                                                    Email(message='Ei voimassa oleva sähköposti')])
class LocationForm(FlaskForm):
    location_name = StringField('Location name', validators=[DataRequired(message=data_req_msg)])
    address = StringField('Address', validators=[DataRequired(message=data_req_msg)])
    postal_code = IntegerField('Postal code', validators=[DataRequired(data_req_msg)])
    city = StringField('City', validators=[DataRequired(message=data_req_msg)])
    coordinates = FloatField('Coordinates')

class Chargers(FlaskForm):
    dc_ac = SelectField('DC / AC', validators=[DataRequired(message=data_req_msg)],
                        choices=[('DC', 'DC'), ('AC', 'AC')])
    manufacturer = SelectField('Charger manufacturer', validators=[DataRequired(message=data_req_msg)],
                                choices=[('ensto','Ensto'), ('garo','Garo'), ('tritium','Tritium')])
    model = SelectField('Charger model', validators=[DataRequired(message=data_req_msg)],
                        choices=[('evf200','EVF200'), ('ls4','LS4'), ('veefil','Veefil')])
    charger_amount = IntegerField('Number of chargers', validators=[DataRequired(message=data_req_msg)])
    charging_power = FloatField('Charging point charging power (kW)', validators=[DataRequired(message=data_req_msg)])
    installation_method = RadioField('Installation method', validators=[DataRequired(message=data_req_msg)],
                                        choices=[('ground', 'Ground mounting'), ('wall', 'Wall mounted')])
    communication = SelectField('Communication', validators=[DataRequired(message=data_req_msg)],
                                choices=[('mobile_internal', 'Mobile with internal modem'),
                                        ('mobile_external', 'Mobile with external modem'),
                                        ('lan', 'LAN (ethernet) to customers network')])
    foundation = RadioField('Concrete foundation needed?', validators=[DataRequired(message=data_req_msg)],
                            choices=[('yes', 'Yes'), ('no', 'No')])

class Installation(FlaskForm):
    grid_connection = SelectField('Current grid connection', validators=[DataRequired(message=data_req_msg)],
                                    choices=[('25','25 A'),
                                            ('35','35 A'),
                                            ('50','50 A'),
                                            ('63','63 A'),
                                            ('80','80 A'),
                                            ('100','100 A'),
                                            ('125','125 A'),
                                            ('160','160 A'),
                                            ('200','200 A'),
                                            ('250','250 A'),
                                            ('over250','> 250 A')])
    grid_cable = StringField('Grid connection cable', validators=[DataRequired(message=data_req_msg)])
    max_power = FloatField('Max. peak power (past 12 mo)', validators=[DataRequired(message=data_req_msg)])
    consumption_point_fuse = SelectField('Consumption point fuse', validators=[DataRequired(message=data_req_msg)],
                                            choices=[('25','25 A'),
                                                    ('35','35 A'),
                                                    ('50','50 A'),
                                                    ('63','63 A'),
                                                    ('80','80 A'),
                                                    ('100','100 A'),
                                                    ('125','125 A'),
                                                    ('160','160 A'),
                                                    ('200','200 A'),
                                                    ('250','250 A'),
                                                    ('over250','> 250 A')])
    maincabinet_rating = SelectField('Main cabinet current rating (In)', validators=[DataRequired(message=data_req_msg)],
                                        choices=[('25','25 A'),
                                                ('35','35 A'),
                                                ('50','50 A'),
                                                ('63','63 A'),
                                                ('80','80 A'),
                                                ('100','100 A'),
                                                ('125','125 A'),
                                                ('160','160 A'),
                                                ('200','200 A'),
                                                ('250','250 A'),
                                                ('over250','> 250 A')])
    empty_fuses = RadioField('Empty fuse slots?', validators=[DataRequired(message=data_req_msg)],
                                choices=[('yes', 'Yes'), ('no', 'No')])
    number_of_slots = IntegerField('Number of empty fuse slots')
    signal_strength = FloatField('Mobile signal strength')
    installation_location = TextAreaField('Installation location')

class CreateUser(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Last name', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email',
                        validators=[DataRequired(message=data_req_msg), Email(message="Not valid email")])
    password = PasswordField('Password',
                             validators=[DataRequired(message=data_req_msg),
                                         Length(min=8, message="Password must be at least 8 characters")])
    confirm_pw = PasswordField('Confirm password',
                               validators= [DataRequired(message=data_req_msg), EqualTo('password', message="Passwords do not match")])
    submit = SubmitField('Create account')

    # Custom validation to validate that email is not in use
    def validate_email(self, email):

        # Get the email from the form and query the DB for it
        email = User.query.filter_by(email=email.data).first()

        # If the DB query returns something, raise validation error
        if email:
            raise ValidationError('This email is already in use')


# Form for logging in to the site.
class LogIn(FlaskForm):
    email = StringField('Sähköposti',
                        validators=[DataRequired(message=data_req_msg), Email(message="Ei voimassa oleva sähköposti")])
    password = PasswordField('Salasana',
                             validators=[DataRequired(message=data_req_msg)])
    remember = BooleanField('Muista minut')
    submit = SubmitField('Kirjaudu sisään')

# Form for registering new users.
class UpdateAccount(FlaskForm):
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


class AddCharger(FlaskForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired(message=data_req_msg)])
    model = StringField('Model name', validators=[DataRequired(message=data_req_msg)])
    product_no = StringField('Product number', validators=[DataRequired(message=data_req_msg)])
    price = FloatField('Price (€)', validators=[DataRequired(message=data_req_msg)])
    type_of_outlet = StringField('Type of outlet', validators=[DataRequired(message=data_req_msg)])
    no_of_outlets = IntegerField('Number of outlets', validators=[DataRequired(message=data_req_msg)])
    dc_ac = SelectField('DC/AC', validators=[DataRequired(message=data_req_msg)],
                        choices=[('ac','AC'),
                                 ('dc','DC')])
    communication = SelectField('Communication type', validators=[DataRequired(message=data_req_msg)],
                                 choices=[('mobile', 'Mobile (3G/4G)'),
                                         ('ethernet', 'Ethernet')])
    mounting_wall = BooleanField('Wall mountable')
    mounting_ground = BooleanField('Ground mountable')
    max_power =  FloatField('Maximum power (kW)', validators=[DataRequired(message=data_req_msg)])
    mcb = BooleanField('MCB in charger')
    rcd_typea = BooleanField('RCD type-A (30mA) in charger')
    rcd_typeb = BooleanField('RCD type-B (30mA) or 6mA DC detection in charger')
    automatic_rcd = BooleanField('Automatically reclosable RCD')
    pwr_outage_eq = BooleanField('Power outage equipment')
    mid_meter = BooleanField('MID-meter in charger')
    mid_readable = BooleanField('MID-meter readable from outside')
    max_cable_d = IntegerField('Maximum cable diameter (mm2)')
    cable_cu_allowed = BooleanField('Copper cable allowed')
    cable_al_allowed = BooleanField('Copper cable allowed')
    submit = SubmitField('Add charger')