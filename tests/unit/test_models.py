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

from sitesurvey.user.models import User

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email and password fields are defined correctly
    """
    user = User(first_name='Matti', last_name='Meikäläinen', email='matti@meikalainen.com')
    user.set_password('test_password123')
    assert user.first_name == 'Matti'
    assert user.last_name == 'Meikäläinen'
    assert user.email == 'matti@meikalainen.com'
    assert user.password != 'test_password123'
    assert user.check_password('test_password123')