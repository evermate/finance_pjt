# products/views/recommendation.py

from datetime import date

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from products.models import DepositProduct, InterestOption

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_by_profile(request):
    asset_param = request.query_params.get('asset')
    top_n = int(request.query_params.get('top_n', 5))
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
    age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))

    four_banks = ["국민은행", "하나은행", "신한은행", "우리은행"]
    TERM_THRESHOLD = 12
    recs = []

    for prod in DepositProduct.objects.select_related('bank').prefetch_related('options'):
        if age >= 40 and prod.bank.kor_co_nm not in four_banks:
            continue

        for opt in prod.options.all():
            if not opt.save_trm or opt.intr_rate is None:
                continue
            try:
                term = int(opt.save_trm)
                rate = float(opt.intr_rate)
            except (TypeError, ValueError):
                continue

            if age <= 29:
                if asset > 100_000_000 and term <= TERM_THRESHOLD:
                    continue
                if asset <= 100_000_000 and term > TERM_THRESHOLD:
                    continue
            elif age < 40:
                if asset > 150_000_000 and term <= TERM_THRESHOLD:
                    continue
                if asset <= 150_000_000 and term > TERM_THRESHOLD:
                    continue
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
