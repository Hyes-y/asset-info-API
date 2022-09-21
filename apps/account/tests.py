from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from apps.user.models import User
from apps.account.models import Account
from apps.asset.models import Asset, AssetInfo


class AccountTest(APITestCase):
    """
    투자 내역, 상세 내역 조회 테스트
    """
    def setUp(self):
        """ test 를 위한 mock 데이터 추가 """
        self.login_url = "/api/v1/login"
        self.account_test_url = "/api/v1/accounts/"
        self.user = User.objects.create(
            name='user1',
            username='test_user',
            password=make_password('test1234')
        )

        self.account = Account.objects.create(
            number='012345678910',
            user=self.user,
            stock_firm='test 증권사',
            name='test 계좌',
            principal=1000,
        )

        self.asset_info = AssetInfo.objects.create(
            isin='testisin',
            name='test asset',
            group='test sector'
        )

        self.asset = Asset.objects.create(
            account=self.account,
            info=self.asset_info,
            price=1100,
            count=1
        )

        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_get_account_success(self):
        """ 투자 내역 조회 성공 테스트 """

        request_url = self.account_test_url + f"{self.account.id}/"
        response = self.client.get(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_detail_success(self):
        """ 투자 내역 조회 성공 테스트 """

        request_url = self.account_test_url
        response = self.client.get(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
