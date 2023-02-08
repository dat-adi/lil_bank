from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication Routes
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    # Account Template Pages
    path('', views.AccountListView.as_view(), name="account_list"),
    path('<int:pk>/', views.AccountView.as_view(), name="account_detail"),
    path('view_account/', views.AccountDetailView.as_view(), name="view_account"),

    # Operation Pages
    path('<int:pk>/transactions/', views.TransactionView.as_view(), name="transactions"),
    path('<int:pk>/balance/', views.BalanceView.as_view(), name="balance"),
    path('<int:pk>/deposit/', views.DepositView.as_view(), name="deposit"),
    path('<int:pk>/withdraw/', views.WithdrawView.as_view(), name="withdraw"),

    # Account CRUD Pages
    path('create_account/', views.AccountCreateView.as_view(), name="create_account"),
    path('modify_account/', views.AccountModifyView.as_view(), name="modify_account"),
    path('delete_account/', views.AccountDeleteView.as_view(), name="delete_account"),
    # Miscellaneous Routes
    path('invalid_operation/', views.InvalidOperation.as_view(), name="invalid_operation"),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
]
