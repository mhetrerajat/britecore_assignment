import json

from tests.base import BaseTestCase


def hello_endpoint(self):
    return self.client.get('/api/v1/', content_type="application/json")


class HelloResourceTestCase(BaseTestCase):
    def test_hello_endpoint(self):
        response = hello_endpoint(self)
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'success')
        self.assert200(response)
