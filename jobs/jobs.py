import pandas as pd
import uuid
from datetime import datetime
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction

from apps.user.models import User
from apps.account.models import Account
from apps.asset.models import AssetInfo, Asset


def update_or_create_object(model, data):
    obj, created = model.objects.update_or_create(**data)
    return obj


class Schedule:
    def __init__(self, initial):
        self.Account = Account
        self.AssetInfo = AssetInfo
        self.Asset = Asset
        self.User = User
        self.group_info = None
        self.asset_info_set = None
        self.initial = initial
    
    def run_test(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 스케쥴러 테스트")
    
    @transaction.atomic()
    def run(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} DB 데이터 동기화")
        self.get_data()
        if self.initial:
            self.set_group_data(initial=self.initial)

        for i, row in self.asset_info_set.iterrows():
            print(f"data upload ... {i}")
            try:
                user_setting = {
                    "name": row['고객이름'],
                    "defaults": {
                        'username': 'user' + str(uuid.uuid4())[-12:],
                        'password': make_password('test1234')
                    }
                }

                user = update_or_create_object(self.User, user_setting)

                account_setting = {
                    'number': row['계좌번호'],
                    'defaults': {
                        'user': user,
                        'stock_firm': row['증권사'],
                        'name': row['계좌명'],
                        'principal': row['투자원금'],
                    }
                }

                account = update_or_create_object(self.Account, account_setting)
                info = self.AssetInfo.objects.get(isin=row['ISIN'])

                asset_setting = {
                    'account': account,
                    'info': info,
                    'defaults': {
                        'price': row['현재가'],
                        'count': row['보유수량']
                    }
                }

                asset = update_or_create_object(self.Asset, asset_setting)
            except:
                continue

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} DB 데이터 동기화 완료")
        return

    def get_data(self):
        asset_info = pd.read_excel('data/account_asset_info_set.xlsx')
        basic_info = pd.read_excel('data/account_basic_info_set.xlsx')
        self.group_info = pd.read_excel('data/asset_group_info_set.xlsx')
        self.asset_info_set = pd.merge(asset_info, basic_info, on='계좌번호', how='inner')

    def set_group_data(self, initial=False):
        obj_list = []
        for i, row in self.group_info.iterrows():
            data = {
                'isin': row['ISIN'],
                'name': row['종목명'],
                'group': row['자산그룹']
            }
            if initial:
                obj_list.append(AssetInfo(**data))
            else:
                update_or_create_object(self.AssetInfo, data)

        if initial:
            self.AssetInfo.objects.bulk_create(obj_list)
        return

