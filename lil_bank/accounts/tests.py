from django.test import TestCase


class TestStatus(TestCase):
    def test_login_page_status(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_sign_up_page_status(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_logout_page_status(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")
