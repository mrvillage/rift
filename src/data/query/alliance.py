from __future__ import annotations

from typing import List, Optional

from _typings.data.alliance import AllianceData

from ..db import execute_read_query

__all__ = (
    "query_applicants",
    "query_members",
    "query_alliance",
    "query_alliances",
    "query_alliances_offset",
    "query_max_alliances_page",
)


async def query_applicants(*, alliance_id: int):
    return await execute_read_query(
        """
        SELECT * FROM nations
        WHERE alliance_id = $1 AND alliance_position = 1;
    """,
        alliance_id,
    )


async def query_members(*, alliance_id: int):
    return await execute_read_query(
        """
        SELECT * FROM nations
        WHERE alliance_id = $1 AND alliance_position != 1;
    """,
        alliance_id,
    )


async def query_alliance(
    *, alliance_id: Optional[int] = None, alliance_name: Optional[str] = None
):
    if alliance_id is not None:
        return (
            await execute_read_query(
                """
            SELECT * FROM alliances
            WHERE id = $1;
        """,
                alliance_id,
            )
        )[0]
    elif alliance_name is not None:
        return (
            await execute_read_query(
                """
            SELECT * FROM alliances
            WHERE LOWER(alliance) = LOWER($1);
        """,
                alliance_name,
            )
        )[0]


async def query_alliances():
    return await execute_read_query("SELECT * FROM alliances;")


async def query_alliances_offset(
    *, limit: int = 50, offset: int = 0
) -> List[AllianceData]:
    return [  # type: ignore
        dict(i)
        for i in await execute_read_query(
            "SELECT * FROM alliances order by rank LIMIT $1 OFFSET $2;", limit, offset
        )
    ]


async def query_max_alliances_page() -> int:
    return (await execute_read_query("SELECT MAX(rank) FROM alliances;"))[0]["max"]
