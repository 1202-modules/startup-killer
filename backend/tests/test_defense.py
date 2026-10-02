import pytest
from backend.app.engine.types import (
    DefenseType,
    GameState,
    StartupTemplate,
    PrivateProfile,
    FinanceConfig,
    PublicProfile,
    RevenueStreamConfig,
)
from backend.app.engine.defense import get_available_defenses

def test_pr_defense_unavailable_without_reputation_crisis():
    # Private profile has allowed_defenses with 'pr', but no reputation attack in active_effects
    state = GameState(
        session_id="test",
        template_slug="coffeebot",
        round_number=1,
        elapsed_months=0,
        cash_kopeks=750000000,
        fixed_cost_kopeks=200000000,
        reputation=77,
        active_effects=[],
    )
    private = PrivateProfile(
        weaknesses=[],
        allowed_defenses=[DefenseType.COST_CUT, DefenseType.PR, DefenseType.SUPPLIER_SWITCH, DefenseType.PIVOT],
        pivot_compatible=True,
        production_partner_alternative=True,
    )
    available = get_available_defenses(state, private)
    assert DefenseType.PR not in available
    assert DefenseType.NONE in available
    assert DefenseType.COST_CUT in available

def test_cost_cut_unavailable_if_already_used():
    state = GameState(
        session_id="test",
        template_slug="coffeebot",
        round_number=2,
        elapsed_months=3,
        cash_kopeks=500000000,
        fixed_cost_kopeks=170000000,
        reputation=77,
        used_defenses=[DefenseType.COST_CUT],
    )
    private = PrivateProfile(
        weaknesses=[],
        allowed_defenses=[DefenseType.COST_CUT],
        pivot_compatible=False,
        production_partner_alternative=False,
    )
    available = get_available_defenses(state, private)
    assert DefenseType.COST_CUT not in available
    assert DefenseType.NONE in available
