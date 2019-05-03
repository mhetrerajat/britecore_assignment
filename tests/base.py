import os

from flask_testing import TestCase

from app import create_app as _create_app
from app import db
from app.utils.parser import DataParser
from config import BASE_DIR


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = _create_app('test')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

        # Add dummy data
        path = os.path.join(BASE_DIR, "sample_data.csv")
        p = DataParser(path, sample_size=0.5, query={'AGENCY_ID': '3'})
        p.parse()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
