from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from ..db import execute_read_query
from ..query import query_alliances_offset, query_max_alliances_page

if TYPE_CHECKING:
    from ..classes import Alliance


async def get_alliance(search: str) -> Optional[Alliance]:
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
    from ..classes import Alliance

    return [
        Alliance(data=i)
        for i in await query_alliances_offset(limit=limit, offset=offset)
    ]


async def get_max_alliances_page() -> int:
    value = await query_max_alliances_page()
    if value - (value // 50):
        return value // 50 + 1
    return value // 50
