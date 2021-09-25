from __future__ import annotations

from typing import List, Optional, TypedDict

__all__ = ("TicketData", "TicketConfigData")


class TicketData(TypedDict):
    ticket_id: int
    ticket_number: int
    config_id: int
    guild_id: int
    user_id: int
    open: bool


class TicketConfigData(TypedDict):
    config_id: int
    category_id: Optional[int]
    guild_id: int
    start_message: str
    archive_category_id: Optional[int]
    role_mentions: List[int]
    user_mentions: List[int]
