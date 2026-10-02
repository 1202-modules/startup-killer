import pytest
from dataclasses import replace
from backend.app.engine.calculator import evaluate_defense
from backend.app.engine.defense import get_available_defenses
from backend.app.engine.types import (
    DefenseType,
    GameState,
    StartupTemplate,
    FinanceConfig,
    PublicProfile,
    PrivateProfile,
    ValidatedAttack,
    AttackType,
    Scale,
    Feasibility,
    Severity,
    Duration,
    WeaknessMatch,
    SceneType,
)


def create_test_state_and_startup(fixed_cost_rubles: int = 2_000_000):
    fixed_cost_kopeks = fixed_cost_rubles * 100
    state = GameState(
        session_id="test_narrative",
        template_slug="coffeebot",
        round_number=1,
        elapsed_months=0,
        cash_kopeks=800_000_000,
        fixed_cost_kopeks=fixed_cost_kopeks,
        reputation=80,
    )
    startup = StartupTemplate(
        slug="coffeebot",
        version=1,
        name="CoffeeBot",
        industry="robotics",
        asset_key="coffeebot_v1",
        engine_version="v1.0",
        finance_config=FinanceConfig(
            initial_cash_kopeks=800_000_000,
            initial_fixed_cost_kopeks=fixed_cost_kopeks,
            initial_reputation=80,
            revenue_streams=[],
        ),
        public_profile=PublicProfile(
            tagline="Robotics",
            description="Coffee robots",
            facts=[],
            strengths=[],
        ),
        private_profile=PrivateProfile(
            weaknesses=[],
            allowed_defenses=[
                DefenseType.COST_CUT,
                DefenseType.PR,
                DefenseType.SUPPLIER_SWITCH,
                DefenseType.PIVOT,
            ],
            pivot_compatible=True,
            production_partner_alternative=True,
        ),
        baseline_series=[],
        baseline_cash_m9_kopeks=500_000_000,
    )
    return state, startup


def create_dummy_attack(defense_hint: DefenseType = DefenseType.NONE):
    return ValidatedAttack(
        attack_type=AttackType.COMPETITION,
        target_stream_ids=[],
        scale=Scale.REGIONAL,
        feasibility=Feasibility.PLAUSIBLE,
        severity=Severity.MEDIUM,
        duration=Duration.TEMPORARY,
        evidence_fact_ids=[],
        weakness_match=WeaknessMatch.NORMAL,
        defense_hint=defense_hint,
        scene_type=SceneType.DEMAND,
        intent="Тестовый удар",
        adapted_event="Тестовое событие",
        headline="Тестовый заголовок",
        narrative="Тестовое повествование",
    )


def test_evaluate_defense_russian_narrative_none():
    state, startup = create_test_state_and_startup()
    attack = create_dummy_attack(defense_hint=DefenseType.NONE)
    decision = evaluate_defense(
        state, startup, attack, round_start_month=1, forced_defense=DefenseType.NONE
    )

    assert not decision.detail.startswith("Selected defense")
    assert decision.detail == (
        "Стартап не предпринял защитных мер (расходы: 0 ₽). "
        "Команда растеряна или сочла контратаку нецелесообразной."
    )


def test_unavailable_defense_is_not_forced():
    state, startup = create_test_state_and_startup()
    startup = replace(
        startup,
        private_profile=replace(startup.private_profile, pivot_compatible=False),
    )
    attack = create_dummy_attack(defense_hint=DefenseType.PR)

    decision = evaluate_defense(state, startup, attack, round_start_month=1)

    assert decision.defense_type in get_available_defenses(state, startup.private_profile)


def test_evaluate_defense_russian_narratives_all_types():
    state, startup = create_test_state_and_startup(fixed_cost_rubles=2_000_000)

    # NONE
    d_none = evaluate_defense(state, startup, create_dummy_attack(DefenseType.NONE), round_start_month=1, forced_defense=DefenseType.NONE)
    assert d_none.detail == (
        "Стартап не предпринял защитных мер (расходы: 0 ₽). "
        "Команда растеряна или сочла контратаку нецелесообразной."
    )

    # COST_CUT: 0.25 * fixed_cost = 500,000 rubles
    d_cost = evaluate_defense(state, startup, create_dummy_attack(DefenseType.COST_CUT), round_start_month=1, forced_defense=DefenseType.COST_CUT)
    assert d_cost.detail == (
        "Экстренное сокращение расходов: урезаны операционные траты и бонусы команды (затраты: 500 000 ₽)."
    )

    # PR: 0.25 * fixed_cost = 500,000 rubles
    d_pr = evaluate_defense(state, startup, create_dummy_attack(DefenseType.PR), round_start_month=1, forced_defense=DefenseType.PR)
    assert d_pr.detail == (
        "Антикризисная PR-кампания и контратака в отраслевых медиа (затраты: 500 000 ₽)."
    )

    # SUPPLIER_SWITCH: 0.45 * fixed_cost = 900,000 rubles
    d_sup = evaluate_defense(state, startup, create_dummy_attack(DefenseType.SUPPLIER_SWITCH), round_start_month=1, forced_defense=DefenseType.SUPPLIER_SWITCH)
    assert d_sup.detail == (
        "Срочный поиск альтернативных поставщиков и перестройка логистической цепочки (затраты: 900 000 ₽)."
    )

    # PIVOT: 0.70 * fixed_cost = 1,400,000 rubles
    d_piv = evaluate_defense(state, startup, create_dummy_attack(DefenseType.PIVOT), round_start_month=1, forced_defense=DefenseType.PIVOT)
    assert d_piv.detail == (
        "Глубокий пивот бизнес-модели и переработка ключевого продукта (затраты: 1 400 000 ₽)."
    )


