from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import (
    LoginForm,
    SignUpForm,
    DepositForm,
    WithdrawForm,
    CreateAccountForm,
)
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, Customer, Transaction


class LoginView(TemplateView):
    """
    This is the view for logging in.
    """
    template_name = "accounts/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    # Now check the input data.
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Check if the user exists.
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                # Check if the password is correct.
                user = User.objects.get(username=form.cleaned_data['username'])
                if user.check_password(form.cleaned_data['password']):
                    # Log in the user.
                    login(request, user)
                    # return render(request, "accounts/login_success.html")
                    # Now redirect to the home page.
                    return redirect('dashboard:landing_page')
                    # return render(request, "accounts/login_success.html")
            return render(request, "accounts/login_fail.html")


class SignUpView(TemplateView):
    """
    This is the view for signing in.
    """
    template_name = "accounts/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
    
    # Now store the input data in the database.
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new user.
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
            )

            # Create a new customer.
            customer = Customer.objects.create(
                id=user.id,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                phone=form.cleaned_data['phone'],
            )

            # Create a new account.
            account = Account.objects.create(
                no=customer.id,
                owner=customer,
            )
            # Redirect to the login page.
            # Write to the database.
            user.save()
            customer.save()
            account.save()
            return render(request, 'accounts/login.html', {'form': LoginForm()})
        return render(request, self.template_name, {'form': form})


class LogoutView(TemplateView):
    """
    This is the view for logging out.
    """
    template_name = "logout.html"

    # This is the view for logging out. It logs out the user and redirects to the login page.
    def get(self, request):
        # Log out the user.
        logout(request)
        # Redirect to the login page.
        return render(request, 'accounts/login.html', {'form': LoginForm()})



    
class TransactionView(LoginRequiredMixin, TemplateView):
    """
    This is the view for displaying transactions.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/transaction_list.html"
    def get(self, request):
        # TODO: Filter transactions by account number.

        # HACK: For now, fetch the first account and use that.
        account = Account.objects.first()

        transactions = Transaction.objects.filter(account=account)

        return render(request, self.template_name, {
            'transactions': transactions,
            'account': account,
        })


class BalanceView(LoginRequiredMixin, TemplateView):
    """
    This is the view for displaying the balance of the account.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/balance_view.html"
    def get(self, request):
        customer = Customer.objects.get(id=request.user.id)
        account = Account.objects.get(owner_id=customer.id)
        return render(request, self.template_name, {'account': account})


class DepositView(LoginRequiredMixin, TemplateView):
    """
    This is the view for depositing money.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/deposit.html"
    def get(self, request):
        form = DepositForm()
        customer = Customer.objects.get(id=request.user.id)
        account = Account.objects.get(owner_id=customer.id)
        return render(request, self.template_name, {'account': account, 'form': form})

    def post(self, request):
        form = DepositForm(request.POST)

        if form.is_valid():
            add_money = form.cleaned_data['add_money']
            customer = Customer.objects.get(id=request.user.id)
            account = Account.objects.get(owner_id=customer.id)
            transaction = Transaction(
                account=account,
                withdrawal=False,
                amount=add_money
            )
            account.balance += add_money
            account.save()
            transaction.save()

            return redirect('accounts:balance')


class WithdrawView(LoginRequiredMixin, TemplateView):
    """
    This is the view for withdrawing money from the
    account.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/withdraw.html"
    def get(self, request):
        form = WithdrawForm()
        customer = Customer.objects.get(id=request.user.id)
        account = Account.objects.get(owner_id=customer.id)
        return render(request, self.template_name, {'account': account, 'form': form})

    def post(self, request):
        form = WithdrawForm(request.POST)

        if form.is_valid():
            rm_money = form.cleaned_data['rm_money']
            customer = Customer.objects.get(id=request.user.id)
            account = Account.objects.get(owner_id=customer.id)

            if rm_money > account.balance:
                return redirect('accounts:invalid_operation')

            transaction = Transaction(
                account=account,
                withdrawal=True,
                amount=rm_money
            )
            account.balance -= rm_money
            account.save()
            transaction.save()

            return redirect('accounts:balance')


class AccountDetailsView(LoginRequiredMixin, TemplateView):
    """
    This is the view for displaying the account details.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "accounts/view_account.html"
    def get(self, request):
        """
        Get request to display the user's profile.
        """
        customer = Customer.objects.get(id=request.user.id)    
        user = User.objects.get(id=request.user.id)
        listBalance = []
        listType = []
        listOwnerID = []
        listNo = []
        for i in Account.objects.filter(owner_id=request.user.id):
            listBalance.append(i.balance)
            listType.append(i.type)
            listOwnerID.append(i.owner_id)
            listNo.append(i.no)
        listNew = [listNo, listBalance, listType, listOwnerID]
        listRes = list(map(list, zip(*listNew)))
        return render(request, self.template_name, {'customer': customer, 'user': user, 'listRes': listRes})


class AccountCreateView(LoginRequiredMixin, TemplateView):
    """
    TODO
    This is a feature that will be worked on in the far
    future.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "accounts/create_account.html"

    def get(self, request):
        form = CreateAccountForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['type']
            customer = Customer.objects.get(id=request.user.id)
            account = Account(
                owner=customer,
                type=account_type
            )
            account.save()
            return redirect('accounts:view_account')


class AccountModifyView(LoginRequiredMixin, TemplateView):
    """
    TODO
    This is a feature that will be worked on in the far
    future.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    pass


class AccountDeleteView(LoginRequiredMixin, TemplateView):
    """
    TODO
    This is a feature that will be worked on in the far
    future.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    pass


class InvalidOperation(TemplateView):
    """
    This is a page that is shown in the case that a user
    performs an invalid operation.
    """
    template_name = "transactions/invalid_operation.html"
