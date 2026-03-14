from app.services.weather_service import get_weather_context
from app.services.anomaly_service import detect_anomalies
from app.services.policy_service import generate_policy


def weather_tool(location):
    weather, city = get_weather_context(location)
    return weather, city


def anomaly_tool(sensor, weather):
    return detect_anomalies(sensor, weather)


def policy_tool(anomalies, risk_level):
    return generate_policy(anomalies, risk_level)
