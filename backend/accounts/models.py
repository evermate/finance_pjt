from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import Bank, DepositProduct, InterestOption  # ✅ 이미 존재하는 Bank 모델 사용

class User(AbstractUser): 
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)  # 생년월일
    gender = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성'), ('O', '기타')], blank=True, null=True)
    main_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, blank=True, null=True)
    monthly_income_range = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # ✅ 프로필 사진

    joined_products = models.ManyToManyField(
        DepositProduct,
        through='JoinedProduct',
        blank=True,
        related_name='joined_users'
    )

    def __str__(self):
        return self.username

class JoinedProduct(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE)
    option = models.ForeignKey(InterestOption, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'option')  # 하나의 조건으로 중복 가입 방지

    def __str__(self):
        return f"{self.user.username} - {self.option}"
    