from __future__ import annotations

import json
from asyncio import get_event_loop
from pathlib import Path
from ssl import create_default_context

from asyncpg import Connection, Pool, create_pool, connect

from ...env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


async def init(conn: Connection) -> Connection:
    await conn.set_type_codec(
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )
    return conn


async def _create_connection() -> Pool:
    path = Path(__file__).parent.parent.parent.parent / "db.crt"
    return await create_pool(  # type: ignore
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl=create_default_context(cafile=path),
        init=init,
    )
    await conn.set_type_codec(
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )
    return conn


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
