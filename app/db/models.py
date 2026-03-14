from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from app.db.database import Base
from datetime import datetime


class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    door_open = Column(Boolean, nullable=False)
    battery = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    light_level = Column(Float, nullable=True)
    device_online = Column(Boolean, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DecisionRecord(Base):
    __tablename__ = "decision_records"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    anomalies = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    cooling_level = Column(String, nullable=True)
    send_alert = Column(Boolean, nullable=False, default=False)
    maintenance_required = Column(Boolean, nullable=False, default=False)
    agent_explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)