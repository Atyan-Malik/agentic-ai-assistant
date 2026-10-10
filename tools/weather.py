
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city: str, forecast_days: int = 1) -> dict:
    """Get current weather and a daily forecast for a city."""

    if not isinstance(city, str) or not city.strip():
        return {
            "success": False,
            "error": "A city name is required.",
        }

    if (
        not isinstance(forecast_days, int)
        or isinstance(forecast_days, bool)
        or not 1 <= forecast_days <= 7
    ):
        return {
            "success": False,
            "error": "forecast_days must be an integer from 1 to 7.",
        }

    try:
        geo_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city.strip(),
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=15,
        )
        geo_response.raise_for_status()

        locations = geo_response.json().get("results", [])

        if not locations:
            return {
                "success": False,
                "error": f"Could not find the location: {city}",
            }

        location = locations[0]

        weather_response = requests.get(
            FORECAST_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "is_day,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_probability_max"
                ),
                "forecast_days": forecast_days,
                "timezone": "auto",
            },
            timeout=20,
        )
        weather_response.raise_for_status()

        data = weather_response.json()

        return {
            "success": True,
            "location": {
                "name": location.get("name", city),
                "country": location.get("country", ""),
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "timezone": data.get("timezone"),
            },
            "current": data.get("current", {}),
            "daily": data.get("daily", {}),
            "units": {
                "temperature": (
                    data.get("current_units", {}).get("temperature_2m")
                ),
                "wind_speed": (
                    data.get("current_units", {}).get("wind_speed_10m")
                ),
                "precipitation": (
                    data.get("current_units", {}).get("precipitation")
                ),
            },
            "source": "Open-Meteo",
        }

    except requests.RequestException as exc:
        return {
            "success": False,
            "error": f"Weather service request failed: {exc}",
        }

    except (KeyError, TypeError, ValueError) as exc:
        return {
            "success": False,
            "error": f"Could not process weather data: {exc}",
        }
