from __future__ import annotations

from typing import Sequence, Tuple, Union

from ..db import execute_read_query


async def query_treaties(alliance_id: int) -> Sequence[Tuple[Union[int, str]]]:
    return [
        dict(i)
        for i in await execute_read_query(
            "SELECT * FROM treaties WHERE from_ = $1 OR to_ = $1;",
            alliance_id,
        )
    ]
