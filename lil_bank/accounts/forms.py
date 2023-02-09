from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Customer , Account
from django.core.validators import RegexValidator
import re

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
    last_name = forms.CharField(max_length=32)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254)
    address = forms.CharField(max_length=256)
    phone = forms.CharField(max_length=16)
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput,min_length=8)
    password2 = forms.CharField(label="Re-enter Password", strip=False, widget=forms.PasswordInput,min_length=8)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[a-zA-Z]+$', first_name):
            raise forms.ValidationError("First name must contain only letters.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[a-zA-Z]+$', last_name):
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^[0-9]+$', phone):
            raise forms.ValidationError("Phone number must contain only numbers.")
        return phone
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter your first name...'
        })

        self.fields['last_name'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter your last name...'
        })

        self.fields['username'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter your name...'
        })

        self.fields['email'].widget.attrs.update({
            'type': 'email',
            'class': 'form-control',
            'placeholder': 'Enter your email...'
        })

        self.fields['address'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter your address...',
            'style': 'height: 10rem'
        })

        self.fields['phone'].widget.attrs.update({
            'type': 'tel',
            'class': 'form-control',
            'placeholder': 'Enter your phone number...'
        })

        self.fields['password1'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Enter your password...'
        })

        self.fields['password2'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Re-enter your password...'
        })


class LoginForm(forms.Form):
    """
    This is the form for logging in.
    """
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'placeholder': 'Enter your name...'
        })
        self.fields['password'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Enter your password...'
        })


class DepositForm(forms.Form):
    """
    This is the form used to deposit cash into an account.
    """
    add_money = forms.IntegerField(min_value=0,max_value=100000)

    def __init__(self, *args, **kwargs):
        super(DepositForm, self).__init__(*args, **kwargs)
        self.fields['add_money'].widget.attrs.update({
            'type': 'number',
            'class': 'form-control',
            'placeholder': 'Enter the deposit amount...'
        })


class WithdrawForm(forms.Form):
    """
    This is the form used to deposit cash into an account.
    """
    rm_money = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(WithdrawForm, self).__init__(*args, **kwargs)
        self.fields['rm_money'].widget.attrs.update({
            'type': 'number',
            'class': 'form-control',
            'placeholder': 'Enter the withdrawal amount...'
        })


class CreateAccountForm(forms.Form):
    """
    This is the form used to create an account.
    """
    type = forms.ChoiceField(choices=[('Checking', 'Checking'), ('Savings', 'Savings')], initial='Checking')

    def __init__(self, *args, **kwargs):
        super(CreateAccountForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs.update({'class': 'form-control'})


class DeleteAccountForm(forms.Form):
    """
    This is the form used to delete an account.
    """
    no = forms.IntegerField()
