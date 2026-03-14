from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_decision_make_api_success():
    payload = {
        "device_id": "sensor_api_001",
        "temperature": 10.0,
        "humidity": 80.0,
        "door_open": True,
        "battery": 10,
        "timestamp": "2026-03-13T10:00:00",
        "light_level": 100.0,
        "device_online": True,
        "location": "Warehouse C"
    }

    response = client.post("/decision/make", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["device_id"] == "sensor_api_001"
    assert data["risk_level"] in ["medium", "high"]
    assert "temperature_too_high" in data["anomalies"]
    assert "humidity_too_high" in data["anomalies"]
    assert "door_open" in data["anomalies"]
    assert "battery_low" in data["anomalies"]
    assert "recommendation" in data
    assert "action" in data
    assert "agent_explanation" in data


def test_decision_make_api_invalid_battery():
    payload = {
        "device_id": "sensor_api_002",
        "temperature": 5.0,
        "humidity": 60.0,
        "door_open": False,
        "battery": 150,
        "timestamp": "2026-03-13T10:00:00",
        "light_level": 100.0,
        "device_online": True,
        "location": "Warehouse A"
    }

    response = client.post("/decision/make", json=payload)

    assert response.status_code == 422


def test_health_api():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
