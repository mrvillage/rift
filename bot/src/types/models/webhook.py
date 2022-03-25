from __future__ import annotations

from typing import TypedDict

__all__ = ("Webhook",)


class Webhook(TypedDict):
    id: int
    channel_id: int
    guild_id: int
    token: str
