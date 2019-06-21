from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email

data_req_msg = 'Pakollinen kenttä'
chargers = [{'manufacturer':'Ensto', 'model':'EVF200', 'DC/AC':'AC'}, {'manufacturer':'Garo', 'model':'LS4', 'DC/AC':'AC'}, {'manufacturer':'Tritium', 'model':'Veefil', 'DC/AC':'DC'}]


class Customer(FlaskForm):
    first_name = StringField('Full name', validators=[DataRequired(message=data_req_msg)])
    title = StringField('Title', validators=[DataRequired(message=data_req_msg)])
    phone_number = StringField('Phone number', validators=[DataRequired(message=data_req_msg)])
    email = StringField('Email', validators=[DataRequired(message=data_req_msg),
                                                    Email(message='Ei voimassa oleva sähköposti')])
class Location(FlaskForm):
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

