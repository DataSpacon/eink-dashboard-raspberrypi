from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode
import json


LATITUDE = 53.376679649292235
LONGITUDE = -2.272413040317866

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def weather_code_to_condition(code):
    """Convert Open-Meteo WMO weather code to a readable condition."""

    conditions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Rime fog",

        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",

        56: "Freezing drizzle",
        57: "Heavy freezing drizzle",

        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",

        66: "Freezing rain",
        67: "Heavy freezing rain",

        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        77: "Snow grains",

        80: "Light showers",
        81: "Showers",
        82: "Heavy showers",

        85: "Light snow showers",
        86: "Heavy snow showers",

        95: "Thunderstorm",
        96: "Thunderstorm + hail",
        99: "Thunderstorm + heavy hail",
    }

    return conditions.get(code, "Unknown")


def get_weather(hours=10):
    """Return real hourly weather data from Open-Meteo."""

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": ",".join([
            "temperature_2m",
            "precipitation_probability",
            "weather_code",
        ]),
        "daily": "sunrise,sunset",
        "forecast_days": 2,
        "timezone": "auto",
    }

    url = OPEN_METEO_URL + "?" + urlencode(params)

    with urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode("utf-8"))

    hourly = data["hourly"]
    daily = data["daily"]

    # Build a lookup of sunrise/sunset for each date.
    sun_times = {}

    for i, date_string in enumerate(daily["time"]):
        sunrise = datetime.fromisoformat(
            daily["sunrise"][i]
        )

        sunset = datetime.fromisoformat(
            daily["sunset"][i]
        )

        sun_times[date_string] = {
            "sunrise": sunrise.strftime("%H:%M"),
            "sunset": sunset.strftime("%H:%M"),
        }

    now = datetime.now()

    weather = []

    for i, timestamp in enumerate(hourly["time"]):

        current = datetime.fromisoformat(timestamp)

        # Ignore hours that have already passed.
        if current < now.replace(
            minute=0,
            second=0,
            microsecond=0
        ):
            continue

        date_string = current.strftime("%Y-%m-%d")

        sun = sun_times.get(date_string, {
            "sunrise": "",
            "sunset": "",
        })

        weather.append({
            "time": current.strftime("%H:%M"),
            "sunrise": sun["sunrise"],
            "sunset": sun["sunset"],
            "rain_probability": hourly["precipitation_probability"][i],
            "condition": weather_code_to_condition(
                hourly["weather_code"][i]
            ),
            "temperature": hourly["temperature_2m"][i],
        })

        if len(weather) >= hours:
            break

    return weather


if __name__ == "__main__":
    for item in get_weather():
        print(item)