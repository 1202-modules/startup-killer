from dataclasses import replace

from backend.app.engine.attack_choices import AttackCatalog, choices_for, load_attack_catalog
from backend.app.engine.loader import load_startups
from tools.balance_simulation import enumerate_startup_paths


def _small_catalog(startup_slug: str) -> AttackCatalog:
    root = __import__("pathlib").Path(__file__).resolve().parents[2]
    catalog = load_attack_catalog(root / "data" / "attack_choices.json")
    choices = tuple(
        choice for round_number in range(1, 4)
        for choice in choices_for(catalog, startup_slug, round_number)[:2]
    )
    return replace(catalog, choices_per_round=2, choices=choices)


def test_enumerator_covers_every_reachable_choice_path_deterministically():
    root = __import__("pathlib").Path(__file__).resolve().parents[2]
    startup = load_startups(root / "data" / "startups.json")["coffeebot"]
    catalog = _small_catalog(startup.slug)
    first = enumerate_startup_paths(startup, catalog)
    second = enumerate_startup_paths(startup, catalog)
    assert len(first) == 8
    assert first == second
    assert {len(result.choice_ids) for result in first} == {3}
    assert len({result.choice_ids for result in first}) == 8


def test_enumerator_stops_each_bankruptcy_path_early():
    root = __import__("pathlib").Path(__file__).resolve().parents[2]
    startup = load_startups(root / "data" / "startups.json")["coffeebot"]
    poor_finances = replace(startup.finance_config, initial_cash_kopeks=10_000, initial_fixed_cost_kopeks=100_000_000, revenue_streams=[replace(stream, initial_monthly_revenue_kopeks=0) for stream in startup.revenue_streams])
    startup = replace(startup, finance_config=poor_finances)
    results = enumerate_startup_paths(startup, _small_catalog(startup.slug))
    assert 0 < len(results) < 8
    assert all(result.final_status == "bankrupt" for result in results)
    assert all(len(result.choice_ids) == 1 for result in results)
