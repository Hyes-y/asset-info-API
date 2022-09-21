from django.db import models
from apps.user.models import User


class Account(models.Model):
    STOCK_FIRMS = (
        ('디셈버증권', '디셈버증권'),
        ('베스트투자', '베스트투자'),
        ('핀트투자증권', '핀트투자증권'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='account')
    name = models.CharField(verbose_name='계좌명', max_length=20)
    number = models.CharField(verbose_name='계좌번호', max_length=20, unique=True)
    principal = models.DecimalField(verbose_name='투자 원금', max_digits=20, decimal_places=2)
    stock_firm = models.CharField(verbose_name='증권사', max_length=20, choices=STOCK_FIRMS)
