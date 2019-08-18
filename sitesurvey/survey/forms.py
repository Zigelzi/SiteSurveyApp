from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, SelectField, FloatField, BooleanField, DateTimeField, DateField,
                     IntegerField, TextAreaField, SubmitField, RadioField)
from wtforms.validators import DataRequired, Email

from sitesurvey import data_req_msg
from sitesurvey.product.models import Charger


class SurveyForm(FlaskForm):
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
    pic_installation_location = FileField('Installation location', validators=[FileAllowed(['jpg', 'png']), DataRequired(message=data_req_msg)])
    pic_maincabinet = FileField('Main cabinet', validators=[FileAllowed(['jpg', 'png']), DataRequired(message=data_req_msg)])
    pic_subcabinet = FileField('Subcabinet', validators=[FileAllowed(['jpg', 'png'])])
    pic_additional = FileField('Additional picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

    # Append the ('id', 'title') tuple from all queried chargers to the lists passed to SelectFields
    def __init__(self, *args, **kwargs):
        """Initialize the class with the most recent DB data for SelectField."""
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.manufacturer.choices = [(charger.manufacturer.lower(), charger.manufacturer) for charger in Charger.query.all()]
        self.model.choices = [(charger.model.lower(), charger.model) for charger in Charger.query.all()]

class WorkorderForm(FlaskForm):
    title = StringField('Workorder title', validators=[DataRequired(message=data_req_msg)])
    requested_date = DateField('Requested ready date', validators=[DataRequired(message=data_req_msg)])
    organization_name = StringField('Organization name', validators=[DataRequired(message=data_req_msg)])
    location_name = StringField('Location name', validators=[DataRequired(message=data_req_msg)])
    public_chargers = IntegerField('Number of public chargers', validators=[DataRequired(message=data_req_msg)])
    public_installation_location = TextAreaField('Installation location description')
    public_charging_power = FloatField('Charging power of public chargers', validators=[DataRequired(message=data_req_msg)])
    private_chargers = IntegerField('Number of private chargers', validators=[DataRequired(message=data_req_msg)])
    private_installation_location = TextAreaField('Installation location description')
    private_charging_power = FloatField('Charging power of private chargers', validators=[DataRequired(message=data_req_msg)])
    attachment_1_title = StringField('Attachment title')
    attachment_1 = FileField('Attach file', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    attachment_2_title = StringField('Attachment title')
    attachment_2 = FileField('Attach file', validators=[FileAllowed(['jpg', 'png', 'pdf'])])
    attachment_3_title = StringField('Attachment title')
    attachment_3 = FileField('Attach file', validators=[FileAllowed(['jpg', 'png', 'pdf'])])

    installation_type = RadioField('Installation type', validators=[DataRequired(message=data_req_msg)],
                                    choices=[('turnkey', 'Turn-key installation'),
                                             ('charger', 'Charger installation')])
    submit = SubmitField('Create new workorder')

class LocationForm(FlaskForm):
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
	submit = SubmitField('Submit')
    