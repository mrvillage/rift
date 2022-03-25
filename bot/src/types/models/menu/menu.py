from __future__ import annotations

from typing import TypedDict

__all__ = ("Menu",)


class Menu(TypedDict):
    id: int
    guild_id: int
    name: str
    description: str
