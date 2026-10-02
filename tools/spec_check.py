"""Offline checks for the deterministic Startup Killer contracts."""
from pathlib import Path
import json
import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


files = [p for p in ROOT.rglob("*.json") if not {"node_modules", ".git", "dist"}.intersection(p.parts)]
for path in files:
    read_json(path)
print(f"JSON parse: {len(files)} files PASS")

for data_name, schema_name in (
    ("startups.json", "startup_schema.json"),
    ("economy_golden_cases.json", "economy_golden_cases_schema.json"),
    ("attack_choices.json", "attack_choices_schema.json"),
):
    data = read_json(ROOT / "data" / data_name)
    schema = read_json(ROOT / "data" / schema_name)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(data, schema)
    print(f"Schema: {data_name} PASS")

startups = read_json(ROOT / "data/startups.json")["startups"]
assert len(startups) == 10 and len({s["slug"] for s in startups}) == 10
catalog = read_json(ROOT / "data/attack_choices.json")
assert catalog["choices_per_round"] == 4
assert len(catalog["choices"]) == 120
expected = {(s["slug"], round_no) for s in startups for round_no in range(1, 4)}
counts = {(slug, round_no): 0 for slug, round_no in expected}
for choice in catalog["choices"]:
    key = (choice["startup_slug"], choice["round_number"])
    assert key in counts
    counts[key] += 1
assert set(counts.values()) == {4}
print("Attack catalog: 10 startups × 3 rounds × 4 choices = 120, PASS")

golden = read_json(ROOT / "data/economy_golden_cases.json")["cases"]
assert len(golden) == 30
print("Economy fixtures: 30 present, PASS")

for rel in ("AGENTS.md", "README.md", "docs/API.md", "docs/DATABASE.md", "implementation/CONFORMANCE_MATRIX.md"):
    assert (ROOT / rel).is_file(), f"missing required document: {rel}"
print("Required deterministic contract documents: present, PASS")
