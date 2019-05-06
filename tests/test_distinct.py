import json

from tests.base import BaseTestCase


class DistinctResourceTestCase(BaseTestCase):
    def test_hello_endpoint(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_distinct()
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
