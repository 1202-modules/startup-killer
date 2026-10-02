"""Cross-check the published contract against the deterministic API surface."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
api = (ROOT / "docs/API.md").read_text(encoding="utf-8")
db = (ROOT / "docs/DATABASE.md").read_text(encoding="utf-8")
agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
routes = (ROOT / "backend/app/api/routes.py").read_text(encoding="utf-8")
schemas = (ROOT / "backend/app/api/schemas.py").read_text(encoding="utf-8")
models = (ROOT / "backend/app/db/models.py").read_text(encoding="utf-8")

assert '"choice_id"' in api and "attack_text" not in api
assert "`POST /sessions/{session_id}/choices`" in api
assert "@router.post(\"/sessions/{session_id}/choices\"" in routes
assert "@router.post(\"/sessions/{session_id}/attacks\"" not in routes
assert "class AttackChoiceRequest" in schemas and "extra=\"forbid\"" in schemas
assert "attack_choices_snapshot" in models and "attack_catalog_version" in models
assert "selected_choice_id" in models and "choice_snapshot" in models
assert "PostgreSQL" in db and "attack_choices_snapshot" in db
assert "data/attack_choices.json" in agents

normative = [
    ROOT / name for name in (
        "AGENTS.md", "README.md", "ANTIGRAVITY_START_HERE.md",
        "docs/PRODUCT.md", "docs/GAME_RULES.md", "docs/API.md",
        "docs/DATABASE.md", "docs/ENGINE_CONTRACT.md",
        "implementation/HANDOFF_GATES.md", "implementation/CONFORMANCE_MATRIX.md",
    )
]
obsolete_contracts = ("ai/OUTPUT_SCHEMA", "ai/PROVIDER_ROUTING", "ADMIN_API.md", "ai_quality_cases")
for path in normative:
    content = path.read_text(encoding="utf-8")
    assert not any(old in content for old in obsolete_contracts), f"obsolete contract referenced by {path.name}"

catalog = json.loads((ROOT / "data/attack_choices.json").read_text(encoding="utf-8"))
assert catalog["catalog_version"] and catalog["choices_per_round"] == 4
assert all(set(c["narrative"]) == {"attack", "company_response", "result"} for c in catalog["choices"])

for path in ("backend/app/ai", "backend/app/worker", "backend/app/api/admin.py"):
    assert not (ROOT / path).exists(), f"obsolete runtime component remains: {path}"
print("Deterministic API, snapshot, catalog, and runtime removal contracts: PASS")
