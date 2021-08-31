from __future__ import annotations

from asyncio import get_event_loop
from ssl import create_default_context
from pathlib import Path

from asyncpg import Pool, create_pool

from ...env import DBHOST, DBNAME, DBPASSWORD, DBPORT, DBUSER


async def _create_connection() -> Pool:
    path = Path(__file__).parent.parent.parent.parent / "db.crt"
    return await create_pool(  # type: ignore
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPASSWORD,
        database=DBNAME,
        ssl=create_default_context(cafile=path),
    )


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
