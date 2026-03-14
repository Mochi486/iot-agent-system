from fastapi import FastAPI
from app.api.routes_health import router as health_router
from app.api.routes_sensor import router as sensor_router
from app.api.routes_decision import router as decision_router
from app.api.routes_logs import router as logs_router
from app.db.database import engine, Base
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IoT Agent System API",
    description="API service for IoT monitoring and AI-based decision making",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "IoT Agent System is running"
    }


app.include_router(health_router)
app.include_router(sensor_router)
app.include_router(decision_router)
app.include_router(logs_router)