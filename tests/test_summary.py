import json

from tests.base import BaseTestCase


class SummaryResourceTestCase(BaseTestCase):
    def test_summarized_data(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({'agency': '3'})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_missing_required_param(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({})
        json.loads(response.data.decode())

        self.assert400(response)

    def test_summarized_data_at_year_level(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({'agency': '3', 'year': '2005'})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_at_risk_state_level(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({
            'agency': '3',
            'risk_state': 'PA'
        })
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_at_multiple_levels(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({
            'agency': '3',
            'risk_state': 'PA',
            'product': 'WORKCOMP'
        })
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)
