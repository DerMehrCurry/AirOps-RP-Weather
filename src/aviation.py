from __future__ import annotations

from datetime import timedelta

from .models import AviationAssessment, FlightLevel, WeatherReport


def _weather_has_thunderstorm(code: int) -> bool:
    return code in {95, 96, 99}


def _level_for_conditions(
    *,
    visibility_m: int,
    gusts_kmh: float,
    wind_kmh: float,
    precipitation_mm: float,
    weather_code: int,
    cape: float = 0,
) -> FlightLevel:
    if (
        visibility_m < 1500
        or gusts_kmh >= 75
        or wind_kmh >= 55
        or precipitation_mm >= 7
        or _weather_has_thunderstorm(weather_code)
        or cape >= 1800
    ):
        return FlightLevel.RED

    if (
        visibility_m < 3000
        or gusts_kmh >= 55
        or wind_kmh >= 40
        or precipitation_mm >= 4
        or cape >= 1000
    ):
        return FlightLevel.ORANGE

    if (
        visibility_m < 7000
        or gusts_kmh >= 35
        or wind_kmh >= 25
        or precipitation_mm >= 1
        or cape >= 400
    ):
        return FlightLevel.YELLOW

    return FlightLevel.GREEN


def assess(report: WeatherReport) -> AviationAssessment:
    current = report.current
    current_level = _level_for_conditions(
        visibility_m=current.visibility,
        gusts_kmh=current.wind_gusts,
        wind_kmh=current.wind_speed,
        precipitation_mm=current.precipitation,
        weather_code=current.weather_code,
    )

    horizon_end = current.time + timedelta(minutes=60)
    future_window = [
        item for item in report.hourly
        if current.time < item.time <= horizon_end
    ]
    if not future_window and report.hourly:
        future_window = [report.hourly[0]]

    future_levels = [
        _level_for_conditions(
            visibility_m=item.visibility,
            gusts_kmh=item.wind_gusts,
            wind_kmh=item.wind_speed,
            precipitation_mm=item.precipitation,
            weather_code=item.weather_code,
            cape=item.cape,
        )
        for item in future_window
    ]
    worst_future = max(future_levels, default=current_level)

    reasons: list[str] = []

    if current.visibility < 3000:
        reasons.append(
            f"Deutlich eingeschränkte Sichtbedingungen bei etwa "
            f"{current.visibility / 1000:.1f} km Sichtweite."
        )
    elif current.visibility < 7000:
        reasons.append(
            f"Eingeschränkte Sichtbedingungen bei etwa "
            f"{current.visibility / 1000:.1f} km Sichtweite."
        )
    else:
        reasons.append(
            f"Gute Sichtbedingungen bei etwa "
            f"{current.visibility / 1000:.1f} km Sichtweite."
        )

    if current.wind_gusts >= 55:
        reasons.append(f"Hohe Windbelastung durch Böen bis {current.wind_gusts:.0f} km/h.")
    elif current.wind_gusts >= 35:
        reasons.append(f"Erhöhte Windbelastung durch Böen bis {current.wind_gusts:.0f} km/h.")
    else:
        reasons.append(f"Geringe Windbelastung mit Böen bis {current.wind_gusts:.0f} km/h.")

    if _weather_has_thunderstorm(current.weather_code):
        reasons.append("Aktuell besteht eine Gewitterlage.")
    elif current.precipitation >= 4:
        reasons.append("Starker Niederschlag beeinträchtigt die Wetterlage.")
    elif current.precipitation >= 1:
        reasons.append("Mäßiger Niederschlag kann den Flugbetrieb beeinflussen.")
    elif current.precipitation > 0:
        reasons.append("Leichter Niederschlag ohne wesentliche Intensität.")
    else:
        reasons.append("Kein relevanter Niederschlag im aktuellen Zeitraum.")

    anticipatory_warning = worst_future > current_level
    display_level = max(current_level, worst_future)

    if anticipatory_warning:
        trend_icon = "📉"
        trend_label = "Verschlechterung erwartet"
        outlook = (
            f"Innerhalb der nächsten 60 Minuten wird eine Verschlechterung auf "
            f"**{level_title(worst_future)}** erwartet. Der angezeigte Status wurde "
            f"vorsorglich angehoben."
        )
    elif worst_future < current_level:
        trend_icon = "📈"
        trend_label = "Verbesserung erwartet"
        outlook = (
            "Innerhalb der nächsten 60 Minuten zeichnet sich eine Verbesserung "
            "der Wetterlage ab."
        )
    else:
        trend_icon = "➡️"
        trend_label = "Stabile Entwicklung"
        outlook = (
            "In den nächsten 60 Minuten werden keine wesentlichen Änderungen "
            "der Wetterlage erwartet."
        )

    return AviationAssessment(
        level=display_level,
        current_level=current_level,
        title=level_title(display_level),
        reasons=reasons,
        outlook=outlook,
        trend_label=trend_label,
        trend_icon=trend_icon,
        anticipatory_warning=anticipatory_warning,
    )


def level_title(level: FlightLevel) -> str:
    return {
        FlightLevel.GREEN: "Günstige Flugbedingungen",
        FlightLevel.YELLOW: "Eingeschränkte Flugbedingungen",
        FlightLevel.ORANGE: "Anspruchsvolle Flugbedingungen",
        FlightLevel.RED: "Sehr ungünstige Flugbedingungen",
    }[level]
