from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    channel_id: int
    latitude: float
    longitude: float
    location_name: str
    timezone: str
    update_minutes: int
    forecast_hours: int

    @classmethod
    def from_env(cls) -> "Settings":
        channel_id_raw = os.getenv("DISCORD_CHANNEL_ID", "").strip()
        if not channel_id_raw.isdigit():
            raise ValueError("DISCORD_CHANNEL_ID must contain a numeric Discord channel ID.")

        update_minutes = int(os.getenv("UPDATE_MINUTES", "10"))
        if update_minutes <= 0 or 60 % update_minutes != 0:
            raise ValueError("UPDATE_MINUTES must be a positive divisor of 60, e.g. 5, 10, 15 or 30.")

        forecast_hours = int(os.getenv("FORECAST_HOURS", "6"))
        if not 1 <= forecast_hours <= 12:
            raise ValueError("FORECAST_HOURS must be between 1 and 12.")

        return cls(
            channel_id=int(channel_id_raw),
            latitude=float(os.getenv("WEATHER_LATITUDE", "53.2464")),
            longitude=float(os.getenv("WEATHER_LONGITUDE", "10.4115")),
            location_name=os.getenv("WEATHER_LOCATION_NAME", "Lüneburg").strip() or "Lüneburg",
            timezone=os.getenv("WEATHER_TIMEZONE", "Europe/Berlin").strip() or "Europe/Berlin",
            update_minutes=update_minutes,
            forecast_hours=forecast_hours,
        )
