from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SensorInput(BaseModel):
    device_id: str = Field(..., description="Unique ID of the IoT device")
    temperature: float = Field(..., description="Temperature reading in Celsius")
    humidity: float = Field(..., description="Humidity percentage")
    door_open: bool = Field(..., description="Whether the storage door is open")
    battery: int = Field(..., ge=0, le=100, description="Battery level percentage")
    timestamp: datetime = Field(..., description="Timestamp of the sensor reading")

    light_level: Optional[float] = Field(default=None, description="Optional light sensor reading")
    device_online: Optional[bool] = Field(default=True, description="Whether the device is online")
    location: Optional[str] = Field(default=None, description="Device location")