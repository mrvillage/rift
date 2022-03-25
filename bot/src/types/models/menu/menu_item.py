from __future__ import annotations

from typing import TypedDict

__all__ = ("MenuItem",)


class MenuItem(TypedDict):
    id: int
    menu_id: int
    type: int
    style: int
    row: int
    label: str
    disabled: bool
    url: str
    emoji: int
    action: int
