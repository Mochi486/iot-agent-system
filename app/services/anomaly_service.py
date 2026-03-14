from app.schema.sensor import SensorInput
from app.schema.weather import WeatherContext


def detect_anomalies(sensor: SensorInput, weather: WeatherContext | None = None) -> dict:
    anomalies = []
    risk_score = 0

    # Temperature check
    if sensor.temperature < 2:
        anomalies.append("temperature_too_low")
        risk_score += 30
    elif sensor.temperature > 8:
        anomalies.append("temperature_too_high")
        risk_score += 30

    # Humidity check
    if sensor.humidity < 30:
        anomalies.append("humidity_too_low")
        risk_score += 15
    elif sensor.humidity > 75:
        anomalies.append("humidity_too_high")
        risk_score += 15

    # Door status check
    if sensor.door_open:
        anomalies.append("door_open")
        risk_score += 20

    # Battery check
    if sensor.battery < 20:
        anomalies.append("battery_low")
        risk_score += 20

    # Device online status check
    if sensor.device_online is False:
        anomalies.append("device_offline")
        risk_score += 30

    # Weather-aware contextual risk adjustments
    if weather is not None:
        # Hot outside weather increases high-temperature risk
        if sensor.temperature > 8 and weather.outside_temperature >= 25:
            anomalies.append("hot_weather_pressure")
            risk_score += 10

        # Cold outside weather increases low-temperature risk
        if sensor.temperature < 2 and weather.outside_temperature <= 5:
            anomalies.append("cold_weather_pressure")
            risk_score += 10

        # High outside humidity increases humidity risk
        if sensor.humidity > 75 and weather.outside_humidity >= 75:
            anomalies.append("humid_weather_pressure")
            risk_score += 10

    # Cap risk score at 100
    risk_score = min(risk_score, 100)

    # Risk level mapping
    if risk_score >= 60:
        risk_level = "high"
    elif risk_score >= 30:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "anomalies": anomalies,
        "risk_score": risk_score,
        "risk_level": risk_level
    }