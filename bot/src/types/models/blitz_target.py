from __future__ import annotations

from typing import TypedDict

__all__ = ("BlitzTarget",)


class BlitzTarget(TypedDict):
    id: int
    blitz_id: int
    war_room_id: int
    nation_id: int
    attacker_ids: int
