from __future__ import annotations

from typing import TypedDict

__all__ = ("CityAutoRole",)


class CityAutoRole(TypedDict):
    role_id: int
    guild_id: int
    min_city: int
    max_city: int
    members_only: bool
    condition: str
