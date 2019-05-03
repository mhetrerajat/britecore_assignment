import json

from app.utils.url_builder import URLBuilder
from tests.base import BaseTestCase
import re

url_builder = URLBuilder()


def get_report(self, params):
    url = url_builder.build('/api/v1/report/', params=params)
    return self.client.get(url)


def get_csv_report(self, params):
    url = url_builder.build('/api/v1/report/csv', params=params)
    return self.client.get(url)


class ReportTestCases(BaseTestCase):
    def test_report_api(self):
        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007'
        }
        response = get_report(self, params)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_report_api_with_aggregation(self):
        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007',
            'aggregation': 'mean'
        }
        response = get_report(self, params)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_report_api_with_filters(self):
        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007',
            'aggregation': 'mean',
            'agency': '3',
            'product_line': 'CL'
        }
        response = get_report(self, params)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_report_api_invalid_group_by(self):
        params = {
            'group_by': 'some_random_group_by',
            'start_year': '2005',
            'end_year': '2007'
        }
        response = get_report(self, params)
        data = json.loads(response.data.decode())

        self.assert400(response)

    def test_csv_report(self):
        params = {
            'group_by': 'year',
            'group_by': 'agency',
            'start_year': '2005',
            'end_year': '2007'
        }
        response = get_csv_report(self, params)
        content = response.headers["Content-Disposition"]
        _pattern = re.search('.csv$', content)
        extension = _pattern.group(0) if _pattern else None
        self.assertEqual(extension, '.csv')
        self.assert200(response)