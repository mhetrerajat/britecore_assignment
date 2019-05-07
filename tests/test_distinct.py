import json

from tests.base import BaseTestCase


class DistinctResourceTestCase(BaseTestCase):
    def test_distinct(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_distinct()
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')

    def test_distinct_with_invalid_user(self):
        # Create User
        self.register_user('admin', 'admin2')

        response = self.get_distinct()
        self.assert401(response)
