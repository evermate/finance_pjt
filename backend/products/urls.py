# products/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BankViewSet, DepositProductViewSet, InterestOptionViewSet
from .views import DjangoTemplateTestView # 테스트 끝나면 지워야됨

router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'deposits', DepositProductViewSet, basename='deposit')
router.register(r'options', InterestOptionViewSet, basename='option')

urlpatterns = [
    path('', include(router.urls)),
    path('test-html/', DjangoTemplateTestView.as_view(), name='test-html'), # 테스트 끝나면 지워야됨
]