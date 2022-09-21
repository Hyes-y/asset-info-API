from rest_framework import serializers
from django.db.models import F
from .models import Transaction, TransactionInfo
from apps.account.models import Account
import bcrypt


class TransactionSerializer(serializers.ModelSerializer):
    """ 거래 내역 생성 (phase 2) 시리얼라이저 """
    signature = serializers.CharField(max_length=100, write_only=True)
    transfer_identifier = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Transaction
        fields = ('tr_info', 'signature', 'transfer_identifier', 'is_transferred')
        read_only_fields = ('tr_info', 'is_transferred')

    def to_representation(self, instance):
        res = {"status": "true"}
        return res

    def validate(self, data):
        """
        데이터 유효성 검증
        - 데이터 존재 여부 확인
        - 요청 데이터와 기존에 저장된 거래내역 정보(해싱)가 일치하는지 확인
        """
        signature = data.get('signature', None)
        identifier = data.get('transfer_identifier', None)

        if not (signature or identifier):
            raise serializers.ValidationError("ERROR: 입력 데이터가 올바르지 않습니다.")

        try:
            tr = TransactionInfo.objects.filter(id=identifier)[0]
        except:
            raise serializers.ValidationError("ERROR: 거래 정보가 없습니다.")

        account_number = str(tr.account.number)
        user_name = str(tr.user.name)
        amount = str(int(tr.amount))
        tr_string = account_number + user_name + amount
        is_valid = False
        if bcrypt.checkpw(tr_string.encode('utf-8'), signature.encode('utf-8')):
            is_valid = True

        if Transaction.objects.filter(tr_info=tr).first():
            is_valid = False

        if not is_valid:
            raise serializers.ValidationError("ERROR: 유효하지 않은 거래 정보입니다.")

        return data

    def create(self, validated_data):
        identifier = validated_data.get('transfer_identifier', None)

        tr = TransactionInfo.objects.filter(id=identifier)[0]
        try:
            account = Account.objects.get(number=tr.account.number)
            account.principal = F('principal') + tr.amount
            account.save()
        except:
            raise

        return self.Meta.model.objects.create(is_transferred=True,
                                              tr_info=tr)


class TransactionCheckSerializer(serializers.ModelSerializer):
    """ 거래 내역 유효성 검증 (phase 1) 시리얼라이저 """
    account_number = serializers.CharField(max_length=20, write_only=True)
    user_name = serializers.CharField(max_length=30, write_only=True)
    transfer_amount = serializers.DecimalField(max_digits=20, decimal_places=2, write_only=True)

    class Meta:
        model = TransactionInfo
        fields = ('id', 'account_number', 'user_name', 'transfer_amount')

    def to_representation(self, instance):
        res = {'transfer_identifier': instance.id}
        return res

    def validate(self, data):
        """
        거래 내역 유효성 검증
        - 계좌 존재 여부
        - 계좌 소유주명과 거래내역 고객명이 일치하는지
        """
        error_message = 'ERROR: 올바르지 않은 입력 정보입니다.'
        account_number = data.get('account_number', None)
        user_name = data.get('user_name', None)

        account = Account.objects.filter(number=account_number)[0]

        if not (account and
                account.user.name == user_name):
            raise serializers.ValidationError(error_message)

        return data

    def create(self, validated_data):
        account_number = validated_data.get('account_number', None)
        transfer_amount = validated_data.get('transfer_amount', None)
        account = Account.objects.filter(number=account_number)[0]
        user = account.user

        try:
            tr_obj = TransactionInfo.objects.create(
                account=account,
                user=user,
                amount=transfer_amount,
            )
        except:
            raise serializers.ValidationError('ERROR: 거래 도중 오류가 발생했습니다.')

        else:
            return tr_obj
