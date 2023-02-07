"""
URL Configuration for the project
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restful_api.urls')),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api-auth/', include('rest_framework.urls')),
]
