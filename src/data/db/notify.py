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
    "credentials_create": standard_dispatch,
    "credentials_update": standard_dispatch,
    "credentials_delete": standard_dispatch,
}
