import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./iot_agent.db")
    WEATHER_API_TIMEOUT: int = int(os.getenv("WEATHER_API_TIMEOUT", 10))
    WEATHER_CACHE_TTL: int = int(os.getenv("WEATHER_CACHE_TTL", 300))

    FALLBACK_TEMPERATURE: float = float(os.getenv("FALLBACK_TEMPERATURE", 18.0))
    FALLBACK_HUMIDITY: float = float(os.getenv("FALLBACK_HUMIDITY", 60.0))
    FALLBACK_WEATHER_CONDITION: str = os.getenv("FALLBACK_WEATHER_CONDITION", "mild")
    FALLBACK_WIND_SPEED: float = float(os.getenv("FALLBACK_WIND_SPEED", 7.0))


settings = Settings()
