"""
URL configuration for the dashboard application.
"""
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.DashboardView.as_view(), name="landing_page"),
    path('about/', views.AboutView.as_view(), name="about_page")
]

