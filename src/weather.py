from __future__ import annotations

from datetime import datetime
from typing import Any

import aiohttp

from .config import Settings
from .models import CurrentWeather, HourlyWeather, WeatherReport


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherClient:
    def __init__(self, session: aiohttp.ClientSession, settings: Settings) -> None:
        self.session = session
        self.settings = settings

    async def fetch(self) -> WeatherReport:
        params = {
            "latitude": self.settings.latitude,
            "longitude": self.settings.longitude,
            "timezone": self.settings.timezone,
            "forecast_days": 2,
            "current": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "apparent_temperature",
                    "precipitation",
                    "weather_code",
                    "cloud_cover",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "wind_gusts_10m",
                    "visibility",
                ]
            ),
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "precipitation_probability",
                    "precipitation",
                    "weather_code",
                    "cloud_cover",
                    "visibility",
                    "wind_speed_10m",
                    "wind_gusts_10m",
                    "cape",
                ]
            ),
            "daily": "sunrise,sunset",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
        }

        timeout = aiohttp.ClientTimeout(total=20)
        async with self.session.get(OPEN_METEO_URL, params=params, timeout=timeout) as response:
            response.raise_for_status()
            data: dict[str, Any] = await response.json()

        return self._parse(data)

    def _parse(self, data: dict[str, Any]) -> WeatherReport:
        current_data = data["current"]
        current = CurrentWeather(
            time=datetime.fromisoformat(current_data["time"]),
            weather_code=int(current_data["weather_code"]),
            temperature=float(current_data["temperature_2m"]),
            apparent_temperature=float(current_data["apparent_temperature"]),
            humidity=int(current_data["relative_humidity_2m"]),
            precipitation=float(current_data["precipitation"]),
            cloud_cover=int(current_data["cloud_cover"]),
            wind_speed=float(current_data["wind_speed_10m"]),
            wind_direction=int(current_data["wind_direction_10m"]),
            wind_gusts=float(current_data["wind_gusts_10m"]),
            visibility=int(current_data["visibility"]),
        )

        hourly_data = data["hourly"]
        times = [datetime.fromisoformat(value) for value in hourly_data["time"]]

        future_rows: list[HourlyWeather] = []
        for index, time in enumerate(times):
            if time < current.time:
                continue
            future_rows.append(
                HourlyWeather(
                    time=time,
                    weather_code=int(hourly_data["weather_code"][index]),
                    temperature=float(hourly_data["temperature_2m"][index]),
                    precipitation_probability=int(
                        hourly_data["precipitation_probability"][index] or 0
                    ),
                    precipitation=float(hourly_data["precipitation"][index] or 0),
                    cloud_cover=int(hourly_data["cloud_cover"][index] or 0),
                    wind_speed=float(hourly_data["wind_speed_10m"][index] or 0),
                    wind_gusts=float(hourly_data["wind_gusts_10m"][index] or 0),
                    visibility=int(hourly_data["visibility"][index] or 0),
                    cape=float(hourly_data["cape"][index] or 0),
                )
            )

        daily = data["daily"]
        return WeatherReport(
            current=current,
            hourly=future_rows,
            sunrise=datetime.fromisoformat(daily["sunrise"][0]),
            sunset=datetime.fromisoformat(daily["sunset"][0]),
        )
