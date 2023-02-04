"""
Views page for the dashboard application.
"""
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    """
    This is the view for the landing page
    in the dashboard section.
    """
    template_name = "dashboard/landing_page.html"


class AboutView(TemplateView):
    """
    This is the view for the about page in the
    dashboard section.
    """
    template_name = "dashboard/about.html"
