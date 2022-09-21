from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from apps.user.models import User
from apps.account.models import Account
from apps.asset.models import Asset, AssetInfo


class AssetTest(APITestCase):
    """
    보유 종목 조회 테스트
    """
    def setUp(self):
        """ test 를 위한 mock 데이터 추가 """
        self.asset_test_url = "/api/v1/assets/"
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

        for i in range(1, 4):
            asset_info = AssetInfo.objects.create(
                isin=f'testisin{str(i)}',
                name=f'test asset{str(i)}',
                group=f'test sector{str(i)}'
            )

            Asset.objects.create(
                account=self.account,
                info=asset_info,
                price=1000 + i * 100,
                count=i
            )

        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_get_assets_success(self):
        """ 보유 종목 조회 성공 테스트 """

        request_url = self.asset_test_url
        response = self.client.get(request_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

