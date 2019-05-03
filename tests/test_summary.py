import json

from app.utils.url_builder import URLBuilder
from tests.base import BaseTestCase

url_builder = URLBuilder()


def get_summarized_data(self, filters, offset=None, limit=None):
    url = url_builder.build('/api/v1/summary/',
                            params=filters,
                            offset=offset,
                            limit=limit)
    return self.client.get(url)


class SummaryResourceTestCase(BaseTestCase):
    def test_summarized_data_no_filters(self):
        response = get_summarized_data(self, {})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_filters(self):
        response = get_summarized_data(self, {'year': '2005'})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_filters_risk_state(self):
        response = get_summarized_data(self, {'risk_state': 'PA'})
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_multiple_filters(self):
        response = get_summarized_data(self, {
            'risk_state': 'PA',
            'product': 'WORKCOMP'
        })
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)

    def test_summarized_data_with_offset_and_limit(self):
        response = get_summarized_data(self, {}, offset=2, limit=2)
        data = json.loads(response.data.decode())

        self.assert200(response)
        self.assertEqual(data.get('status'), 'success')
        self.assertGreater(len(data.get('data', [])), 0)
