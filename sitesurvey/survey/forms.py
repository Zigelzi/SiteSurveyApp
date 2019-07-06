from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, FloatField, BooleanField, DateTimeField,
                     IntegerField, TextAreaField, SubmitField, RadioField)
from wtforms.validators import DataRequired, Email

from sitesurvey import data_req_msg
from sitesurvey.charger.models import Charger


class SurveyForm(FlaskForm):
    # Query charger information from database and create SelectField tuples for every charger
    # chargers = Charger.query.all()
    # manufacturer_choices = []
    # model_choices = []

    # for charger in chargers:
    #     manufacturer_choices.append(charger.manufacturer_choices())
    #     model_choices.append(charger.model_choices())

    # Contact person selections
    first_name = StringField('First name', validators=[DataRequired(message=data_req_msg)])
    last_name = StringField('Last name', validators=[DataRequired(message=data_req_msg)])
    title = StringField('Title', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email', validators=[DataRequired(message=data_req_msg),
                                             Email(message='Not valid email')])

    phone_number = StringField('Phone number', validators=[DataRequired(message=data_req_msg)])

    # Location selections                                                    
    location_name = StringField('Location name', validators=[DataRequired(message=data_req_msg)])
    address = StringField('Address', validators=[DataRequired(message=data_req_msg)])
    postal_code = StringField('Postal code', validators=[DataRequired(data_req_msg)])
    city = StringField('City', validators=[DataRequired(message=data_req_msg)])
    country = SelectField('Country', validators=[DataRequired(message=data_req_msg)],
                                     choices=[('Finland', 'Finland'),
                                              ('Sweden', 'Sweden'),
                                              ('Norway', 'Norway'),
                                              ('Germany', 'Germany')])
    coordinate_lat = FloatField('Lateral coordinates')
    coordinate_long = FloatField('Longitudal coordinates')

    # Charger selections
    dc_ac = SelectField('DC / AC', validators=[DataRequired(message=data_req_msg)],
                        choices=[('DC', 'DC'), ('AC', 'AC')])
    manufacturer = SelectField('Charger manufacturer', validators=[DataRequired(message=data_req_msg)])
    model = SelectField('Charger model', validators=[DataRequired(message=data_req_msg)])
    charger_amount = IntegerField('Number of chargers', validators=[DataRequired(message=data_req_msg)])
    charging_power = FloatField('Charging point charging power (kW)', validators=[DataRequired(message=data_req_msg)])
    installation_method = RadioField('Installation method', validators=[DataRequired(message=data_req_msg)],
                                        choices=[('ground', 'Ground mounting'),
                                                 ('wall', 'Wall mounted')])
    communication = SelectField('Communication', validators=[DataRequired(message=data_req_msg)],
                                choices=[('mobile_internal', 'Mobile with internal modem'),
                                        ('mobile_external', 'Mobile with external modem'),
                                        ('lan', 'LAN (ethernet) to customers network')])
    foundation = BooleanField('Concrete foundation needed?')

    # Installation selections
    requested_date = DateTimeField('Requested delivery date', validators=[DataRequired(message=data_req_msg)],format='%d.%m.%Y')
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
    empty_fuses = BooleanField('Empty fuse slots?')
    number_of_slots = IntegerField('Number of empty fuse slots')
    signal_strength = FloatField('Mobile signal strength')
    installation_location = TextAreaField('Installation location')
    submit = SubmitField('Submit')

    #TODO: Add image upload fields
    # Image of main cabinet
    # Image of installation location
    # Image of subcabinet (optional)
    # Additional image
    # Additional image

    # Append the ('id', 'title') tuple from all queried chargers to the lists passed to SelectFields
    def __init__(self, *args, **kwargs):
        """Initialize the class with the most recent DB data for SelectField."""
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.manufacturer.choices = [(charger.manufacturer.lower(), charger.manufacturer) for charger in Charger.query.all()]
        self.model.choices = [(charger.model.lower(), charger.model) for charger in Charger.query.all()]