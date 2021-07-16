from __future__ import annotations

from typing import Sequence, Tuple, Union

from ..db import execute_read_query


async def get_treaties(alliance_id: int) -> Sequence[Tuple[Union[int, str]]]:
    return [
        tuple(i)
        for i in await execute_read_query(
            "SELECT * FROM treaties WHERE from_ = $1 OR to_ = $1;",
            alliance_id,
        )
    ]
