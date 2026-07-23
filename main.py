import asyncio
import logging
import os
import sys

import discord
from dotenv import load_dotenv

from src.bot import AirOpsWeatherBot


def configure_logging() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main() -> None:
    load_dotenv()
    configure_logging()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logging.critical("DISCORD_TOKEN is not configured.")
        sys.exit(1)

    bot = AirOpsWeatherBot()
    asyncio.run(bot.start(token))


if __name__ == "__main__":
    main()
