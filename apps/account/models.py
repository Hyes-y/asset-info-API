from django.db import models
from apps.user.models import User


class Account(models.Model):
    STOCK_FIRMS = (
        ('디셈버증권', '디셈버증권'),
        ('베스트투자', '베스트투자'),
        ('핀트투자증권', '핀트투자증권'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='user')
    name = models.CharField(verbose_name='계좌명', max_length=20)
    number = models.CharField(verbose_name='계좌번호', max_length=20)
    principal = models.DecimalField(verbose_name='투자 원금', max_digits=20, decimal_places=2)
    stock_firm = models.CharField(verbose_name='증권사', max_length=20, choices=STOCK_FIRMS)


class AssetInfo(models.Model):
    GROUPS = (
        ('미국 주식', '미국 주식'),
        ('미국섹터 주식', '미국섹터 주식'),
        ('선진국 주식', '선진국 주식'),
        ('신흥국 주식', '신흥국 주식'),
        ('전세계 주식', '전세계 주식'),
        ('부동산 / 원자재', '부동산 / 원자재'),
        ('채권 / 현금', '채권 / 현금'),
    )
    isin = models.CharField(verbose_name='ISIN', max_length=12)
    name = models.CharField(verbose_name='종목명', max_length=20)
    group = models.CharField(verbose_name='자산군', max_length=20, choices=GROUPS)


class Asset(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='account_id', related_name='asset')
    info = models.ForeignKey(AssetInfo, on_delete=models.DO_NOTHING, db_column='asset_info', related_name='info')
    price = models.DecimalField(verbose_name='현재가', max_digits=20, decimal_places=2)
    count = models.PositiveIntegerField(verbose_name='수량')

