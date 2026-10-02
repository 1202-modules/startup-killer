from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import pytest
from backend.app.engine.loader import load_startups

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def test_all_startups_baseline_recalculated_exact_to_kopek():
    startups = load_startups(DATA_DIR / "startups.json")
    
    Q = lambda v: int(Decimal(v).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    
    for slug, startup in startups.items():
        cash = startup.initial_cash_kopeks
        fixed = startup.initial_fixed_cost_kopeks
        
        # Month 0 check
        m0 = startup.baseline_series[0]
        assert m0.closing_cash_kopeks == startup.initial_cash_kopeks
        assert m0.month == 0
        
        for m in range(1, 10):
            rev_total = 0
            var_total = 0
            for stream in startup.revenue_streams:
                # baseline formula: initial * (1 + monthly_growth_bps/10000)^(m-1)
                growth_factor = (Decimal(1) + Decimal(stream.monthly_growth_bps) / Decimal(10000)) ** (m - 1)
                rev = Q(Decimal(stream.initial_monthly_revenue_kopeks) * growth_factor)
                var = Q(Decimal(rev) * Decimal(stream.variable_cost_bps) / Decimal(10000))
                rev_total += rev
                var_total += var
            
            profit = rev_total - var_total - fixed
            cash += profit
            
            b = startup.baseline_series[m]
            assert b.revenue_kopeks == rev_total, f"{slug} month {m} revenue mismatch"
            assert b.variable_cost_kopeks == var_total, f"{slug} month {m} var cost mismatch"
            assert b.profit_kopeks == profit, f"{slug} month {m} profit mismatch"
            assert b.closing_cash_kopeks == cash, f"{slug} month {m} closing cash mismatch"
            
        assert cash == startup.baseline_cash_m9_kopeks
        assert cash > 0
