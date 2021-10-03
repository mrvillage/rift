from __future__ import annotations

from typing import TYPE_CHECKING, List

from ..db import execute_read_query

__all__ = ("query_treaties",)
if TYPE_CHECKING:
    from _typings import TreatyData

async def query_treaties(alliance_id: int) -> List[TreatyData]:
    return await execute_read_query(
        "SELECT * FROM treaties WHERE from_ = $1 OR to_ = $1;",
        alliance_id,
    )
