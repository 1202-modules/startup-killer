from decimal import Decimal
import pytest
from backend.app.engine.scoring import calculate_score
from backend.app.engine.types import FinalStatus, BaselineMonth

def test_scoring_baseline_coffeebot():
    # Coffeebot baseline: B = 472385682, C = 472385682
    baseline_series = [
        BaselineMonth(month=i, closing_cash_kopeks=472385682, revenue_kopeks=270714177, variable_cost_kopeks=94749962, profit_kopeks=-24035785)
        for i in range(10)
    ]
    # In month 9: burn = fixed(200_000_000) + var(94_749_962) - rev(270_714_177) = 24_035_785
    fixed_cost = 200000000
    actual_cash = 472385682
    actual_revenue = 270714177
    actual_var_cost = 94749962
    
    score = calculate_score(
        actual_cash_kopeks=actual_cash,
        actual_revenue_kopeks=actual_revenue,
        actual_variable_cost_kopeks=actual_var_cost,
        actual_fixed_cost_kopeks=fixed_cost,
        bankruptcy_month=None,
        unpaid_obligations_kopeks=0,
        baseline_series=baseline_series,
        baseline_fixed_cost_kopeks=fixed_cost,
    )
    assert score.score == 0
    assert score.damage == 0.0
    assert score.solvency == 0.0
    assert score.early_bankruptcy == 0.0
    assert score.final_status == FinalStatus.SURVIVED

def test_scoring_weak_local_coffeebot():
    baseline_series = [
        BaselineMonth(month=0, closing_cash_kopeks=750000000),
        BaselineMonth(month=9, closing_cash_kopeks=472385682, revenue_kopeks=270714177, variable_cost_kopeks=94749962, profit_kopeks=-24035785)
    ]
    fixed_cost = 200000000
    actual_cash = 462789771
    actual_revenue = 270714177
    actual_var_cost = 94749962
    
    score = calculate_score(
        actual_cash_kopeks=actual_cash,
        actual_revenue_kopeks=actual_revenue,
        actual_variable_cost_kopeks=actual_var_cost,
        actual_fixed_cost_kopeks=fixed_cost,
        bankruptcy_month=None,
        unpaid_obligations_kopeks=0,
        baseline_series=baseline_series,
        baseline_fixed_cost_kopeks=fixed_cost,
    )
    assert score.score == 14
    assert abs(score.damage - 14.219604776251453) < 1e-6
    assert score.solvency == 0.0
    assert score.early_bankruptcy == 0.0

def test_scoring_structural_95pct_coffeebot():
    baseline_series = [
        BaselineMonth(month=0, closing_cash_kopeks=750000000),
        BaselineMonth(month=9, closing_cash_kopeks=472385682, revenue_kopeks=270714177, variable_cost_kopeks=94749962, profit_kopeks=-24035785)
    ]
    fixed_cost = 200000000
    actual_cash = 0
    actual_revenue = 12878763
    actual_var_cost = 4507567
    
    score = calculate_score(
        actual_cash_kopeks=actual_cash,
        actual_revenue_kopeks=actual_revenue,
        actual_variable_cost_kopeks=actual_var_cost,
        actual_fixed_cost_kopeks=fixed_cost,
        bankruptcy_month=4,
        unpaid_obligations_kopeks=17009241,
        baseline_series=baseline_series,
        baseline_fixed_cost_kopeks=fixed_cost,
    )
    assert score.damage == 700.0
    assert score.solvency == 200.0
    assert score.early_bankruptcy == 62.5
    assert score.score == 963
    assert score.final_status == FinalStatus.BANKRUPT
