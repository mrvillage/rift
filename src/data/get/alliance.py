from __future__ import annotations

from typing import List

from ..classes import Alliance
from ..db import execute_read_query
from ..query import query_alliances_offset


async def get_alliance(search):
    from ..classes.alliance import Alliance

    alliance = await execute_read_query(
        "SELECT * FROM alliances WHERE LOWER(name) = LOWER($1);", search
    )
    if alliance:
        return await Alliance.fetch(alliance[0][0])
    alliance = await execute_read_query(
        "SELECT * FROM alliances WHERE LOWER(acronym) = LOWER($1);", search
    )
    if alliance:
        return await Alliance.fetch(alliance[0][0])


async def get_alliances_offset(*, limit: int = 50, offset: int = 0) -> List[Alliance]:
    return [
        Alliance(data=list(i.values()))
        for i in await query_alliances_offset(limit=limit, offset=offset)
    ]
