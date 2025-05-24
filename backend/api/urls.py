# backend/api/urls.py
from django.urls import path
# 아래처럼 map_search.py 에 정의된 함수를 직접 임포트하세요
from .views.map_search      import search_bank
from .views.youtube_search  import YouTubeSearchAPIView

urlpatterns = [
    path('map/search-bank/', search_bank, name='search-bank'),
    path('youtube/search/',   YouTubeSearchAPIView.as_view(), name='youtube-search'),
]
