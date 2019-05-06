import json

from app import db
from app.models import User
from tests.base import BaseTestCase


class AuthResourcesTestCase(BaseTestCase):
    def test_registration(self):
        response = self.register_user('admin', 'admin')
        data = json.loads(response.data.decode())

        self.assertEqual(data.get('status'), 'success')
        self.assertEqual(data.get('data', {}).get('username'), 'admin')

    def test_register_duplicate_user(self):
        user = User(username='admin', password='admin')
        db.session.add(user)
        db.session.commit()

        with self.client:
            response = self.register_user('admin', 'admin')
            data = json.loads(response.data.decode())

            self.assert400(response)
            self.assertEqual(data.get('status'), 'failed')

    def test_missing_params(self):
        with self.client:
            response = self.register_user(None, 'admin')
            data = json.loads(response.data.decode())

            self.assert400(response)
            self.assertEqual(data.get('status'), 'failed')
