import json
from pathlib import Path
import pytest
from backend.app.engine.calculator import run_golden_case
from backend.app.engine.loader import load_startups

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

@pytest.fixture(scope="module")
def startups_map():
    return load_startups(DATA_DIR / "startups.json")

@pytest.fixture(scope="module")
def golden_cases():
    with open(DATA_DIR / "economy_golden_cases.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["cases"]

def test_golden_cases_count(golden_cases):
    assert len(golden_cases) == 30

@pytest.mark.parametrize("case_index", list(range(30)))
def test_individual_golden_case(case_index, golden_cases, startups_map):
    case = golden_cases[case_index]
    startup_slug = case["startup_slug"]
    mode = case["mode"]
    startup = startups_map[startup_slug]
    
    result = run_golden_case(startup, mode)
    
    # 1. Compare monthly ledger length
    expected_ledger = case["monthly_ledger"]
    actual_ledger = result.monthly_ledger
    assert len(actual_ledger) == len(expected_ledger), (
        f"Case {startup_slug} {mode}: ledger length mismatch (expected {len(expected_ledger)}, got {len(actual_ledger)})"
    )
    
    # 2. Compare each month exact to kopek
    for m_idx, (act, exp) in enumerate(zip(actual_ledger, expected_ledger)):
        month_num = m_idx + 1
        assert act.month == exp["month"] == month_num
        assert len(act.streams) == len(exp["streams"])
        
        for s_act, s_exp in zip(act.streams, exp["streams"]):
            assert s_act.id == s_exp["id"]
            assert s_act.baseline_revenue_kopeks == s_exp["baseline_revenue_kopeks"], (
                f"{startup_slug} {mode} m{month_num} {s_act.id} baseline rev mismatch"
            )
            assert s_act.shock_bps == s_exp["shock_bps"], (
                f"{startup_slug} {mode} m{month_num} {s_act.id} shock_bps mismatch"
            )
            assert s_act.revenue_kopeks == s_exp["revenue_kopeks"], (
                f"{startup_slug} {mode} m{month_num} {s_act.id} revenue mismatch"
            )
            assert s_act.variable_cost_kopeks == s_exp["variable_cost_kopeks"], (
                f"{startup_slug} {mode} m{month_num} {s_act.id} var cost mismatch"
            )
            
        assert act.revenue_kopeks == exp["revenue_kopeks"], f"{startup_slug} {mode} m{month_num} total rev mismatch"
        assert act.variable_cost_kopeks == exp["variable_cost_kopeks"], f"{startup_slug} {mode} m{month_num} total var mismatch"
        assert act.fixed_cost_kopeks == exp["fixed_cost_kopeks"], f"{startup_slug} {mode} m{month_num} fixed cost mismatch"
        assert act.profit_kopeks == exp["profit_kopeks"], f"{startup_slug} {mode} m{month_num} profit mismatch"
        assert act.closing_cash_kopeks == exp["closing_cash_kopeks"], f"{startup_slug} {mode} m{month_num} cash mismatch"
        assert act.unpaid_obligations_kopeks == exp["unpaid_obligations_kopeks"], f"{startup_slug} {mode} m{month_num} unpaid obligations mismatch"
        
    # 3. Compare closing cash and bankruptcy month
    assert result.closing_cash_kopeks == case["closing_cash_kopeks"]
    assert result.bankruptcy_month == case["bankruptcy_month"]
    
    # 4. Compare score components
    exp_score = case["score"]
    act_score = result.score_breakdown
    assert act_score is not None
    assert abs(act_score.damage - exp_score["damage"]) < 1e-5, f"{startup_slug} {mode} damage mismatch"
    assert abs(act_score.solvency - exp_score["solvency"]) < 1e-5, f"{startup_slug} {mode} solvency mismatch"
    assert abs(act_score.early_bankruptcy - exp_score["early_bankruptcy"]) < 1e-5, f"{startup_slug} {mode} early_bankruptcy mismatch"
    assert act_score.score == exp_score["score"], f"{startup_slug} {mode} score mismatch"
