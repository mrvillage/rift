from __future__ import annotations

import json
from typing import TYPE_CHECKING

import asyncpg

from .bot import bot
from .env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

__all__ = ("query",)

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from asyncpg import Connection, Pool


async def init(conn: Connection) -> Connection:
    await conn.set_type_codec(  # type: ignore
        "json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
    )
    return conn


async def create_pool() -> Pool:
    global POOL
    POOL = await asyncpg.create_pool(  # type: ignore
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        init=init,
    )
    return POOL


async def create_notify_connection() -> Connection:
    global NOTIFY_CONNECTION
    NOTIFY_CONNECTION = await asyncpg.connect(  # type: ignore
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    await init(NOTIFY_CONNECTION)
    for channel, callback in LISTENERS.items():
        await NOTIFY_CONNECTION.add_listener(channel, callback)  # type: ignore
    return NOTIFY_CONNECTION


async def query(query: str, *args: Any) -> Any:
    # type is partially unknown
    return await POOL.fetch(query, *args)  # type: ignore


def standard_dispatch(conn: Connection, pid: int, channel: str, payload: str) -> None:
    bot.dispatch(channel, json.loads(payload))


LISTENERS: dict[str, Callable[[Connection, int, str, Any], None]] = {}
# will not be None after init
POOL: Pool = None  # type: ignore
NOTIFY_CONNECTION: Connection = None  # type: ignore
