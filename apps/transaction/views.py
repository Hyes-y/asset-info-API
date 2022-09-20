# django rest api
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
# local modules
from .models import Transaction, TransactionInfo
from .serializers import TransactionSerializer, TransactionCheckSerializer


class TransactionViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """ 거래 내역 생성 Viewset """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionCheckViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """ 거래 내역 유효성 검증 Viewset """

    queryset = TransactionInfo.objects.all()
    serializer_class = TransactionCheckSerializer