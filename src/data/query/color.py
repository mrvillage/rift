from __future__ import annotations

import json
from typing import Dict, List, Union

from ..db import execute_read_query

__all__ = ("query_color", "query_colors", "query_nation_color_counts")


async def query_color(color: str) -> Dict[str, Union[int, str]]:
    return {i["color"]: i for i in await query_colors()}[color]


async def query_colors() -> List[Dict[str, Union[int, str]]]:
    return dict(
        (
            await execute_read_query(
                "SELECT colors FROM colors ORDER BY datetime DESC LIMIT 1;"
            )
        )[0]
    )["colors"]


async def query_nation_color_counts() -> List[Dict[str, Union[int, str]]]:
    return [
        dict(i)
        for i in await execute_read_query(
            "SELECT color, COUNT(color) FROM nations GROUP BY color;"
        )
    ]
