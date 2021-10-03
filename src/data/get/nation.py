from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..db import execute_read_query

__all__ = ("get_nation",)

if TYPE_CHECKING:
    from ..classes import Nation


async def get_nation(search: str) -> Optional[Nation]:
    from ..classes import Nation

    nation = await execute_read_query(
        "SELECT * FROM nations WHERE LOWER(name) = LOWER($1);", search
    )
    if nation:
        return await Nation.fetch(nation[0][0])
    nation = await execute_read_query(
        "SELECT * FROM nations WHERE LOWER(leader) = LOWER($1);", search
    )
    if nation:
        return await Nation.fetch(nation[0][0])
