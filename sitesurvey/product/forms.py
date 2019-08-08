from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

from sitesurvey import data_req_msg

class AddChargerForm(FlaskForm):
    manufacturer = StringField('Manufacturer', validators=[DataRequired(message=data_req_msg)])
    model = StringField('Model name', validators=[DataRequired(message=data_req_msg)])
    product_no = StringField('Product number', validators=[DataRequired(message=data_req_msg)])
    price = FloatField('Price (€)', validators=[DataRequired(message=data_req_msg)])
    type_of_outlet = SelectField('Type of outlet', validators=[DataRequired(message=data_req_msg)],
                                 choices=[('type2_socket', 'Type2 socket'),
                                          ('type2_cable', 'Type2 fixed cable'),
                                          ('chademo', 'CHAdeMO cable'),
                                          ('ccs', 'CCS cable'),
                                          ('chademo_ccs', 'CHAdeMO + CCS cables'),
                                          ('chademo_ccs_type2', 'CHAdeMO + CCS + Type2 cables')])
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
    cable_al_allowed = BooleanField('Aluminium cable allowed')
    submit = SubmitField('Add charger')

