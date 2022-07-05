from __future__ import annotations

import asyncio

from src import cache
from src import commands as commands
from src import components as components
from src import db, tasks
from src.bot import bot


async def main() -> None:
    print("Connecting to database...", flush=True)
    await db.create_pool()
    await db.create_notify_connection()
    print("Initializing cache...", flush=True)
    await cache.initialize()
    bot.running_tasks = [
        tasks.PnWDataTask().start(),
        tasks.PnWSubscriptionsTask().start(),
    ]
    print("Connecting to Discord...", flush=True)
    await bot.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
