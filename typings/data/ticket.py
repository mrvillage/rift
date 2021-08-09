from __future__ import annotations

from typing import Optional, TypedDict

__all__ = ("TicketData", "TicketConfigData")


class TicketData(TypedDict):
    ticket_id: int
    channel_id: int
    config_id: int
    guild_id: int
    user_id: int
    open: bool


class TicketConfigData(TypedDict):
    config_id: int
    category_id: Optional[int]
    guild_id: int
