from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Bank  # ✅ 이미 존재하는 Bank 모델 사용

class User(AbstractUser): 
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)  # 생년월일
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성'), ('O', '기타')], blank=True, null=True)
    main_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, blank=True, null=True)
    monthly_income_range = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # ✅ 프로필 사진

    def __str__(self):
        return self.username
