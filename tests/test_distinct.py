import json

from tests.base import BaseTestCase


def get_distinct(self):
    return self.client.get('/api/v1/distinct', content_type="application/json")


class DistinctResourceTestCase(BaseTestCase):
    def test_hello_endpoint(self):
        response = get_distinct(self)
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'success')
        self.assert200(response)
