"""Explicit deterministic attack and defense rules for four v2 startups."""
from __future__ import annotations

from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from backend.app.engine.scoring import calculate_score
from backend.app.engine.types import (
    DefenseDecision, DefenseType, Duration, EngineOutcome, GameState,
    MonthlyLedgerRow, StartupTemplate, StreamLedgerRow, ValidatedAttack,
)

DECAY = {'temporary': 6000, 'persistent': 8500, 'structural': 10000}
MONTHS = {'temporary': 3, 'persistent': 6, 'structural': 9}
# group letter, cost RUB, mitigation factor, months, variable-cost bps, discount bps, stream scope
DEFENSES: dict[str, dict[str, tuple]] = {
    'petmind': {
        'independent_audit': ('a', 350000, 6200, 9, {}, {}),
        'second_factory': ('b', 700000, 4200, 9, {'collars': 400}, {}),
        'retention_offer': ('c', 150000, 5000, 3, {}, {'subscription': 500}),
    },
    'coffeebot': {
        'campus_redeploy': ('a', 350000, 6000, 9, {}, {}),
        'service_reserve': ('b', 600000, 5500, 9, {'kiosks': 200, 'service': 200}, {}),
        'loyalty_program': ('c', 250000, 6200, 9, {}, {}),
        'sla_guarantee': ('d', 220000, 5500, 9, {}, {}),
    },
    'foodrover': {
        'route_rebuild': ('a', 500000, 5500, 9, {'delivery': 300}, {}),
        'battery_reserve': ('b', 700000, 4500, 9, {'delivery': 250, 'maintenance': 250}, {}),
        'restaurant_retention': ('c', 350000, 5500, 3, {}, {'delivery': 400}),
        'partner_service': ('d', 250000, 5000, 9, {'maintenance': 200}, {}),
    },
    'studygenie': {
        'quality_audit': ('a', 250000, 6000, 9, {}, {}),
        'backup_provider': ('b', 500000, 4500, 9, {'subscriptions': 300, 'schools': 300}, {}),
        'student_retention': ('c', 180000, 5500, 3, {}, {'subscriptions': 400}),
        'school_success_team': ('d', 180000, 5500, 9, {}, {}),
    },
}
DEFENSE_LABELS = {
    'none': 'Защита не запущена', 'cost_cut': 'Аварийное сокращение расходов',
    'independent_audit': 'Независимый аудит', 'second_factory': 'Второй завод',
    'retention_offer': 'Предложение подписчикам', 'campus_redeploy': 'Перенос точек',
    'service_reserve': 'Резерв обслуживания', 'loyalty_program': 'Программа лояльности',
    'sla_guarantee': 'Гарантия сервиса', 'route_rebuild': 'Перестройка маршрутов',
    'battery_reserve': 'Резерв аккумуляторов', 'restaurant_retention': 'Удержание ресторанов',
    'partner_service': 'Партнёрский сервис', 'quality_audit': 'Аудит качества',
    'backup_provider': 'Резервный поставщик сервиса', 'student_retention': 'Удержание учеников',
    'school_success_team': 'Команда для школ',
}


