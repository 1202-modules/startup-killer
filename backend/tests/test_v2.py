from copy import deepcopy
from itertools import product
import json
from pathlib import Path

from backend.app.engine.attack_choices import choices_for, load_attack_catalog, to_validated_attack
from backend.app.engine.calculator import simulate_round
from backend.app.engine.loader import load_startups
from backend.app.engine.types import GameState
from backend.app.engine.v2 import _month, _select

ROOT = Path(__file__).resolve().parents[2]
STARTUPS = load_startups(ROOT / 'data/startups.json')
CATALOG = load_attack_catalog(ROOT / 'data/attack_choices.json')
V2 = ('petmind', 'coffeebot', 'foodrover', 'studygenie',
      'sleepwork', 'fitmirror', 'cloudkitchen', 'agrodrone', 'moodads', 'renteverything')


def play(slug, letters):
    startup = STARTUPS[slug]
    state = GameState('v2-test', slug, 1, 0, startup.initial_cash_kopeks,
                      startup.initial_fixed_cost_kopeks, startup.initial_reputation)
    outcomes = []
    for round_number, letter in enumerate(letters, 1):
        choice = choices_for(CATALOG, slug, round_number)['ABCD'.index(letter)]
        outcome = simulate_round(state, startup, to_validated_attack(choice, startup))
        outcomes.append(outcome)
        state = outcome.state_after
        if state.is_bankrupt:
            break
    return outcomes


def test_combo_requires_r1_and_r2_flags_for_every_chain():
    for slug in V2:
        for letter in 'ABC':
            coherent = play(slug, letter * 3)
            assert coherent[1].details['combo_triggered']
            assert coherent[2].details['combo_triggered']
            for first in 'ABCD':
                if first == letter:
                    continue
                bypass = play(slug, first + letter * 2)
                assert not bypass[1].details['combo_triggered']
                assert not bypass[2].details['combo_triggered']


def test_same_group_replaces_and_different_group_multiplies():
    state = play('petmind', 'BB')[1].state_after
    assert len([e for e in state.v2_data['effects'] if e['group'] == 'petmind_b']) == 1
    startup = STARTUPS['petmind']
    state = deepcopy(state)
    state.v2_data['effects'] = [
        {'group': 'petmind_a', 'cause': 'petmind_a', 'streams': {'collars': 5000}, 'duration': 'structural', 'remaining': 9},
        {'group': 'petmind_c', 'cause': 'petmind_c', 'streams': {'collars': 5000}, 'duration': 'structural', 'remaining': 9},
    ]
    row, _ = _month(state, startup, 7)
    assert row.streams[0].shock_bps == 7500


def test_defense_affects_only_matching_cause_and_starts_next_month():
    startup = STARTUPS['petmind']
    state = GameState('v2-test', 'petmind', 1, 0, startup.initial_cash_kopeks,
                      startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                      v2_data={'effects': [
                          {'group': 'petmind_b', 'cause': 'petmind_b', 'streams': {'collars': 5000}, 'duration': 'structural', 'remaining': 9},
                          {'group': 'petmind_d', 'cause': 'petmind_d', 'streams': {'subscription': 5000}, 'duration': 'structural', 'remaining': 9},
                      ], 'defenses': [{'name': 'second_factory', 'start': 2, 'months': 9,
                                      'group': 'petmind_b', 'factor': 4200,
                                      'variable': {'collars': 400}, 'discount': {}}]})
    first, _ = _month(state, startup, 1)
    second, _ = _month(state, startup, 2)
    assert first.streams[0].shock_bps == 5000
    assert second.streams[0].shock_bps == 2100
    assert first.streams[1].shock_bps == second.streams[1].shock_bps == 5000
    state.v2_data['effects'][0]['cause'] = 'customer_churn'
    churn, _ = _month(state, startup, 2)
    assert churn.streams[0].shock_bps == 5000


def test_none_reason_and_cost_cut_gate():
    startup = STARTUPS['petmind']
    state = GameState('v2-test', 'petmind', 1, 0, startup.initial_cash_kopeks,
                      startup.initial_fixed_cost_kopeks, startup.initial_reputation)
    decision, name, forecasts = _select(state, startup, 1, 0)
    assert name == 'none'
    assert forecasts[0]['defense'] == 'none'
    assert 'Защита не запущена' in decision.reason
    assert 'cost_cut' not in state.v2_data.get('defenses', [])
    low_cash = GameState('v2-test', 'petmind', 1, 0, 190000000,
                         startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                         v2_data={'effects': [{'group': 'petmind_b', 'cause': 'petmind_b',
                                                   'streams': {'collars': 2000},
                                               'duration': 'structural', 'remaining': 9}]})
    assert _select(low_cash, startup, 1, 0)[1] == 'cost_cut'


def test_defense_forecast_counts_months_after_current_round():
    startup = STARTUPS['petmind']
    state = GameState('v2-test', 'petmind', 1, 0, startup.initial_cash_kopeks,
                      startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                      v2_data={'effects': [{'group': 'petmind_b', 'cause': 'petmind_b',
                                           'streams': {'collars': 2500}, 'duration': 'structural',
                                           'remaining': 9}]})
    assert _select(state, startup, 1, 0)[1] == 'second_factory'


