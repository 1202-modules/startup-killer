from pathlib import Path

from backend.app.config import Settings

ROOT = Path(__file__).resolve().parents[2]


def test_runtime_config_needs_no_ai_credentials():
    settings = Settings(_env_file=None)
    assert not {"APP_MASTER_KEY_B64", "ADMIN_PASSWORD_HASH", "MAX_QUEUE_SIZE"}.intersection(Settings.model_fields)
    assert settings.SECRET_KEY
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "APP_MASTER_KEY_B64" not in compose + env_example
    assert "ADMIN_PASSWORD_HASH" not in compose + env_example


def test_compose_has_no_worker():
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    assert "  worker:" not in compose
    assert "backend.app.worker" not in compose


def test_configured_healthchecks_match_api_routes():
    route_source = (ROOT / "backend/app/api/routes.py").read_text(encoding="utf-8")
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    dockerfile = (ROOT / "Dockerfile.backend").read_text(encoding="utf-8")
    path = "/api/v1/health/live"
    assert '@router.get("/health/live"' in route_source
    assert path in compose
    assert path in dockerfile
