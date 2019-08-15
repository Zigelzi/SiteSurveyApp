from datetime import datetime

from sitesurvey import db
from sitesurvey.user.models import survey_contact_rel
from sitesurvey.product.models import Product, Productcategory

# Many-to-Many relationship table(s)
product_category_rel = db.Table('product_category',
                        db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
                         db.Column('product_category_id', db.Integer, db.ForeignKey('productcategory.id'))
                         )

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(30), nullable=False, default='created')

    # Installation related information
    installation_method = db.Column(db.String(30), nullable=False)
    concrete_foundation = db.Column(db.Boolean)
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
    workorder_id = db.Column(db.Integer, db.ForeignKey('workorder.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    # Table relationshipts and backrefs
    contact_person = db.relationship('Contactperson', secondary=survey_contact_rel, backref='surveys', lazy=True)
    pictures = db.relationship('Surveypicture', backref='survey', lazy=True)

    def __repr__(self):
        return f'Survey <Survey ID {self.id} | Workorder ID {self.workorder_id}>'

class Surveypicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    picture_filename = db.Column(db.String(15), nullable=False)

    # Foreign keys
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

    def __repr__(self):
        return f'Survey picture <{self.title}>'

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    coordinate_lat = db.Column(db.Float)
    coordinate_long = db.Column(db.Float)

    # Backref to Workorder table
    workorders = db.relationship('Workorder', backref='location', lazy=True)
    surveys = db.relationship('Survey', backref='location', lazy=True)

    def __repr__(self):
        return f'Location <{self.name} | {self.address} | {self.postal_code} | {self.city} | {self.country}>'

class Workorder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)

    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    requested_date = db.Column(db.DateTime) # Requested delivery date when the project is ready
    ready_date = db.Column(db.DateTime) # When the project was actually ready
    status = db.Column(db.String(30), nullable=False, default='created')
    
    public_chargers = db.Column(db.Integer, nullable=False)
    public_installation_location = db.Column(db.Text, nullable=False)
    public_charging_power = db.Column(db.Float, nullable=False)

    private_chargers = db.Column(db.Integer, nullable=False)
    private_installation_location = db.Column(db.Text, nullable=False)
    private_charging_power = db.Column(db.Float, nullable=False)
    installation_type = db.Column(db.String(10), nullable=False)

    # Foreign keys
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))

    # Backrefs
    line_items = db.relationship('Lineitem', backref='workorder', lazy=True)
    attachments = db.relationship('Workorderattachment', backref='workorder', lazy=True)

    def __repr__(self):
        return f'Workorder <{self.id} | {self.title} | Created {self.create_date} | Updated {self.update_date} | {self.status}>'

class Workorderattachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    picture_filename = db.Column(db.String(15), nullable=False)

    # Foreign keys
    workorder_id = db.Column(db.Integer, db.ForeignKey('workorder.id'))

    def __repr__(self):
        return f'Attachment <{self.title}>'

class Lineitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discount = db.Column(db.DECIMAL(3,2), default=0.00)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    
    # Foreign keys
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    workorder_id = db.Column(db.Integer, db.ForeignKey('workorder.id'))

    def __repr__(self):
        return f'LineItem <{self.id} | {self.quantity} | {self.total}>'



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign keys
    workorder_id = db.Column(db.Integer, db.ForeignKey('workorder.id'))

    def __repr__(self):
        return f'<Comment <{self.comment} | Created {self.create_date} | Updated {self.update_date}> '
