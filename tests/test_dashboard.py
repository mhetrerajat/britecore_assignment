
from tests.base import BaseTestCase


class DashboardResourceTestCase(BaseTestCase):
    def test_dashboard(self):
        # Create User
        self.register_user('admin', 'admin')

        response = self.get_dashboard()
        self.assert200(response)
