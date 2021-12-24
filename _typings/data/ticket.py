from __future__ import annotations

from typing import List, Optional, TypedDict

__all__ = ("TicketData", "TicketConfigData")


class TicketData(TypedDict):
    id: int
    ticket_number: int
    config: int
    guild: int
    user: int
    open: bool


class TicketConfigData(TypedDict):
    id: int
    category: Optional[int]
    guild: int
    start_message: str
    archive_category: Optional[int]
    role_mentions: List[int]
    user_mentions: List[int]
