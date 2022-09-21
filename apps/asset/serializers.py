from rest_framework import serializers
from .models import Asset, AssetInfo


class AssetInfoSerializer(serializers.ModelSerializer):
    """ 보유 종목 정보 시리얼라이저 """
    class Meta:
        model = AssetInfo
        fields = ('name', 'group', 'isin')


class AssetSerializer(serializers.ModelSerializer):
    """
    보유 종목 조회 시리얼라이저
    보유 종목 정보와 총 금액(보유 수량 * 현재가) 제공
    """
    info = AssetInfoSerializer(read_only=True)
    total = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = Asset
        fields = ('info', 'total')

