from __future__ import annotations

from asyncio import get_event_loop
from ssl import create_default_context
from pathlib import Path

from asyncpg import Pool, create_pool

from ...env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


async def _create_connection() -> Pool:
    path = Path(__file__).parent.parent.parent.parent / "db.crt"
    return await create_pool(  # type: ignore
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl=create_default_context(cafile=path),
    )


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
