from __future__ import annotations

from typing import Any, Tuple, Union

from ..db import execute_read_query


async def get_menu(*, menu_id: str) -> Tuple[Any]:
    return tuple(
        (await execute_read_query("SELECT * FROM menus WHERE id = $1;", menu_id))[0]
    )
