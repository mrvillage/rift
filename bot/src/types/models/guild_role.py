from __future__ import annotations

from typing import TypedDict

__all__ = ("GuildRole",)


class GuildRole(TypedDict):
    id: int
    guild_id: int
    permissions: int
