from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict

__all__ = ("MenuData", "MenuInterfaceData", "MenuItemData")


class MenuData(TypedDict):
    id: int
    guild: int
    name: Optional[str]
    description: Optional[str]
    items: List[List[int]]


class MenuInterfaceData(TypedDict):
    menu: int
    message: int
    channel: int


class MenuItemData(TypedDict):
    id: int
    guild: int
    type_: str
    data_: Dict[str, Any]  # fully type this
