from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from apps.user.models import User
from apps.account.models import Account
import bcrypt


class TransactionTest(APITestCase):
    """
    투자금 입금 테스트
    """
    def setUp(self):
        """ test 를 위한 mock 데이터 추가 """
        self.phase1_test_url = "/api/v1/transactions/validation/"
        self.phase2_test_url = "/api/v1/transactions/"

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

        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    def test_phase1_success(self):
        """ 투자금 입금 phase 1 성공 테스트 """

        data = {
            'account_number': self.account.number,
            'user_name': self.user.name,
            'transfer_amount': 1000,
        }
        request_url = self.phase1_test_url
        response = self.client.post(request_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_phase2_success(self):
        """ 투자금 입금 phase 2 성공 테스트 """
        # phase 2 테스트를 위해 phase 1 실행
        phase1_data = {
            'account_number': self.account.number,
            'user_name': self.user.name,
            'transfer_amount': 1000,
        }
        request_url = self.phase1_test_url
        response = self.client.post(request_url, data=phase1_data, format='json')
        transfer_identifier = response.data['transfer_identifier']

        # phase 2 테스트
        string = self.account.number + self.user.name + str(1000)
        signature = bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        phase2_data = {
            'signature': signature,
            'transfer_identifier': transfer_identifier,
        }
        request_url = self.phase2_test_url
        response = self.client.post(request_url, data=phase2_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
