from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
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
from django.contrib import messages
from .logger import logger

# Now we implement logger in every view.


class LoginView(TemplateView):
    """
    This is the view for logging in.
    """
    template_name = "accounts/login.html"

    def get(self, request, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    # Now check the input data.
    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, "accounts/login_fail.html")

        # Check if the user exists.
        if not User.objects.filter(username=form.cleaned_data['username']).exists():
            return render(request, "accounts/login_fail.html")

        # Check if the password is correct.
        user = User.objects.get(username=form.cleaned_data['username'])
        if not user.check_password(form.cleaned_data['password']):
            return render(request, "accounts/login_fail.html")

        # Log in the user.
        login(request, user)

        # Now redirect to the home page.
        # The logger is used here.
        logger.info('User %s logged in successfully.' % user.username)
        return redirect('dashboard:landing_page')


class SignUpView(TemplateView):
    """
    This is the view for signing in.
    """
    template_name = "accounts/signup.html"

    def get(self, request, **kwargs):
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
            # Write to the database.
            user.save()
            customer.save()
            account.save()

            # Redirect to the login page.
            # The logger is used here.
            logger.info('User %s signed up successfully.' % user.username)
            return redirect('/accounts/login/')
        else:
            # The logger is used here.
            logger.info('User sign up failed.')
            return render(request, self.template_name, {'form': form})
        # return render(request, self.template_name, {'form': form})


class LogoutView(TemplateView):
    """
    This is the view for logging out.
    """
    template_name = "logout.html"

    # This is the view for logging out. It logs out the user and redirects to the login page.
    def get(self, request, **kwargs):
        # Log out the user.
        logout(request)
        # Redirect to the login page.
        # The logger is used here.
        logger.info('User logged out successfully.')
        return render(request, 'accounts/login.html', {'form': LoginForm()})


class TransactionView(LoginRequiredMixin, TemplateView):
    """
    This is the view for displaying transactions.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/transactions.html"

    def get(self, request, **kwargs):
        try:
            account = Account.objects.get(no=kwargs['pk'])
            transactions = Transaction.objects.filter(account=account)
        except ObjectDoesNotExist as err:
            return redirect('accounts:invalid_operation')
        
        # The logger is used here.
        logger.info('User %s viewed transactions successfully.' % request.user.username)

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

    def get(self, request, **kwargs):
        account = Account.objects.get(no=kwargs['pk'])
        # The logger is used here.
        logger.info('User %s viewed balance successfully.' % request.user.username)
        return render(request, self.template_name, {'account': account})


class DepositView(LoginRequiredMixin, TemplateView):
    """
    This is the view for depositing money.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/deposit.html"

    def get(self, request, **kwargs):
        form = DepositForm()
        account = Account.objects.get(no=kwargs['pk'])
        return render(request, self.template_name, {'account': account, 'form': form})

    def post(self, request, **kwargs):
        form = DepositForm(request.POST)

        if form.is_valid():
            add_money = form.cleaned_data['add_money']
            account = Account.objects.get(no=kwargs['pk'])
            transaction = Transaction(
                account=account,
                withdrawal=False,
                amount=add_money
            )
            account.balance += add_money
            account.save()
            transaction.save()
            # The logger is used here.
            logger.info('User %s deposited money successfully.' % request.user.username)
            return redirect('accounts:balance', pk=kwargs['pk'])


class WithdrawView(LoginRequiredMixin, TemplateView):
    """
    This is the view for withdrawing money from the
    account.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "transactions/withdraw.html"

    def get(self, request, **kwargs):
        form = WithdrawForm()
        account = Account.objects.get(no=kwargs['pk'])
        return render(request, self.template_name, {'account': account, 'form': form})

    def post(self, request, **kwargs):
        form = WithdrawForm(request.POST)

        if form.is_valid():
            rm_money = form.cleaned_data['rm_money']
            account = Account.objects.get(no=kwargs['pk'])

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
            # The logger is used here.
            logger.info('User %s withdrew money successfully.' % request.user.username)
            return redirect('accounts:balance', pk=kwargs['pk'])


class AccountListView(LoginRequiredMixin, ListView):
    """
    This is the view for listing the different accounts.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "accounts/account_list.html"

    Model = Account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = self.get_queryset()

        return context

    def get_queryset(self, **kwargs):
        customer = Customer.objects.get(id=self.request.user.id)
        queryset = Account.objects.filter(owner=customer).order_by('no')
        # The logger is used here.
        logger.info('User %s viewed account list successfully.' % self.request.user.username)
        return queryset


class AccountDetailView(LoginRequiredMixin, TemplateView):
    """
    This is the view for displaying the account details.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "accounts/view_account.html"

    def get(self, request, **kwargs):
        """
        Get request to display the user's profile.
        """
        customer = Customer.objects.get(id=request.user.id)
        list_balance = []
        list_type = []
        list_owner_id = []
        list_no = []
        for i in Account.objects.filter(owner_id=request.user.id):
            list_balance.append(i.balance)
            list_type.append(i.type)
            list_owner_id.append(i.owner_id)
            list_no.append(i.no)
        list_new = [list_no, list_balance, list_type, list_owner_id]
        list_res = list(map(list, zip(*list_new)))
        # The logger is used here.
        logger.info('User %s viewed account details successfully.' % request.user.username)
        return render(request, self.template_name, {
            'customer': customer,
            'user': request.user,
            'listRes': list_res
        })


class AccountCreateView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "accounts/create_account.html"

    def get(self, request, **kwargs):
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
            # The logger is used here.
            logger.info('User %s created account successfully.' % request.user.username)

            return redirect('accounts:view_account')


class InvalidOperation(TemplateView):
    """
    This is a page that is shown in the case that a user
    performs an invalid operation.
    """
    template_name = "transactions/invalid_operation.html"


class AccountView(LoginRequiredMixin, TemplateView):
    """
    This page lists the accounts present for the customer,
    and redirects them to pages with operations for that
    account.
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = "accounts/account_detail.html"

    def get(self, request, **kwargs):
        account = Account.objects.filter(
            owner=self.request.user.id,
            no=kwargs['pk']
        )
        # The logger is used here.
        logger.info('User %s viewed account successfully.' % request.user.username)
        return render(request, self.template_name, {
            'account': account
        })


def delete_account(request, pk):
    account = Account.objects.get(no=pk)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Your account has been successfully deleted.')
        return redirect('accounts:view_account')
    # The logger is used here.
    logger.info('User %s deleted account successfully.' % request.user.username)
    return render(request, 'accounts/confirm_delete_account.html', {'account': account})
