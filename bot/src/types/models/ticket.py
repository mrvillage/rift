from __future__ import annotations

from typing import TypedDict

__all__ = ("Ticket",)


class Ticket(TypedDict):
    id: int
    ticket_number: int
    config_id: int
    guild_id: int
    channel_id: int
    owner_id: int
    archived: bool
