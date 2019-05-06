import json

from tests.base import BaseTestCase


class SummaryResourceTestCase(BaseTestCase):
    def test_summarized_data_no_filters(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_filters(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({'year': '2005'})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_filters_risk_state(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({'risk_state': 'PA'})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_multiple_filters(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({
            'risk_state': 'PA',
            'product': 'WORKCOMP'
        })
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_offset_and_limit(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_summarized_data({}, offset=2, limit=2)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)
