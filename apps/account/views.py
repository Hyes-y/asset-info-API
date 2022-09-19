# django rest api
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
# django modules
from django.db.models import Sum, F
# local modules
from .models import Account
from apps.user.models import User
from .serializers import AccountSerializer, AccountDetailSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """ 계좌 내역 조회 Viewset """
    def get_queryset(self):
        user = User.objects.get(id=2)
        account = Account.objects.filter(user=user).annotate(
            total_assets=Sum(F('asset__price') * F('asset__count'))
        )
        return account

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'retrieve':
            return AccountDetailSerializer

        elif hasattr(self, 'action') and self.action == 'list':
            return AccountSerializer

