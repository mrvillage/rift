from __future__ import annotations

from typing import TypedDict

__all__ = ("WarRoomConfig",)


class WarRoomConfig(TypedDict):
    id: int
    name: str
    channel_id: int
    category_ids: list[int]
    guild_id: int
    message: str
    mention_ids: list[int]
    name_format: str
    reuse: bool
    condition: str
    track_wars: bool
    advise: bool
