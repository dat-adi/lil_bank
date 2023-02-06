from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.forms import ModelForm
# from .models import Customer

# class AccountForm(ModelForm):
#     """
#     This is the form for creating and editing accounts.
#     """
#     class Meta:
#         model = Customer
#         fields = ['account_name', 'account_type', 'account_balance', 'account_owner']

class SignUpForm(forms.Form):
    """
    This is the form for signing up.
    """
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    # password2 should match password1
    password2 = forms.CharField(label="Password confirmation", strip=False, widget=forms.PasswordInput, help_text="Enter the same password as before, for verification.")

class LoginForm(forms.Form):
    """
    This is the form for logging in.
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

