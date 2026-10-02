import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.seed import seed_startups
from backend.app.db.session import Base, get_db
from backend.app.main import app


def test_full_game_uses_only_catalog_choices():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    with SessionLocal() as db:
        seed_startups(db)

    def override_get_db():
        with SessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as client:
            csrf = client.get("/api/v1/bootstrap").json()["csrf_token"]
            created = client.post("/api/v1/sessions", headers={
                "X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4()),
            }, json={"nickname": "CatalogPlayer"}).json()
            session_id = created["session_id"]
            for round_number in range(1, 4):
                detail = client.get(f"/api/v1/sessions/{session_id}").json()
                choice = next(c for c in detail["available_choices"] if c["round_number"] == round_number)
                result = client.post(
                    f"/api/v1/sessions/{session_id}/choices",
                    headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
                    json={"choice_id": choice["id"]},
                )
                assert result.status_code == 200
                assert result.json()["months_simulated"] == list(range((round_number - 1) * 3 + 1, round_number * 3 + 1))
                if round_number < 3 and result.json()["next_action"] == "continue":
                    continued = client.post(
                        f"/api/v1/sessions/{session_id}/continue",
                        headers={"X-CSRF-Token": csrf, "Idempotency-Key": str(uuid.uuid4())},
                        json={"resolved_round_id": result.json()["round_id"]},
                    )
                    assert continued.status_code == 200
                    assert continued.json()["next_round"] == round_number + 1
            detail = client.get(f"/api/v1/sessions/{session_id}").json()
            assert detail["status"] == "completed"
            assert detail["elapsed_months"] <= 9
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
