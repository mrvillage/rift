from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..db import execute_read_query

__all__ = ("query_war", "query_attack", "query_attacks")

if TYPE_CHECKING:
    from _typings import AttackData, WarData


async def query_war(id: int, /) -> WarData:
    return (await execute_read_query("SELECT * FROM wars WHERE id = $1;", id))[0]


async def query_attack(id: int, /) -> AttackData:
    return (await execute_read_query("SELECT * FROM attacks WHERE id = $1;", id))[0]


async def query_attacks(war_id: int, /) -> List[AttackData]:
    return await execute_read_query("SELECT * FROM attacks WHERE war_id = $1;", war_id)
