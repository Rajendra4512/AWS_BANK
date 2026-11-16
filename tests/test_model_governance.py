import json
from pathlib import Path

import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from fastapi.testclient import TestClient

from app.artifacts import ArtifactStore


@pytest.fixture
def app_context(tmp_path, monkeypatch):
    data = tmp_path / "data"
    artifacts = tmp_path / "artifacts"
    data.mkdir()
    artifacts.mkdir()
    monkeypatch.setenv("AWS_BANK_DATA_DIR", str(data))
    monkeypatch.setenv("AWS_BANK_ARTIFACT_DIR", str(artifacts))
    monkeypatch.setenv("AWS_BANK_ARTIFACT_BACKEND", "local")
    monkeypatch.setenv("AWS_BANK_BOOTSTRAP_PASSWORD", "governance-admin-password-2026")
    import app.main as main

    main.DATA = data
    main.ART = artifacts
    main.DB = data / "bank.sqlite3"
    main.login_attempts.clear()
    with TestClient(main.app) as client:
        assert client.post("/api/login", json={"username": "admin", "password": "governance-admin-password-2026"}).status_code == 200
        yield main, client


def seed_model(main, version, status="candidate"):
    store = ArtifactStore(main.ART, backend="local")
    store.save({"version": version, "synthetic": True}, version)
    with main.db() as connection:
        connection.execute(
            "INSERT INTO models VALUES(?,?,?,?,?)",
            (version, main.now(), json.dumps({"synthetic": True}), status, "synthetic"),
        )


def seed_evaluation(main, version, *, passed=True, model_version=None, timestamp=None):
    result = {
        "ml_model_eval": {
            "status": "completed",
            "model_version": version if model_version is None else model_version,
            "quality_gate": {"passed": passed, "min_recall": 0.5, "max_false_positive_rate": 0.5},
        }
    }
    with main.db() as connection:
        connection.execute(
            "INSERT INTO evaluations(ts,actor,suite,results) VALUES(?,?,?,?)",
            (timestamp or main.now(), "admin", "synthetic-governance", json.dumps(result)),
        )


def audit_actions(main):
    with main.db() as connection:
        return [row["action"] for row in connection.execute("SELECT action FROM audit ORDER BY id")]


def test_synthetic_generator_is_deterministic_and_meets_holdout_gate(app_context):
    main, _ = app_context
    X, y = main.synthetic(seed=42, n=2000)
    X_again, y_again = main.synthetic(seed=42, n=2000)
    assert np.array_equal(X, X_again)
    assert np.array_equal(y, y_again)
    assert 0.02 < float(y.mean()) < 0.06

    train_x, _, train_y, _ = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=250, class_weight="balanced", random_state=42),
    )
    model.fit(train_x, train_y)
    eval_x, eval_y = main.synthetic(seed=4242, n=600)
    predictions = (model.predict_proba(eval_x)[:, 1] >= 0.5).astype(int)
    tn, fp, _, _ = confusion_matrix(eval_y, predictions, labels=[0, 1]).ravel()
    assert recall_score(eval_y, predictions, zero_division=0) >= 0.5
    assert fp / max(fp + tn, 1) <= 0.5


def test_candidate_without_evaluation_is_denied_and_active_is_preserved(app_context):
    main, client = app_context
    seed_model(main, 1, status="active")
    seed_model(main, 2)
    response = client.post("/api/admin/models/2/promote")
    assert response.status_code == 409
    assert client.get("/api/models").json()[0]["status"] == "candidate"
    assert any(action == "model.promotion_rejected" for action in audit_actions(main))


def test_failed_stale_and_mismatched_evaluations_are_denied(app_context):
    main, client = app_context
    seed_model(main, 1, status="active")
    seed_model(main, 2)
    seed_evaluation(main, 2, passed=False)
    assert client.post("/api/admin/models/2/promote").status_code == 409

    seed_model(main, 3)
    seed_evaluation(main, 3, model_version=2)
    assert client.post("/api/admin/models/3/promote").status_code == 409

    seed_model(main, 4)
    seed_evaluation(main, 4, timestamp="2000-01-01T00:00:00+00:00")
    assert client.post("/api/admin/models/4/promote").status_code == 409


def test_passing_evaluation_allows_promotion_and_audits(app_context):
    main, client = app_context
    seed_model(main, 1)
    seed_evaluation(main, 1, passed=True)
    response = client.post("/api/admin/models/1/promote")
    assert response.status_code == 200
    assert response.json()["active_version"] == 1
    assert "model.promote" in audit_actions(main)


def test_unauthorized_promotion_is_denied(app_context):
    main, client = app_context
    seed_model(main, 1)
    client.post("/api/logout")
    assert client.post("/api/admin/models/1/promote").status_code == 401


def test_rollback_requires_prior_approval_and_preserves_active_on_rejection(app_context):
    main, client = app_context
    seed_model(main, 1)
    seed_evaluation(main, 1)
    assert client.post("/api/admin/models/1/promote").status_code == 200
    seed_model(main, 2)
    seed_evaluation(main, 2)
    assert client.post("/api/admin/models/2/promote").status_code == 200
    seed_model(main, 3)

    rejected = client.post("/api/admin/models/3/rollback")
    assert rejected.status_code == 409
    models = client.get("/api/models").json()
    active = next(model for model in models if model["status"] == "active")
    assert active["version"] == 2

    rolled_back = client.post("/api/admin/models/1/rollback")
    assert rolled_back.status_code == 200
    assert rolled_back.json()["active_version"] == 1
    assert "model.rollback" in audit_actions(main)


def test_corrupted_rollback_artifact_is_denied(app_context):
    main, client = app_context
    seed_model(main, 1)
    seed_evaluation(main, 1)
    assert client.post("/api/admin/models/1/promote").status_code == 200
    seed_model(main, 2)
    seed_evaluation(main, 2)
    assert client.post("/api/admin/models/2/promote").status_code == 200
    ArtifactStore(main.ART, backend="local").path(1).write_bytes(b"corrupted")
    response = client.post("/api/admin/models/1/rollback")
    assert response.status_code == 409
    assert client.get("/api/models").json()[0]["version"] == 2
