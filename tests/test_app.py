import os
import tempfile

os.environ["DATABASE_URL"] = f"sqlite:///{tempfile.gettempdir()}/ai_job_tracker_test.db"
os.environ["MODEL_PATH"] = f"{tempfile.gettempdir()}/ai_job_tracker_test_model.pkl"

from fastapi.testclient import TestClient

from app.main import app
from app.services.ranking_model import LogisticRankingModel


def test_model_returns_score_between_zero_and_one() -> None:
    model = LogisticRankingModel(weights=[1, 1, 1, 1, 1], bias=-2)
    score = model.predict([0.5, 0.5, 0.5, 0.5, 0.5])
    assert 0 <= score <= 1


def test_recommendation_endpoint_works_and_returns_sorted_jobs() -> None:
    with TestClient(app) as client:
        response = client.get("/recommend/jobs/1?user_id=10")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) > 0
    assert len(payload) <= 10
    assert all(0 <= item["score"] <= 1 for item in payload)
    assert payload == sorted(payload, key=lambda item: item["score"], reverse=True)
    assert {"job_id", "title", "company", "score", "matched_skills", "missing_skills", "reason"} <= set(payload[0])


def test_feedback_endpoint_works() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/events/feedback",
            json={"user_id": 10, "job_id": 1, "event_type": "save"},
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["user_id"] == 10
    assert payload["job_id"] == 1
    assert payload["event_type"] == "save"

