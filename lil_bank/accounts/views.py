from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, SignUpForm

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
