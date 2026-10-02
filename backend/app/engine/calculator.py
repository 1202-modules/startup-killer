from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional, Tuple, Dict
import copy

from backend.app.engine.constants import (
    SEVERITY_BPS,
    SCALE_BPS,
    FEASIBILITY_BPS,
    WEAKNESS_MATCH_BPS,
    DECAY_BPS,
    MAX_DURATION_MONTHS,
    INCIDENT_COST_BPS,
    REPUTATION_DELTAS,
    DEFAULT_STREAM_CAP_BPS,
)
from backend.app.engine.defense import (
    get_available_defenses,
    get_defense_cost_kopeks,
)
from backend.app.engine.scoring import calculate_score
from backend.app.engine.types import (
    ActiveDefenseModifier,
    ActiveEffect,
    AttackType,
    DefenseDecision,
    DefenseType,
    Duration,
    EngineOutcome,
    FinalScore,
    FinalStatus,
    GameState,
    MonthlyLedgerRow,
    RevenueStreamConfig,
    Severity,
    StartupTemplate,
    StreamLedgerRow,
    ValidatedAttack,
)


def quantize_kopeks(val: Decimal) -> int:
    return int(val.quantize(Decimal(1), rounding=ROUND_HALF_UP))


@dataclass
class SimulationResult:
    monthly_ledger: List[MonthlyLedgerRow]
    closing_cash_kopeks: int
    bankruptcy_month: Optional[int]
    unpaid_obligations_kopeks: int
    score_breakdown: FinalScore
    final_state: GameState


def calculate_attack_impact(
    attack: ValidatedAttack,
) -> Tuple[int, int, int]:
    # Rule: downgrade critical if evidence_fact_ids is empty
    effective_severity = attack.severity
    if effective_severity == Severity.CRITICAL and not attack.evidence_fact_ids:
        effective_severity = Severity.STRONG

    sev = SEVERITY_BPS[effective_severity]
    scale = SCALE_BPS[attack.scale]
    feas = FEASIBILITY_BPS[attack.feasibility]
    wm = WEAKNESS_MATCH_BPS[attack.weakness_match]

    # 1. Shock bps
    raw_shock = (
        Decimal(sev) * Decimal(scale) * Decimal(feas) * Decimal(wm)
    ) / Decimal(10000**3)
    shock_bps = quantize_kopeks(raw_shock)
    shock_bps = min(shock_bps, DEFAULT_STREAM_CAP_BPS)

    # 2. Incident cost bps (only for cost, supply, technology, finance)
    # does NOT multiply by weakness_match
    incident_cost_bps = 0
    if attack.attack_type in (
        AttackType.COST,
        AttackType.SUPPLY,
        AttackType.TECHNOLOGY,
        AttackType.FINANCE,
    ):
        raw_inc_sev = INCIDENT_COST_BPS[effective_severity]
        raw_inc = (
            Decimal(raw_inc_sev) * Decimal(scale) * Decimal(feas)
        ) / Decimal(10000**2)
        incident_cost_bps = quantize_kopeks(raw_inc)

    # 3. Reputation delta: only for REPUTATION attack type by default
    rep_delta = 0
    if attack.attack_type == AttackType.REPUTATION:
        rep_base = REPUTATION_DELTAS[effective_severity]
        raw_rep = (
            Decimal(rep_base) * Decimal(scale) * Decimal(feas)
        ) / Decimal(10000**2)
        rep_delta = quantize_kopeks(raw_rep)

    return shock_bps, incident_cost_bps, rep_delta


