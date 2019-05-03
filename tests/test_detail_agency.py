import json
from random import randint

from tests.base import BaseTestCase


def get_agencies(self):
    return self.client.get('/api/v1/detail/agency')


def create_agency(self):
    data = {
        'id': str(randint(5000, 10000)),
        'agency_appointment_year': 1957,
        'active_producers': 14,
        'max_age': 85,
        'min_age': 48,
        'vendor': 'Unknown',
        'comissions_start_year': 2011,
        'comissions_end_year': 2013
    }
    return self.client.post('/api/v1/detail/agency',
                            data=json.dumps(data),
                            content_type='application/json')


class DetailAgencyResourceTestCase(BaseTestCase):
    def test_get_agencies(self):
        response = get_agencies(self)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')

    def test_create_agency(self):
        response = create_agency(self)
        json.loads(response.data.decode())

        self.assert200(response)
