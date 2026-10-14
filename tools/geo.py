
import requests


def geocode_location(location: str) -> dict:
    """Convert a location name into latitude and longitude."""

    if not location or not location.strip():
        raise ValueError("Location cannot be empty.")

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location.strip(),
        "format": "jsonv2",
        "limit": 1,
    }

    headers = {
        "User-Agent": "EnvironmentalImpactAssessmentAssistant/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15,
    )
    response.raise_for_status()

    results = response.json()

    if not results:
        raise ValueError(f"Location not found: {location}")

    result = results[0]

    return {
        "latitude": float(result["lat"]),
        "longitude": float(result["lon"]),
        "display_name": result["display_name"],
    }
