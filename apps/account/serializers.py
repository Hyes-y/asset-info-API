from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Account


class AccountSerializer(ModelSerializer):
    """ 투자 내역 조회 (투자 화면) 시리얼라이저 """
    total_assets = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'name', 'stock_firm', 'number', 'total_assets', 'user')


class AccountDetailSerializer(AccountSerializer):
    """
    투자 상세 내역 조회 (투자 상세 화면) 시리얼라이저

    총 수익금(total_profits) = 총 자산(total_asset) - 투자 원금(principal)
    수익률(profits_ratio) = 총 수익금(total_profits) / 투자 원금(principal) * 100
    """
    total_profits = SerializerMethodField()
    profits_ratio = SerializerMethodField()

    class Meta:
        model = Account
        fields = ('name', 'stock_firm', 'number', 'principal', 'total_assets',
                  'total_profits', 'profits_ratio', 'user')

    def get_total_profits(self, obj):
        """ 총 수익금 반환 함수 """
        return obj.total_assets - obj.principal

    def get_profits_ratio(self, obj):
        """ 수익률 반환 함수 """
        return ((obj.total_assets - obj.principal) / obj.principal) * 100
