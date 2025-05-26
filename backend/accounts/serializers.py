# accounts/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from datetime import date 
from rest_framework import serializers
from .models import User, JoinedProduct
from products.models import Bank, DepositProduct
from products.serializers import DepositProductFullSerializer, InterestOptionSerializer

class CustomRegisterSerializer(RegisterSerializer):
    birth_date = serializers.DateField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['birth_date'] = self.validated_data.get('birth_date')
        return data

    def save(self, request):
        user = super().save(request)
        user.birth_date = self.validated_data.get('birth_date')
        user.save()
        return user

# ✅ 주거래 은행 정보 출력용
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['fin_co_no', 'kor_co_nm']

# ✅ 상품 요약용 시리얼라이저 추가
class DepositProductSimpleSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.kor_co_nm', read_only=True)
    class Meta:
        model = DepositProduct
        fields = ['fin_prdt_cd', 'fin_prdt_nm', 'product_type', 'bank_name']


class JoinedProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.fin_prdt_nm', read_only=True)
    product_type = serializers.CharField(source='product.product_type', read_only=True)
    option = InterestOptionSerializer(read_only=True)

    class Meta:
        model = JoinedProduct
        fields = ['id', 'product_name', 'product_type', 'option', 'joined_at']


# ✅ 마이페이지 및 유저 정보 출력용
class UserSerializer(serializers.ModelSerializer):
    main_bank = BankSerializer(read_only=True)
    age = serializers.SerializerMethodField()
    joined_products = JoinedProductSerializer(source='joinedproduct_set', many=True, read_only=True)

    def get_age(self, obj):
        if obj.birth_date:
            return date.today().year - obj.birth_date.year + 1
        return None

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'age', 'birth_date', 'phone_number', 'gender',
            'main_bank', 'monthly_income_range',
            'profile_image',
            'joined_products',
        ]

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone_number',
            'birth_date',
            'gender',
            'main_bank',
            'monthly_income_range',
            'profile_image',
        ]
