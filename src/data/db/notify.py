from __future__ import annotations

import json
from typing import TYPE_CHECKING

from ...ref import bot

__all__ = ("listeners",)

if TYPE_CHECKING:
    from typing import Any, Callable, Dict

    from asyncpg import Connection


def standard_dispatch(conn: Connection, pid: int, channel: str, payload: str) -> None:
    bot.dispatch(channel, json.loads(payload))


listeners: Dict[str, Callable[[Connection, int, str, Any], None]] = {
    "insert_credentials": standard_dispatch,
    "update_credentials": standard_dispatch,
    "delete_credentials": standard_dispatch,
}