def simulate_month(
    state: GameState,
    startup: StartupTemplate,
    month: int,
    stream_shocks: Optional[Dict[str, int]] = None,
    one_time_incident_cost_kopeks: int = 0,
    defense_payment_kopeks: int = 0,
) -> Tuple[MonthlyLedgerRow, GameState]:
    stream_rows: List[StreamLedgerRow] = []
    total_rev = 0
    total_var = 0

    # 1. Fixed costs calculation (non-compounding: always 85% of baseline fixed cost if cost cut active)
    has_active_cost_cut = any(
        m.defense_type == DefenseType.COST_CUT and month > m.activated_month
        for m in state.active_defense_modifiers
    )
    if has_active_cost_cut:
        current_fixed_cost = quantize_kopeks(
            Decimal(startup.initial_fixed_cost_kopeks) * Decimal(8500) / Decimal(10000)
        )
    else:
        current_fixed_cost = startup.initial_fixed_cost_kopeks

    # 2. Process existing streams
    for stream in startup.revenue_streams:
        # 2a. Baseline revenue for this month
        growth_factor = (
            Decimal(1) + Decimal(stream.monthly_growth_bps) / Decimal(10000)
        ) ** (month - 1)
        base_rev = quantize_kopeks(
            Decimal(stream.initial_monthly_revenue_kopeks) * growth_factor
        )

        # 2b. Shock calculation
        if stream_shocks is not None and stream.id in stream_shocks:
            shock_bps = stream_shocks[stream.id]
            is_rep_crisis_on_stream = False
        else:
            stream_effects = [
                eff for eff in state.active_effects if eff.target_stream_id == stream.id
            ]
            if not stream_effects:
                shock_bps = 0
                is_rep_crisis_on_stream = False
            else:
                is_rep_crisis_on_stream = any(
                    eff.origin_attack_type == AttackType.REPUTATION for eff in stream_effects
                )
                groups: Dict[str, int] = {}
                for eff in stream_effects:
                    groups[eff.stack_group] = max(
                        groups.get(eff.stack_group, 0), eff.magnitude_bps
                    )
                rem = Decimal(1)
                for eff_bps in groups.values():
                    rem *= Decimal(10000 - eff_bps) / Decimal(10000)
                shock_bps = quantize_kopeks((Decimal(1) - rem) * Decimal(10000))
                shock_bps = min(shock_bps, DEFAULT_STREAM_CAP_BPS)

        # 2c. Supplier switch defense on target stream
        cur_var_cost_bps = stream.variable_cost_bps
        has_supplier_switch_on_stream = any(
            m.defense_type == DefenseType.SUPPLIER_SWITCH
            and (m.target_stream_id == stream.id or m.target_stream_id is None)
            and month >= m.activated_month + 1
            for m in state.active_defense_modifiers
        )
        if has_supplier_switch_on_stream:
            # Removes 70% of supply-interruption shock, variable cost bps +400
            shock_bps = quantize_kopeks(Decimal(shock_bps) * Decimal(3000) / Decimal(10000))
            cur_var_cost_bps += 400

        # 2d. Stream revenue after shock
        stream_rev = quantize_kopeks(
            Decimal(base_rev) * (Decimal(10000 - shock_bps) / Decimal(10000))
        )

        # 2e. PR defense: restores 30% of lost revenue on streams affected by reputation crisis (months 1..3 of PR)
        has_active_pr = any(
            m.defense_type == DefenseType.PR
            and (m.activated_month + 1 <= month <= m.activated_month + 3)
            for m in state.active_defense_modifiers
        )
        if has_active_pr and is_rep_crisis_on_stream:
            lost_rev = base_rev - stream_rev
            if lost_rev > 0:
                recovered = quantize_kopeks(Decimal(lost_rev) * Decimal(3000) / Decimal(10000))
                stream_rev += recovered

        # 2f. Cost cut operational revenue penalty: -5%
        if has_active_cost_cut:
            stream_rev = quantize_kopeks(Decimal(stream_rev) * Decimal(9500) / Decimal(10000))

        # 2g. Stream variable cost
        stream_var = quantize_kopeks(
            Decimal(stream_rev) * Decimal(cur_var_cost_bps) / Decimal(10000)
        )

        stream_rows.append(
            StreamLedgerRow(
                id=stream.id,
                baseline_revenue_kopeks=base_rev,
                shock_bps=shock_bps,
                revenue_kopeks=stream_rev,
                variable_cost_kopeks=stream_var,
            )
        )
        total_rev += stream_rev
        total_var += stream_var

    # 3. Pivot defense new stream (active 2 months after activation: month >= activated_month + 2)
    has_active_pivot = any(
        m.defense_type == DefenseType.PIVOT and month >= m.activated_month + 2
        for m in state.active_defense_modifiers
    )
    if has_active_pivot:
        initial_company_rev = sum(s.initial_monthly_revenue_kopeks for s in startup.revenue_streams)
        pivot_rev = quantize_kopeks(Decimal(initial_company_rev) * Decimal(1500) / Decimal(10000))
        total_initial_var = sum(
            quantize_kopeks(Decimal(s.initial_monthly_revenue_kopeks) * Decimal(s.variable_cost_bps) / Decimal(10000))
            for s in startup.revenue_streams
        )
        pivot_var_bps = quantize_kopeks(Decimal(total_initial_var * 10000) / Decimal(initial_company_rev))
        pivot_var = quantize_kopeks(Decimal(pivot_rev) * Decimal(pivot_var_bps) / Decimal(10000))

        stream_rows.append(
            StreamLedgerRow(
                id="pivot",
                baseline_revenue_kopeks=0,
                shock_bps=0,
                revenue_kopeks=pivot_rev,
                variable_cost_kopeks=pivot_var,
            )
        )
        total_rev += pivot_rev
        total_var += pivot_var

    profit = (
        total_rev
        - total_var
        - current_fixed_cost
        - one_time_incident_cost_kopeks
        - defense_payment_kopeks
    )

    tentative_cash = state.cash_kopeks + profit
    if tentative_cash < 0:
        closing_cash = 0
        unpaid = -tentative_cash
        is_bankrupt = True
        bankruptcy_month = month
    else:
        closing_cash = tentative_cash
        unpaid = 0
        is_bankrupt = False
        bankruptcy_month = None

    ledger_row = MonthlyLedgerRow(
        month=month,
        streams=stream_rows,
        revenue_kopeks=total_rev,
        variable_cost_kopeks=total_var,
        fixed_cost_kopeks=current_fixed_cost,
        profit_kopeks=profit,
        closing_cash_kopeks=closing_cash,
        unpaid_obligations_kopeks=unpaid,
        incident_cost_kopeks=one_time_incident_cost_kopeks,
        defense_cost_kopeks=defense_payment_kopeks,
    )

    # 4. Decay and cleanup active effects
    new_effects: List[ActiveEffect] = []
    for eff in state.active_effects:
        if eff.duration_type == Duration.STRUCTURAL:
            new_effects.append(eff)
        else:
            next_mag = quantize_kopeks(
                Decimal(eff.magnitude_bps) * Decimal(eff.decay_bps) / Decimal(10000)
            )
            rem_months = eff.months_remaining - 1
            if rem_months > 0 and next_mag > 0:
                new_effects.append(
                    ActiveEffect(
                        stack_group=eff.stack_group,
                        target_stream_id=eff.target_stream_id,
                        magnitude_bps=next_mag,
                        duration_type=eff.duration_type,
                        months_remaining=rem_months,
                        decay_bps=eff.decay_bps,
                        source_round=eff.source_round,
                        origin_attack_type=eff.origin_attack_type,
                    )
                )

    new_state = GameState(
        session_id=state.session_id,
        template_slug=state.template_slug,
        round_number=state.round_number,
        elapsed_months=month,
        cash_kopeks=closing_cash,
        fixed_cost_kopeks=current_fixed_cost,
        reputation=state.reputation,
        active_effects=new_effects,
        used_defenses=list(state.used_defenses),
        active_defense_modifiers=list(state.active_defense_modifiers),
        is_bankrupt=state.is_bankrupt or is_bankrupt,
        bankruptcy_month=state.bankruptcy_month or bankruptcy_month,
        unpaid_obligations_kopeks=unpaid,
        score_breakdown=state.score_breakdown,
    )

    return ledger_row, new_state


