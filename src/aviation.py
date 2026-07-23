from __future__ import annotations

from .models import AviationAssessment, FlightLevel, HourlyWeather, WeatherReport


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
    # Intentionally conservative RP thresholds. They are not aviation minima.
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

    future = report.hourly[:2]
    future_levels = [
        _level_for_conditions(
            visibility_m=item.visibility,
            gusts_kmh=item.wind_gusts,
            wind_kmh=item.wind_speed,
            precipitation_mm=item.precipitation,
            weather_code=item.weather_code,
            cape=item.cape,
        )
        for item in future
    ]
    worst_future = max(future_levels, default=current_level)

    reasons: list[str] = []

    if current.visibility < 3000:
        reasons.append(f"Die Sichtweite ist mit etwa {current.visibility / 1000:.1f} km deutlich eingeschränkt.")
    elif current.visibility < 7000:
        reasons.append(f"Die Sichtweite ist mit etwa {current.visibility / 1000:.1f} km eingeschränkt.")
    else:
        reasons.append(f"Die Sichtweite liegt bei etwa {current.visibility / 1000:.1f} km.")

    if current.wind_gusts >= 55:
        reasons.append(f"Es treten kräftige Windböen bis {current.wind_gusts:.0f} km/h auf.")
    elif current.wind_gusts >= 35:
        reasons.append(f"Windböen bis {current.wind_gusts:.0f} km/h können den Flugbetrieb beeinflussen.")
    else:
        reasons.append(f"Die Windbelastung ist mit Böen bis {current.wind_gusts:.0f} km/h gering.")

    if _weather_has_thunderstorm(current.weather_code):
        reasons.append("Aktuell besteht eine Gewitterlage.")
    elif current.precipitation >= 4:
        reasons.append("Aktuell fällt starker Niederschlag.")
    elif current.precipitation >= 1:
        reasons.append("Aktuell fällt mäßiger Niederschlag.")
    elif current.precipitation > 0:
        reasons.append("Aktuell fällt leichter Niederschlag.")
    else:
        reasons.append("Aktuell fällt kein relevanter Niederschlag.")

    if worst_future > current_level:
        trend_icon = "📉"
        trend_label = "Verschlechterung"
        minutes = 60 if len(future_levels) > 1 and future_levels[1] == worst_future else 30
        outlook = (
            f"Innerhalb der nächsten {minutes} Minuten wird eine Verschlechterung "
            f"auf **{level_title(worst_future)}** erwartet."
        )
    elif worst_future < current_level:
        trend_icon = "📈"
        trend_label = "Verbesserung"
        outlook = "Innerhalb der nächsten 60 Minuten zeichnet sich eine Verbesserung der Wetterlage ab."
    else:
        trend_icon = "➡️"
        trend_label = "Stabil"
        outlook = "In den nächsten 60 Minuten werden keine wesentlichen Änderungen erwartet."

    return AviationAssessment(
        level=current_level,
        title=level_title(current_level),
        reasons=reasons,
        outlook=outlook,
        trend_label=trend_label,
        trend_icon=trend_icon,
    )


def level_title(level: FlightLevel) -> str:
    return {
        FlightLevel.GREEN: "Günstige Flugbedingungen",
        FlightLevel.YELLOW: "Eingeschränkte Flugbedingungen",
        FlightLevel.ORANGE: "Anspruchsvolle Flugbedingungen",
        FlightLevel.RED: "Sehr ungünstige Flugbedingungen",
    }[level]
