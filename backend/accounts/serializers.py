# accounts/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False)  # 선택적으로 설정 (필수로 바꿀 수도 있음)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['age'] = self.validated_data.get('age', None)
        return data
