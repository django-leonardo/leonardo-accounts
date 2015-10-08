from django.conf.urls import url

from .views import *
from leonardo.decorators import require_auth

urlpatterns = [
    url(r'^$',
        AccountListView.as_view(),
        name='accounts-list'),
    url(r'^$',
        AccountListView.as_view(),
        name='index'),
#    url(r'^create/$', self.account_create_view.as_view(),
#        name='accounts-create'),
    url(r'^(?P<pk>\d+)/update/$', AccountUpdateView.as_view(),
        name='accounts-update'),
    url(r'^(?P<pk>\d+)/$', TransferListView.as_view(),
        name='accounts-detail'),
#    url(r'^(?P<pk>\d+)/freeze/$', self.account_freeze_view.as_view(),
#        name='accounts-freeze'),
#    url(r'^(?P<pk>\d+)/thaw/$', self.account_thaw_view.as_view(),
#        name='accounts-thaw'),
    url(r'^(?P<pk>\d+)/top-up/$', AccountTopUpView.as_view(),
        name='accounts-top-up'),
#    url(r'^(?P<pk>\d+)/withdraw/$', self.account_withdraw_view.as_view(),
#        name='accounts-withdraw'),
#    url(r'^transfers/$', self.transfer_list_view.as_view(),
#        name='transfers-list'),
#    url(r'^transfers/(?P<reference>[A-Z0-9]{32})/$',
#        self.transfer_detail_view.as_view(),
#        name='transfers-detail'),
#    url(r'^reports/deferred-income/$',
#        self.report_deferred_income.as_view(),
#        name='report-deferred-income'),
#    url(r'^reports/profit-loss/$',
#        self.report_profit_loss.as_view(),
#        name='report-profit-loss'),

]

# for sure
require_auth(urlpatterns)
