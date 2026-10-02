from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from backend.app.engine.constants import DEFENSE_COST_BPS
from backend.app.engine.types import (
    AttackType,
    DefenseType,
    GameState,
    PrivateProfile,
)


def quantize_kopeks(val: Decimal) -> int:
    return int(val.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def get_defense_cost_kopeks(defense: DefenseType, current_fixed_cost_kopeks: int) -> int:
    bps = DEFENSE_COST_BPS.get(defense, 0)
    if bps == 0:
        return 0
    return quantize_kopeks(
        Decimal(current_fixed_cost_kopeks) * Decimal(bps) / Decimal(10000)
    )


def get_available_defenses(state: GameState, private: PrivateProfile) -> List[DefenseType]:
    available: List[DefenseType] = [DefenseType.NONE]
    
    # 1. cost_cut: once per game, needs money, allowed in profile
    if DefenseType.COST_CUT in private.allowed_defenses and DefenseType.COST_CUT not in state.used_defenses:
        cost = get_defense_cost_kopeks(DefenseType.COST_CUT, state.fixed_cost_kopeks)
        if state.cash_kopeks >= cost:
            available.append(DefenseType.COST_CUT)
            
    # 2. pr: needs active reputation crisis in active_effects, needs money, allowed in profile
    has_active_rep_crisis = any(
        eff.origin_attack_type == AttackType.REPUTATION for eff in state.active_effects
    )
    if DefenseType.PR in private.allowed_defenses and has_active_rep_crisis:
        cost = get_defense_cost_kopeks(DefenseType.PR, state.fixed_cost_kopeks)
        if state.cash_kopeks >= cost:
            available.append(DefenseType.PR)
            
    # 3. supplier_switch: needs supplier alternative in profile, needs active supply interruption, needs money
    has_supply_attack = any(
        eff.origin_attack_type == AttackType.SUPPLY for eff in state.active_effects
    )
    if (
        DefenseType.SUPPLIER_SWITCH in private.allowed_defenses
        and private.production_partner_alternative
        and has_supply_attack
    ):
        cost = get_defense_cost_kopeks(DefenseType.SUPPLIER_SWITCH, state.fixed_cost_kopeks)
        if state.cash_kopeks >= cost:
            available.append(DefenseType.SUPPLIER_SWITCH)
            
    # 4. pivot: once per game, needs pivot_compatible in profile, needs money
    if (
        DefenseType.PIVOT in private.allowed_defenses
        and private.pivot_compatible
        and DefenseType.PIVOT not in state.used_defenses
    ):
        cost = get_defense_cost_kopeks(DefenseType.PIVOT, state.fixed_cost_kopeks)
        if state.cash_kopeks >= cost:
            available.append(DefenseType.PIVOT)
            
    return available
