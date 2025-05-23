# backend/api/views.py
import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def search_bank(request):
    query = request.GET.get('query')
    if not query:
        return Response({'error': 'query 파라미터가 필요합니다.'}, status=400)

    kakao_url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = { 'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}' }
    params = { 'query': query }

    try:
        res = requests.get(kakao_url, headers=headers, params=params)
        print('📦 Kakao 응답:', res.status_code)
        return Response(res.json(), status=res.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
