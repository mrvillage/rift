from __future__ import annotations

from typing import TYPE_CHECKING, List

import discord
from discord import Message

from ...cache import cache
from ..db import execute_query, execute_read_query

__all__ = (
    "query_menu",
    "query_menu_item",
    "insert_interface",
    "query_menus",
    "query_menus_guild",
)

if TYPE_CHECKING:
    from _typings import MenuData, MenuItemData


async def query_menu(menu_id: int, guild_id: int) -> MenuData:
    return (
        await execute_read_query(
            "SELECT * FROM menus WHERE menu_id = $1 AND guild_id = $2;",
            menu_id,
            guild_id,
        )
    )[0]


async def query_menu_item(item_id: int, guild_id: int) -> MenuItemData:
    return (
        await execute_read_query(
            "SELECT * FROM menu_items WHERE item_id = $1 AND guild_id = $2;",
            item_id,
            guild_id,
        )
    )[0]


async def insert_interface(*, menu_id: int, message: Message) -> None:
    if TYPE_CHECKING:
        assert isinstance(message.guild, discord.Guild)
    await execute_query(
        "INSERT INTO menu_interfaces (menu_id, message_id) VALUES ($1, $2);",
        menu_id,
        message.id,
    )
    cache.add_menu_interface({"menu_id": menu_id, "message_id": message.id})


async def query_menus() -> List[MenuData]:
    return await execute_read_query("SELECT * FROM menus;")


async def query_menus_guild(*, guild_id: int) -> List[MenuData]:
    return await execute_read_query(
        "SELECT * FROM menus WHERE guild_id = $1;", guild_id
    )
