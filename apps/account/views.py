# django rest api
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# django modules
from django.db.models import Sum, F
# local modules
from .models import Account
from .serializers import AccountSerializer, AccountDetailSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    투자 내역 조회 Viewset
    list: 로그인 한 유저의 투자 내역을 조회할 수 있다.
    (계좌명, 증권사, 계좌번호, 계좌 총 자산)
    retrieve: 로그인한 유저의 투자 상세 내역을 조회할 수 있다.
    (계좌명, 증권사, 계좌번호, 계좌 총 자산, 투자원금, 총 수익금, 수익률)
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ 유저의 계좌 정보와 해당 계좌의 총 자산(현재가 * 수량)을 포함하는 쿼리셋 반환 """
        user = self.request.user
        account = Account.objects.filter(user=user).annotate(
            total_assets=Sum(F('asset__price') * F('asset__count'))
        )
        return account

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'retrieve':
            return AccountDetailSerializer

        elif hasattr(self, 'action') and self.action == 'list':
            return AccountSerializer

