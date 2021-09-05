from __future__ import annotations

import json
from typing import Dict, Union

from ..db import execute_read_query

__all__ = ("query_color",)


async def query_color(color: str) -> Dict[str, Union[int, str]]:
    return json.loads(
        dict(
            (
                await execute_read_query(
                    "SELECT colors FROM colors ORDER BY datetime DESC LIMIT 1;"
                )
            )[0]
        )["colors"][color]
    )
