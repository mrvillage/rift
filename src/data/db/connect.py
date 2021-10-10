from __future__ import annotations

import json
from asyncio import get_event_loop

from asyncpg import Connection, Pool, create_pool

from ...env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


async def init(conn: Connection) -> Connection:
    await conn.set_type_codec(  # type: ignore
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )
    return conn


async def _create_connection() -> Pool:
    return await create_pool(  # type: ignore
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        init=init,
    )


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
