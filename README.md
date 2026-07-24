# 🚁 AirOps RP Weather

An open-source Discord bot providing real-time aviation weather information for roleplay communities using data from Open-Meteo.

## Features

- Live weather powered by Open-Meteo
- Aviation-oriented flight-condition assessment
- Four status levels: green, yellow, orange and red
- Anticipatory assessment of the next 60 minutes
- Operational weather notes
- Six-hour forecast
- Sunrise and sunset
- Persistent Discord embed
- Automatic updates
- Railway deployment
- MIT License

## Requirements

- Python 3.13+
- Discord bot token
- Discord channel ID

## Installation

```bash
git clone https://github.com/DerMehrCurry/AirOps-RP-Weather.git
cd AirOps-RP-Weather
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example`.

## Local start

```bash
python main.py
```

## Railway deployment

Connect the GitHub repository to a Railway service and configure the required environment variables.

Use this start command:

```text
python3 main.py
```

A push to the connected branch can trigger a new Railway deployment.

## Flight-condition levels

| Status | Meaning |
|---|---|
| 🟢 | Günstige Flugbedingungen |
| 🟡 | Eingeschränkte Flugbedingungen |
| 🟠 | Anspruchsvolle Flugbedingungen |
| 🔴 | Sehr ungünstige Flugbedingungen |

The assessment is intended exclusively for roleplay and must not be used for real-world flight planning or operational decisions.

## Current version

**v1.2.1**

### Changes in v1.2.1

- More compact status presentation
- Written wind direction
- Separate gust display
- Clearer weather-development section
- Improved mobile forecast formatting
- Cleaner footer
- Documentation updated for Railway

## Planned

- v1.3.0: DWD weather warnings
- v1.4.0: Multiple locations
- v1.5.0: Slash commands

## License

This project is licensed under the MIT License.
