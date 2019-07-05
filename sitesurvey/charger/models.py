from sitesurvey import db


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
    mounting_wall = db.Column(db.Boolean, nullable=False) # Can charger be mounted directly to wall?
    mounting_ground = db.Column(db.Boolean, nullable=False) # Can charger be installed to ground?
    max_power = db.Column(db.Float, nullable=False)
    mcb = db.Column(db.Boolean, nullable=False)
    rcd_typea = db.Column(db.Boolean, nullable=False)
    rcd_typeb = db.Column(db.Boolean, nullable=False)
    automatic_rcd = db.Column(db.Boolean, nullable=False)
    pwr_outage_eq = db.Column(db.Boolean, nullable=False)
    mid_meter = db.Column(db.Boolean, nullable=False)
    mid_readable = db.Column(db.Boolean, nullable=False) # Is the MID-meter readable from outside w/o tools
    max_cable_d = db.Column(db.Integer, nullable=False)
    cable_cu_allowed = db.Column(db.Boolean, nullable=False)
    cable_al_allowed = db.Column(db.Boolean, nullable=False)

    # Backref to surveys to query charger used in survey
    surveys = db.relationship('Survey', backref='charger', lazy=True)

    # Create FlaskForm SelectField choices tuple with format ('id', 'title')
    def manufacturer_choices(self):
        return (self.manufacturer.lower(), self.manufacturer)

    def model_choices(self):
        return (self.model.lower(), self.model)

    def __repr__(self):
        return f'Charger <{self.manufacturer} |{self.model} |{self.product_no} |{self.dc_ac} | {self.type_of_outlet} | {self.no_of_outlets} |{self.communication} | {self.max_power}>'
