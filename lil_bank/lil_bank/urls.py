"""
URL Configuration for the project
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Lil' Bank API Specification",
        default_version='v1',
        description="By the people; for the people.",
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restful_api.urls')),
    path('', include('dashboard.urls', namespace='dashboard')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc")
]
