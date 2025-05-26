from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import SimulationSerializer
from .utils import simulate_retirement
import pandas as pd

class SimulationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SimulationSerializer(data=request.data)
        if not serializer.is_valid():
            # 필수항목이 하나라도 빠졌을 때
            return Response({
                'error': '모든 입력 항목을 채워주세요!',
                'details': serializer.errors
            },
            status=400
            )

        data = serializer.validated_data

        # 고정 파라미터
        return_volatility = 0.05
        inflation_rate    = 0.03
        tax_rate          = 0.154
        fee_rate          = 0.005

        # 시뮬레이션 실행
        df = simulate_retirement(
            start_age=data['start_age'],
            retirement_age=data['retirement_age'],
            end_age=data['end_age'],
            initial_assets=data['initial_assets'],
            initial_savings=data['initial_savings'],
            savings_growth_rate=data['savings_growth_rate'],
            mean_return=data['mean_return'],
            return_volatility=return_volatility,
            inflation_rate=inflation_rate,
            tax_rate=tax_rate,
            fee_rate=fee_rate,
            annual_expense=data['annual_expense'],
            n_simulations=data['n_simulations']
        )

        # 요약 통계
        df_summary = pd.DataFrame({
            'age': df.columns.astype(int),
            'median_assets': df.median(),
            'p10_assets': df.quantile(0.1),
            'p90_assets': df.quantile(0.9),
        })

        return Response(df_summary.to_dict(orient='list'))
    