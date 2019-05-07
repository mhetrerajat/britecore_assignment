import base64
import json
import os
from datetime import datetime

from flask_testing import TestCase

from app import create_app as _create_app
from app import db
from app.utils.parser import DataParser
from app.utils.url_builder import URLBuilder
from config import BASE_DIR

url_builder = URLBuilder()


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
        p = DataParser(path, query={'AGENCY_ID': '3'})
        p.parse()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def get_basic_auth_token(self):
        username = "admin"
        password = "admin"
        return 'Basic ' + base64.b64encode(
            bytes("{0}:{1}".format(username, password),
                  'ascii')).decode('ascii')

    def get_dashboard(self):
        return self.client.get(
            '/', headers={'Authorization': self.get_basic_auth_token()})

    def register_user(self, username, password):
        return self.client.post('/api/v1/auth/register',
                                data=json.dumps({
                                    'username': username,
                                    'password': password
                                }),
                                content_type='application/json')

    def get_agency(self, agency_id):
        return self.client.get(
            '/api/v1/detail/agency/{0}'.format(agency_id),
            headers={'Authorization': self.get_basic_auth_token()},
            content_type="application/json")

    def get_agencies(self, filters=None):
        url = url_builder.build('/api/v1/detail/agency', params=filters)
        return self.client.get(
            url, headers={'Authorization': self.get_basic_auth_token()})

    def create_agency(self, agency_id=None, id_missing=False):
        agency_id = datetime.utcnow().strftime(
            '%Y%m%d%H%M%S') if not agency_id else agency_id
        data = {
            'id': agency_id if not id_missing else None,
            'agency_appointment_year': 1957,
            'active_producers': 14,
            'max_age': 85,
            'min_age': 48,
            'vendor': 'Unknown',
            'comissions_start_year': 2011,
            'comissions_end_year': 2013
        }
        return self.client.post(
            '/api/v1/detail/agency',
            data=json.dumps(data),
            headers={'Authorization': self.get_basic_auth_token()},
            content_type='application/json')

    def get_distinct(self):
        return self.client.get(
            '/api/v1/distinct',
            headers={'Authorization': self.get_basic_auth_token()},
            content_type="application/json")

    def get_report(self, params):
        url = url_builder.build('/api/v1/report/', params=params)
        return self.client.get(
            url, headers={'Authorization': self.get_basic_auth_token()})

    def get_csv_report(self, params):
        url = url_builder.build('/api/v1/report/csv', params=params)
        return self.client.get(
            url, headers={'Authorization': self.get_basic_auth_token()})

    def get_summarized_data(self, filters, offset=None, limit=None):
        url = url_builder.build('/api/v1/summary/',
                                params=filters,
                                offset=offset,
                                limit=limit)
        return self.client.get(
            url, headers={'Authorization': self.get_basic_auth_token()})
