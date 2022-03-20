from __future__ import annotations

import asyncio

from rift import commands as commands
from rift import db
from rift.bot import bot
from rift.cache import cache


async def main() -> None:
    await db.create_pool()
    await db.create_notify_connection()
    await cache.initialize()
    await bot.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
