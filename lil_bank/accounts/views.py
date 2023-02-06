from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Account, Customer

# class LoginForm(forms.Form):
#     """
#     This is the form for logging in.
#     """
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)

class LoginView(TemplateView):
    """
    This is the view for logging in.
    """
    template_name = "accounts/login.html"
    # This is the view for logging in.
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
                    return render(request, "accounts/login_success.html")
            return render(request, "accounts/login_fail.html")
    


class SignUpView(TemplateView):
    """
    This is the view for signing in.
    """
    template_name = "accounts/signup.html"
    # This is the view for signing in.
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
    template_name = "accounts/logout.html"
    # This is the view for logging out. It logs out the user and redirects to the login page.
    def get(self, request):
        # Log out the user.
        logout(request)
        # Redirect to the login page.
        return render(request, 'accounts/login.html', {'form': LoginForm()})
    