import time
import requests
from app.schema.weather import WeatherContext
from app.config import settings

LOCATION_COORDINATES = {
    "Warehouse A": {
        "city": "London",
        "latitude": 51.5074,
        "longitude": -0.1278
    },
    "Warehouse B": {
        "city": "Manchester",
        "latitude": 53.4808,
        "longitude": -2.2426
    },
    "Warehouse C": {
        "city": "Birmingham",
        "latitude": 52.4862,
        "longitude": -1.8904
    },
    "Warehouse D": {
        "city": "Glasgow",
        "latitude": 55.8642,
        "longitude": -4.2518
    }
}

FALLBACK_WEATHER = WeatherContext(
    outside_temperature=settings.FALLBACK_TEMPERATURE,
    outside_humidity=settings.FALLBACK_HUMIDITY,
    weather_condition=settings.FALLBACK_WEATHER_CONDITION,
    wind_speed=settings.FALLBACK_WIND_SPEED
)

WEATHER_CACHE = {}
CACHE_TTL_SECONDS = settings.WEATHER_CACHE_TTL


def weather_code_to_text(code: int) -> str:
    if code == 0:
        return "clear"
    elif code in [1, 2, 3]:
        return "cloudy"
    elif code in [45, 48]:
        return "fog"
    elif code in [51, 53, 55, 56, 57]:
        return "drizzle"
    elif code in [61, 63, 65, 66, 67]:
        return "rain"
    elif code in [71, 73, 75, 77]:
        return "snow"
    elif code in [80, 81, 82]:
        return "rain showers"
    elif code in [95, 96, 99]:
        return "thunderstorm"
    else:
        return "unknown"


def get_weather_context(location: str | None) -> tuple[WeatherContext, str]:
    coords = LOCATION_COORDINATES.get(location)

    if not coords:
        print(f"[Weather] Unknown location: {location}, using fallback weather.")
        return FALLBACK_WEATHER, "Unknown"

    city = coords["city"]
    latitude = coords["latitude"]
    longitude = coords["longitude"]

    cache_key = city
    now = time.time()

    if cache_key in WEATHER_CACHE:
        cached_item = WEATHER_CACHE[cache_key]
        if now - cached_item["timestamp"] < CACHE_TTL_SECONDS:
            print(f"[Weather] Using cached weather for {city}")
            return cached_item["weather"], city

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params, timeout=settings.WEATHER_API_TIMEOUT)
        response.raise_for_status()

        data = response.json()

        print(f"[Weather] API response for {city}: {data}")

        current = data.get("current", {})

        weather = WeatherContext(
            outside_temperature=current.get("temperature_2m", settings.FALLBACK_TEMPERATURE),
            outside_humidity=current.get("relative_humidity_2m", settings.FALLBACK_HUMIDITY),
            weather_condition=weather_code_to_text(current.get("weather_code", -1)),
            wind_speed=current.get("wind_speed_10m", settings.FALLBACK_WIND_SPEED)
        )

        WEATHER_CACHE[cache_key] = {
            "weather": weather,
            "timestamp": now
        }

        return weather, city

    except requests.RequestException as e:
        print(f"[Weather] Weather API error for {city}: {e}")
        return FALLBACK_WEATHER, city
