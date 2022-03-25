from __future__ import annotations

from typing import TypedDict

__all__ = ("Subscription",)


class Subscription(TypedDict):
    id: int
    guild_id: int
    channel_id: int
    owner_id: int
    event: str
    sub_types: list[str]
    condition: str
    mentions: list[int]
