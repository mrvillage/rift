from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

__all__ = ("MenuData", "MenuInterfaceData", "MenuItemData")


class MenuData(TypedDict):
    menu_id: int
    guild_id: int
    name: Optional[str]
    description: Optional[str]
    items: List[List[int]]
    permissions: None  # unknown typing since unimplemented


class MenuInterfaceData(TypedDict):
    menu_id: int
    message_id: int


class MenuItemData(TypedDict):
    item_id: int
    menu_id: int
    type_: str
    data_: Dict[str, Any]  # fully type this
