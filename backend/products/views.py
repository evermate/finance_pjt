# products/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.db.models import IntegerField
from django.db.models.functions import Cast

from .models import Bank, DepositProduct, InterestOption
from .serializers import BankSerializer, DepositProductSerializer, InterestOptionSerializer


# ─── 변경: 기본 페이지 크기를 지정한 커스텀 페이징 클래스 추가 ─────────────────────
class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # 한 페이지당 10개씩 반환


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    은행 목록 및 상세 조회 API
    ReadOnlyModelViewSet을 사용하여 조회 기능만 제공
    lookup_field를 'fin_co_no'로 설정하여 URL에 은행 코드로 상세 조회 가능
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    lookup_field = 'fin_co_no'


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DepositProduct
from .serializers import DepositProductSerializer

class DepositProductViewSet(viewsets.ModelViewSet):
    """
    정기예금(Deposit) 상품 API 뷰셋
    - 기본 CRUD는 ModelViewSet이 제공
    - /recommend/ 액션으로 추천 기능 추가
    """
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer

    @action(detail=False, methods=['get'], url_path='recommend')
    def recommend(self, request):
        """
        추천 엔드포인트: /api/products/deposits/recommend/
        GET 파라미터:
          - top_n: 상위 몇 개를 반환할지 (기본값 5)
          - min_term: 최소 저축 기간(개월) 필터링 (선택)
          - max_term: 최대 저축 기간(개월) 필터링 (선택)
        반환:
          - 옵션별 연환산 금리 기준 상위 top_n개 리스트 (JSON)
        """
        # 요청 쿼리에서 top_n, min_term, max_term 가져오기
        top_n    = int(request.query_params.get('top_n', 5))  # top_n: 기본 5
        min_term = request.query_params.get('min_term')       # 최소 기간 (optional)
        max_term = request.query_params.get('max_term')       # 최대 기간 (optional)

        # 1) DB에서 모든 상품과 옵션을 미리 조회하여 N+1 쿼리 방지
        #    - select_related('bank'): 은행(FK) 조인
        #    - prefetch_related('options'): 옵션(M2M 또는 FK) 조인
        products = DepositProduct.objects.select_related('bank') \
                                         .prefetch_related('options') \
                                         .all()

        recs = []  # 추천 결과를 담을 리스트

        # 2) 상품별, 옵션별로 순회하며 score 계산
        for prod in products:
            for opt in prod.options.all():
                # ——————————————
                # 2-1) 필수 값이 없으면 스킵
                #    - save_trm: 저축 기간(개월)
                #    - intr_rate: 기본 금리
                if not opt.save_trm or not opt.intr_rate:
                    # None 또는 빈 문자열인 경우 continue
                    continue

                # 2-2) 문자열→수치 변환: int(save_trm), float(intr_rate)
                try:
                    term = int(opt.save_trm)   # 기간(개월)
                    rate = float(opt.intr_rate)  # 금리(%)
                except (TypeError, ValueError):
                    # 변환 실패 시 해당 옵션 건너뛰기
                    continue

                # 2-3) 기간 필터링
                #    - min_term이 지정돼 있으면 term < min_term 옵션 제외
                if min_term and term < int(min_term):
                    continue
                #    - max_term이 지정돼 있으면 term > max_term 옵션 제외
                if max_term and term > int(max_term):
                    continue

                # 2-4) 연환산 금리 계산 (단리 기준)
                #    annualized = rate * (12 / term)
                #    ex) 6개월, rate=2.6 → 2.6*(12/6)=5.2% 연환산
                annualized = rate * (12 / term)

                # 2-5) 추천 리스트에 담기
                recs.append({
                    'fin_prdt_cd': prod.fin_prdt_cd,           # 상품 코드
                    'fin_prdt_nm': prod.fin_prdt_nm,           # 상품 이름
                    'bank': {
                        'fin_co_no': prod.bank.fin_co_no,      # 은행 코드
                        'kor_co_nm': prod.bank.kor_co_nm,      # 은행 이름
                    },
                    'option_id': opt.id,                       # 옵션 고유 ID
                    'save_trm': term,                          # 저축 기간(개월)
                    'intr_rate': rate,                         # 기본 금리(%)
                    'annualized_rate': round(annualized, 4),   # 연환산 금리(소수점 4자리)
                    'score': round(annualized, 4),             # 정렬 기준 점수
                })

        # 3) score 기준 내림차순 정렬 후 상위 top_n개 자르기
        top_recs = sorted(recs, key=lambda x: x['score'], reverse=True)[:top_n]

        # 4) Response로 반환 (JSON)
        return Response(top_recs)

    



class InterestOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    금리 옵션 목록 및 상세 조회 API
    select_related를 사용해 product 정보를 미리 로드하여 성능 최적화
    """
    queryset = InterestOption.objects.select_related('product')
    serializer_class = InterestOptionSerializer


# ─── 테스트용 HTML 렌더링 뷰 (완료 후 삭제) ────────────────────────────────────────
from django.shortcuts import render
from django.views import View

class DjangoTemplateTestView(View):
    def get(self, request):
        products = DepositProduct.objects.all()
        context = {
            'message': '템플릿 렌더링 성공!',
            'products': products,
        }
        return render(request, 'products/django.html', context)