from __future__ import annotations

from typing import Any, Tuple, Union

from ..db import execute_read_query


async def get_menu(*, menu_id: int) -> Tuple[Any]:
    return tuple(
        (await execute_read_query("SELECT * FROM menus WHERE menu_id = $1;", menu_id))[
            0
        ]
    )


async def get_menu_item(*, item_id: int) -> Tuple[Any]:
    return tuple(
        (
            await execute_read_query(
                "SELECT * FROM menu_items WHERE item_id = $1;", item_id
            )
        )[0]
    )
