from pydantic import BaseModel, Field
from typing import Optional


class WeatherContext(BaseModel):
    outside_temperature: float = Field(..., description="Outside temperature in Celsius")
    outside_humidity: float = Field(..., description="Outside humidity percentage")
    weather_condition: str = Field(..., description="Weather condition such as sunny, rainy, cloudy")
    wind_speed: Optional[float] = Field(default=None, description="Wind speed in km/h")