def project_defense_outcome(
    initial_state: GameState,
    startup: StartupTemplate,
    round_start_month: int,
    candidate: DefenseType,
    incident_cost_kopeks: int,
) -> Tuple[int, int, Optional[int]]:
    cost = get_defense_cost_kopeks(candidate, initial_state.fixed_cost_kopeks)
    if initial_state.cash_kopeks < cost:
        return -1, cost, None

    cur_state = copy.deepcopy(initial_state)
    if candidate != DefenseType.NONE:
        # Determine target stream for supplier switch if applicable
        target_s = None
        if candidate == DefenseType.SUPPLIER_SWITCH:
            for eff in cur_state.active_effects:
                if eff.origin_attack_type == AttackType.SUPPLY:
                    target_s = eff.target_stream_id
                    break
        cur_state.active_defense_modifiers.append(
            ActiveDefenseModifier(
                defense_type=candidate,
                activated_round=cur_state.round_number,
                activated_month=round_start_month,
                target_stream_id=target_s,
            )
        )

    for step in range(round_start_month, 10):
        m = step
        defense_pay = cost if m == round_start_month else 0
        inc_cost = incident_cost_kopeks if m == round_start_month else 0
        row, cur_state = simulate_month(
            state=cur_state,
            startup=startup,
            month=m,
            one_time_incident_cost_kopeks=inc_cost,
            defense_payment_kopeks=defense_pay,
        )
        if cur_state.is_bankrupt:
            return 0, cost, m

    return cur_state.cash_kopeks, cost, None