def q(value: Decimal) -> int:
    return int(value.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _active_defense(data: dict[str, Any], month: int):
    for item in data.get('defenses', []):
        if item['start'] <= month < item['start'] + item['months']:
            yield item


def _month(state: GameState, startup: StartupTemplate, month: int, incident: int = 0, defense_cost: int = 0):
    data = deepcopy(state.v2_data)
    defenses = list(_active_defense(data, month))
    cut = any(d['name'] == 'cost_cut' for d in defenses)
    fixed = q(Decimal(startup.initial_fixed_cost_kopeks) * Decimal(8500 if cut else 10000) / 10000)
    rows = []
    total_rev = total_var = 0
    for stream in startup.revenue_streams:
        base = q(Decimal(stream.initial_monthly_revenue_kopeks) *
                 (Decimal(1) + Decimal(stream.monthly_growth_bps) / 10000) ** (month - 1))
        remaining = Decimal(1)
        var_bps = stream.variable_cost_bps
        discount_factor = Decimal(1)
        for effect in data.get('effects', []):
            magnitude = effect['streams'].get(stream.id, 0)
            if magnitude:
                for defense in defenses:
                    if defense['group'] == effect['group'] and effect.get('cause') != 'customer_churn':
                        magnitude = q(Decimal(magnitude) * Decimal(defense['factor']) / 10000)
                remaining *= Decimal(10000 - magnitude) / 10000
        shock = min(9500, q((1 - remaining) * 10000))
        for defense in defenses:
            if defense['name'] == 'cost_cut':
                discount_factor *= Decimal(9500) / 10000
            else:
                var_bps += defense['variable'].get(stream.id, 0)
                discount_factor *= Decimal(10000 - defense['discount'].get(stream.id, 0)) / 10000
        revenue = q(Decimal(base) * Decimal(10000 - shock) / 10000 * discount_factor)
        variable = q(Decimal(revenue) * Decimal(var_bps) / 10000)
        rows.append(StreamLedgerRow(stream.id, base, shock, revenue, variable))
        total_rev += revenue
        total_var += variable
    profit = total_rev - total_var - fixed - incident - defense_cost
    tentative = state.cash_kopeks + profit
    unpaid = max(0, -tentative)
    closing = max(0, tentative)
    row = MonthlyLedgerRow(month, rows, total_rev, total_var, fixed, profit, closing, unpaid, incident, defense_cost)
    next_effects = []
    for effect in data.get('effects', []):
        if effect['remaining'] <= 1:
            continue
        reduced = {stream: q(Decimal(loss) * Decimal(DECAY[effect['duration']]) / 10000)
                   for stream, loss in effect['streams'].items()}
        next_effects.append({**effect, 'streams': reduced, 'remaining': effect['remaining'] - 1})
    data['effects'] = next_effects
    new_state = deepcopy(state)
    new_state.v2_data = data
    new_state.cash_kopeks = closing
    new_state.fixed_cost_kopeks = fixed
    new_state.elapsed_months = month
    if unpaid:
        new_state.is_bankrupt = True
        new_state.bankruptcy_month = month
        new_state.unpaid_obligations_kopeks = unpaid
    return row, new_state


def _forecast(state: GameState, startup: StartupTemplate, start: int, name: str, cost: int, incident: int):
    trial = deepcopy(state)
    if name != 'none':
        trial.v2_data.setdefault('defenses', []).append(_modifier(start, name, startup.slug))
    bankruptcy = None
    for month in range(start, 10):
        _, trial = _month(trial, startup, month, incident if month == start else 0,
                          cost if month == start else 0)
        if trial.is_bankrupt:
            bankruptcy = month
            break
    return bankruptcy, trial.cash_kopeks


def _modifier(start: int, name: str, slug: str) -> dict[str, Any]:
    if name == 'cost_cut':
        return {'name': name, 'start': start + 1, 'months': 9, 'group': '',
                'factor': 10000, 'variable': {}, 'discount': {}}
    group, _, factor, months, variable, discount = DEFENSES[slug][name]
    return {'name': name, 'start': start + 1, 'months': months,
            'group': f'{slug}_{group}', 'factor': factor,
            'variable': variable, 'discount': discount}


def _select(state: GameState, startup: StartupTemplate, start: int, incident: int):
    none_bankrupt, none_cash = _forecast(state, startup, start, 'none', 0, incident)
    candidates = [('none', 0, none_bankrupt, none_cash)]
    active_groups = {e['group'] for e in state.v2_data.get('effects', []) if e.get('cause') != 'customer_churn'}
    prior = state.v2_data.get('defenses', [])
    for name, (letter, rubles, *_rest) in DEFENSES[startup.slug].items():
        group = f'{startup.slug}_{letter}'
        if (group not in active_groups or
            any(d['group'] == group and d['start'] <= start + 1 < d['start'] + d['months'] for d in prior)):
            continue
        cost = rubles * 100
        if state.cash_kopeks < cost:
            continue
        bankrupt, cash = _forecast(state, startup, start, name, cost, incident)
        candidates.append((name, cost, bankrupt, cash))
    if none_bankrupt is not None and not any(d['name'] == 'cost_cut' for d in prior):
        cost = q(Decimal(state.fixed_cost_kopeks) * Decimal(2500) / 10000)
        if state.cash_kopeks >= cost:
            bankrupt, cash = _forecast(state, startup, start, 'cost_cut', cost, incident)
            candidates.append(('cost_cut', cost, bankrupt, cash))
    # Survival dominates. If all fail, prefer later failure before cost.
    best = min(enumerate(candidates), key=lambda pair: (
        pair[1][2] is not None, -(pair[1][3] if pair[1][2] is None else pair[1][2]),
        pair[1][1], pair[0]))[1]
    name, cost, bankruptcy, cash = best
    if name == 'none':
        reason = ('Защита не запущена: доступные меры не улучшают прогноз до девятого месяца.'
                  if len(candidates) > 1 else 'Защита не запущена: подходящей меры для текущей причины нет.')
    else:
        reason = ('Выбрана мера, предотвращающая банкротство.' if bankruptcy is None and none_bankrupt is not None
                  else 'Выбрана мера с лучшим прогнозом денег к девятому месяцу.')
    detail = (f'{DEFENSE_LABELS[name]}: затраты {cost // 100:,} ₽.' +
              ('' if name == 'none' else f' {reason}')).replace(',', ' ')
    forecasts = [
        {'defense': candidate, 'cost_kopeks': candidate_cost,
         'bankruptcy_month': candidate_bankruptcy, 'projected_cash_m9_kopeks': cash_m9}
        for candidate, candidate_cost, candidate_bankruptcy, cash_m9 in candidates
    ]
    return DefenseDecision(DefenseType(name), cost, start + 1, detail, reason), name, forecasts


def simulate_v2_round(state: GameState, startup: StartupTemplate, attack: ValidatedAttack,
                      forced_defense: DefenseType | None = None) -> EngineOutcome:
    if state.is_bankrupt or state.elapsed_months >= 9:
        raise ValueError('game already completed')
    spec = attack.v2_effect
    assert spec is not None
    start = (state.round_number - 1) * 3 + 1
    before = set(state.v2_data.get('flags', []))
    combo = spec.get('combo')
    matched = bool(combo and set(combo.get('requires_all', [])).issubset(before))
    applied = combo if matched else spec['base_effect']
    group = spec['group']
    pre = deepcopy(state)
    data = pre.v2_data
    data['flags'] = sorted(before | set(applied['set_flags']))
    data['effects'] = [effect for effect in data.get('effects', []) if effect['group'] != group]
    data['effects'].append({'group': group, 'cause': spec.get('cause', group),
                            'streams': dict(applied['stream_loss_bps']),
                            'duration': applied['duration'], 'remaining': MONTHS[applied['duration']]})
    pre.reputation = max(0, min(100, pre.reputation + applied['reputation_delta']))
    incident = applied['incident_cost_kopeks']
    if forced_defense == DefenseType.NONE:
        defense = DefenseDecision(DefenseType.NONE, 0, start + 1,
                                  'Защита отключена для контрольной симуляции.',
                                  'Контрольная симуляция без защиты.')
        defense_name = 'none'
        forecasts = []
    elif forced_defense is not None:
        raise ValueError('v2 forced defense supports NONE only')
    else:
        defense, defense_name, forecasts = _select(pre, startup, start, incident)
    if defense_name != 'none':
        data.setdefault('defenses', []).append(_modifier(start, defense_name, startup.slug))
        if defense_name == 'cost_cut':
            pre.used_defenses.append(DefenseType.COST_CUT)
    ledger = []
    current = pre
    for month in range(start, start + 3):
        row, current = _month(current, startup, month, incident if month == start else 0,
                              defense.cost_kopeks if month == start else 0)
        ledger.append(row)
        if current.is_bankrupt:
            break
    if not current.is_bankrupt:
        current.round_number += 1
    final = None
    if current.is_bankrupt or current.elapsed_months == 9:
        row = ledger[-1]
        final = calculate_score(row.closing_cash_kopeks, row.revenue_kopeks,
                                row.variable_cost_kopeks, row.fixed_cost_kopeks,
                                current.bankruptcy_month, row.unpaid_obligations_kopeks,
                                startup.baseline_series, startup.initial_fixed_cost_kopeks,
                                deep_runway_months=8, deep_cash_ratio=Decimal('0.6'))
        current.score_breakdown = final
    last = ledger[-1]
    baseline = startup.baseline_series[last.month]
    details = {'combo_triggered': matched, 'effect_group': group,
               'affected_streams': dict(applied['stream_loss_bps']),
               'incident_cost_kopeks': incident,
               'baseline_cash_kopeks': baseline.closing_cash_kopeks,
               'player_damage_kopeks': baseline.closing_cash_kopeks - last.closing_cash_kopeks,
               'baseline_revenue_kopeks': baseline.revenue_kopeks,
               'revenue_damage_kopeks': baseline.revenue_kopeks - last.revenue_kopeks,
               'opened_flags': applied['set_flags'], 'defense_name': defense_name,
               'defense_cost_kopeks': defense.cost_kopeks, 'defense_reason': defense.reason}
    return EngineOutcome(state.round_number, len(ledger), ledger, current,
                         current.cash_kopeks - state.cash_kopeks,
                         sum(row.revenue_kopeks - startup.baseline_series[row.month].revenue_kopeks for row in ledger),
                         current.reputation - state.reputation, defense,
                         final_status=final.final_status if final else None,
                         score_breakdown=final, engine_version='v2.0', details=details,
                         audit={'defense_candidates': forecasts})
