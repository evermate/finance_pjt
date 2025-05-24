# products/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include

# ✅ views 디렉토리 기준으로 변경된 경로
from .views.main import BankViewSet, DepositProductViewSet, InterestOptionViewSet
from .views.recommendation import recommend_by_profile

router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'deposits', DepositProductViewSet, basename='deposit')
router.register(r'options', InterestOptionViewSet, basename='option')

urlpatterns = [
    path('', include(router.urls)),
    path('deposits/recommend_by_profile/', recommend_by_profile),
]
