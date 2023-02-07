from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('user_profile/', views.UserProfile.as_view(), name="user_profile"),
    path('transactions/', views.TransactionView.as_view(), name="transactions"),
    path('balance/', views.BalanceView.as_view(), name="balance"),
    path('deposit/', views.DepositView.as_view(), name="deposit"),
    path('withdraw/', views.WithdrawView.as_view(), name="withdraw"),
    path('create_account/', views.AccountCreateView.as_view(), name="create_account"),
    path('view_account/', views.AccountDetailsView.as_view(), name="view_account"),
    path('modify_account/', views.AccountModifyView.as_view(), name="modify_account"),
    path('delete_account/', views.AccountDeleteView.as_view(), name="delete_account"),
    path('invalid_operation/', views.InvalidOperation.as_view(), name="invalid_operation")
]
