import json

from tests.base import BaseTestCase


def get_agency(self, agency_id):
    return self.client.get('/api/v1/detail/agency/{0}'.format(agency_id),
                           content_type="application/json")


class DetailAgencyItemResourceTestCase(BaseTestCase):
    def test_get_agency(self):
        agency_id = "3"
        response = get_agency(self, agency_id)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
