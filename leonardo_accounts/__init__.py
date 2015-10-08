
from decimal import Decimal as D

from django.apps import AppConfig


default_app_config = 'leonardo_accounts.Config'


LEONARDO_APPS = [
    'leonardo_accounts',
    'accounts',
]

LEONARDO_CONFIG = {
    'ACCOUNTS_UNIT_NAME': ('Giftcard', ('Account unit name')),
    'ACCOUNTS_UNIT_NAME_PLURAL': ('Pending', ('Account unit name plural')),
    'ACCOUNTS_MAX_ACCOUNT_VALUE': (D('10000.00'), ('Max account value')),
    'ACCOUNTS_MIN_LOAD_VALUE': (D('30.00'), ('Min load value')),
}

LEONARDO_PLUGINS = [
    ('leonardo_accounts.apps.accounts', ('Accounts: User'),)
]


class Config(AppConfig):
    name = 'leonardo_accounts'
    verbose_name = "Leonardo Accounts"

    def ready(self):

        # activate account-transfer
        from .checkout.methods import AccountTransferPaymentMethod
