# django rest api
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
# django modules
from django.db.models import Sum, F
# local modules
from .models import Account
from .serializers import AccountSerializer, AccountDetailSerializer


class AccountViewSet(viewsets.GenericViewSet):
    """ 계좌 내역 조회 Viewset """
    def get_queryset(self):
        user = self.request.user
        account = Account.objects.filter(user=user).aggregate(
            total_assets=Sum(F('asset__price') * F('asset__count'))
        )
        return account

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'detail':
            return AccountDetailSerializer

        elif hasattr(self, 'action') and self.action == 'info':
            return AccountSerializer

    @action(methods=['get'], detail=False, url_path=None, url_name=None)
    def info(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def detail(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
