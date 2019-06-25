from sitesurvey import db, app, login_manager, bcrypt
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# TODO: Sort out the many-to-many relationships

# Many to many relationship tables

# How organizations and organization types are related
org_type_rel = db.Table('org_type',
                        db.Column('org_id', db.Integer, db.ForeignKey('organization.id')),
                         db.Column('type_id', db.Integer, db.ForeignKey('orgtype.id'))
                         )

# How organizations and contact persons are related
contact_person_rel = db.Table('org_contact_person',
                        db.Column('org_id', db.Integer, db.ForeignKey('organization.id')),
                         db.Column('contact_id', db.Integer, db.ForeignKey('contactperson.id'))
                         )

# How surveys and contact persons are related
survey_contact_rel = db.Table('survey_contact_person',
                        db.Column('survey_id', db.Integer, db.ForeignKey('survey.id')),
                         db.Column('contact_id', db.Integer, db.ForeignKey('contactperson.id'))
                         )

# How surveys and locations are related
survey_llocation_rel = db.Table('survey_location',
                        db.Column('survey_id', db.Integer, db.ForeignKey('survey.id')),
                         db.Column('location_id', db.Integer, db.ForeignKey('location.id'))
                         )

class User(db.Model, UserMixin):
    # When the login token expires in seconds
    expires_sec = 1800

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Backref to show surveys done by user surveys model
    surveys = db.relationship('Survey', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f'User <{self.first_name} | {self.last_name} | {self.email}>'

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(100), nullable=False)
    org_number = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"""Organization <{self.org_name} | {self.org_number} | {self.address} | {self.postal_code} |
                                 {self.city} | {self.country}"""

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grid_connection = db.Column(db.Integer)
    grid_cable = db.Column(db.String(15))
    max_power = db.Column(db.Float)
    consumtion_fuse = db.Column(db.Integer)
    maincabinet_rating = db.Column(db.Integer)
    empty_fuses = db.Column(db.Boolean)
    number_of_slots = db.Column(db.Integer)
    signal_strength = db.Column(db.Float)
    installation_location = db.Column(db.String(255))

    # Foreign keys to User and Charger models
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    charger_id = db.Column(db.Integer(), db.ForeignKey('charger.id'))

    def __repr__(self):
        return f""" Survey <{self.id} |{self.grid_connection} |{self.grid_cable} | {self.max_power} |
                            {self.maincabinet_rating}>"""

class Charger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    product_no = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    type_of_outlet = db.Column(db.String(10), nullable=False)
    no_of_outlets = db.Column(db.Integer) # Number of outlets in the charger
    dc_ac = db.Column(db.String(2), nullable=False)
    communication = db.Column(db.String(20), nullable=False)
    mounting = db.Column(db.String(50), nullable=False) # How charger is mounted in place (wall, ground etc)
    max_power = db.Column(db.Float, nullable=False)
    mcb = db.Column(db.Boolean, nullable=False)
    rcd_typea = db.Column(db.Boolean, nullable=False)
    rcd_typeb = db.Column(db.Boolean, nullable=False)
    automatic_rcd = db.Column(db.Boolean, nullable=False)
    pwr_outage_eq = db.Column(db.Boolean, nullable=False)
    mid_meter = db.Column(db.Boolean, nullable=False)
    mid_readabe = db.Column(db.Boolean, nullable=False) # Is the MID-meter readable from outside w/o tools
    max_cable_d = db.Column(db.Integer, nullable=False)

    # Backref to survey to see which chargers are used in which surveys
    charger_id = db.relationship('Survey', backref='charger', lazy='dynamic')

    def __repr__(self):
        return f"""Charger <{self.manufacturer} |{self.model} |{self.product_no} |{self.dc_ac} |
                            {self.type_of_outlet} |{self.no_of_outlets} |{self.communication} | 
                            {self.max_power}>"""

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    coordinate_lat = db.Column(db.Float)
    coordinate_long = db.Column(db.Float)

    def __repr__(self):
        return f"""Location <{self.name} |{self.address} |{self.postal_code} |{self.city} |
                            {self.country}>"""

class OrgType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'OrgType <{self.title} | {self.description}>'

class ContactPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(40))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(20))

    def __repr__(self):
        return f' ContactPerson <{self.first_name} | {self.last_name} | {self.title} |{self.email} | {self.phone_number}>'