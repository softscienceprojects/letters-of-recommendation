from datetime import datetime, timedelta
import unittest

from app import create_app, db
from app.models import *
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelTests(unittest.TestCase):
    """
    Run this from the command line with `python tests.py` to see the test suite run.

    """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
        


if __name__ == '__main__':
    unittest.main(verbosity=2)
