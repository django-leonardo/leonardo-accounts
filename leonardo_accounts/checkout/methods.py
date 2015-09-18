

from django.utils.translation import ugettext as _
from leonardo_store.payments.methods import PaymentMethod
from .views import PaymentDetailsView


class AccountTransferPaymentMethod(PaymentMethod):
    code = 'accounttransfer'
    name = _('Account Transfer')
    description = _('Account Transfer')
    view = PaymentDetailsView
