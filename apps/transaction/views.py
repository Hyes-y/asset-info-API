from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, TransactionInfo
from .serializers import TransactionSerializer, TransactionCheckSerializer


class TransactionViewSet(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """ 거래 내역 생성 (phase 2) Viewset """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


class TransactionCheckViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """ 거래 내역 유효성 검증 (phase 1) Viewset """

    queryset = TransactionInfo.objects.all()
    serializer_class = TransactionCheckSerializer
    permission_classes = [IsAuthenticated]