from django.test import TestCase
from accounts.models import Customer, Account, Transaction


class TestTransactions(TestCase):
    customer = None
    account = None
    transaction = None

    @classmethod
    def setUpTestData(cls):
        cls.customer = Customer.objects.create(
            id="1",
            first_name="Test",
            last_name="User",
            address="#1 Test, User Nagar",
            phone="19199191"
        )
        cls.account = Account.objects.create(
            type='checking',
            owner=cls.customer,
            balance=10000
        )
        cls.transaction = Transaction.objects.create(
            account=cls.account,
            withdrawal=False,
            amount=500
        )

    def test_transactions_status(self):
        response = self.client.get('/accounts/transactions/', {
            'account': self.account
        })
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_balance_status(self):
        response = self.client.get('/accounts/balance/', {
            'account': self.account
        })

        self.assertEqual(response.status_code, 200, "The page seems to be down.")

"""
    def test_deposit_status(self):
        response = self.client.get('/accounts/deposit/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_withdraw_status(self):
        response = self.client.get('/accounts/withdraw/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_create_account_status(self):
        response = self.client.get('/accounts/create_account/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_view_account_status(self):
        response = self.client.get('/accounts/view_account/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_modify_account_status(self):
        response = self.client.get('/accounts/modify_account/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_delete_account_status(self):
        response = self.client.get('/accounts/delete_account/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")

    def test_invalid_operation_status(self):
        response = self.client.get('/accounts/invalid_operation/')
        self.assertEqual(response.status_code, 200, "The page seems to be down.")
"""
