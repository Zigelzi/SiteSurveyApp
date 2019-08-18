from datetime import datetime, time

from flask_login import UserMixin
import jwt

from sitesurvey import db, app, login_manager, bcrypt



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Many to many relationship tables

# Organizations and organization association table
org_type_rel = db.Table('org_type',
                        db.Column('org_id', db.Integer, db.ForeignKey('organization.id')),
                         db.Column('type_id', db.Integer, db.ForeignKey('orgtype.id'))
                         )

# Surveys and contact person association table
survey_contact_rel = db.Table('survey_contact_person',
                        db.Column('survey_id', db.Integer, db.ForeignKey('survey.id')),
                         db.Column('contact_id', db.Integer, db.ForeignKey('contactperson.id'))
                         )

class User(db.Model, UserMixin):
    # When the login token expires in seconds
    expires_sec = 1800

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # Foreign keys
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))

    # Backref to show surveys done by user
    surveys = db.relationship('Survey', backref='user', lazy=True)

    def set_password(self, password):
        """Set the password of the user"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check that the submitted password matches to password stored in DB."""
        return bcrypt.check_password_hash(self.password, password)

    def get_password_token(self, expires_in=600):
        """Create JWT token for password reset email which expire time is specified in expises_in variable.
            Returns UTF-8 formatted JWT token to attach reset email"""
        return jwt.encode({'reset_password':self.id, 'exp': time() + expires_in}, 
                            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_password_token(token):
        """Check that the submitted token for password reset matches to token created by the application and returns the user information if token is correct"""
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                             algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f'User <{self.first_name} | {self.last_name} | {self.email} |>'

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(100), nullable=False)
    org_number = db.Column(db.String(20), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    country = db.Column(db.String(30), nullable=False)

    # One-to-many and many-to-many relations
    org_type = db.relationship('Orgtype', secondary=org_type_rel, backref='organizations', lazy=True)
    contact_persons = db.relationship('Contactperson', backref='organization', lazy=True)
    users = db.relationship('User', backref='organization', lazy=True)

    # Foreign keys
    workorder_id = db.Column(db.Integer, db.ForeignKey('workorder.id'))
    
    def __repr__(self):
        return f'Organization <{self.org_name} | {self.org_number} | {self.city} | {self.country}'

class Orgtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'Organization type <{self.title} | {self.description}>'

class Contactperson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(40))
    email = db.Column(db.String(120))
    phone_number = db.Column(db.String(20))

    # Foreign keys
    parent_org = db.Column(db.Integer, db.ForeignKey('organization.id'))

    def __repr__(self):
        return f' ContactPerson <{self.first_name} | {self.last_name} | {self.title} |{self.email} | {self.phone_number}>'