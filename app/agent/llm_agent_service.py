import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from app.services.weather_service import get_weather_context
from app.services.anomaly_service import detect_anomalies
from app.services.policy_service import generate_policy


@tool
def weather_tool(location: str) -> str:
    """Get current external weather context for a warehouse location."""
    weather, city = get_weather_context(location)
    return (
        f"City: {city}, "
        f"Condition: {weather.weather_condition}, "
        f"Temperature: {weather.outside_temperature}°C, "
        f"Humidity: {weather.outside_humidity}%, "
        f"Wind Speed: {weather.wind_speed} km/h"
    )


@tool
def anomaly_tool(sensor_json: str) -> str:
    """Detect anomalies from structured sensor data JSON plus weather context."""
    import json
    from app.schema.sensor import SensorInput

    data = json.loads(sensor_json)
    sensor = SensorInput(**data)
    weather, city = get_weather_context(sensor.location)
    result = detect_anomalies(sensor, weather)
    return json.dumps(result)


@tool
def policy_tool(anomalies_json: str, risk_level: str) -> str:
    """Generate recommendation and action plan from anomalies and risk level."""
    import json
    anomalies = json.loads(anomalies_json)
    result = generate_policy(anomalies, risk_level)
    return json.dumps({
        "recommendation": result["recommendation"],
        "action": result["action"].model_dump(),
        "agent_explanation": result["agent_explanation"]
    })


def build_llm():
    model_name = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
    return ChatOpenAI(model=model_name, temperature=0)


def run_llm_agent(sensor):
    import json
    from langchain.agents import create_agent

    llm = build_llm()

    agent = create_agent(
        model=llm,
        tools=[weather_tool, anomaly_tool, policy_tool],
        system_prompt=(
            "You are an IoT monitoring decision agent. "
            "Use the provided tools to inspect weather, detect anomalies, and generate policy decisions. "
            "Return a concise, professional decision summary for operations engineers."
        )
    )

    sensor_payload = json.dumps(sensor.model_dump(), default=str)

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": (
                    "Analyze this IoT sensor reading and produce a final decision summary. "
                    f"Sensor data: {sensor_payload}"
                )
            }
        ]
    })

    return result
