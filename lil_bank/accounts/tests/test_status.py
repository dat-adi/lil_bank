from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Customer, Account
from lil_bank.settings import LOGIN_URL


class TestStatus(TestCase):
    '''
    Test cases for URLs an unauthenticated user might try to access.
    '''
    def test_login_page_status(self):
        response = self.client.get(LOGIN_URL)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text="Log In", status_code=200)

    def test_sign_up_page_status(self):
        response = self.client.get('/accounts/signup/')
        self.assertContains(response, text="Sign up", status_code=200)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_logout_page_status(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text="Log In", status_code=200)

        response = self.client.post('/accounts/logout/')
        self.assertEqual(
            response.status_code, 405, "The page is weirdly accessible"
        )

    def test_account_list_status(self):
        response = self.client.get('/accounts/', follow=True)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text="Log In", status_code=200)

    def test_view_account_status(self):
        response = self.client.get('/accounts/view_account/', follow=True)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text="Log In", status_code=200)

    def test_create_account_status(self):
        response = self.client.get('/accounts/create_account/', follow=True)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text="Log In", status_code=200)

    def test_invalid_operation_status(self):
        response = self.client.get('/accounts/invalid_operation/', follow=True)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text="Log In", status_code=200)


class TestStatusAuthenticated(TestCase):
    '''
    Test cases covering all URLs an authenticated user might access
    '''
    def setUp(self):
        # Create Test User and login
        self.user = User.objects.create(username='test')
        self.client.force_login(self.user)

        # Set up a customer and her account
        self.customer = Customer.objects.create(
            id=str(self.user.id),
            first_name="Test",
            last_name="User",
            address="#1 Test, User Nagar",
            phone="19199191"
        )
        self.account = Account.objects.create(
            type='checking',
            owner=self.customer,
            balance=10000
        )

    def tearDown(self) -> None:
        self.client.logout()
        self.account.delete()
        self.customer.delete()
        self.user.delete()
        return super().tearDown()

    def test_account_list_status(self):
        response = self.client.get('/accounts/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_account_detail_status(self):
        response = self.client.get(f'/accounts/{self.account.no}/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_view_account_status(self):
        response = self.client.get('/accounts/view_account/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_transactions_status(self):
        response = self.client.get(f'/accounts/{self.account.no}/transactions/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_balance_status(self):
        response = self.client.get(f'/accounts/{self.account.no}/balance/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_deposit_status(self):
        response = self.client.get(f'/accounts/{self.account.no}/deposit/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_withdraw_status(self):
        response = self.client.get(f'/accounts/{self.account.no}/withdraw/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_create_account_status(self):
        response = self.client.get('/accounts/create_account/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )

    def test_delete_account_status(self):
        response = self.client.get(
            path=f'/accounts/delete_account/{self.account.no}', follow=True
        )
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text='Confirm', status_code=200)

    def test_invalid_operation_status(self):
        response = self.client.get('/accounts/invalid_operation/')
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
