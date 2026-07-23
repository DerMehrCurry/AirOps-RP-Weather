# 🚁 AirOps RP Weather

An open-source Discord bot providing real-time aviation weather information for roleplay communities using data from Open-Meteo.

---

## ✨ Features

- 🌤️ Live weather powered by Open-Meteo
- 🚁 Flight condition assessment
- 🟢🟡🟠🔴 Flight condition levels
- 📈 Weather trend analysis
- 🌅 Sunrise & Sunset
- 💨 Wind, gusts and visibility
- 🌧️ Precipitation information
- 🕒 Hourly forecast
- ♻️ Persistent Discord embed (message editing)
- 🔄 Automatic updates every 10 minutes
- 🔓 Open Source (MIT License)

---

## Screenshot

*A screenshot will be added here.*

---

## Requirements

- Python 3.13+
- Discord Bot
- Railway (recommended)

---

## Installation

```bash
git clone https://github.com/DerMehrCurry/AirOps-RP-Weather.git
cd AirOps-RP-Weather
pip install -r requirements.txt
```

Create a `.env` file:

```env
DISCORD_TOKEN=YOUR_TOKEN
DISCORD_CHANNEL_ID=YOUR_CHANNEL_ID

WEATHER_LOCATION_NAME=Lüneburg
WEATHER_LATITUDE=53.2464
WEATHER_LONGITUDE=10.4115
WEATHER_TIMEZONE=Europe/Berlin

UPDATE_MINUTES=10
FORECAST_HOURS=6
LOG_LEVEL=INFO
```

## Running locally

```bash
python main.py
```

## Railway

Start Command:

```text
python3 main.py
```

Every push to the `main` branch triggers an automatic deployment.

## Flight Condition Levels

| Status | Meaning |
|--------|---------|
| 🟢 | Good flight conditions |
| 🟡 | Restricted flight conditions |
| 🟠 | Challenging flight conditions |
| 🔴 | Very unfavorable flight conditions |

> This assessment is intended for aviation roleplay only.

## Current Version

**v1.2.0**

## Roadmap

- v1.3 – DWD weather warnings
- v1.4 – Multiple locations
- v1.5 – Slash Commands

## License

MIT License
