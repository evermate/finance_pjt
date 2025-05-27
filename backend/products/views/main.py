from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch, OuterRef, Subquery, FloatField
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView

from ..models import Bank, DepositProduct, InterestOption
from ..serializers import BankSerializer, DepositProductSerializer, InterestOptionSerializer


# 📄 기본 페이지네이션 설정
class StandardResultsPagination(PageNumberPagination):
    page_size = 10


# 📄 은행 API
class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    lookup_field = 'fin_co_no'


# 📄 정기예금/적금 API
class DepositProductViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer

    @action(detail=False, methods=['get'], url_path='recommend')
    def recommend(self, request):
        top_n = int(request.query_params.get('top_n', 5))
        min_term = request.query_params.get('min_term')
        max_term = request.query_params.get('max_term')

        products = DepositProduct.objects.select_related('bank') \
                                         .prefetch_related('options') \
                                         .all()

        recs = []
        for prod in products:
            for opt in prod.options.all():
                if not opt.save_trm or not opt.intr_rate2:
                    continue
                try:
                    term = int(opt.save_trm)
                    rate = float(opt.intr_rate2)
                except (TypeError, ValueError):
                    continue
                if min_term and term < int(min_term):
                    continue
                if max_term and term > int(max_term):
                    continue
                annualized = rate * (12 / term)
                recs.append({
                    'fin_prdt_cd': prod.fin_prdt_cd,
                    'fin_prdt_nm': prod.fin_prdt_nm,
                    'bank': {
                        'fin_co_no': prod.bank.fin_co_no,
                        'kor_co_nm': prod.bank.kor_co_nm,
                    },
                    'option_id': opt.id,
                    'save_trm': term,
                    'intr_rate2': rate,
                    'annualized_rate': round(annualized, 4),
                    'score': round(annualized, 4),
                })

        top_recs = sorted(recs, key=lambda x: x['score'], reverse=True)[:top_n]
        return Response(top_recs)

    @action(detail=False, methods=['get'], url_path='sorted')
    def sorted(self, request):
        term = request.query_params.get('term')
        product_type = request.query_params.get('type', 'saving')  # 기본: 적금
    
        if term is None:
            return Response({"error": "term query param is required"}, status=400)
    
        rate_subquery = InterestOption.objects.filter(
            product=OuterRef('pk'),
            save_trm=term,
            intr_rate2__isnull=False
        ).order_by('-intr_rate2').values('intr_rate2')[:1]
    
        products = DepositProduct.objects.filter(product_type=product_type) \
            .annotate(top_rate=Subquery(rate_subquery, output_field=FloatField())) \
            .order_by('-top_rate') \
            .prefetch_related('options', 'bank')
    
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='slider')
    def slider(self, request):
        banks_param = request.query_params.get('banks')
        banks = banks_param.split(',') if banks_param else ["국민은행","하나은행","신한은행","우리은행"]
        limit = int(request.query_params.get('limit', 2))

        result = []
        for bank_name in banks:
            qs = self.queryset.filter(bank__kor_co_nm=bank_name)
            qs = qs.prefetch_related('options')
            best_per_product = []
            for prod in qs:
                opts = [o for o in prod.options.all() if o.intr_rate is not None]
                if not opts:
                    continue
                best = max(opts, key=lambda o: o.intr_rate)
                best_per_product.append((prod, best))
            top_n = sorted(best_per_product, key=lambda x: x[1].intr_rate, reverse=True)[:limit]
            for prod, opt in top_n:
                result.append({
                    'fin_prdt_cd': prod.fin_prdt_cd,
                    'fin_prdt_nm': prod.fin_prdt_nm,
                    'bank':        {'kor_co_nm': prod.bank.kor_co_nm},
                    'option_id':   opt.id,
                    'save_trm':    int(opt.save_trm),
                    'intr_rate':   opt.intr_rate,
                })

        return Response(result)


# 📄 금리 옵션 API
class InterestOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InterestOption.objects.select_related('product')
    serializer_class = InterestOptionSerializer

class DepositProductDetailView(RetrieveAPIView):
    queryset = DepositProduct.objects.all()
    serializer_class = DepositProductSerializer
