# backend/api/views/youtube_search.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
import requests

class YouTubeSearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = request.query_params.get('q')
        if not q:
            return Response({'error': 'q 파라미터가 필요합니다.'}, status=400)

        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part':       'snippet',
            'q':          q,
            'type':       'video',
            'maxResults': 10,
            'key':        settings.YOUTUBE_API_KEY,
        }
        resp = requests.get(url, params=params)
        return Response(resp.json())
