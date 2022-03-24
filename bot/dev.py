from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

load_dotenv("../.env")
os.environ["DB_PASSWORD"] = os.environ["POSTGRES_PASSWORD"]

from src import commands as commands  # noqa: E402
from src import db  # noqa: E402
from src.bot import bot  # noqa: E402
from src.cache import cache  # noqa: E402


async def main() -> None:
    await db.create_pool()
    await db.create_notify_connection()
    await cache.initialize()
    await bot.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
