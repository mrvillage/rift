from __future__ import annotations

from typing import TypedDict

__all__ = ("AllianceAutoRole",)


class AllianceAutoRole(TypedDict):
    id: int
    role_id: int
    guild_id: int
    alliance_id: int
    access_level: int
    condition: str
