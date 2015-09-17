from django.conf.urls import include, patterns
from accounts.dashboard.app import application as accounts_app


urlpatterns = patterns('',
                       (r'^dashboard/accounts/', include(accounts_app.urls)),
                       )
