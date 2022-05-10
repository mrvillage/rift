from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv  # type: ignore

load_dotenv(".env")
load_dotenv(".env.dev")
os.environ["DB_PASSWORD"] = os.environ["POSTGRES_PASSWORD"]

from src import cache  # noqa: E402
from src import db  # noqa: E402
from src import commands as commands  # noqa: E402
from src import components as components  # noqa: E402
from src.bot import bot  # noqa: E402


async def main() -> None:
    print("Connecting to database...", flush=True)
    await db.create_pool()
    await db.create_notify_connection()
    print("Initializing cache...", flush=True)
    await cache.initialize()
    # bot.running_tasks = [tasks.PnWDataTask().start()]
    print("Connecting to Discord...", flush=True)
    await bot.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
