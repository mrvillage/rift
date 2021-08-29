from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

import discord
from discord import Message

from ..db import execute_query, execute_read_query


async def query_menu(*, menu_id: int) -> Dict[str, Any]:
    return dict(
        (await execute_read_query("SELECT * FROM menus WHERE menu_id = $1;", menu_id))[
            0
        ]
    )


async def query_menu_item(*, item_id: int) -> Dict[str, Any]:
    return dict(
        (
            await execute_read_query(
                "SELECT * FROM menu_items WHERE item_id = $1;", item_id
            )
        )[0]
    )


async def insert_interface(*, menu_id: int, message: Message) -> None:
    if TYPE_CHECKING:
        assert isinstance(message.guild, discord.Guild)
    await execute_query(
        "INSERT INTO menu_interfaces (menu_id, message_id) VALUES ($1, $2);",
        menu_id,
        message.id,
    )


async def query_menus() -> List[Dict[str, Any]]:
    return [dict(i) for i in await execute_read_query("SELECT * FROM menus;")]


async def query_menus_user(*, user_id: int) -> List[Dict[str, Any]]:
    return [
        dict(i)
        for i in await execute_read_query(
            "SELECT * FROM menus WHERE owner_id = $1;", user_id
        )
    ]
