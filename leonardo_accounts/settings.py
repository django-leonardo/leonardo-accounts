
from oscar.defaults import OSCAR_DASHBOARD_NAVIGATION

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': 'Accounts',
        'icon': 'icon-globe',
        'children': [
            {
                'label': 'Accounts',
                'url_name': 'dashboard:accounts-list',
            },
            {
                'label': 'Transfers',
                'url_name': 'dashboard:transfers-list',
            },
            {
                'label': 'Deferred income report',
                'url_name': 'dashboard:report-deferred-income',
            },
            {
                'label': 'Profit/loss report',
                'url_name': 'dashboard:report-profit-loss',
            },
        ]
    })

# show secondary accounts in profile actions
STORE_ACCOUNTS_SHOW_SECONDARY = True
