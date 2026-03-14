from app.schema.sensor import SensorInput
from app.schema.weather import WeatherContext
from app.services.anomaly_service import detect_anomalies


def test_detect_anomalies_normal_case():
    sensor = SensorInput(
        device_id="sensor_001",
        temperature=5.0,
        humidity=60.0,
        door_open=False,
        battery=80,
        timestamp="2026-03-13T10:00:00",
        light_level=100.0,
        device_online=True,
        location="Warehouse A"
    )

    weather = WeatherContext(
        outside_temperature=15.0,
        outside_humidity=65.0,
        weather_condition="cloudy",
        wind_speed=10.0
    )

    result = detect_anomalies(sensor, weather)

    assert result["anomalies"] == []
    assert result["risk_score"] == 0
    assert result["risk_level"] == "low"


def test_detect_anomalies_high_temp_with_hot_weather():
    sensor = SensorInput(
        device_id="sensor_002",
        temperature=10.0,
        humidity=60.0,
        door_open=False,
        battery=80,
        timestamp="2026-03-13T10:00:00",
        light_level=100.0,
        device_online=True,
        location="Warehouse C"
    )

    weather = WeatherContext(
        outside_temperature=30.0,
        outside_humidity=70.0,
        weather_condition="hot",
        wind_speed=5.0
    )

    result = detect_anomalies(sensor, weather)

    assert "temperature_too_high" in result["anomalies"]
    assert "hot_weather_pressure" in result["anomalies"]
    assert result["risk_score"] == 40
    assert result["risk_level"] == "medium"


def test_detect_anomalies_multiple_critical_conditions():
    sensor = SensorInput(
        device_id="sensor_003",
        temperature=10.0,
        humidity=80.0,
        door_open=True,
        battery=10,
        timestamp="2026-03-13T10:00:00",
        light_level=100.0,
        device_online=False,
        location="Warehouse C"
    )

    weather = WeatherContext(
        outside_temperature=30.0,
        outside_humidity=80.0,
        weather_condition="hot",
        wind_speed=5.0
    )

    result = detect_anomalies(sensor, weather)

    assert "temperature_too_high" in result["anomalies"]
    assert "humidity_too_high" in result["anomalies"]
    assert "door_open" in result["anomalies"]
    assert "battery_low" in result["anomalies"]
    assert "device_offline" in result["anomalies"]
    assert "hot_weather_pressure" in result["anomalies"]
    assert "humid_weather_pressure" in result["anomalies"]
    assert result["risk_score"] == 100
    assert result["risk_level"] == "high"