def test_named_defense_is_not_reused_after_it_was_recorded():
    startup = STARTUPS['petmind']
    state = GameState('v2-test', 'petmind', 1, 0, startup.initial_cash_kopeks,
                      startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                      v2_data={'effects': [{'group': 'petmind_a', 'cause': 'petmind_a',
                                           'streams': {'collars': 2500}, 'duration': 'structural',
                                           'remaining': 9}],
                               'defenses': [{'name': 'independent_audit', 'start': 1, 'months': 3,
                                             'group': 'petmind_a', 'factor': 5500,
                                             'variable': {}, 'discount': {}}]})
    _, selected, forecasts = _select(state, startup, 1, 0)
    assert selected != 'independent_audit'
    assert all(item['defense'] != 'independent_audit' for item in forecasts)


def test_independent_revenue_discounts_multiply():
    startup = STARTUPS['studygenie']
    state = GameState('v2-test', 'studygenie', 1, 0, startup.initial_cash_kopeks,
                      startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                      v2_data={'effects': [], 'defenses': [
                          {'name': 'student_retention', 'start': 1, 'months': 3,
                           'group': 'studygenie_c', 'factor': 5500, 'variable': {},
                           'discount': {'subscriptions': 400}},
                          {'name': 'cost_cut', 'start': 1, 'months': 9,
                           'group': '', 'factor': 10000, 'variable': {}, 'discount': {}},
                      ]})
    row, _ = _month(state, startup, 1)
    from decimal import Decimal, ROUND_HALF_UP
    base = startup.revenue_streams[0].initial_monthly_revenue_kopeks
    expected = int((Decimal(base) * Decimal('0.96') * Decimal('0.95')).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    assert row.streams[0].revenue_kopeks == expected


def test_all_64_paths_replay_deterministically_and_show_baseline_damage():
    for slug in V2:
        for letters in product('ABCD', repeat=3):
            path = ''.join(letters)
            first = play(slug, path)
            second = play(slug, path)
            assert [(o.state_after.cash_kopeks, o.details, o.defense.defense_type)
                    for o in first] == [(o.state_after.cash_kopeks, o.details, o.defense.defense_type)
                                       for o in second]
            for outcome in first:
                details = outcome.details
                assert details['player_damage_kopeks'] == details['baseline_cash_kopeks'] - outcome.state_after.cash_kopeks
                assert details['baseline_revenue_kopeks'] - outcome.monthly_ledger[-1].revenue_kopeks == details['revenue_damage_kopeks']


def test_v2_schema_rejects_out_of_range_explicit_loss():
    source = json.loads((ROOT / 'data/attack_choices.json').read_text())
    choice = next(item for item in source['choices'] if item['startup_slug'] == 'petmind')
    choice['v2_effect']['base_effect']['stream_loss_bps']['collars'] = 9501
    import pytest
    with pytest.raises(ValueError, match='invalid attack catalog'):
        load_attack_catalog(source)


def test_v2_deep_crisis_cash_threshold_is_sixty_percent():
    from decimal import Decimal
    from backend.app.engine.scoring import calculate_score
    startup = STARTUPS['petmind']
    cash = startup.baseline_cash_m9_kopeks * 65 // 100
    args = (cash, startup.initial_fixed_cost_kopeks, 0,
            startup.initial_fixed_cost_kopeks, None, 0,
            startup.baseline_series, startup.initial_fixed_cost_kopeks)
    assert calculate_score(*args, deep_runway_months=8, deep_cash_ratio=Decimal('0.6')).final_status.value == 'survived'
    assert calculate_score(*args).final_status.value == 'deep_crisis'


def test_inevitable_bankruptcy_prefers_latest_then_unpaid(monkeypatch):
    import backend.app.engine.v2 as v2
    startup = STARTUPS['petmind']
    state = GameState('x', 'petmind', 1, 0, 100000000, startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                      v2_data={'effects': [{'group': 'petmind_b', 'cause': 'petmind_b', 'streams': {'collars': 9000}, 'duration': 'structural', 'remaining': 9}]})
    outcomes = {'none': (7, 0, 100, 10), 'second_factory': (8, 0, 60, 20), 'cost_cut': (8, 0, 80, 20)}
    monkeypatch.setattr(v2, '_forecast', lambda *args: outcomes[args[3]])
    decision, name, _ = v2._select(state, startup, 1, 0)
    assert name == 'second_factory'


def test_survival_beats_higher_prebankruptcy_revenue(monkeypatch):
    import backend.app.engine.v2 as v2
    startup = STARTUPS['petmind']
    state = GameState('x', 'petmind', 1, 0, 100000000, startup.initial_fixed_cost_kopeks, startup.initial_reputation,
                      v2_data={'effects': [{'group': 'petmind_b', 'cause': 'petmind_b', 'streams': {'collars': 9000}, 'duration': 'structural', 'remaining': 9}]})
    outcomes = {'none': (7, 0, 100, 1000), 'second_factory': (None, 50000000, 0, 100), 'cost_cut': (8, 0, 50, 900)}
    monkeypatch.setattr(v2, '_forecast', lambda *args: outcomes[args[3]])
    decision, name, _ = v2._select(state, startup, 1, 0)
    assert name == 'second_factory'
