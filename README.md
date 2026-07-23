# AirOps RP Weather

A lightweight Discord weather bot for aviation and air-rescue roleplay. It uses real Open-Meteo data, publishes one continuously updated Discord embed, and provides detailed weather-based flight-operation notes without making the pilot's decision.

> **Important:** AirOps RP Weather is intended for roleplay and simulation only. It is not an aviation weather service and must not be used for real flight planning or operational decisions.

## Features

- Real weather data from Open-Meteo
- One persistent Discord embed instead of repeated messages
- Updates at exact 10-minute clock marks
- Green, yellow, orange and red weather status
- Current temperature, wind, gusts, visibility, cloud cover and precipitation
- Detailed flight-operation notes
- 60-minute weather trend
- Configurable hourly forecast
- No Open-Meteo API key required
- Designed for simple hosting platforms such as Pella

## Quick start

### 1. Create a Discord application

1. Open the Discord Developer Portal.
2. Create a new application and add a bot.
3. Copy the bot token.
4. Invite the bot with these permissions:
   - View Channel
   - Send Messages
   - Embed Links
   - Read Message History

Do not publish or commit the bot token.

### 2. Configure environment variables

Copy `.env.example` to `.env` for local use:

```bash
cp .env.example .env
```

Set at least:

```env
DISCORD_TOKEN=your_token
DISCORD_CHANNEL_ID=your_numeric_channel_id
```

To obtain the channel ID, enable Discord Developer Mode and use **Copy Channel ID**.

### 3. Install and start

```bash
python -m pip install -r requirements.txt
python main.py
```

## Pella deployment

1. Create a Python server in Pella.
2. Select this GitHub repository as the code source.
3. Add the variables from `.env.example` in Pella's environment-variable or secrets section.
4. Use `main.py` as the start file if Pella asks for one.
5. Start the server and inspect the console log.

The bot updates immediately after connecting and then at `00`, `10`, `20`, `30`, `40` and `50` minutes by default.

## Configuration

| Variable | Required | Default | Description |
|---|---:|---|---|
| `DISCORD_TOKEN` | Yes | — | Discord bot token |
| `DISCORD_CHANNEL_ID` | Yes | — | Numeric target channel ID |
| `WEATHER_LOCATION_NAME` | No | `Lüneburg` | Displayed location |
| `WEATHER_LATITUDE` | No | `53.2464` | Weather latitude |
| `WEATHER_LONGITUDE` | No | `10.4115` | Weather longitude |
| `WEATHER_TIMEZONE` | No | `Europe/Berlin` | IANA timezone |
| `UPDATE_MINUTES` | No | `10` | Update interval; must divide 60 |
| `FORECAST_HOURS` | No | `6` | Hourly rows shown, 1–12 |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## Status logic

The colored status is an automated RP-oriented summary based on visibility, sustained wind, gusts, precipitation, thunderstorm weather codes and CAPE forecast data.

The included thresholds are deliberately conservative and are **not** official aviation minima. The detailed measurements remain visible so pilots can make their own RP decisions.

## Project status

This repository currently contains the initial functional beta. Thresholds, presentation and forecast logic will continue to be refined before the first stable release.

## License

MIT
