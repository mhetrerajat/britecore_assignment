import json
import re

from tests.base import BaseTestCase


class ReportTestCases(BaseTestCase):
    def test_report_api(self):
        # Create User
        self.register_user('admin', 'admin')

        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007'
        }
        response = self.get_report(params)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_report_api_with_aggregation(self):
        # Create User
        self.register_user('admin', 'admin')

        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007',
            'aggregation': 'mean'
        }
        response = self.get_report(params)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_report_api_with_filters(self):
        # Create User
        self.register_user('admin', 'admin')

        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007',
            'aggregation': 'mean',
            'agency': '3',
            'product_line': 'CL'
        }
        response = self.get_report(params)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_report_api_invalid_group_by(self):
        # Create User
        self.register_user('admin', 'admin')

        params = {
            'group_by': 'some_random_group_by',
            'start_year': '2005',
            'end_year': '2007'
        }
        response = self.get_report(params)
        json.loads(response.data.decode())

        self.assert400(response)

    def test_csv_report(self):
        # Create User
        self.register_user('admin', 'admin')

        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007'
        }
        response = self.get_csv_report(params)
        content = response.headers["Content-Disposition"]
        _pattern = re.search('.csv$', content)
        extension = _pattern.group(0) if _pattern else None
        self.assertEqual(extension, '.csv')
        self.assert200(response)
