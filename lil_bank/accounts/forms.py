from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
# from .models import Account

# class AccountForm(ModelForm):
#     """
#     This is the form for creating and editing accounts.
#     """
#     class Meta:
#         model = Account
#         fields = ['account_name', 'account_type', 'account_balance', 'account_owner']

# class SignUpForm(UserCreationForm):
#     """
#     This is the form for signing up.
#     """
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', )

class LoginForm(forms.Form):
    """
    This is the form for logging in.
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

