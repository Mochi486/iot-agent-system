from fastapi import APIRouter
from app.schema.sensor import SensorInput

router = APIRouter(prefix="/sensor", tags=["Sensor"])


@router.post("/upload")
def upload_sensor_data(sensor: SensorInput):
    return {
        "message": "Sensor data received successfully",
        "data": sensor.model_dump()
    }