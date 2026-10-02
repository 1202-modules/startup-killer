"""Load and validate the immutable, data-driven attack catalog."""

from dataclasses import dataclass
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from jsonschema import Draft202012Validator

from backend.app.engine.types import (
    AttackType,
    DefenseType,
    Duration,
    Feasibility,
    Scale,
    SceneType,
    Severity,
    StartupTemplate,
    ValidatedAttack,
    WeaknessMatch,
)


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = ROOT / "data" / "attack_choices_schema.json"


@dataclass(frozen=True)
class AttackChoice:
    id: str
    startup_slug: str
    round_number: int
    title: str
    short_description: str
    result_headline: str
    attack_type: str
    severity: str
    scale: str
    feasibility: str
    target_stream_ids: tuple[str, ...]
    weakness_id: str | None
    weakness_match: str
    evidence_fact_ids: tuple[str, ...]
    duration: str
    stack_group: str
    scene_type: str
    narrative: Mapping[str, str]
    v2_effect: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class AttackCatalog:
    catalog_version: str
    choices_per_round: int
    choices: tuple[AttackChoice, ...]


def _read_document(source: Path | Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(source, Mapping):
        return source
    return json.loads(Path(source).read_text(encoding="utf-8"))


def _validate_schema(document: Mapping[str, Any]) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    error = next(
        iter(sorted(validator.iter_errors(document), key=lambda item: tuple(map(str, item.absolute_path)))),
        None,
    )
    if error:
        path = ".".join(str(part) for part in error.absolute_path) or "catalog"
        raise ValueError(f"invalid attack catalog at {path}: {error.message}")


def load_attack_catalog(source: Path | Mapping[str, Any]) -> AttackCatalog:
    document = _read_document(source)
    _validate_schema(document)

    choices_data = document["choices"]
    choice_ids = [item["id"] for item in choices_data]
    if len(choice_ids) != len(set(choice_ids)):
        raise ValueError("duplicate choice id in attack catalog")

    count = document["choices_per_round"]
    slots: dict[tuple[str, int], int] = {}
    for item in choices_data:
        key = item["startup_slug"], item["round_number"]
        slots[key] = slots.get(key, 0) + 1
    if any(number != count for number in slots.values()):
        raise ValueError("attack catalog choices_per_round count mismatch")
    for slug in {item["startup_slug"] for item in choices_data}:
        if any((slug, round_number) not in slots for round_number in range(1, 4)):
            raise ValueError(f"attack catalog choices_per_round missing round for {slug}")

    choices = tuple(
        AttackChoice(
            id=item["id"],
            startup_slug=item["startup_slug"],
            round_number=item["round_number"],
            title=item["title"],
            short_description=item["short_description"],
            result_headline=item["result_headline"],
            attack_type=item["attack_type"],
            severity=item["severity"],
            scale=item["scale"],
            feasibility=item["feasibility"],
            target_stream_ids=tuple(item["target_stream_ids"]),
            weakness_id=item.get("weakness_id"),
            weakness_match=item["weakness_match"],
            evidence_fact_ids=tuple(item["evidence_fact_ids"]),
            duration=item["duration"],
            stack_group=item["stack_group"],
            scene_type=item["scene_type"],
            narrative=MappingProxyType(dict(item["narrative"])),
            v2_effect=MappingProxyType(item["v2_effect"]) if item.get("v2_effect") else None,
        )
        for item in choices_data
    )
    return AttackCatalog(
        catalog_version=document["catalog_version"],
        choices_per_round=count,
        choices=choices,
    )


def validate_attack_catalog(
    catalog: AttackCatalog | Mapping[str, Any],
    startups: Mapping[str, StartupTemplate],
) -> None:
    if not isinstance(catalog, AttackCatalog):
        catalog = load_attack_catalog(catalog)

    counts: dict[tuple[str, int], int] = {}
    for choice in catalog.choices:
        startup = startups.get(choice.startup_slug)
        if startup is None:
            raise ValueError(f"unknown startup {choice.startup_slug}")
        key = choice.startup_slug, choice.round_number
        counts[key] = counts.get(key, 0) + 1

        stream_ids = {stream.id for stream in startup.revenue_streams}
        missing_streams = set(choice.target_stream_ids) - stream_ids
        if missing_streams:
            raise ValueError(f"unknown stream {sorted(missing_streams)[0]} for {choice.id}")
        if choice.v2_effect:
            for phase in ("base_effect", "combo"):
                effect = choice.v2_effect.get(phase)
                if effect and set(effect["stream_loss_bps"]) - stream_ids:
                    raise ValueError(f"unknown v2 stream for {choice.id}")
            if choice.v2_effect["group"] != choice.stack_group:
                raise ValueError(f"v2 group mismatch for {choice.id}")

        weakness_by_id = {item.id: item for item in startup.private_profile.weaknesses}
        if choice.weakness_id:
            weakness = weakness_by_id.get(choice.weakness_id)
            if weakness is None:
                raise ValueError(f"unknown weakness {choice.weakness_id} for {choice.id}")
            if weakness.attack_type != choice.attack_type:
                raise ValueError(f"weakness attack_type mismatch for {choice.id}")
        elif choice.weakness_match == WeaknessMatch.EXACT.value:
            raise ValueError(f"exact weakness match requires weakness_id for {choice.id}")

        fact_ids = {fact.id for fact in startup.public_profile.facts}
        if not choice.evidence_fact_ids or set(choice.evidence_fact_ids) - fact_ids:
            raise ValueError(f"invalid evidence fact reference for {choice.id}")

    for slug in startups:
        for round_number in range(1, 4):
            if counts.get((slug, round_number), 0) != catalog.choices_per_round:
                raise ValueError(f"choices_per_round count mismatch for {slug} round {round_number}")


def choices_for(catalog: AttackCatalog, startup_slug: str, round_number: int) -> list[AttackChoice]:
    return [
        choice
        for choice in catalog.choices
        if choice.startup_slug == startup_slug and choice.round_number == round_number
    ]


def to_validated_attack(choice: AttackChoice, startup: StartupTemplate) -> ValidatedAttack:
    if choice.startup_slug != startup.slug:
        raise ValueError(f"choice {choice.id} does not belong to startup {startup.slug}")
    return ValidatedAttack(
        attack_type=AttackType(choice.attack_type),
        target_stream_ids=list(choice.target_stream_ids),
        scale=Scale(choice.scale),
        feasibility=Feasibility(choice.feasibility),
        severity=Severity(choice.severity),
        duration=Duration(choice.duration),
        evidence_fact_ids=list(choice.evidence_fact_ids),
        weakness_match=WeaknessMatch(choice.weakness_match),
        defense_hint=DefenseType.NONE,
        scene_type=SceneType(choice.scene_type),
        intent=choice.stack_group,
        adapted_event=choice.narrative["attack"],
        headline=choice.result_headline,
        narrative=choice.narrative["result"],
        v2_effect=dict(choice.v2_effect) if choice.v2_effect else None,
    )
