from __future__ import absolute_import

from celery import shared_task
from django.core import management


@shared_task
def close_expired_accounts():
    '''close any expired accounts and transfer
    their funds to the 'expired' account.'''
    management.call_command('close_expired_accounts', interactive=False)
    return {'result': 'Closing expired accounts OK'}


@shared_task
def refill_accounts():
    '''refill accounts from fiobank'''
    raise NotImplementedError
