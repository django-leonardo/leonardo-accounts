from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from leonardo.decorators import require_auth

from .views import *

urlpatterns = [
    url(r'^$',
        login_required(AccountListView.as_view()),
        name='index'),
#    url(r'^create/$', self.account_create_view.as_view(),
#        name='accounts-create'),
    url(r'^(?P<pk>\d+)/update/$', login_required(AccountUpdateView.as_view()),
        name='accounts-update'),
    url(r'^(?P<pk>\d+)/$', login_required(TransferListView.as_view()),
        name='accounts-detail'),
#    url(r'^(?P<pk>\d+)/freeze/$', self.account_freeze_view.as_view(),
#        name='accounts-freeze'),
#    url(r'^(?P<pk>\d+)/thaw/$', self.account_thaw_view.as_view(),
#        name='accounts-thaw'),
    url(r'^(?P<pk>\d+)/top-up/$', login_required(AccountTopUpView.as_view()),
        name='accounts-top-up'),
    url(r'^(?P<pk>\d+)/withdraw/$', login_required(AccountWithdrawView.as_view()),
        name='accounts-withdraw'),
    url(r'^transfers/$', login_required(TransferListView.as_view()),
        name='transfers-list'),
    url(r'^transfers/(?P<reference>[A-Z0-9]{32})/$',
        login_required(TransferDetailView.as_view()),
        name='transfers-detail'),
#    url(r'^reports/deferred-income/$',
#        self.report_deferred_income.as_view(),
#        name='report-deferred-income'),
#    url(r'^reports/profit-loss/$',
#        self.report_profit_loss.as_view(),
#        name='report-profit-loss'),

]

# for sure
require_auth(urlpatterns)
