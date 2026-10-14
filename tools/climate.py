
import requests


def get_climate_data(latitude: float, longitude: float) -> dict:
    """Retrieve current weather and available air-quality indicators."""

    headers = {
        "User-Agent": "EnvironmentalImpactAssessmentAssistant/1.0"
    }

    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,"
                       "precipitation,wind_speed_10m",
            "timezone": "auto",
        },
        headers=headers,
        timeout=20,
    )
    weather_response.raise_for_status()
    weather = weather_response.json()

    air_response = requests.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "pm10,pm2_5,nitrogen_dioxide,"
                       "ozone,us_aqi",
            "timezone": "auto",
        },
        headers=headers,
        timeout=20,
    )
    air_response.raise_for_status()
    air_quality = air_response.json()

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "weather": weather.get("current", {}),
        "weather_units": weather.get("current_units", {}),
        "air_quality": air_quality.get("current", {}),
        "air_quality_units": air_quality.get("current_units", {}),
        "retrieved_at": weather.get("current", {}).get("time"),
    }
