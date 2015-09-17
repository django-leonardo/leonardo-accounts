
from django.apps import AppConfig

default_app_config = 'leonardo_accounts.Config'


LEONARDO_APPS = [
    'leonardo_accounts',
    'accounts'
]


class Config(AppConfig):
    name = 'leonardo_accounts'
    verbose_name = "Leonardo Accounts"
