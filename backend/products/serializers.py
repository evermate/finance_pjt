from rest_framework import serializers
from .models import Bank, DepositProduct, InterestOption

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class InterestOptionSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.fin_prdt_cd', read_only=True)  # ✅ 상품 ID 직접 포함

    class Meta:
        model = InterestOption
        fields = [
            'id',
            'save_trm',
            'intr_rate_type_nm',
            'intr_rate',
            'intr_rate2',
            'rsrv_type_nm',
            'product',  # ✅ 추가됨
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
            'join_member',      # ✅ 가입 대상
            'join_way',         # ✅ 가입 방법
            'spcl_cnd',         # ✅ 우대 조건
            'options',  # 전체 옵션 포함됨
        ]

class DepositProductFullSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.kor_co_nm', read_only=True)
    options = InterestOptionSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = [
            'fin_prdt_cd',
            'fin_prdt_nm',
            'product_type',
            'bank_name',
            'options',  # ✅ 금리 옵션 포함됨
        ]
        