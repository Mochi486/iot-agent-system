import json
from app.db.database import SessionLocal
from app.db.models import SensorRecord, DecisionRecord
from app.schema.sensor import SensorInput
from app.schema.decision import DecisionOutput


def save_sensor_record(sensor: SensorInput) -> None:
    db = SessionLocal()
    try:
        record = SensorRecord(
            device_id=sensor.device_id,
            temperature=sensor.temperature,
            humidity=sensor.humidity,
            door_open=sensor.door_open,
            battery=sensor.battery,
            timestamp=sensor.timestamp,
            light_level=sensor.light_level,
            device_online=sensor.device_online,
            location=sensor.location
        )
        db.add(record)
        db.commit()
    finally:
        db.close()


def save_decision_record(decision: DecisionOutput) -> None:
    db = SessionLocal()
    try:
        record = DecisionRecord(
            device_id=decision.device_id,
            risk_score=decision.risk_score,
            risk_level=decision.risk_level,
            anomalies=json.dumps(decision.anomalies),
            recommendation=decision.recommendation,
            cooling_level=decision.action.cooling_level,
            send_alert=decision.action.send_alert,
            maintenance_required=decision.action.maintenance_required,
            agent_explanation=decision.agent_explanation
        )
        db.add(record)
        db.commit()
    finally:
        db.close()


def get_recent_decisions(limit: int = 10) -> list[dict]:
    db = SessionLocal()
    try:
        records = (
            db.query(DecisionRecord)
            .order_by(DecisionRecord.created_at.desc())
            .limit(limit)
            .all()
        )

        results = []
        for record in records:
            results.append({
                "id": record.id,
                "device_id": record.device_id,
                "risk_score": record.risk_score,
                "risk_level": record.risk_level,
                "anomalies": json.loads(record.anomalies),
                "recommendation": record.recommendation,
                "cooling_level": record.cooling_level,
                "send_alert": record.send_alert,
                "maintenance_required": record.maintenance_required,
                "agent_explanation": record.agent_explanation,
                "created_at": record.created_at.isoformat() if record.created_at else None
            })

        return results
    finally:
        db.close()