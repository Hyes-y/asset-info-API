from rest_framework import serializers
from .models import Asset, AssetInfo


class AssetInfoSerializer(serializers.ModelSerializer):
    """ 투자 정보 조회 시리얼라이저 """
    class Meta:
        model = AssetInfo
        fields = ('name', 'group', 'isin')


class AssetSerializer(serializers.ModelSerializer):
    info = AssetInfoSerializer(read_only=True)
    total = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = Asset
        fields = ('info', 'total')

