import datetime
from decimal import Decimal as D

from django.views import generic
from django.core.urlresolvers import reverse
from django import http
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from oscar.core.loading import get_model
from oscar.templatetags.currency_filters import currency

from accounts.dashboard import forms, reports
from accounts import facade, names, exceptions

AccountType = get_model('accounts', 'AccountType')
Account = get_model('accounts', 'Account')
Transfer = get_model('accounts', 'Transfer')
Transaction = get_model('accounts', 'Transaction')


class AccountListView(generic.ListView):
    model = Account
    context_object_name = 'accounts'
    template_name = 'accounts/account_list.html'
    form_class = forms.SearchForm
    description = _("All %s") % names.UNIT_NAME_PLURAL.lower()

    def get_context_data(self, **kwargs):
        ctx = super(AccountListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['title'] = names.UNIT_NAME_PLURAL
        ctx['unit_name'] = names.UNIT_NAME
        ctx['queryset_description'] = self.description
        return ctx

    def get_queryset(self):
        queryset = self.request.user.accounts.all()
        if getattr(settings, 'STORE_ACCOUNTS_SHOW_SECONDARY', True):
            queryset = queryset | self.request.user.account_set.all()

        if 'code' not in self.request.GET:
            # Form not submitted
            self.form = self.form_class()
            return queryset

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            # Form submitted but invalid
            return queryset

        # Form valid - build queryset and description
        data = self.form.cleaned_data
        desc_template = _(
            "%(status)s %(unit)ss %(code_filter)s %(name_filter)s")
        desc_ctx = {
            'unit': names.UNIT_NAME.lower(),
            'status': "All",
            'code_filter': "",
            'name_filter': "",
        }
        if data['name']:
            queryset = queryset.filter(name__icontains=data['name'])
            desc_ctx['name_filter'] = _(
                " with name matching '%s'") % data['name']
        if data['code']:
            queryset = queryset.filter(code=data['code'])
            desc_ctx['code_filter'] = _(
                " with code '%s'") % data['code']
        if data['status']:
            queryset = queryset.filter(status=data['status'])
            desc_ctx['status'] = data['status']

        self.description = desc_template % desc_ctx

        return queryset


class AccountCreateView(generic.CreateView):
    model = Account
    context_object_name = 'account'
    template_name = 'accounts/account_form.html'
    form_class = forms.NewAccountForm

    def get_context_data(self, **kwargs):
        ctx = super(AccountCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Create a new %s") % names.UNIT_NAME.lower()
        return ctx

    def form_valid(self, form):
        account = form.save()

        # Load transaction
        source = form.get_source_account()
        amount = form.cleaned_data['initial_amount']
        try:
            facade.transfer(source, account, amount,
                            user=self.request.user,
                            description=_("Creation of account"))
        except exceptions.AccountException as e:
            messages.error(
                self.request,
                _("Account created but unable to load funds onto new "
                  "account: %s") % e)
        else:
            messages.success(
                self.request,
                _("New account created with code '%s'") % account.code)
        return http.HttpResponseRedirect(
            reverse('dashboard:accounts-detail', kwargs={'pk': account.id}))


class AccountUpdateView(generic.UpdateView):
    model = Account
    context_object_name = 'account'
    template_name = 'accounts/account_form.html'
    form_class = forms.UpdateAccountForm

    def get_context_data(self, **kwargs):
        ctx = super(AccountUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = _("Update '%s' account") % self.object.name
        return ctx

    def form_valid(self, form):
        account = form.save()
        messages.success(self.request, _("Account saved"))
        return http.HttpResponseRedirect(
            reverse('dashboard:accounts-detail', kwargs={'pk': account.id}))


class AccountTopUpView(generic.UpdateView):
    model = Account
    template_name = 'accounts/account_top_up.html'
    form_class = forms.TopUpAccountForm

    def form_valid(self, form):
        account = self.object
        amount = form.cleaned_data['amount']
        try:
            facade.transfer(form.get_source_account(), account, amount,
                            user=self.request.user,
                            description=_("Top-up account"))
        except exceptions.AccountException as e:
            messages.error(self.request,
                           _("Unable to top-up account: %s") % e)
        else:
            messages.success(
                self.request, _("%s added to account") % currency(amount))
        return http.HttpResponseRedirect(reverse('dashboard:accounts-detail',
                                                 kwargs={'pk': account.id}))


class AccountWithdrawView(generic.UpdateView):
    model = Account
    template_name = 'accounts/account_withdraw.html'
    form_class = forms.WithdrawFromAccountForm

    def form_valid(self, form):
        account = self.object
        amount = form.cleaned_data['amount']
        try:
            facade.transfer(account, form.get_source_account(), amount,
                            user=self.request.user,
                            description=_("Return funds to source account"))
        except exceptions.AccountException as e:
            messages.error(self.request,
                           _("Unable to withdraw funds from account: %s") % e)
        else:
            messages.success(
                self.request,
                _("%s withdrawn from account") % currency(amount))
        return http.HttpResponseRedirect(reverse('dashboard:accounts-detail',
                                                 kwargs={'pk': account.id}))


class AccountTransactionsView(generic.ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'accounts/account_detail.html'

    def get(self, request, *args, **kwargs):
        self.account = get_object_or_404(Account, id=kwargs['pk'])
        return super(AccountTransactionsView, self).get(
            request, *args, **kwargs)

    def get_queryset(self):
        return self.account.transactions.all().order_by('-date_created')

    def get_context_data(self, **kwargs):
        ctx = super(AccountTransactionsView, self).get_context_data(**kwargs)
        ctx['account'] = self.account
        return ctx


class TransferListView(generic.ListView):
    model = Transfer
    context_object_name = 'transfers'
    template_name = 'accounts/transfer_list.html'
    form_class = forms.TransferSearchForm
    description = _("All transfers")

    def get_context_data(self, **kwargs):
        ctx = super(TransferListView, self).get_context_data(**kwargs)
        ctx['form'] = self.form
        ctx['queryset_description'] = self.description
        return ctx

    def get_queryset(self):
        queryset = self.model.objects.all()

        if 'reference' not in self.request.GET:
            # Form not submitted
            self.form = self.form_class()
            return queryset

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            # Form submitted but invalid
            return queryset

        # Form valid - build queryset and description
        data = self.form.cleaned_data
        desc_template = _(
            "Transfers %(reference)s %(date)s")
        desc_ctx = {
            'reference': "",
            'date': "",
        }
        if data['reference']:
            queryset = queryset.filter(reference=data['reference'])
            desc_ctx['reference'] = _(
                " with reference '%s'") % data['reference']

        if data['start_date'] and data['end_date']:
            # Add 24 hours to make search inclusive
            date_from = data['start_date']
            date_to = data['end_date'] + datetime.timedelta(days=1)
            queryset = queryset.filter(date_created__gte=date_from).filter(date_created__lt=date_to)
            desc_ctx['date'] = _(" created between %(start_date)s and %(end_date)s") % {
                'start_date': data['start_date'],
                'end_date': data['end_date']}
        elif data['start_date']:
            queryset = queryset.filter(date_created__gte=data['start_date'])
            desc_ctx['date'] = _(" created since %s") % data['start_date']
        elif data['end_date']:
            date_to = data['end_date'] + datetime.timedelta(days=1)
            queryset = queryset.filter(date_created__lt=date_to)
            desc_ctx['date'] = _(" created before %s") % data['end_date']

        self.description = desc_template % desc_ctx
        return queryset


class TransferDetailView(generic.DetailView):
    model = Transfer
    context_object_name = 'transfer'
    template_name = 'accounts/transfer_detail.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.get(reference=self.kwargs['reference'])
