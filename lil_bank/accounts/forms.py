from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Customer , Account

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
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254)
    address = forms.CharField(max_length=256)
    phone = forms.CharField(max_length=16)
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Re-enter Password", strip=False, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    """
    This is the form for logging in.
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class DepositForm(forms.Form):
    """
    This is the form used to deposit cash into an account.
    """
    add_money = forms.IntegerField(max_value=100000)


class WithdrawForm(forms.Form):
    """
    This is the form used to deposit cash into an account.
    """
    rm_money = forms.IntegerField()

class CreateAccountForm(forms.Form):
    """
    This is the form used to create an account.
    """
    type = forms.ChoiceField(choices=[('Checking', 'Checking'), ('Savings', 'Savings')], initial='Checking')