def format_defense_detail(defense_type: DefenseType, cost_kopeks: int) -> str:
    cost_rubles = cost_kopeks // 100
    cost_formatted = f"{cost_rubles:,}".replace(",", " ")

    if defense_type == DefenseType.NONE:
        return "Защита не запущена: прогнозируемая экономия меньше её стоимости (расходы: 0 ₽)."
    elif defense_type == DefenseType.COST_CUT:
        return f"Экстренное сокращение расходов: урезаны операционные траты и бонусы команды (затраты: {cost_formatted} ₽)."
    elif defense_type == DefenseType.PR:
        return f"Антикризисная PR-кампания и контратака в отраслевых медиа (затраты: {cost_formatted} ₽)."
    elif defense_type == DefenseType.SUPPLIER_SWITCH:
        return f"Срочный поиск альтернативных поставщиков и перестройка логистической цепочки (затраты: {cost_formatted} ₽)."
    elif defense_type == DefenseType.PIVOT:
        return f"Глубокий пивот бизнес-модели и переработка ключевого продукта (затраты: {cost_formatted} ₽)."
    else:
        return f"Защитный манёвр {defense_type.value} (затраты: {cost_formatted} ₽)."


def select_best_defense(
    state: GameState,
    startup: StartupTemplate,
    round_start_month: int,
    incident_cost_kopeks: int,
    forced_defense: Optional[DefenseType] = None,
) -> DefenseDecision:
    if forced_defense is not None:
        cost = get_defense_cost_kopeks(forced_defense, state.fixed_cost_kopeks)
        effective_delay = 1
        if forced_defense == DefenseType.PIVOT:
            effective_delay = 2
        return DefenseDecision(
            defense_type=forced_defense,
            cost_kopeks=cost,
            effective_from_month=round_start_month + effective_delay,
            detail=format_defense_detail(forced_defense, cost),
        )

    available = get_available_defenses(state, startup.private_profile)
    defense_enum_order = [
        DefenseType.NONE,
        DefenseType.COST_CUT,
        DefenseType.PR,
        DefenseType.SUPPLIER_SWITCH,
        DefenseType.PIVOT,
    ]

    none_bankruptcy = project_defense_outcome(state, startup, round_start_month, DefenseType.NONE, incident_cost_kopeks)[2]
    best_candidate = DefenseType.NONE
    best_key = None

    for candidate in defense_enum_order:
        if candidate not in available:
            continue
        if candidate == DefenseType.COST_CUT and none_bankruptcy is None:
            continue
        projected_cash, defense_cost, bankruptcy_month = project_defense_outcome(
            initial_state=state,
            startup=startup,
            round_start_month=round_start_month,
            candidate=candidate,
            incident_cost_kopeks=incident_cost_kopeks,
        )
        if projected_cash < 0:
            continue

        key = (bankruptcy_month is None, projected_cash if bankruptcy_month is None else bankruptcy_month, -defense_cost)
        if best_key is None or key > best_key:
            best_key = key
            best_candidate = candidate

    chosen_cost = get_defense_cost_kopeks(best_candidate, state.fixed_cost_kopeks)
    effective_delay = 1
    if best_candidate == DefenseType.PIVOT:
        effective_delay = 2
    return DefenseDecision(
        defense_type=best_candidate,
        cost_kopeks=chosen_cost,
        effective_from_month=round_start_month + effective_delay,
        detail=format_defense_detail(best_candidate, chosen_cost),
        reason=("Защита не запущена: прогнозируемая экономия меньше её стоимости."
                if best_candidate == DefenseType.NONE else
                "Выбрана мера с лучшим прогнозом денег к девятому месяцу."),
    )


def evaluate_defense(
    state: GameState,
    startup: StartupTemplate,
    attack: Optional[ValidatedAttack] = None,
    round_start_month: int = 1,
    incident_cost_kopeks: int = 0,
    forced_defense: Optional[DefenseType] = None,
) -> DefenseDecision:
    return select_best_defense(
        state=state,
        startup=startup,
        round_start_month=round_start_month,
        incident_cost_kopeks=incident_cost_kopeks,
        forced_defense=forced_defense,
    )


