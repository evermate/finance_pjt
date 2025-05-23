# products/views.py

from datetime import date

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import OuterRef, Subquery, FloatField

from .models import Bank, DepositProduct, InterestOption
from .serializers import BankSerializer, DepositProductSerializer, InterestOptionSerializer


# ─── 기본 페이지네이션 설정 ────────────────────────────────────────
class StandardResultsPagination(PageNumberPagination):
    page_size = 10  # 한 페이지당 10개씩 반환


# ─── 은행 API ─────────────────────────────────────────────────────
class BankViewSet(viewsets.ReadOnlyModelViewSet):
    """
    은행 목록 및 상세 조회
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    lookup_field = 'fin_co_no'


# ─── 예금/적금 상품 API ────────────────────────────────────────────
class DepositProductViewSet(viewsets.ModelViewSet):
    queryset = DepositProduct.objects.select_related('bank').prefetch_related('options')
    serializer_class = DepositProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['fin_prdt_nm', 'bank__kor_co_nm']
    ordering_fields = ['dcls_strt_day', 'fin_prdt_nm']

    @action(
        detail=False, methods=['get'], url_path='recommend_by_profile',
        authentication_classes=[TokenAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def recommend_by_profile(self, request):
        asset_param = request.query_params.get('asset')
        top_n       = int(request.query_params.get('top_n', 5))
        if asset_param is None:
            return Response({"error": "asset 파라미터는 필수입니다."}, status=400)
        try:
            asset = float(asset_param)
        except ValueError:
            return Response({"error": "asset은 숫자 형태여야 합니다."}, status=400)

        bd = getattr(request.user, 'birth_date', None)
        if not bd:
            return Response({"error": "생년월일 정보가 없습니다."}, status=400)
        today = date.today()
        age   = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))

        four_banks     = ["국민은행", "하나은행", "신한은행", "우리은행"]
        TERM_THRESHOLD = 12
        recs = []

        for prod in self.queryset:
            # 40대 이상은 4대 은행만, 그리고 단기 상품(≤12개월)만
            if age >= 40:
                if prod.bank.kor_co_nm not in four_banks:
                    continue

            for opt in prod.options.all():
                if not opt.save_trm or opt.intr_rate is None:
                    continue
                try:
                    term = int(opt.save_trm)
                    rate = float(opt.intr_rate)
                except (TypeError, ValueError):
                    continue

                # 20대 이하
                if age <= 29:
                    if asset > 100_000_000:
                        # 장기만(12개월 초과)
                        if term <= TERM_THRESHOLD:
                            continue
                    else:
                        # 단기만(12개월 이하)
                        if term > TERM_THRESHOLD:
                            continue

                # 30대 (30 ≤ age < 40)
                elif age < 40:
                    if asset > 150_000_000:
                        if term <= TERM_THRESHOLD:
                            continue
                    else:
                        if term > TERM_THRESHOLD:
                            continue

                # 40대 이상(else 블록): 위에서 4대 은행만 필터링 했으니, 단기만(12개월 이하)
                else:
                    if term > TERM_THRESHOLD:
                        continue

                recs.append({
                    'fin_prdt_cd': prod.fin_prdt_cd,
                    'fin_prdt_nm': prod.fin_prdt_nm,
                    'bank': {
                        'fin_co_no': prod.bank.fin_co_no,
                        'kor_co_nm': prod.bank.kor_co_nm,
                    },
                    'option_id':    opt.id,
                    'save_trm':     term,
                    'intr_rate':    rate,
                })

        top_recs = sorted(recs, key=lambda x: x['intr_rate'], reverse=True)[:top_n]
        return Response(top_recs)

# ─── 금리 옵션 API ────────────────────────────────────────────────────
class InterestOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterestOption.objects.select_related('product')
    serializer_class = InterestOptionSerializer
