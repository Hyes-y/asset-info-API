from django.db import models
from apps.account.models import Account
from apps.user.models import User


class TransactionInfo(models.Model):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name='transaction')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transaction')
    amount = models.DecimalField(verbose_name='거래 금액', max_digits=20, decimal_places=2)


class Transaction(models.Model):
    tr_info = models.OneToOneField(TransactionInfo, on_delete=models.CASCADE, primary_key=True)
    is_transferred = models.BooleanField(verbose_name='거래 여부', default=False)