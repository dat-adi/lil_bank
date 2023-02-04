"""
This file is for testing the status of the dashboard page.
"""
from django.test import Client, TestCase


class TestStatus(TestCase):
    def test_status(self):
        c: Client = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")
