"""
This file is for testing the status of the dashboard page.
"""
from django.test import TestCase


class TestStatus(TestCase):
    def test_landing_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_about_page_status(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

