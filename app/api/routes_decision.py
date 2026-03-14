from fastapi import APIRouter
from app.schema.sensor import SensorInput
from app.schema.decision import DecisionOutput
from app.agent.agent_controller import run_agent
from app.services.logging_service import save_sensor_record, save_decision_record

router = APIRouter(prefix="/decision", tags=["Decision"])


@router.post("/make", response_model=DecisionOutput)
def make_decision(sensor: SensorInput):
    weather, city, anomaly_result, policy_result, explanation, llm_result = run_agent(sensor)

    final_explanation = explanation

    try:
        if isinstance(llm_result, dict) and "messages" in llm_result:
            messages = llm_result["messages"]
            if messages:
                final_explanation = explanation + " LLM summary: " + messages[-1].content
    except Exception:
        pass

    decision = DecisionOutput(
        device_id=sensor.device_id,
        risk_score=anomaly_result["risk_score"],
        risk_level=anomaly_result["risk_level"],
        anomalies=anomaly_result["anomalies"],
        recommendation=policy_result["recommendation"],
        action=policy_result["action"],
        agent_explanation=final_explanation
    )

    save_sensor_record(sensor)
    save_decision_record(decision)

    return decision
