from __future__ import annotations

import asyncio

from src import cache
from src import commands as commands
from src import db, tasks
from src.bot import bot


async def main() -> None:
    await db.create_pool()
    await db.create_notify_connection()
    await cache.initialize()
    bot.running_tasks = [tasks.PnWDataTask().start()]
    await bot.run()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
