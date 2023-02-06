from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('user_profile/', views.UserProfile.as_view(), name="user_profile"),
]
