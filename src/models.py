from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum


class FlightLevel(IntEnum):
    GREEN = 0
    YELLOW = 1
    ORANGE = 2
    RED = 3


@dataclass(frozen=True, slots=True)
class CurrentWeather:
    time: datetime
    weather_code: int
    temperature: float
    apparent_temperature: float
    humidity: int
    precipitation: float
    cloud_cover: int
    wind_speed: float
    wind_direction: int
    wind_gusts: float
    visibility: int


@dataclass(frozen=True, slots=True)
class HourlyWeather:
    time: datetime
    weather_code: int
    temperature: float
    precipitation_probability: int
    precipitation: float
    cloud_cover: int
    wind_speed: float
    wind_gusts: float
    visibility: int
    cape: float


@dataclass(frozen=True, slots=True)
class WeatherReport:
    current: CurrentWeather
    hourly: list[HourlyWeather]
    sunrise: datetime
    sunset: datetime


@dataclass(frozen=True, slots=True)
class AviationAssessment:
    level: FlightLevel
    current_level: FlightLevel
    title: str
    reasons: list[str]
    outlook: str
    trend_label: str
    trend_icon: str
    anticipatory_warning: bool
