from app.services.policy_service import generate_policy


def test_generate_policy_normal_case():
    result = generate_policy(anomalies=[], risk_level="low")

    assert result["recommendation"] == "System operating normally."
    assert result["action"].cooling_level is None
    assert result["action"].send_alert is False
    assert result["action"].maintenance_required is False


def test_generate_policy_temperature_and_door():
    anomalies = ["temperature_too_high", "door_open"]
    result = generate_policy(anomalies=anomalies, risk_level="medium")

    assert "Increase cooling level and inspect cooling equipment" in result["recommendation"]
    assert "Close the storage door and inspect the door seal" in result["recommendation"]
    assert result["action"].cooling_level == "increase"
    assert result["action"].send_alert is True
    assert result["action"].maintenance_required is False


def test_generate_policy_battery_and_offline():
    anomalies = ["battery_low", "device_offline"]
    result = generate_policy(anomalies=anomalies, risk_level="high")

    assert "Schedule battery replacement and inspect power supply" in result["recommendation"]
    assert "Check network connection and escalate to maintenance" in result["recommendation"]
    assert result["action"].send_alert is True
    assert result["action"].maintenance_required is True


def test_generate_policy_weather_context():
    anomalies = ["temperature_too_high", "hot_weather_pressure"]
    result = generate_policy(anomalies=anomalies, risk_level="medium")

    assert "Increase cooling level and inspect cooling equipment" in result["recommendation"]
    assert "Consider increased cooling load due to hot external weather" in result["recommendation"]
    assert result["action"].cooling_level == "increase"
    assert result["action"].send_alert is True
