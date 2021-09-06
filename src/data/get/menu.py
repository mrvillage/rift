from __future__ import annotations

from typing import Any, Dict

from src.data.query.menu import query_menu_item

from ...errors import MenuItemNotFoundError, MenuNotFoundError
from ..query import query_menu, query_menu_item


async def get_menu(menu_id: int, guild_id: int) -> Dict[str, Any]:
    try:
        return await query_menu(menu_id, guild_id)
    except IndexError:
        raise MenuNotFoundError(menu_id)


async def get_menu_item(item_id: int, guild_id: int) -> Dict[str, Any]:
    try:
        return await query_menu_item(item_id, guild_id)
    except IndexError:
        raise MenuItemNotFoundError(item_id)
