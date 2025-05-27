# backend/products/views/ai_recommendation.py
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from openai import OpenAI
import traceback
import json

from .recommendation import RecommendViewSet

# OpenAI 클라이언트 초기화 (gpt-4o-mini 사용)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Function Calling 스키마 정의
functions = [
    {
        "name": "get_recommendations",
        "description": "사용자에게 가장 적합한 3개 금융상품을 반환합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "recommendations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fin_prdt_cd": {"type": "string"},
                            "reason":      {"type": "string"}
                        },
                        "required": ["fin_prdt_cd", "reason"]
                    }
                }
            },
            "required": ["recommendations"]
        }
    }
]

class AIRecommendAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # 1) 자산 파라미터 검사
            asset_param = request.query_params.get('asset')
            if asset_param is None:
                return Response({'error': 'asset 파라미터는 필수입니다.'}, status=400)
            try:
                asset = float(asset_param)
            except ValueError:
                return Response({'error': 'asset은 숫자 형태여야 합니다.'}, status=400)

            # 2) 사용자 프로필
            user = request.user
            bd = getattr(user, 'birth_date', None)
            if not bd:
                return Response({'error': '생년월일 정보가 없습니다.'}, status=400)
            today = date.today()
            age = today.year - bd.year +1
            gender = getattr(user, 'gender', 'O')

            # 3) 기존 추천 10개 가져오기
            rec_view = RecommendViewSet()
            rec_view.request = request
            base_res = rec_view.recommend_by_profile(request)
            top10 = base_res.data[:10]

            # 4) 프롬프트 구성
            products_info = [
                f"[{p['fin_prdt_cd']}] {p['fin_prdt_nm']} - 은행:{p['bank']['kor_co_nm']}, "
                f"기간:{p['save_trm']}개월, 금리:{p['intr_rate']}%"
                for p in top10
            ]
            prompt = (
                "아래 10개의 예·적금 상품 목록 중 사용자에게 가장 적합한 3개를 선정하십시오."
                "각 상품 코드(fin_prdt_cd)와 함께, 최소 2~3문장으로 구체적이며,"
                "선택되지 않은 나머지 상품 대비 장점을 명확히 설명하는(reason) JSON 배열을 반환해주세요."
                f"\n사용자: 나이 {age}세, 성별 {gender}, 자산 {asset:.0f}원.\n"
                "상품 목록:\n" + "\n".join(products_info)
            )

            # 5) 함수 호출 방식으로 OpenAI 요청
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a financial expert."},
                    {"role": "user",   "content": prompt}
                ],
                functions=functions,
                function_call={"name": "get_recommendations"},
                max_tokens=800,
                temperature=0.7,
            )

            # 6) 함수 호출 응답에서 arguments 추출
            message = resp.choices[0].message
            if hasattr(message, 'function_call'):
                args = message.function_call.arguments
                data = json.loads(args)
                ai_recs = data.get('recommendations', [])
            else:
                ai_recs = []

            # 7) 기존 top10 데이터와 병합
            merged = []
            for ai in ai_recs:
                code = ai.get('fin_prdt_cd')
                reason = ai.get('reason')
                prod = next((p for p in top10 if p['fin_prdt_cd'] == code), None)
                if prod:
                    item = prod.copy()
                    item['reason'] = reason
                    merged.append(item)

            return Response(merged)

        except Exception as e:
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)

