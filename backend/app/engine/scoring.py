from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from backend.app.engine.types import BaselineMonth, FinalScore, FinalStatus


def clamp_decimal(val: Decimal, low: Decimal, high: Decimal) -> Decimal:
    return max(low, min(high, val))


def quantize_half_up(val: Decimal) -> int:
    return int(val.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def calculate_risk(cash_kopeks: int, revenue_kopeks: int, variable_cost_kopeks: int, fixed_cost_kopeks: int) -> Decimal:
    burn = fixed_cost_kopeks + variable_cost_kopeks - revenue_kopeks
    if burn <= 0:
        return Decimal(0)
    runway = Decimal(cash_kopeks) / Decimal(burn)
    return clamp_decimal((Decimal(12) - runway) / Decimal(12), Decimal(0), Decimal(1))


def calculate_score(
    actual_cash_kopeks: int,
    actual_revenue_kopeks: int,
    actual_variable_cost_kopeks: int,
    actual_fixed_cost_kopeks: int,
    bankruptcy_month: Optional[int],
    unpaid_obligations_kopeks: int,
    baseline_series: List[BaselineMonth],
    baseline_fixed_cost_kopeks: int,
    deep_runway_months: int = 12,
    deep_cash_ratio: Decimal = Decimal('0.7'),
) -> FinalScore:
    m9_baseline = next(b for b in baseline_series if b.month == 9)
    baseline_cash_m9 = m9_baseline.closing_cash_kopeks
    
    is_bankrupt = bankruptcy_month is not None or unpaid_obligations_kopeks > 0
    actual_cash = 0 if is_bankrupt else actual_cash_kopeks
    
    # 1. Component A: Damage (0..700)
    if baseline_cash_m9 <= 0:
        comp_a = Decimal(0)
    else:
        fraction_lost = Decimal(baseline_cash_m9 - actual_cash) / Decimal(baseline_cash_m9)
        comp_a = Decimal(700) * clamp_decimal(fraction_lost, Decimal(0), Decimal(1))
        
    # 2. Component K: Solvency degradation (0..200)
    risk_baseline = calculate_risk(
        cash_kopeks=m9_baseline.closing_cash_kopeks,
        revenue_kopeks=m9_baseline.revenue_kopeks,
        variable_cost_kopeks=m9_baseline.variable_cost_kopeks,
        fixed_cost_kopeks=baseline_fixed_cost_kopeks,
    )
    
    if is_bankrupt:
        risk_actual = Decimal(1)
    else:
        risk_actual = calculate_risk(
            cash_kopeks=actual_cash_kopeks,
            revenue_kopeks=actual_revenue_kopeks,
            variable_cost_kopeks=actual_variable_cost_kopeks,
            fixed_cost_kopeks=actual_fixed_cost_kopeks,
        )
        
    if risk_baseline >= Decimal(1):
        comp_k = Decimal(0)
    else:
        solvency_ratio = (risk_actual - risk_baseline) / (Decimal(1) - risk_baseline)
        comp_k = Decimal(200) * clamp_decimal(solvency_ratio, Decimal(0), Decimal(1))
        
    # 3. Component E: Early bankruptcy (0..100)
    if is_bankrupt and bankruptcy_month is not None:
        comp_e = Decimal(100) * Decimal(9 - bankruptcy_month) / Decimal(8)
    else:
        comp_e = Decimal(0)
        
    # Total score
    raw_total = comp_a + comp_k + comp_e
    final_score_int = clamp_decimal(Decimal(quantize_half_up(raw_total)), Decimal(0), Decimal(1000))
    
    # Final status determination
    burn_now = actual_fixed_cost_kopeks + actual_variable_cost_kopeks - actual_revenue_kopeks
    runway_now = (Decimal(actual_cash_kopeks) / Decimal(burn_now)) if burn_now > 0 else Decimal("Infinity")
    
    if is_bankrupt:
        status = FinalStatus.BANKRUPT
    elif burn_now > 0 and runway_now <= Decimal(3) and actual_cash_kopeks > 0:
        status = FinalStatus.NEAR_BANKRUPTCY
    elif (burn_now > 0 and runway_now <= Decimal(deep_runway_months)) or (Decimal(actual_cash_kopeks) < deep_cash_ratio * Decimal(baseline_cash_m9)):
        status = FinalStatus.DEEP_CRISIS
    else:
        status = FinalStatus.SURVIVED
        
    return FinalScore(
        damage=float(comp_a),
        solvency=float(comp_k),
        early_bankruptcy=float(comp_e),
        score=int(final_score_int),
        final_status=status,
    )
