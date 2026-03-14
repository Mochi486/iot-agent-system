def agent_reasoning(sensor, weather, anomaly_result, policy_result):

    explanation = policy_result["agent_explanation"]

    weather_note = (
        f" External weather context: "
        f"{weather.weather_condition}, "
        f"{weather.outside_temperature}°C, "
        f"humidity {weather.outside_humidity}%."
    )

    return explanation + weather_note
