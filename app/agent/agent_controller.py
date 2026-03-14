from app.agent.tools import weather_tool, anomaly_tool, policy_tool
from app.agent.reasoning import agent_reasoning
from app.agent.llm_agent_service import run_llm_agent


def run_agent(sensor):
    weather, city = weather_tool(sensor.location)
    anomaly_result = anomaly_tool(sensor, weather)
    policy_result = policy_tool(
        anomaly_result["anomalies"],
        anomaly_result["risk_level"]
    )

    explanation = agent_reasoning(
        sensor=sensor,
        weather=weather,
        city=city,
        anomaly_result=anomaly_result,
        policy_result=policy_result
    )

    llm_result = None
    try:
        llm_result = run_llm_agent(sensor)
    except Exception as e:
        llm_result = {"error": str(e)}

    return weather, city, anomaly_result, policy_result, explanation, llm_result
