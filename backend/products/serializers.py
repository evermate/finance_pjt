from rest_framework import serializers
from .models import Bank, DepositProduct, InterestOption

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class InterestOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestOption
        fields = [
            'save_trm',
            'intr_rate_type_nm',
            'intr_rate',
            'intr_rate2',
            'rsrv_type_nm',
        ]


class DepositProductSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.kor_co_nm')
    options = InterestOptionSerializer(many=True, read_only=True)  # 전체 옵션 포함

    class Meta:
        model = DepositProduct
        fields = [
            'fin_prdt_cd',
            'dcls_strt_day',
            'fin_prdt_nm',
            'bank_name',
            'options',  # 전체 옵션 포함됨
        ]
