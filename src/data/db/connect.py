from __future__ import annotations

import json
from asyncio import get_event_loop

from asyncpg import Connection, Pool, connect, create_pool

from ...env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from .notify import listeners


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


async def _create_notify_connection() -> Connection:
    conn: Connection = await connect(  # type: ignore
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    await init(conn)
    for channel, callback in listeners.items():
        await conn.add_listener(channel, callback)  # type: ignore
    return conn


loop = get_event_loop()
connection = loop.run_until_complete(_create_connection())
notify_connection = loop.run_until_complete(_create_notify_connection())
