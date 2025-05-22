from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BankViewSet, DepositProductViewSet, InterestOptionViewSet

router = DefaultRouter()
router.register(r'banks', BankViewSet, basename='bank')
router.register(r'deposits', DepositProductViewSet, basename='deposit')
router.register(r'options', InterestOptionViewSet, basename='option')

urlpatterns = [
    path('', include(router.urls)),
]
