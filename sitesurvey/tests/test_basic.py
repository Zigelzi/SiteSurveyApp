import os
import sys
import unittest

parent_dir = os.path.dirname

# Add the package root directory to sys.path so imports work
sys.path.append(parnet_dir(parnet_dir(parnet_dir(os.path.abspath(__file__)))))

from sitesurvey.config import basedir
from sitesurvey import app, db

TEST_DB = 'test.db'
sql_lite_db_uri = 'sqlite:///' + os.path.join(basedir, TEST_DB) 

class BasicTest(unittest.TestCase):

    # Setting up and tearing down the Flask app for testing purposes

    # setUp method to execute before every test case
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = sql_lite_db_uri
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        def tearDown(self):
            pass

    # TESTS
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()