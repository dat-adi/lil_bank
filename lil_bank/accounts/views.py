from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Account, Customer


class LoginView(TemplateView):
    """
    This is the view for logging in.
    """
    template_name = "accounts/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    # Now check the input data.
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Check if the user exists.
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                # Check if the password is correct.
                user = User.objects.get(username=form.cleaned_data['username'])
                if user.check_password(form.cleaned_data['password']):
                    # Log in the user.
                    login(request, user)
                    # return render(request, "accounts/login_success.html")
                    # Now redirect to the home page.
                    return redirect('dashboard:landing_page')
                    # return render(request, "accounts/login_success.html")
            return render(request, "accounts/login_fail.html")


class SignUpView(TemplateView):
    """
    This is the view for signing in.
    """
    template_name = "accounts/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
    
    # Now store the input data in the database.
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new user.
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )

            # Create a new customer.
            customer = Customer.objects.create(
                id=user.id,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
            )

            # Create a new account.
            account = Account.objects.create(
                no=customer.id,
                name=form.cleaned_data['first_name'] + ' ' + form.cleaned_data['last_name'],
                type='Checking',
                owner=customer,
                balance=0.,
            )
            # Redirect to the login page.
            # Write to the database.
            user.save()
            customer.save()
            account.save()
            return render(request, 'accounts/login.html', {'form': LoginForm()})
        return render(request, self.template_name, {'form': form})


class LogoutView(TemplateView):
    """
    This is the view for logging out.
    """
    template_name = "logout.html"

    # This is the view for logging out. It logs out the user and redirects to the login page.
    def get(self, request):
        # Log out the user.
        logout(request)
        # Redirect to the login page.
        return render(request, 'accounts/login.html', {'form': LoginForm()})


    
class TransactionView(TemplateView):
    """
    This is the view for displaying transactions.
    """
    pass


class BalanceView(TemplateView):
    """
    This is the view for displaying the balance of the account.
    """
    pass


class DepositView(TemplateView):
    """
    This is the view for depositing money.
    """
    pass


class WithdrawView(TemplateView):
    """
    This is the view for withdrawing money from the
    account.
    """
    pass


class AccountDetailsView(TemplateView):
    """
    This is the view for displaying the account details.
    """
    template_name = "accounts/view_account.html"
    def get(self, request):
        """
        Get request to display the user's profile.
        """
        customer = Customer.objects.get(id=request.user.id)    
        user = User.objects.get(id=request.user.id)   
        return render(request, self.template_name, {'customer': customer, 'user': user})


class AccountCreateView(TemplateView):
    """
    TODO
    This is a feature that will be worked on in the far
    future.
    """
    pass


class AccountModifyView(TemplateView):
    """
    TODO
    This is a feature that will be worked on in the far
    future.
    """
    pass


class AccountDeleteView(TemplateView):
    """
    TODO
    This is a feature that will be worked on in the far
    future.
    """
    pass
