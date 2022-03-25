from __future__ import annotations

from typing import TypedDict

__all__ = ("Embassy",)


class Embassy(TypedDict):
    id: int
    config_id: int
    guild_id: int
    channel_id: int
    alliance_id: int
    archived: bool
