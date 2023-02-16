from django.contrib.auth.models import User
from django.test import TestCase
from accounts.models import Customer
from accounts.forms import SignUpForm, LoginForm
from lil_bank.settings import LOGIN_URL


class TestAuthentication(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'test_user_1',
            'email': 'test@user.com',
            'address': '#1 Test, User Nagar',
            'phone': '1234567890',
            'password1': 'test_user_password',
            'password2': 'test_user_password',
        }

    def test_signup(self):
        # Note down count of current users
        users = User.objects.all().count()

        # Validate form
        form = SignUpForm(self.data)
        self.assertTrue(form.is_valid(), 'Form is invalid')

        # POST self.data and check if it redirects to login page
        response = self.client.post(
            '/accounts/signup/', data=self.data, follow=True
        )
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text='Log In', status_code=200)

        # Check if a new user was added
        self.assertEqual(
            User.objects.all().count(), users + 1, 'User was not added'
        )

        # Get the current user and see if a new customer was also
        # created for her
        user = User.objects.get(username=self.data['username'])
        customer = Customer.objects.get(id=str(user.id))
        self.assertTrue(customer, 'No new customer was created')

        # Clean up
        customer.delete() 
        user.delete()

    def test_login(self):
        data = { 'username': 'test', 'password': 'test_password' }

        # Create the user
        user = User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save()

        # Validate form
        form = LoginForm(data)
        self.assertTrue(form.is_valid(), 'Form is invalid')

        # Check if after login we get redirected to the dashboard
        response = self.client.post(LOGIN_URL, data=data, follow=True)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text=data['username'], status_code=200)

        # Cleanup
        self.client.logout()
        user.delete()

    def test_logout(self):
        # Create the user
        user = User.objects.create(username='dummy')
        user.set_password('dummy_password')
        user.save()

        # Test if log in works
        logged_in = self.client.login(
            username='dummy', password='dummy_password'
        )
        self.assertTrue(logged_in, 'User is not logged in')
        
        # Upon a get request to logout, we should get redirected back
        # to the login page
        response = self.client.get('/accounts/logout/', follow=True)
        self.assertEqual(
            response.status_code, 200, "The page seems to be down."
        )
        self.assertContains(response, text='Log In', status_code=200)

        # Cleanup
        user.delete()