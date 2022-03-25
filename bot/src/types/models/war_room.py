from __future__ import annotations

from typing import TypedDict

__all__ = ("WarRoom",)


class WarRoom(TypedDict):
    id: int
    config_id: int
    guild_id: int
    channel_id: int
    nation_id: int
    war_ids: list[int]
    archived: bool
    thread: bool
