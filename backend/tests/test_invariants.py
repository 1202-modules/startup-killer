from pathlib import Path
import pytest

from backend.app.engine.calculator import simulate_round, calculate_attack_impact
from backend.app.engine.constants import (
    SEVERITY_BPS,
    SCALE_BPS,
    FEASIBILITY_BPS,
    WEAKNESS_MATCH_BPS,
)
from backend.app.engine.loader import load_startups
from backend.app.engine.types import (
    AttackType,
    DefenseType,
    Duration,
    Feasibility,
    FinalStatus,
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

def test_attack_impact_formula_calculation():
    # 1. Demand attack has no incident cost and no rep delta
    attack_demand = ValidatedAttack(
        attack_type=AttackType.DEMAND,
        target_stream_ids=["kiosks"],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.WEAK,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
        weakness_match=WeaknessMatch.NORMAL,
    )
    # weak=1200 * local=4000 * plausible=8000 * normal=10000 / 10000^3 = 384 bps
    shock, inc_cost, rep_delta = calculate_attack_impact(attack_demand)
    assert shock == 384
    assert inc_cost == 0
    assert rep_delta == 0

    # 2. Reputation attack calculates rep delta: -3 * 4000 * 8000 / 10000^2 = -0.96 -> -1
    attack_rep = ValidatedAttack(
        attack_type=AttackType.REPUTATION,
        target_stream_ids=["kiosks"],
        scale=Scale.LOCAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.WEAK,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
        weakness_match=WeaknessMatch.NORMAL,
    )
    shock_rep, _, rep_delta_rep = calculate_attack_impact(attack_rep)
    assert shock_rep == 384
    assert rep_delta_rep == -1

def test_incident_cost_only_for_applicable_attack_types():
    # Cost attack
    attack_cost = ValidatedAttack(
        attack_type=AttackType.COST,
        target_stream_ids=["kiosks"],
        scale=Scale.REGIONAL,
        feasibility=Feasibility.ESTABLISHED_IN_STATE,
        severity=Severity.MEDIUM,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
    )
    # inc_bps: medium=3500 * regional=6500 * established=10000 / 10000^2 = 2275 bps
    shock, inc_cost, _ = calculate_attack_impact(attack_cost)
    assert inc_cost == 2275

def test_simulate_round_with_defense_selection(coffeebot):
    state = GameState(
        session_id="sim_test",
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
        scale=Scale.COMPANY_WIDE,
        feasibility=Feasibility.ESTABLISHED_IN_STATE,
        severity=Severity.STRONG,
        duration=Duration.STRUCTURAL,
        evidence_fact_ids=[],
        weakness_match=WeaknessMatch.NORMAL,
    )
    outcome = simulate_round(state, coffeebot, attack)
    assert outcome.round_number == 1
    assert len(outcome.monthly_ledger) == 3
    assert outcome.state_after.elapsed_months == 3
    assert outcome.defense.defense_type in [DefenseType.NONE, DefenseType.COST_CUT, DefenseType.PIVOT, DefenseType.SUPPLIER_SWITCH]

def test_game_terminates_early_on_bankruptcy(coffeebot):
    # Extreme shock to trigger bankruptcy
    state = GameState(
        session_id="bankrupt_test",
        template_slug="coffeebot",
        round_number=1,
        elapsed_months=0,
        cash_kopeks=100000,  # very low cash: 1,000 rubles
        fixed_cost_kopeks=coffeebot.initial_fixed_cost_kopeks,
        reputation=coffeebot.initial_reputation,
    )
    attack = ValidatedAttack(
        attack_type=AttackType.DEMAND,
        target_stream_ids=["kiosks", "service"],
        scale=Scale.COMPANY_WIDE,
        feasibility=Feasibility.ESTABLISHED_IN_STATE,
        severity=Severity.CRITICAL,
        duration=Duration.STRUCTURAL,
        evidence_fact_ids=[],
    )
    outcome = simulate_round(state, coffeebot, attack)
    assert outcome.state_after.is_bankrupt is True
    assert outcome.final_status == FinalStatus.BANKRUPT
    assert outcome.score_breakdown is not None
    assert outcome.score_breakdown.score > 0
    assert outcome.monthly_ledger[-1].unpaid_obligations_kopeks > 0
