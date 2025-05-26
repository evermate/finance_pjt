import numpy as np
import pandas as pd

def simulate_retirement(
    start_age: int,
    retirement_age: int,
    end_age: int,
    initial_assets: float,
    initial_savings: float,
    savings_growth_rate: float,
    mean_return: float,
    return_volatility: float,
    inflation_rate: float,
    tax_rate: float,
    fee_rate: float,
    annual_expense: float,
    n_simulations: int
) -> pd.DataFrame:
    years = end_age - start_age + 1
    ages = np.arange(start_age, end_age + 1)
    results = np.zeros((n_simulations, years))

    for sim in range(n_simulations):
        assets = initial_assets
        for i, age in enumerate(ages):
            # (1) 동적 저축
            savings = (initial_savings * ((1 + savings_growth_rate) ** i)
                       if age < retirement_age else 0)
            # (2) 랜덤 수익률
            annual_rate = np.random.normal(mean_return, return_volatility)
            # (3) 세후·수수료 차감 수익
            gross_return = (assets + savings) * annual_rate
            net_return = gross_return * (1 - tax_rate) - (assets + savings) * fee_rate
            # (4) 인플 전 자산
            pre_inf = assets + savings + net_return
            # (5) 인플레이션 반영
            real_assets = pre_inf / (1 + inflation_rate)
            # (6) 은퇴 후 지출 반영
            if age >= retirement_age:
                real_assets = max(real_assets - annual_expense, 0)
            assets = real_assets
            results[sim, i] = assets

    return pd.DataFrame(results, columns=ages)