from django.test import TestCase

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('localhost:8000')
        self.assertEqual(response.status_code, 200)

    def test_index_loads_properly(self):
        """The index page failed to load properly"""
        response = self.client.get('localhost:8000')
        self.assertEqual(response.status_code, 404)
# Add other test-suite