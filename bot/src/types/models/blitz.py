from __future__ import annotations

import datetime
from typing import TypedDict

__all__ = ("Blitz",)


class Blitz(TypedDict):
    id: int
    date: datetime.datetime
    name: str
    message: str
    alliance_ids: list[int]
    planning_alliance_ids: list[int]
    war_room_config: int
    direct_message: bool
    in_game_message: bool
