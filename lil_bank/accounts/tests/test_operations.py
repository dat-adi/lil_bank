from django.contrib.auth.models import User
from django.db.models import Q
from django.test import TestCase
from django.utils.http import urlencode
from accounts.models import Customer, Account
from accounts.forms import CreateAccountForm, DepositForm, WithdrawForm

class TestOperations(TestCase):
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
        return super().setUp()

    def tearDown(self) -> None:
        self.client.logout()
        self.account.delete()
        self.customer.delete()
        self.user.delete()
        return super().tearDown()

    def test_create_account(self) -> None:
        # Get the current count of existing accounts
        accounts = Account.objects.all().count()

        # Check if data if valid
        data = { 'type': 'Checking' }
        form = CreateAccountForm(data)
        self.assertTrue(form.is_valid(), 'Form is invalid')

        # Post and check if we redirect back to Account Details page
        response = self.client.post(
            '/accounts/create_account/', data=data, follow=True
        )
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(
            response, text='Your Account Details', status_code=200
        )

        # Check if # of accounts has increased by 1
        self.assertEqual(
            Account.objects.all().count(), accounts + 1, 'No new account added'
        )

        # Since we have only two accounts, it shouldn't be hard to
        # figure out the account added!  Just exclude self.account
        new_account = Account.objects.get(~Q(no=self.account.no))

        self.assertEqual(
            new_account.type, data['type'],
            'Type of new account differs from data submitted'
        )
        self.assertEqual(
            new_account.balance, 0.,
            "New account's balance is not 0"
        )
        new_account.delete()

    def test_delete_account(self) -> None:
        # Create dummy account which we shall try and delete
        test_account = Account.objects.create(
            type='Savings',
            owner=self.customer
        )

        # Keep a record of the current count of existing accounts
        accounts = Account.objects.all().count()

        # Post and check if we redirect back to Account Details page
        response = self.client.post(
            f'/accounts/delete_account/{test_account.no}/', follow=True
        )
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(
            response, text='Your Account Details', status_code=200
        )

        # Check if # of accounts has decreased by 1
        self.assertEqual(
            Account.objects.all().count(), accounts - 1, 'Account still exists'
        )

        # Make sure the test_account is nowhere to be found
        self.assertFalse(
            Account.objects.filter(no=test_account.no), 'Account still exists'
        )

    def test_deposit(self) -> None:
        # Note current account balance
        previous_balance = self.account.balance

        # Validate form
        data = { 'add_money': 500. }
        form = DepositForm(data)
        self.assertTrue(form.is_valid(), 'Form is invalid')

        # Post and check if we redirect back to Account Balance page
        response = self.client.post(
            f'/accounts/{self.account.no}/deposit/', data=data, follow=True
        )
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(
            response, text='Account Balance', status_code=200
        )

        # Refresh self.account since update was done with a different
        # reference elsewhere
        self.account.refresh_from_db()

        # Check if money was added to previous balance
        self.assertEqual(
            self.account.balance, previous_balance + data['add_money'],
            'Account Balance is not as expected after a deposit'
        )

    def test_withdraw(self) -> None:
        # Note current account balance
        previous_balance = self.account.balance
        self.assertNotEqual(previous_balance, 0., 'Account Balance is zero')

        # Validate form
        data = { 'rm_money': previous_balance }
        form = WithdrawForm(data)
        self.assertTrue(form.is_valid(), 'Form is invalid')

        # Post and check if we redirect back to Account Balance page
        response = self.client.post(
            f'/accounts/{self.account.no}/withdraw/', data=data, follow=True
        )
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(
            response, text='Account Balance', status_code=200
        )

        # Refresh self.account since update was done with a different
        # reference elsewhere
        self.account.refresh_from_db()

        # Check if balance is zero now
        self.assertEqual(
            self.account.balance, 0.,
            'Account Balance is greater than zero after a full withdraw'
        )