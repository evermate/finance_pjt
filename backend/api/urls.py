# backend/api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('map/search-bank/', views.search_bank),
]
