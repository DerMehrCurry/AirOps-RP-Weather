from __future__ import annotations

from datetime import datetime, timedelta

import discord

from .aviation import assess
from .config import Settings
from .models import FlightLevel, WeatherReport


COLORS = {
    FlightLevel.GREEN: 0x2ECC71,
    FlightLevel.YELLOW: 0xF1C40F,
    FlightLevel.ORANGE: 0xE67E22,
    FlightLevel.RED: 0xE74C3C,
}

STATUS_EMOJI = {
    FlightLevel.GREEN: "🟢",
    FlightLevel.YELLOW: "🟡",
    FlightLevel.ORANGE: "🟠",
    FlightLevel.RED: "🔴",
}


def wind_direction(degrees: int) -> str:
    directions = [
        "Nord", "Nordost", "Ost", "Südost",
        "Süd", "Südwest", "West", "Nordwest",
    ]
    return directions[round(degrees / 45) % 8]


def weather_emoji(code: int) -> str:
    if code == 0:
        return "☀️"
    if code in {1, 2}:
        return "🌤️"
    if code == 3:
        return "☁️"
    if code in {45, 48}:
        return "🌫️"
    if code in {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}:
        return "🌧️"
    if code in {71, 73, 75, 77, 85, 86}:
        return "🌨️"
    if code in {95, 96, 99}:
        return "⛈️"
    return "🌦️"


def build_embed(report: WeatherReport, settings: Settings, now: datetime) -> discord.Embed:
    current = report.current
    assessment = assess(report)
    status = STATUS_EMOJI[assessment.level]

    description_lines = [
        f"**{status} {assessment.title}**",
        f"📍 **{settings.location_name}**",
    ]
    if assessment.anticipatory_warning:
        description_lines.append(
            "⚠️ Der Status berücksichtigt bereits die erwartete Entwicklung "
            "der nächsten 60 Minuten."
        )

    embed = discord.Embed(
        title="🚁 Flug- und Wetterlage",
        description="\n".join(description_lines),
        color=COLORS[assessment.level],
        timestamp=now,
    )

    embed.add_field(
        name="🌡️ Aktuelle Wetterlage",
        value=(
            f"{weather_emoji(current.weather_code)} **{current.temperature:.1f} °C** "
            f"· gefühlt {current.apparent_temperature:.1f} °C\n"
            f"💨 **Wind aus {wind_direction(current.wind_direction)}** "
            f"mit {current.wind_speed:.0f} km/h\n"
            f"🌬️ **Böen bis {current.wind_gusts:.0f} km/h**\n"
            f"👁️ **{current.visibility / 1000:.1f} km** Sichtweite\n"
            f"☁️ **{current.cloud_cover} %** Bewölkung\n"
            f"🌧️ **{current.precipitation:.1f} mm** Niederschlag\n"
            f"💧 **{current.humidity} %** Luftfeuchtigkeit"
        ),
        inline=False,
    )

    embed.add_field(
        name="🚁 Flugbetriebliche Hinweise",
        value="\n".join(f"• {reason}" for reason in assessment.reasons),
        inline=False,
    )

    embed.add_field(
        name=f"{assessment.trend_icon} Wetterentwicklung",
        value=f"**{assessment.trend_label}**\n{assessment.outlook}",
        inline=False,
    )

    forecast_lines: list[str] = []
    for item in report.hourly[: settings.forecast_hours]:
        forecast_lines.append(
            f"**{item.time:%H:%M} Uhr** · {weather_emoji(item.weather_code)} "
            f"{item.temperature:.0f} °C\n"
            f"└ 🌧️ {item.precipitation_probability}% · "
            f"💨 {item.wind_speed:.0f} km/h · Böen {item.wind_gusts:.0f} km/h"
        )

    embed.add_field(
        name=f"🕒 Vorschau – nächste {len(forecast_lines)} Stunden",
        value="\n".join(forecast_lines) if forecast_lines else "Keine Prognosedaten verfügbar.",
        inline=False,
    )

    embed.add_field(
        name="🌅 Tageslicht",
        value=(
            f"Sonnenaufgang: **{report.sunrise:%H:%M} Uhr**\n"
            f"Sonnenuntergang: **{report.sunset:%H:%M} Uhr**"
        ),
        inline=False,
    )

    next_update = next_aligned_update(now, settings.update_minutes)
    embed.set_footer(
        text=(
            f"AirOps RP Weather · Aktualisiert {now:%d.%m.%Y, %H:%M} Uhr "
            f"· Nächste Aktualisierung {next_update:%H:%M} Uhr\n"
            "Automatisierte Wetterhinweise – die Einsatzentscheidung bleibt beim Piloten."
        )
    )
    return embed


def next_aligned_update(now: datetime, interval_minutes: int) -> datetime:
    next_minute = ((now.minute // interval_minutes) + 1) * interval_minutes
    if next_minute >= 60:
        return now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    return now.replace(minute=next_minute, second=0, microsecond=0)
