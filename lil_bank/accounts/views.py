from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, SignUpForm

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.forms import ModelForm
# from .models import Account

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

class LogoutView(TemplateView):
    """
    This is the view for logging out.
    """
    template_name = "accounts/logout.html"
