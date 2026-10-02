import hashlib
import json
from pathlib import Path
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.models import StartupTemplate, StartupTemplateVersion


def find_default_startups_json_path() -> Path:
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        candidate = parent / "data" / "startups.json"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("Could not find data/startups.json in parent directories.")


def compute_startup_sha256(startup_dict: dict) -> str:
    """Computes a deterministic canonical SHA-256 hash of a startup dictionary."""
    canonical_bytes = json.dumps(startup_dict, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(canonical_bytes).hexdigest()


def verify_manifest_if_present(json_path: Path) -> None:
    manifest_path = json_path.parent.parent / "MANIFEST.sha256"
    if manifest_path.is_file():
        content_hash = hashlib.sha256(json_path.read_bytes()).hexdigest()
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            if len(parts) == 2 and parts[1].strip() == "data/startups.json":
                expected_hash = parts[0].strip()
                if content_hash != expected_hash:
                    raise ValueError(
                        f"data/startups.json checksum mismatch: expected {expected_hash}, got {content_hash}"
                    )
                break


def seed_startups(session: Session, startups_json_path: Optional[Path] = None) -> List[StartupTemplate]:
    """Loads 10 startups from data/startups.json, records templates and version 1.
    
    Idempotent: will not create duplicate templates or versions if they already exist.
    """
    path = startups_json_path or find_default_startups_json_path()
    verify_manifest_if_present(path)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    startups_list = data.get("startups", [])
    if len(startups_list) != 10:
        raise ValueError(f"Expected exactly 10 startups in {path}, found {len(startups_list)}")

    templates: List[StartupTemplate] = []

    for item in startups_list:
        slug = item["slug"]
        version = int(item["version"])
        content_sha256 = compute_startup_sha256(item)

        # 1. Fetch or create StartupTemplate
        template = session.scalar(
            select(StartupTemplate).where(StartupTemplate.slug == slug)
        )
        if not template:
            template = StartupTemplate(
                slug=slug,
                is_enabled=True,
                current_version=version,
            )
            session.add(template)
            session.flush()

        # 2. Fetch or create StartupTemplateVersion
        template_version = session.scalar(
            select(StartupTemplateVersion).where(
                StartupTemplateVersion.template_id == template.id,
                StartupTemplateVersion.version == version,
            )
        )
        if not template_version:
            template_version = StartupTemplateVersion(
                template_id=template.id,
                version=version,
                name=item["name"],
                industry=item["industry"],
                public_profile=item["public_profile"],
                private_profile=item["private_profile"],
                finance_config=item["finance_config"],
                asset_key=item["asset_key"],
                baseline_series=item["baseline_series"],
                baseline_cash_m9_kopeks=item["baseline_cash_m9_kopeks"],
                content_sha256=content_sha256,
                engine_version=item.get("engine_version", "economy-v1"),
            )
            session.add(template_version)

        if template.current_version < version:
            template.current_version = version

        templates.append(template)

    session.commit()
    return templates