def simulate_round(
    state: GameState,
    startup: StartupTemplate,
    attack: ValidatedAttack,
    forced_defense: Optional[DefenseType] = None,
) -> EngineOutcome:
    if attack.v2_effect:
        from backend.app.engine.v2 import simulate_v2_round
        return simulate_v2_round(state, startup, attack, forced_defense)
    # Guard clauses
    if state.is_bankrupt:
        return EngineOutcome(
            round_number=state.round_number,
            months_simulated=0,
            monthly_ledger=[],
            state_after=state,
            cash_delta_kopeks=0,
            revenue_delta_kopeks=0,
            reputation_delta=0,
            defense=DefenseDecision(DefenseType.NONE, 0, 0, "Партия завершена (банкротство)"),
            final_status=FinalStatus.BANKRUPT,
            score_breakdown=state.score_breakdown,
            engine_version="v1.0",
        )

    if state.elapsed_months >= 9:
        return EngineOutcome(
            round_number=state.round_number,
            months_simulated=0,
            monthly_ledger=[],
            state_after=state,
            cash_delta_kopeks=0,
            revenue_delta_kopeks=0,
            reputation_delta=0,
            defense=DefenseDecision(DefenseType.NONE, 0, 0, "Игра уже завершена"),
            final_status=FinalStatus.SURVIVED,
            score_breakdown=state.score_breakdown,
            engine_version="v1.0",
        )

    round_start_month = (state.round_number - 1) * 3 + 1

    # 1. Compute attack impact
    shock_bps, incident_cost_bps, rep_delta = calculate_attack_impact(attack)
    one_time_incident_kopeks = quantize_kopeks(
        Decimal(state.fixed_cost_kopeks) * Decimal(incident_cost_bps) / Decimal(10000)
    )

    # 2. Update state with new effects
    new_effects = list(state.active_effects)
    # Target stream handling: Cost/Finance without target streams only charges incident cost
    if attack.attack_type in (AttackType.COST, AttackType.FINANCE) and not attack.target_stream_ids:
        target_ids = []
    elif attack.target_stream_ids:
        target_ids = attack.target_stream_ids
    else:
        target_ids = [s.id for s in startup.revenue_streams]

    for s_id in target_ids:
        new_effects.append(
            ActiveEffect(
                stack_group=attack.intent or f"attack_r{state.round_number}",
                target_stream_id=s_id,
                magnitude_bps=shock_bps,
                duration_type=attack.duration,
                months_remaining=MAX_DURATION_MONTHS[attack.duration],
                decay_bps=DECAY_BPS[attack.duration],
                source_round=state.round_number,
                origin_attack_type=attack.attack_type,
            )
        )

    new_reputation = max(0, min(100, state.reputation + rep_delta))

    pre_round_state = GameState(
        session_id=state.session_id,
        template_slug=state.template_slug,
        round_number=state.round_number,
        elapsed_months=state.elapsed_months,
        cash_kopeks=state.cash_kopeks,
        fixed_cost_kopeks=state.fixed_cost_kopeks,
        reputation=new_reputation,
        active_effects=new_effects,
        used_defenses=list(state.used_defenses),
        active_defense_modifiers=list(state.active_defense_modifiers),
        is_bankrupt=state.is_bankrupt,
        bankruptcy_month=state.bankruptcy_month,
        unpaid_obligations_kopeks=state.unpaid_obligations_kopeks,
    )

    # 3. Select defense
    defense_decision = select_best_defense(
        state=pre_round_state,
        startup=startup,
        round_start_month=round_start_month,
        incident_cost_kopeks=one_time_incident_kopeks,
        forced_defense=forced_defense,
    )

    if defense_decision.defense_type != DefenseType.NONE:
        pre_round_state.used_defenses.append(defense_decision.defense_type)
        # Find target stream for supplier switch
        target_s = None
        if defense_decision.defense_type == DefenseType.SUPPLIER_SWITCH:
            for eff in pre_round_state.active_effects:
                if eff.origin_attack_type == AttackType.SUPPLY:
                    target_s = eff.target_stream_id
                    break
        pre_round_state.active_defense_modifiers.append(
            ActiveDefenseModifier(
                defense_type=defense_decision.defense_type,
                activated_round=state.round_number,
                activated_month=round_start_month,
                target_stream_id=target_s,
            )
        )

    # 4. Simulate the 3 months
    monthly_ledger: List[MonthlyLedgerRow] = []
    cur_state = pre_round_state

    for step in range(3):
        m = round_start_month + step
        defense_pay = defense_decision.cost_kopeks if step == 0 else 0
        inc_cost = one_time_incident_kopeks if step == 0 else 0
        row, cur_state = simulate_month(
            state=cur_state,
            startup=startup,
            month=m,
            one_time_incident_cost_kopeks=inc_cost,
            defense_payment_kopeks=defense_pay,
        )
        monthly_ledger.append(row)
        if cur_state.is_bankrupt:
            break

    # Advance round number if not bankrupt
    if not cur_state.is_bankrupt:
        cur_state.round_number += 1

    # Calculate score if game complete (bankrupt or finished round 3)
    final_score = None
    final_status = None
    if cur_state.is_bankrupt or cur_state.elapsed_months >= 9:
        last_row = monthly_ledger[-1]
        final_score = calculate_score(
            actual_cash_kopeks=last_row.closing_cash_kopeks,
            actual_revenue_kopeks=last_row.revenue_kopeks,
            actual_variable_cost_kopeks=last_row.variable_cost_kopeks,
            actual_fixed_cost_kopeks=last_row.fixed_cost_kopeks,
            bankruptcy_month=cur_state.bankruptcy_month,
            unpaid_obligations_kopeks=last_row.unpaid_obligations_kopeks,
            baseline_series=startup.baseline_series,
            baseline_fixed_cost_kopeks=startup.initial_fixed_cost_kopeks,
        )
        final_status = final_score.final_status
        cur_state.score_breakdown = final_score

    start_cash = state.cash_kopeks
    end_cash = cur_state.cash_kopeks
    cash_delta = end_cash - start_cash

    total_rev_delta = sum(
        row.revenue_kopeks - startup.baseline_series[row.month].revenue_kopeks
        for row in monthly_ledger
    )

    return EngineOutcome(
        round_number=state.round_number,
        months_simulated=len(monthly_ledger),
        monthly_ledger=monthly_ledger,
        state_after=cur_state,
        cash_delta_kopeks=cash_delta,
        revenue_delta_kopeks=total_rev_delta,
        reputation_delta=new_reputation - state.reputation,
        defense=defense_decision,
        final_status=final_status,
        score_breakdown=final_score,
        engine_version="v1.0",
    )


