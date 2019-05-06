import json

from tests.base import BaseTestCase


class DetailAgencyResourceTestCase(BaseTestCase):
    def test_get_agencies(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_agencies()
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')

    def test_get_agencies_with_filters(self):
        # Create User
        self.register_user('admin', 'admin')

        filters = {'agency_appointment_year': "1957"}
        response = self.get_agencies(filters=filters)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')

    def test_create_agency(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.create_agency()
        json.loads(response.data.decode())

        self.assert200(response)

    def test_create_agency_without_id(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.create_agency(id_missing=True)
        json.loads(response.data.decode())

        self.assert400(response)
