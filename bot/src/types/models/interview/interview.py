from __future__ import annotations

from typing import TypedDict

__all__ = ("Interview",)


class Interview(TypedDict):
    id: int
    config_id: int
    owner_id: int
    ticket_id: int
    require_link: bool
