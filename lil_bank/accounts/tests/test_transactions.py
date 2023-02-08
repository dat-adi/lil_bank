from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Customer, Account

class TestTransactions(TestCase):
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


    #def test_invalid_operation_status(self):
    #    response = self.client.get('/accounts/invalid_operation/')
    #    self.assertEqual(response.status_code, 200, "The page seems to be down.")
