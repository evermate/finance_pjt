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
            'id',
            'save_trm',
            'intr_rate_type_nm',
            'intr_rate',
            'intr_rate2',
            'rsrv_type_nm',
        ]


class DepositProductSerializer(serializers.ModelSerializer):
    bank = BankSerializer(read_only=True)
    options = InterestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = [
            'fin_prdt_cd',
            'fin_prdt_nm',
            'product_type',
            'bank',
            'max_limit',
            'dcls_strt_day',
            'mtrt_int',      # 만기 후 이자율
            'spcl_cnd',      # 우대조건
            'join_deny',     # 가입제한
            'join_way',      # 가입방법
            'join_member',   # 가입대상
            'options',
        ]
