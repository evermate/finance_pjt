from django.urls import path
from .views import SimulationAPIView

urlpatterns = [
    path('', SimulationAPIView.as_view(), name='simulation'),
]