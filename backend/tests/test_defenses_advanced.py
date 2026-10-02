from pathlib import Path
from decimal import Decimal
import pytest

from backend.app.engine.calculator import simulate_round
from backend.app.engine.loader import load_startups
from backend.app.engine.types import (
    AttackType,
    DefenseType,
    Duration,
    Feasibility,
    GameState,
    Scale,
    Severity,
    ValidatedAttack,
    WeaknessMatch,
)

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

@pytest.fixture
def coffeebot():
    return load_startups(DATA_DIR / "startups.json")["coffeebot"]

def test_cost_cut_does_not_compound_and_persists_across_rounds(coffeebot):
    state = GameState(
        session_id="cost_cut_test",
        template_slug="coffeebot",
        round_number=1,
        elapsed_months=0,
        cash_kopeks=coffeebot.initial_cash_kopeks,
        fixed_cost_kopeks=coffeebot.initial_fixed_cost_kopeks,
        reputation=coffeebot.initial_reputation,
    )
    # Mild attack, force cost_cut
    attack = ValidatedAttack(
        attack_type=AttackType.DEMAND,
        target_stream_ids=["kiosks"],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.WEAK,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
    )
    outcome1 = simulate_round(state, coffeebot, attack, forced_defense=DefenseType.COST_CUT)
    
    # Month 1: payment 2500 bps = 50_000_000, fixed cost is 200_000_000
    m1 = outcome1.monthly_ledger[0]
    assert m1.fixed_cost_kopeks == 200000000
    assert m1.defense_cost_kopeks == 50000000
    
    # Month 2: fixed cost is 85% = 170_000_000
    m2 = outcome1.monthly_ledger[1]
    assert m2.fixed_cost_kopeks == 170000000
    
    # Month 3: fixed cost MUST STILL BE 170_000_000 (NOT compounded to 144.5m!)
    m3 = outcome1.monthly_ledger[2]
    assert m3.fixed_cost_kopeks == 170000000
    
    # Round 2: simulate next round with DefenseType.NONE
    # Cost cut penalty (-5% rev, -15% fixed cost) must persist in round 2!
    attack2 = ValidatedAttack(
        attack_type=AttackType.DEMAND,
        target_stream_ids=["kiosks"],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.WEAK,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
    )
    outcome2 = simulate_round(outcome1.state_after, coffeebot, attack2, forced_defense=DefenseType.NONE)
    m4 = outcome2.monthly_ledger[0]
    assert m4.fixed_cost_kopeks == 170000000
    
    # Verify stream revenue in m4 has -5% penalty
    # baseline revenue for m4 kiosks is coffeebot.baseline_series[4].streams[0]
    # Total revenue must reflect 5% operational reduction
    raw_m4_kiosks_base = coffeebot.baseline_series[4].revenue_kopeks
    # with 5% cut, revenue is significantly lower than baseline
    assert m4.revenue_kopeks < raw_m4_kiosks_base

def test_pivot_activates_in_month_3_and_adds_stream_to_ledger(coffeebot):
    state = GameState(
        session_id="pivot_test",
        template_slug="coffeebot",
        round_number=1,
        elapsed_months=0,
        cash_kopeks=coffeebot.initial_cash_kopeks,
        fixed_cost_kopeks=coffeebot.initial_fixed_cost_kopeks,
        reputation=coffeebot.initial_reputation,
    )
    attack = ValidatedAttack(
        attack_type=AttackType.DEMAND,
        target_stream_ids=["kiosks"],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.WEAK,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
    )
    outcome = simulate_round(state, coffeebot, attack, forced_defense=DefenseType.PIVOT)
    
    # Month 1 & 2: preparation, no pivot stream
    assert len(outcome.monthly_ledger[0].streams) == 2
    assert len(outcome.monthly_ledger[1].streams) == 2
    
    # Month 3: Pivot activates! New stream must be present in ledger
    m3 = outcome.monthly_ledger[2]
    assert len(m3.streams) == 3
    pivot_stream = next(s for s in m3.streams if s.id == "pivot")
    assert pivot_stream.revenue_kopeks > 0
    # Ledger integrity: sum of streams matches total revenue
    assert sum(s.revenue_kopeks for s in m3.streams) == m3.revenue_kopeks
    assert sum(s.variable_cost_kopeks for s in m3.streams) == m3.variable_cost_kopeks

def test_cost_attack_without_target_stream_has_no_revenue_shock(coffeebot):
    state = GameState(
        session_id="cost_test",
        template_slug="coffeebot",
        round_number=1,
        elapsed_months=0,
        cash_kopeks=coffeebot.initial_cash_kopeks,
        fixed_cost_kopeks=coffeebot.initial_fixed_cost_kopeks,
        reputation=coffeebot.initial_reputation,
    )
    attack = ValidatedAttack(
        attack_type=AttackType.COST,
        target_stream_ids=[],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.MEDIUM,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
    )
    outcome = simulate_round(state, coffeebot, attack, forced_defense=DefenseType.NONE)
    m1 = outcome.monthly_ledger[0]
    # No shock on streams
    for stream in m1.streams:
        assert stream.shock_bps == 0
        assert stream.revenue_kopeks == stream.baseline_revenue_kopeks
    # But incident cost is charged
    assert m1.incident_cost_kopeks > 0

def test_bankrupt_guard_clause_prevents_simulating(coffeebot):
    state = GameState(
        session_id="bankrupt_guard_test",
        template_slug="coffeebot",
        round_number=2,
        elapsed_months=3,
        cash_kopeks=0,
        fixed_cost_kopeks=coffeebot.initial_fixed_cost_kopeks,
        reputation=coffeebot.initial_reputation,
        is_bankrupt=True,
        bankruptcy_month=3,
    )
    attack = ValidatedAttack(
        attack_type=AttackType.DEMAND,
        target_stream_ids=["kiosks"],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.WEAK,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
    )
    outcome = simulate_round(state, coffeebot, attack)
    assert outcome.months_simulated == 0
    assert len(outcome.monthly_ledger) == 0
    assert outcome.state_after.is_bankrupt is True
