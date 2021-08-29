from __future__ import annotations

from typing import Dict, Union

from ..db import execute_read_query

__all__ = ("query_color",)


async def query_color(color: str) -> Dict[str, Union[int, str]]:
    return dict(
        (await execute_read_query("SELECT * FROM colors WHERE color = $1;", color))[0]
    )
