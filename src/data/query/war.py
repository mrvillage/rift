from __future__ import annotations

from typing import TYPE_CHECKING

from ..db import execute_read_query

__all__ = ("query_war", "query_attack")

if TYPE_CHECKING:
    from _typings import AttackData, WarData


async def query_war(id: int, /) -> WarData:
    return (await execute_read_query("SELECT * FROM wars WHERE id = $1;", id))[0]


async def query_attack(id: int, /) -> AttackData:
    return (await execute_read_query("SELECT * FROM attacks WHERE id = $1;", id))[0]
