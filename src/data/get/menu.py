from __future__ import annotations

from typing import TYPE_CHECKING

from ...errors import MenuItemNotFoundError, MenuNotFoundError
from ..query import query_menu, query_menu_item

__all__ = ("get_menu", "get_menu_item")

if TYPE_CHECKING:
    from _typings import MenuData, MenuItemData


async def get_menu(menu_id: int, guild_id: int) -> MenuData:
    try:
        return await query_menu(menu_id, guild_id)
    except IndexError:
        raise MenuNotFoundError(menu_id)


async def get_menu_item(item_id: int, guild_id: int) -> MenuItemData:
    try:
        return await query_menu_item(item_id, guild_id)
    except IndexError:
        raise MenuItemNotFoundError(item_id)
