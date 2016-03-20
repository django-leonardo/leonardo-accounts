
from decimal import Decimal as D

from django.apps import AppConfig


default_app_config = 'leonardo_accounts.Config'


LEONARDO_APPS = [
    'leonardo_accounts',
    'accounts',
]

LEONARDO_CONFIG = {
    'ACCOUNTS_UNIT_NAME': ('Account', ('Account unit name')),
    'ACCOUNTS_UNIT_NAME_PLURAL': ('Accounts', ('Account unit name plural')),
    'ACCOUNTS_MAX_ACCOUNT_VALUE': (D('1000000.00'), ('Max account value')),
    'ACCOUNTS_MIN_LOAD_VALUE': (D('0.00'), ('Min load value')),
}

LEONARDO_PLUGINS = [
    ('leonardo_accounts.apps.accounts', ('Accounts: User'),)
]

LEONARDO_STORE_PROFILE_ACTIONS = [
    'leonardo_accounts/_actions.html'
]


class Config(AppConfig):
    name = 'leonardo_accounts'
    verbose_name = "Leonardo Accounts"

    def ready(self):

        # activate account-transfer
        from .checkout.methods import AccountTransferPaymentMethod
