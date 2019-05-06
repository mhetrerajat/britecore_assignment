import json

from tests.base import BaseTestCase


class DetailAgencyItemResourceTestCase(BaseTestCase):
    def test_get_agency(self):

        # Create User
        self.register_user('admin', 'admin')

        agency_id = "3"
        response = self.get_agency(agency_id)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
