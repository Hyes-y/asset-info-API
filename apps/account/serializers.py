from django.db.models import Sum, F
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Account, Asset


class AccountSerializer(ModelSerializer):
    """ 투자 시리얼라이저 """
    class Meta:
        model = Account
        fields = ('name', 'stock_firm', 'number', 'total_assets')


class AccountDetailSerializer(AccountSerializer):
    class Meta:
        model = Account
        fields = ('name', 'stock_firm', 'number', 'total_assets'
                  'principal', )
