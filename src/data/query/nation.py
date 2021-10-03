from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from ..db import execute_read_query

__all__ = ("query_nation", "query_nations")

if TYPE_CHECKING:
    from _typings import NationData


async def query_nation(
    *, nation_id: Optional[int] = None, nation_name: Optional[str] = None
) -> Optional[NationData]:
    if nation_id is not None:
        return (
            await execute_read_query(
                """
            SELECT * FROM nations
            WHERE id = $1;
        """,
                nation_id,
            )
        )[0]
    elif nation_name is not None:
        return (
            await execute_read_query(
                "SELECT * FROM nations WHERE LOWER(name) = LOWER($1);",
                nation_name,
            )
        )[0]


async def query_nations() -> List[NationData]:
    return await execute_read_query("SELECT * FROM nations;")
