from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_returns_expected_response():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "application": "student-ml-api",
        "version": "1.0.1",
    }


def test_predict_returns_doubled_value():
    response = client.post("/predict", json={"value": 10})

    assert response.status_code == 200
    assert response.json()["input"] == 10
    assert response.json()["prediction"] == 20


def test_predict_rejects_missing_value():
    response = client.post("/predict", json={})

    assert response.status_code == 422


def test_predict_rejects_invalid_value():
    response = client.post("/predict", json={"value": "not-a-number"})

    assert response.status_code == 422
