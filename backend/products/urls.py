# products/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include

# ✅ views 디렉토리 기준으로 변경된 경로
from products.views.main import BankViewSet, DepositProductViewSet, InterestOptionViewSet
from products.views.recommendation import RecommendViewSet
from .views.ai_recommendation import AIRecommendAPIView



router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'deposits', DepositProductViewSet, basename='deposit')
router.register(r'options', InterestOptionViewSet, basename='option')
router.register(r'recommends',  RecommendViewSet, basename='recommend')

urlpatterns = [
    path('', include(router.urls)),  # <-- /banks/, /deposits/ 등
    path('ai-recommend/', AIRecommendAPIView.as_view(), name='ai-recommend'),
]