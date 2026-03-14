from app.schema.decision import ActionPlan


def generate_policy(anomalies: list[str], risk_level: str) -> dict:
    recommendations = []

    cooling_level = None
    send_alert = False
    maintenance_required = False

    # Temperature-related policies
    if "temperature_too_high" in anomalies:
        recommendations.append("Increase cooling level and inspect cooling equipment")
        cooling_level = "increase"

    if "temperature_too_low" in anomalies:
        recommendations.append("Reduce cooling intensity and inspect thermostat settings")
        cooling_level = "decrease"

    # Humidity-related policies
    if "humidity_too_high" in anomalies:
        recommendations.append("Inspect humidity control and ventilation conditions")

    if "humidity_too_low" in anomalies:
        recommendations.append("Review humidity regulation settings")

    # Door-related policies
    if "door_open" in anomalies:
        recommendations.append("Close the storage door and inspect the door seal")
        send_alert = True

    # Battery-related policies
    if "battery_low" in anomalies:
        recommendations.append("Schedule battery replacement and inspect power supply")
        maintenance_required = True

    # Device status policies
    if "device_offline" in anomalies:
        recommendations.append("Check network connection and escalate to maintenance")
        send_alert = True
        maintenance_required = True

    # Weather-context policies
    if "hot_weather_pressure" in anomalies:
        recommendations.append("Consider increased cooling load due to hot external weather")
        send_alert = True

    if "cold_weather_pressure" in anomalies:
        recommendations.append("Check insulation and temperature control against cold external weather")

    if "humid_weather_pressure" in anomalies:
        recommendations.append("Review moisture protection under high external humidity conditions")

    # Additional escalation for higher risks
    if risk_level == "high":
        send_alert = True

    # Fallback recommendation
    if not recommendations:
        recommendation_text = "System operating normally."
    else:
        recommendation_lines = ["Recommended actions:"]
        for item in recommendations:
            recommendation_lines.append(f"- {item}")
        recommendation_text = "\n".join(recommendation_lines)

    action = ActionPlan(
        cooling_level=cooling_level,
        send_alert=send_alert,
        maintenance_required=maintenance_required
    )

    # Explanation text
    if risk_level == "low":
        agent_explanation = "The system is operating within acceptable conditions."
    elif risk_level == "medium":
        agent_explanation = "Some abnormal conditions were detected and should be monitored or inspected."
    else:
        agent_explanation = "Multiple critical anomalies were detected, requiring immediate attention."

    return {
        "recommendation": recommendation_text,
        "action": action,
        "agent_explanation": agent_explanation
    }