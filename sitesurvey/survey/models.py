from datetime import datetime

from sitesurvey import db
from sitesurvey.user.models import survey_contact_rel


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    requested_date = db.Column(db.DateTime) # Requested delivery date when the project is ready
    ready_date = db.Column(db.DateTime) # When the project was actually ready
    status = db.Column(db.String(30), nullable=False, default='created')

    # Location related information
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    coordinate_lat = db.Column(db.Float)
    coordinate_long = db.Column(db.Float)

    # Charger related information
    number_of_chargers = db.Column(db.Integer, nullable=False)
    cp_charging_power = db.Column(db.Float, nullable=False)
    installation_method = db.Column(db.String(30), nullable=False)
    concrete_foundation = db.Column(db.Boolean)

    # Installation related information
    grid_connection = db.Column(db.Integer)
    grid_cable = db.Column(db.String(15))
    max_power = db.Column(db.Float)
    consumption_fuse = db.Column(db.Integer)
    maincabinet_rating = db.Column(db.Integer)
    empty_fuses = db.Column(db.Boolean)
    number_of_slots = db.Column(db.Integer)
    signal_strength = db.Column(db.Float)
    installation_location = db.Column(db.String(255))

    # Foreign keys to User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    charger_id = db.Column(db.Integer, db.ForeignKey('charger.id'))

    # Many-to-Many relationships
    contact_person = db.relationship('Contactperson', secondary=survey_contact_rel, backref='surveys', lazy=True)

    def __repr__(self):
        return f'Survey <{self.id} | {self.name} | {self.address} | {self.postal_code} | {self.city}>'