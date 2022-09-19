import pandas as pd
import uuid
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.user.models import User
from apps.account.models import Account, AssetInfo, Asset


class Command(BaseCommand):
    help = 'initial set(user)'

    @transaction.atomic()
    def handle(self, *args, **options):
        print("DB 초기 데이터 생성")

        group_info = pd.read_excel('data/asset_group_info_set.xlsx')
        asset_info = pd.read_excel('data/account_asset_info_set.xlsx')
        basic_info = pd.read_excel('data/account_basic_info_set.xlsx')

        asset_info_set = pd.merge(asset_info, basic_info, on='계좌번호', how='inner')

        AssetInfo.objects.bulk_create([
            AssetInfo(isin=row['ISIN'], name=row['종목명'], group=['자산그룹']) \
            for i, row in group_info.iterrows()
        ])

        for i, row in asset_info_set.iterrows():
            print(f"asset_info_uploading ... {i}")
            user, created = User.objects.get_or_create(
                name=row['고객이름'],
                defaults={
                    'username': 'user' + str(uuid.uuid4())[-12:],
                    'password': make_password('test1234')
                }
            )

            account, created = Account.objects.get_or_create(
                number=row['계좌번호'],
                defaults={
                    'user': user,
                    'stock_firm': row['증권사'],
                    'name': row['계좌명'],
                    'principal': row['투자원금'],
                }
            )

            info = AssetInfo.objects.get(isin=row['ISIN'])
            Asset.objects.get_or_create(
                account=account,
                info=info,
                defaults={
                    'price': row['현재가'],
                    'count': row['보유수량']
                }
            )
