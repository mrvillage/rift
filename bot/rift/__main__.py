from __future__ import annotations

import asyncio

from . import db
from .bot import bot


async def main() -> None:
    await db.create_pool()
    await db.create_notify_connection()
    await bot.run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
