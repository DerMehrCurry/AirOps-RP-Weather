from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import aiohttp
import discord

from .config import Settings
from .embed import build_embed
from .weather import WeatherClient


LOGGER = logging.getLogger("airops")


class AirOpsWeatherBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        super().__init__(intents=intents)

        self.settings = Settings.from_env()
        self.http_session: aiohttp.ClientSession | None = None
        self.weather_task: asyncio.Task[None] | None = None

    async def setup_hook(self) -> None:
        self.http_session = aiohttp.ClientSession(
            headers={"User-Agent": "AirOps-RP-Weather/0.1"}
        )

    async def on_ready(self) -> None:
        LOGGER.info("Logged in as %s (%s)", self.user, self.user.id if self.user else "unknown")

        if self.weather_task is None or self.weather_task.done():
            self.weather_task = asyncio.create_task(self.weather_loop())

    async def close(self) -> None:
        if self.weather_task:
            self.weather_task.cancel()
        if self.http_session:
            await self.http_session.close()
        await super().close()

    async def weather_loop(self) -> None:
        await self.wait_until_ready()

        while not self.is_closed():
            try:
                await self.update_weather_message()
            except asyncio.CancelledError:
                raise
            except Exception:
                LOGGER.exception("Weather update failed.")

            await asyncio.sleep(self.seconds_until_next_mark())

    async def update_weather_message(self) -> None:
        if not self.http_session:
            raise RuntimeError("HTTP session has not been initialized.")

        channel = self.get_channel(self.settings.channel_id)
        if channel is None:
            channel = await self.fetch_channel(self.settings.channel_id)

        if not isinstance(channel, discord.TextChannel):
            raise TypeError("DISCORD_CHANNEL_ID does not reference a text channel.")

        weather = await WeatherClient(self.http_session, self.settings).fetch()
        now = datetime.now(ZoneInfo(self.settings.timezone))
        embed = build_embed(weather, self.settings, now)

        message = await self.find_existing_message(channel)
        if message:
            await message.edit(content=None, embed=embed)
            LOGGER.info("Weather message updated.")
        else:
            await channel.send(embed=embed)
            LOGGER.info("New weather message created.")

    async def find_existing_message(
        self, channel: discord.TextChannel
    ) -> discord.Message | None:
        if not self.user:
            return None

        async for message in channel.history(limit=50):
            if message.author.id != self.user.id or not message.embeds:
                continue
            if message.embeds[0].title == "🚁 Flug- und Wetterlage":
                return message
        return None

    def seconds_until_next_mark(self) -> float:
        now = datetime.now(ZoneInfo(self.settings.timezone))
        minute = ((now.minute // self.settings.update_minutes) + 1) * self.settings.update_minutes

        if minute >= 60:
            target = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            target = now.replace(minute=minute, second=0, microsecond=0)

        return max((target - now).total_seconds(), 1.0)
