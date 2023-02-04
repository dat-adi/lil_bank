from django.shortcuts import render
from django.views.generic import TemplateView


class LoginView(TemplateView):
    """
    This is the view for logging in.
    """
    template_name = "accounts/login.html"


class SignUpView(TemplateView):
    """
    This is the view for signing in.
    """
    template_name = "accounts/signup.html"


class LogoutView(TemplateView):
    """
    This is the view for logging out.
    """
    template_name = "accounts/logout.html"
