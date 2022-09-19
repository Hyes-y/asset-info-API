from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from .models import Account


class AccountSerializer(ModelSerializer):
    total_assets = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    """ 투자 정보 조회 시리얼라이저 """
    class Meta:
        model = Account
        fields = ('id', 'name', 'stock_firm', 'number', 'total_assets', 'user')


class AccountDetailSerializer(AccountSerializer):
    total_profits = SerializerMethodField()
    profits_ratio = SerializerMethodField()

    class Meta:
        model = Account
        fields = ('name', 'stock_firm', 'number', 'principal', 'total_assets',
                  'total_profits', 'profits_ratio', 'user')

    def get_total_profits(self, obj):
        return obj.total_assets - obj.principal

    def get_profits_ratio(self, obj):
        return ((obj.total_assets - obj.principal) / obj.principal) * 100
