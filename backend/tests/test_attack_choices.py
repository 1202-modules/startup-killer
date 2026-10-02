from copy import deepcopy
from importlib import import_module, util
import json
from pathlib import Path

import pytest

from backend.app.engine.loader import load_startups


ROOT = Path(__file__).resolve().parents[2]
STARTUPS = load_startups(ROOT / "data" / "startups.json")


def catalog_api():
    module_name = "backend.app.engine.attack_choices"
    assert util.find_spec(module_name), "attack choice catalog API is not implemented"
    module = import_module(module_name)
    for name in (
        "load_attack_catalog",
        "validate_attack_catalog",
        "choices_for",
        "to_validated_attack",
    ):
        assert hasattr(module, name), f"catalog API is missing {name}"
    return module


def test_catalog_has_four_choices_for_every_startup_and_round():
    api = catalog_api()
    catalog = api.load_attack_catalog(ROOT / "data" / "attack_choices.json")
    api.validate_attack_catalog(catalog, STARTUPS)

    assert catalog.choices_per_round == 4
    assert len(catalog.choices) == 120
    assert {
        len(api.choices_for(catalog, slug, round_number))
        for slug in STARTUPS
        for round_number in range(1, 4)
    } == {4}


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("startup_slug", "missing_startup", "startup"),
        ("target_stream_ids", ["missing-stream"], "stream"),
        ("weakness_id", "missing-weakness", "weakness"),
        ("evidence_fact_ids", ["missing-fact"], "evidence"),
    ],
)
def test_catalog_rejects_invalid_references(field, value, message):
    api = catalog_api()
    source = json.loads((ROOT / "data" / "attack_choices.json").read_text())
    invalid = deepcopy(source)
    if field == "startup_slug":
        for choice in invalid["choices"]:
            if choice["startup_slug"] == "coffeebot":
                choice[field] = value
    else:
        invalid["choices"][0][field] = value
    with pytest.raises(ValueError, match=message):
        api.validate_attack_catalog(invalid, STARTUPS)


def test_catalog_rejects_invalid_enum():
    api = catalog_api()
    source = json.loads((ROOT / "data" / "attack_choices.json").read_text())
    invalid_enum = deepcopy(source)
    invalid_enum["choices"][0]["severity"] = "catastrophic"
    with pytest.raises(ValueError, match="severity"):
        api.load_attack_catalog(invalid_enum)


def test_catalog_requires_every_configured_round_slot():
    api = catalog_api()
    source = json.loads((ROOT / "data" / "attack_choices.json").read_text())
    source["choices"].pop()

    with pytest.raises(ValueError, match="choices_per_round"):
        api.load_attack_catalog(source)


def test_catalog_rejects_duplicate_choice_ids():
    api = catalog_api()
    source = json.loads((ROOT / "data" / "attack_choices.json").read_text())
    source["choices"][1]["id"] = source["choices"][0]["id"]

    with pytest.raises(ValueError, match="duplicate"):
        api.load_attack_catalog(source)


def test_choice_maps_to_validated_attack():
    api = catalog_api()
    catalog = api.load_attack_catalog(ROOT / "data" / "attack_choices.json")
    choice = api.choices_for(catalog, "coffeebot", 1)[0]
    attack = api.to_validated_attack(choice, STARTUPS["coffeebot"])

    assert attack.attack_type.value == choice.attack_type
    assert attack.target_stream_ids == list(choice.target_stream_ids)
    assert attack.severity.value == choice.severity
    assert attack.scale.value == choice.scale
    assert attack.feasibility.value == choice.feasibility
    assert attack.duration.value == choice.duration
    assert attack.evidence_fact_ids == list(choice.evidence_fact_ids)


def test_choice_has_no_client_supplied_economic_values():
    api = catalog_api()
    catalog = api.load_attack_catalog(ROOT / "data" / "attack_choices.json")
    choice = api.choices_for(catalog, "coffeebot", 1)[0]
    attack = api.to_validated_attack(choice, STARTUPS["coffeebot"])

    assert not hasattr(choice, "effects")
    assert not hasattr(choice, "damage_bps")
    assert not hasattr(attack, "damage_bps")


def test_choice_cannot_be_adapted_for_another_startup():
    api = catalog_api()
    catalog = api.load_attack_catalog(ROOT / "data" / "attack_choices.json")
    choice = api.choices_for(catalog, "coffeebot", 1)[0]

    with pytest.raises(ValueError, match="does not belong"):
        api.to_validated_attack(choice, STARTUPS["petmind"])