def run_golden_case(startup: StartupTemplate, mode: str) -> SimulationResult:
    state = GameState(
        session_id="golden_case",
        template_slug=startup.slug,
        round_number=1,
        elapsed_months=0,
        cash_kopeks=startup.initial_cash_kopeks,
        fixed_cost_kopeks=startup.initial_fixed_cost_kopeks,
        reputation=startup.initial_reputation,
    )

    stream_0_id = startup.revenue_streams[0].id
    stream_1_id = startup.revenue_streams[1].id

    ledger: List[MonthlyLedgerRow] = []

    for m in range(1, 10):
        if mode == "baseline":
            shocks = {stream_0_id: 0, stream_1_id: 0}
        elif mode == "weak_local_one_stream":
            if m == 1:
                shocks = {stream_0_id: 384, stream_1_id: 0}
            elif m == 2:
                shocks = {stream_0_id: 230, stream_1_id: 0}
            elif m == 3:
                shocks = {stream_0_id: 138, stream_1_id: 0}
            else:
                shocks = {stream_0_id: 0, stream_1_id: 0}
        elif mode == "structural_95pct_all_streams":
            shocks = {stream_0_id: 9500, stream_1_id: 9500}
        else:
            raise ValueError(f"Unknown golden mode {mode}")

        row, state = simulate_month(
            state=state,
            startup=startup,
            month=m,
            stream_shocks=shocks,
        )
        ledger.append(row)

        if state.is_bankrupt:
            break

    last_row = ledger[-1]
    score = calculate_score(
        actual_cash_kopeks=last_row.closing_cash_kopeks,
        actual_revenue_kopeks=last_row.revenue_kopeks,
        actual_variable_cost_kopeks=last_row.variable_cost_kopeks,
        actual_fixed_cost_kopeks=last_row.fixed_cost_kopeks,
        bankruptcy_month=state.bankruptcy_month,
        unpaid_obligations_kopeks=last_row.unpaid_obligations_kopeks,
        baseline_series=startup.baseline_series,
        baseline_fixed_cost_kopeks=startup.initial_fixed_cost_kopeks,
    )

    return SimulationResult(
        monthly_ledger=ledger,
        closing_cash_kopeks=last_row.closing_cash_kopeks,
        bankruptcy_month=state.bankruptcy_month,
        unpaid_obligations_kopeks=last_row.unpaid_obligations_kopeks,
        score_breakdown=score,
        final_state=state,
    )
