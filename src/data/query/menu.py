from __future__ import annotations

from typing import Any, List, Tuple, Union

from discord import Message

from ..db import execute_query, execute_read_query


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


async def insert_interface(*, menu_id: int, message: Message) -> None:
    await execute_query(
        "INSERT INTO menu_interfaces (menu_id, message_id) VALUES ($1, $2);",
        menu_id,
        message.id,
        message.channel.id,
        message.guild.id,
    )


async def get_menus() -> List[Tuple[Any]]:
    return [tuple(i) for i in await execute_read_query("SELECT * FROM menus;")]


async def get_user_menus(*, user_id: int) -> List[Tuple[Any]]:
    return [
        tuple(i)
        for i in await execute_read_query("SELECT * FROM menus WHERE owner_id = $1;")
    ]
