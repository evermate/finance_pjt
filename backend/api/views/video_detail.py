# backend/api/views/video_detail.py
from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import AllowAny
from django.conf                import settings
import requests

class YouTubeVideoDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        vid = request.query_params.get('id')
        if not vid:
            return Response({'error': 'id 파라미터가 필요합니다.'}, status=400)

        url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part':       'snippet,contentDetails,statistics',
            'id':         vid,
            'key':        settings.YOUTUBE_API_KEY,
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        # items 리스트가 없어도 빈 배열로 대응
        items = data.get('items', [])
        if not items:
            return Response({'error': '존재하지 않는 비디오입니다.'}, status=404)
        return Response(items[0])
