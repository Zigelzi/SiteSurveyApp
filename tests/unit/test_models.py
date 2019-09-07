"""
Unit tests for the sitesurvey.BLUEPRINT_NAME.models files. BLUEPRINT_NAME is the name of the 
blueprint package (folder) name under the main sitesurvey package.

"""
import os
import sys
import pytest

parent_dir = os.path.dirname

# Add the package root directory to sys.path so imports work
sys.path.append(parent_dir(parent_dir(parent_dir(os.path.abspath(__file__)))))

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