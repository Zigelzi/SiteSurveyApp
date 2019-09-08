"""
Unit tests for the sitesurvey.BLUEPRINT_NAME.models files. BLUEPRINT_NAME is the name of the 
blueprint package (folder) name under the main sitesurvey package.

"""
import os
import sys
import pytest
from datetime import datetime

parent_dir = os.path.dirname

# Add the package root directory to sys.path so imports work
sys.path.append(parent_dir(parent_dir(parent_dir(os.path.abspath(__file__)))))



"""
+ ---------------------------------------- +
| PRODUCT PACKAGE MODELS                   |
| Unit tests for sitesurvey.product.models |
+ ---------------------------------------- +
"""
from sitesurvey.product.models import Product, Productcategory

def test_new_product():
    """
    GIVEN a Product model
    WHEN a new Product is created
    THEN check that the product_number, product_name, unit_of_material and price fields are defined correctly
    """
    product = Product(product_number='CND-1000',
                      product_name='Product of testing',
                      unit_of_material='pcs' ,
                      price=1234.99)
    assert product.product_number == 'CND-1000'
    assert product.product_name == 'Product of testing'
    assert product.unit_of_material == 'pcs'
    assert product.price == 1234.99

def test_new_productcategory():
    """
    GIVEN a Productcategory model
    WHEN a new Productcategory is created
    THEN check that the title and description fields are defined correctly
    """
    product_category = Productcategory(title='Charger', description='Charger product group for testings')
    assert product_category.title == 'Charger'
    assert product_category.description == 'Charger product group for testings'

"""
+ ---------------------------------------- +
| SURVEY PACKAGE MODELS                    |
| Unit tests for sitesurvey.survey.models  |
+ ---------------------------------------- +
"""
from sitesurvey.survey.models import Survey

def test_new_survey():
    now = datetime.utcnow()
    survey = Survey(create_date=now,
                    update_date=now,
                    status='created',
                    installation_method='Ground',
                    concrete_foundation=False,
                    grid_connection=63,
                    grid_cable='AXMK 50+50',
                    max_power=33.2,
                    consumption_fuse=63,
                    maincabinet_rating=250,
                    empty_fuses=True,
                    number_of_slots=2,
                    signal_strength=-33.2,
                    installation_location='Testing parking garage at parking hall P2')
    assert survey.create_date == now
    assert survey.status == 'created'
    assert survey.installation_method == 'Ground'
    assert survey.concrete_foundation == False
    assert survey.grid_connection == 63
    assert survey.grid_cable == 'AXMK 50+50'
    assert survey.max_power == 33.2
    assert survey.consumption_fuse == 63
    assert survey.maincabinet_rating == 250
    assert survey.empty_fuses == True
    assert survey.number_of_slots == 2
    assert survey.signal_strength == -33.2
    assert survey.installation_location == 'Testing parking garage at parking hall P2'


""" 
+ ---------------------------------------- +
| USER PACKAGE MODELS                      |
| Unit tests for sitesurvey.product.models |
+ ---------------------------------------- +
"""
from sitesurvey.user.models import User, Organization, Orgtype, Contactperson

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that the first_name, last_name, email and password fields are defined correctly
    """
    user = User(first_name='Matti', last_name='Meikäläinen', email='matti@meikalainen.com')
    user.set_password('test_password123')
    assert user.first_name == 'Matti'
    assert user.last_name == 'Meikäläinen'
    assert user.email == 'matti@meikalainen.com'
    assert user.password != 'test_password123'
    assert user.check_password('test_password123')

def test_new_organization():
    """
    GIVEN a Organization model
    WHEN a new Organization is created
    THEN check that the org_name, org_number, address, postal_code, city and country
    fields are defined correctly
    """
    organization = Organization(org_name='Test Org',
                                org_number='1234567-9',
                                address='Organization street 1',
                                postal_code='00100',
                                city='Testilä',
                                country='Finland')
    assert organization.org_name =='Test Org'
    assert organization.org_number =='1234567-9'
    assert organization.address == 'Organization street 1'
    assert organization.postal_code == '00100'
    assert organization.city == 'Testilä'
    assert organization.country == 'Finland'

def test_new_orgtype():
    """
    GIVEN a Orgtype model
    WHEN a new Orgtype is created
    THEN check that the title and description fields are defined correctly
    """
    org_type = Orgtype(title='Contractor', description='This is a testing organization type')
    assert org_type.title == 'Contractor'
    assert org_type.description == 'This is a testing organization type'

def test_new_contactperson():
    """
    GIVEN a Contactperson model
    WHEN a new Contactperson is created
    THEN check that the first_name, last_name, title, email and phone number fields are 
    defined correctly
    """
    contact_person = Contactperson(first_name='Konsta',
                                   last_name='Kontakti',
                                   title='Property manager',
                                   email='konsta@kikkailija.com',
                                   phone_number='+358401231234')
    assert contact_person.first_name == 'Konsta'
    assert contact_person.last_name == 'Kontakti'
    assert contact_person.title == 'Property manager'
    assert contact_person.email == 'konsta@kikkailija.com'
    assert contact_person.phone_number == '+358401231234'