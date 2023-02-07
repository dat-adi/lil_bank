from .test_base import BaseUserTest
from lil_bank.settings import LOGIN_URL
from accounts.forms import LoginForm


class TestStatus(BaseUserTest):
    def test_login_page_status(self):
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200, "The page seems to be down.")
        self.assertContains(response, text="Log in", status_code=200)

    def test_user_with_wrong_credentials(self):
        form = LoginForm()
        response = self.client.post(LOGIN_URL, form={
            'username': self.USERNAME,
            'password': self.PASSWORD + "1",
        }, follow=False)
        self.assertFormError(
            response,
            field=None,
            form=form,
            errors=[
                'Please enter a username and a password.'
            ]
        )

        """
        response = self.client.post(LOGIN_URL, data={
            'username': self.USERNAME + "abc",
            'password': self.PASSWORD,
        }, follow=False)
        self.assertContains(response, text="Log in", status_code=200)
        self.assertFormError(
            response,
            field=None,
            form='form',
            errors=[
                'Please enter a username and a password.'
            ]
        )"""

    def test_sign_up_page_status(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, text="Sign up", status_code=200)
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_logout_page_status(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

        response = self.client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 405, "The page is weirdly accessible")

#    def test_user_profile_status(self):
#        response = self.client.get('/accounts/user_profile/')
#        self.assertEqual(response.status_code, 200, "The page seems to be down.")


